#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import functools
import os
import random
import sys

import dateutil.parser
import gdpy
import pytz
import time
from datetime import datetime, timedelta

from gwc import globals
from gwc.globals import _logger

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser

CurrentTime = time.strftime('_%Y_%m_%d_%H_%M_%S', time.localtime())

UTC_OFFSET = timedelta(hours=8)
TZ_CST = pytz.timezone("Asia/Shanghai")


def tmp_task_name(workflow_name, version):
    return "{}_{}{}".format(workflow_name, version, CurrentTime)


def format_time(ts_or_time_str, to_timestamp=False, format='%Y-%m-%d %H:%M:%S'):
    """统一将时间戳和时间字符串转时间"""
    if not ts_or_time_str:
        return ts_or_time_str
    if isinstance(ts_or_time_str, str):
        parser = dateutil.parser.parser()
        utc_date = parser.parse(ts_or_time_str)
        ts_or_time_str = time.mktime(utc_date.utctimetuple())
    if to_timestamp:
        return ts_or_time_str
    return time.strftime(format, time.localtime(ts_or_time_str))


class catch_exceptions(object):
    """给函数增加重试功能
    :param retry_times: 重试次数 ( **note**: 重试 1 次会执行 2 次函数)
    :param catch_exceptions: 需要捕获的异常，出现这个异常时才进行重试。
                             默认是 ``Exception``
    :rtype catch_exceptions: 单个异常类或者多个异常类组成的 **元组**
    """

    def __init__(self, retry_times=1, catch_exceptions=None):
        self.retry_times = retry_times
        self.catch_exceptions = catch_exceptions or (Exception,)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            retry_times = kwargs.pop('_retry_times', self.retry_times)

            for n in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except self.catch_exceptions as exc:
                    if not hasattr(exc, 'status'):
                        raise
                    # 404异常返回到调用处处理
                    if exc.status // 100 == 4:
                        raise

                    # 不捕获特定的异常
                    no_retry_exception(exc, func)

                    random_time = random.randint(n * 60, (1 << n) * 60)
                    _logger.warning('gdpy operation: %s failed. Retry after %d seconds', func.__name__, random_time)
                    print('gdpy operation: {} failed. Retry after {} seconds'.format(func.__name__, random_time))
                    time.sleep(random_time)

                    if n == retry_times - 1:
                        # 最后一次重试失败，重新抛出异常给上一层
                        retry_exception(exc, func)

        return _wrapper


def retry_exception(exc, func):
    """需要重试的异常
    :return:
    """
    if isinstance(exc, gdpy.exceptions.RequestError):
        _logger.warning(
            'Failed to %s! status: %s, error: %s\nNetWork Connection Error, '
            'please check your network and retry.', func.__name__, exc.status,
            exc.error_message.decode('utf-8'))
        print('Failed to {}!\nstatus: {}\nerror: {}\n'.format(func.__name__, exc.status,
                                                              exc.error_message.decode(
                                                                  'utf-8')), file=sys.stderr)
        print('NetWork Connection Error, please check your network and retry.', file=sys.stderr)
        os._exit(-1)
    elif isinstance(exc, gdpy.exceptions.ServerError) and exc.status // 100 == 5:
        print('Please retry, if failed again, contact with the staff of GeneDock.', file=sys.stderr)
        os._exit(-1)


def no_retry_exception(exc, func):
    """不需要重试的异常
    :return:
    """
    if isinstance(exc, ConfigParser.NoSectionError):
        _logger.warning(
            'Can not find section: "{}" in config file: "{}".'.format(exc.section, globals.CONFIGFILE))
        print('Please config your account information.', file=sys.stderr)
        print(
            'Using: "gwc config" or "gwc config -e [endpoint] -i [access_id] -k [access_key]".',
            file=sys.stderr)
    elif isinstance(exc, ConfigParser.NoOptionError):
        _logger.warning(
            'Can not find option: "{}" in section: "{}" in config file: "{}".'.format(exc.option,
                                                                                      exc.section,
                                                                                      globals.CONFIGFILE))
        print('Please config your account information.', file=sys.stderr)
        print(
            'Using: "gwc config" or "gwc config -e [endpoint] -i [access_id] -k [access_key]".',
            file=sys.stderr)
    elif isinstance(exc, ValueError):
        _logger.warning('Failed to %s! error: %s', func.__name__, exc)
        print('Failed to {}!\nerror: {}'.format(func.__name__, exc), file=sys.stderr)
    elif isinstance(exc, gdpy.exceptions.ServerError) and exc.status // 100 != 5:
        _logger.warning('Failed to %s! status: %s, error: %s, 错误: %s', func.__name__, exc.status,
                        exc.error_message.decode('utf-8'),
                        exc.error_message_chs.decode('utf-8'))
        print('Failed to {}!\nstatus: {}\nerror: {}\n错误: {}'.format(
            func.__name__, exc.status,
            exc.error_message.decode('utf-8'),
            exc.error_message_chs.decode('utf-8')),
            file=sys.stderr
        )
    else:
        return

    sys.exit(-1)


@catch_exceptions()
def get_version(operation, name, res_account, project_name, gd_auth, endpoint, tool_id=None):
    """
    获取工具或工作流的最新版本号/指定工具id的版本号

    Args：
        operation: 'workflow'或'tool'
        name: 工作流名称或工具名称
        res_account: 指定从该账号下获取资源
        tool_id: 工具的 id

    Returns:
        version: 工作流或工具最新版本号/指定工具id的版本号
    """

    version = 1
    if operation == 'workflow':
        workflow = gdpy.Workflows(gd_auth, endpoint, res_account, project_name)
        resp = workflow.get_workflow(name)
        for item in gdpy.utils.json_loader(resp.response.text).get('workflows'):
            operation_version = item.get('version')
            if operation_version > version:
                version = operation_version
    elif operation == 'tool':
        tool = gdpy.Tools(gd_auth, endpoint, res_account, project_name)
        resp = tool.get_tool(name)
        for item in gdpy.utils.json_loader(resp.response.text).get('tools'):
            operation_version = item.get('configs').get('version')
            if tool_id:
                # 传入 tool id 获取指定的版本号
                if tool_id == item.get('configs').get('_id'):
                    return int(operation_version)
            else:
                # 没传入 id 就取最新的版本号
                if operation_version > version:
                    version = operation_version
        # 这里表示此账号下的 tools 没有对应的 tool_id
        if tool_id:
            return None
    _logger.info(
        'Get %s latest version successfully! name: %s, version: %s, resource account: %s.',
        operation, name, version, res_account
    )
    return int(version)
