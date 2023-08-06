import os
import unittest
from KE import KE
from KE.v4.user import User
from KE.v4.project import Project
from KE.client import KE4CONF


class UserV4TestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self.client = KE(KE4CONF['host'], port=KE4CONF['port'], username=KE4CONF['username'], password=KE4CONF['password'], version=4, debug=True)

    def test_user_properties(self):
        users = self.client.users()
        print(users)
        user = users[0]
        self.assertIsInstance(user, User)

    def test_create_project(self):
        project = self.client.create_project('test_project', maintain_model_type='AUTO_MAINTAIN')
        self.assertIsInstance(project, Project)

    def test_list_access(self):
        users = self.client.users()
        user = users[1]
        access = user.list_access()
        print(access)

    def test_list_row_access(self):
        users = self.client.users()
        user = users[0]
        res = user.list_row_access('learn_kylin', 'KYLIN_CAL_DT')
        print(res)

    def test_list_col_access(self):
        users = self.client.users()
        user = users[0]
        res = user.list_col_access('learn_kylin', 'KYLIN_CAL_DT')
        print(res)