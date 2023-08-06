# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import re
import sys

import datetime
import yaml
from gdpy import exceptions

from gwc import utility
from ._base import Runner


class WorkflowAlreadyExisting(Exception):

    def __init__(self, wf_info):
        self.wf_info = wf_info
        self.message = (
            "The workflow with name '{}' already exists, latest version: '{}', "
            "workflow id: {}, inputs: \n\n{}".format(
                wf_info['name'], wf_info['version'], wf_info['id'],
                json.dumps(wf_info.get("inputs", {}), indent=4)
            )
        )
        super(WorkflowAlreadyExisting, self).__init__(self.message)


class WorkflowNotFound(Exception):

    def __init__(self, workflow_name, version):
        self.message = (
            "Not found! please check the workflow name '{}' and workflow version '{}'"
            "".format(workflow_name, version)
        )
        super(WorkflowNotFound, self).__init__(self.message)


class WDLRunner(Runner):

    WF_NAME_PATTERN = re.compile("workflow\s+(.*).*?{")

    runner_type = 'wdl'

    @classmethod
    def _parse_workflow_name(cls, source_file):
        with open(source_file) as f:
            content = f.read()
        res = cls.WF_NAME_PATTERN.findall(content)
        if len(res) != 1:
            raise ValueError("Illegal format, please check the WDL source file {}".format(source_file))

        return res[0].strip()

    def run(self, init_params):
        return self.run_wdl(
            workflow_name=getattr(init_params, "workflow_name", None),
            workflow_id=getattr(init_params, "workflow_id", None),
            version=getattr(init_params, 'version', None),
            inputs_file=getattr(init_params, "inputs_file"),
            remote_output_dir=getattr(init_params, "remote_output_dir"),
            task_name=getattr(init_params, "task_name", None),
            is_yaml=getattr(init_params, "is_yaml", False),
        )

    def create_workflow(self, source, dependencies_zip=None, wf_name=None):

        wf_name = wf_name or self._parse_workflow_name(source)

        try:
            remote_wf_list = self.workflows.get_workflow_info_by_name(wf_name)
        except exceptions.ServerError as e:
            if e.status != 404:
                raise
            remote_wf_list = []

        if remote_wf_list:
            # list of list (list workflow response)
            wf_info = self._get_latest_workflow(remote_wf_list)
            raise WorkflowAlreadyExisting(wf_info)

        print("Start creating a new workflow with name {} ...".format(wf_name))
        result = self.workflows.create_workflow(
            name=wf_name,
            description="auto created from gwc at {}".format(datetime.datetime.now()),
            attachment={
                "source_file": source,
                "dependencies_zip": dependencies_zip
            }
        )
        wf_info = result.response.json()
        wf_info['version'] = 1
        return wf_info

    def update_workflow(
            self, source, wf_name=None, version=None, dependencies_zip=None,
            include_empty_imports=False):
        """

        :param source: wdl 文件
        :param dependencies_zip: wdl依赖文件（zip压缩包）
        :param wf_name: 指定工作流名称，没有则会从source中解析
        :param version: 指定工作流版本号，用于指定版本的更新, 如果不指定，则默认新增一个版本号
        :param include_empty_imports: 是否包含空的imports文件
        :return:
        """

        wf_name = wf_name or self._parse_workflow_name(source)

        try:
            remote_wf_list = self.workflows.get_workflow_info_by_name(wf_name, version)
        except exceptions.ServerError as e:
            if e.status != 404:
                raise
            remote_wf_list = []

        if not remote_wf_list:
            raise WorkflowNotFound(wf_name, version)

        # list of list (list wokflow response)
        wf_info = self._get_latest_workflow(remote_wf_list)

        wf_id = wf_info['id']
        wf_version = version or wf_info['version']

        print(
            "[CREATE] Start update the existing workflow "
            "{} (id: {}, version {} )...".format(wf_name, wf_id, wf_version)
        )
        new_wf_info = self.workflows.update_workflow(
            name_or_id=wf_id,
            version=wf_version,
            attachment={
                "source_file": source,
                "dependencies_zip": dependencies_zip,
            },
            include_empty_imports=include_empty_imports,
            override=True if version else False  # 如果指定了version则覆盖
        ).response.json()

        return new_wf_info

    def run_wdl(
            self, inputs_file, remote_output_dir, task_name=None,
            workflow_name=None, workflow_id=None, version=None, is_yaml=False
    ):
        if not (workflow_name or workflow_id):
            print("[ERROR] The 'workflow name' or 'workflow id' must be present", file=sys.stderr)
            return False

        if not workflow_id and workflow_name:
            remote_wf_list = self.workflows.get_workflow_info_by_name(workflow_name, version)
            if not remote_wf_list:
                print(
                    "Run the WDL workflow failed! The workflow '{}' not found. (specified version: {})"
                    "".format(workflow_name, version),
                    file=sys.stderr
                )
                return False
            wf_info = self._get_latest_workflow(remote_wf_list)
        else:
            wf_info = {
                "id": workflow_id,
                "version": version
            }

        wf_id = wf_info['id']
        wf_version = wf_info['version']  # finally version

        with open(inputs_file) as f:
            if is_yaml:
                inputs = yaml.load(f, yaml.SafeLoader)
            else:
                inputs = json.load(f)

        task_name = task_name or utility.tmp_task_name(workflow_name, wf_version)
        if not remote_output_dir:
            remote_output_dir = "{}:/home/admin/{}/".format(self.account, task_name)
            print('[ALTER] The default remote output directory will be set to "{}"'.format(remote_output_dir))

        result = self.tasks.create_task(
            wf_id, wf_version,
            parameters={
                "inputs": inputs,
                "output_dir": remote_output_dir,
                "name": task_name
            },
        )
        print('Run the WDL workflow successfully!\ntask_id: {}'.format(result.task_id), file=sys.stdout)
        return True

    @staticmethod
    def _get_latest_workflow(remote_wf_list):
        """
        获取最大版本号的工作流
        :param remote_wf_list:
        :return:
        """
        remote_wf_list = sorted(remote_wf_list[0], key=lambda x: x['version'], reverse=True)
        return remote_wf_list[0]
