# -*- coding: utf-8 -*-


from ._base import Runner
from .wdl import WDLRunner
from .gwl import GWLRunner


__RUNNER_MAP = {
    WDLRunner.runner_type: WDLRunner,
    GWLRunner.runner_type: GWLRunner
}


def get_runner(runner_type, **kwargs):

    klass = __RUNNER_MAP.get(runner_type)
    if not klass:
        raise RuntimeError("Unsupported runner type '{}'".format(runner_type))
    return klass(**kwargs)  # type: Runner
