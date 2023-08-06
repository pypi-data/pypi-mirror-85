# -*- coding: utf-8 -*-

from gdpy import api
from gdpy import auth


class Runner(object):

    runner_type = None

    def __init__(
            self, gd_auth, endpoint, account, user,
            res_account_name=None, project='default'
    ):
        self.account = account
        self.user = user
        self.res_account_name = res_account_name or self.account
        self.project_name = project
        self.auth = gd_auth
        self.endpoint = endpoint
        self.workflows = api.Workflows(
            auth=self.auth,
            res_account_name=self.res_account_name,
            endpoint=self.endpoint,
            project_name=project,
            workflow_type=self.runner_type
        )
        self.tasks = api.Tasks(
            auth=self.auth,
            res_account_name=self.res_account_name,
            endpoint=self.endpoint,
            project_name=project,
            task_type=self.runner_type
        )

    @classmethod
    def new(cls, access_key_id, access_key_secret, endpoint, account, user,
            res_account_name=None, project='default'):
        gd_auth = auth.GeneDockAuth(
            access_key_secret=access_key_secret,
            access_key_id=access_key_id
        )
        return cls(gd_auth, endpoint, account, user, res_account_name, project)

    def run(self, *args, **kwargs):
        raise NotImplementedError
