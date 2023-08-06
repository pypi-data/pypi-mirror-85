# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys

import gdpy
from gdpy import exceptions

from gwc import utility
from gwc.globals import _logger
from ._base import Runner


class GWLRunner(Runner):
    runner_type = 'gwl'

    def run(self, init_params):
        return self.active_workflow(
            parameters_file=getattr(init_params, 'parameters'),
            workflow_name=getattr(init_params, "name"),
            workflow_version=getattr(init_params, "version"),
            task_name=getattr(init_params, "task"),
            workflow_owner=getattr(init_params, "account", None),
        )

    def active_workflow(self, parameters_file, workflow_name, workflow_version=None, task_name=None,
                        workflow_owner=None):
        """
        运行工作流
        :param workflow_name: 工作流名称
        :param parameters_file: 工作流运行所需的配置文件（配置文件中输入项数据的名称必须填写）
        :param task_name: 指定Task名称（不填则为系统默认生成名称）
        :param workflow_version: 工作流版本（不填默认以最新版本运行）
        """

        workflow_owner = workflow_owner or self.res_account_name
        if not workflow_version:
            try:
                workflow_version = utility.get_version(
                    'workflow', workflow_name, workflow_owner, self.project_name
                )
            except exceptions.ServerError as e:
                if e.status // 100 == 4:
                    print(
                        'Error: {}\n'
                        'Please check the input "workflow name" or '
                        '"resource account" (if authoried by others).'.format(e.error_message)
                    )
                    return False

        workflow_param_file = parameters_file
        workflow_param = gdpy.yml_utils.yaml_loader(workflow_param_file)

        if not workflow_param.get("task_name") and not task_name:
            task_name = utility.tmp_task_name(workflow_name, workflow_version)

        workflow_param['name'] = task_name
        workflow_param['Property']['reference_task'][0]['id'] = 'null'

        for node in workflow_param['Outputs']:
            node_info = workflow_param['Outputs'][node]
            out_data_name = node_info['data'][0]['name']
            out_data_format = node_info['formats'][0]
            if (out_data_name == '<Please input the name of the output data in here>' or
                    out_data_name is None or
                    out_data_name == ''
            ):
                out_data_name = '/home/' + self.user + '/' + task_name + '/' + node + '.' + out_data_format
                node_info['data'][0]['name'] = out_data_name

        workflow_param = gdpy.yml_utils.yaml_dumper(workflow_param)
        with open(task_name + '_tmp.yml', 'w') as f:
            f.write(workflow_param.decode('utf-8'))

        try:
            func = utility.catch_exceptions()(self.tasks.active_workflow)
            resp = func(task_name + '_tmp.yml', workflow_name, workflow_version, workflow_owner)
        except exceptions.ServerError as e:
            if e.status // 100 == 4:
                print(
                    'Error: {}\n'
                    'Please check the input "workflow name", "workflow version", '
                    '"the inputs data name in parameters file" '
                    'or "resource account" (if authorized by others).'.format(e.error_message),
                    file=sys.stderr
                )
                return False
            raise
        else:

            if resp.status == 200:
                _logger.info(
                    'Run the workflow successfully! name: %s, version: %s. task_name: %s, task_id: %s',
                    workflow_name, workflow_version, resp.task_name, resp.task_id)
                print(
                    'Run the workflow successfully!\ntask_name: %s, task_id: %s' % (resp.task_name, resp.task_id),
                    file=sys.stdout
                )
            else:
                _logger.info(
                    'Run the workflow successfully! name: %s, version: %s. split: %s, splitting: %s',
                    workflow_name, workflow_version, resp.split, resp.splitting
                )
                print('Run the workflow successfully!\nFastq file is splitting！', file=sys.stdout)

            os.remove(task_name + '_tmp.yml')
            return True
