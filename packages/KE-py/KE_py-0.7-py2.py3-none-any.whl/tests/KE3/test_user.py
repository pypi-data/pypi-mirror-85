from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE
from KE.v3.user import User
from KE.client import KE3CONF as CONF


class UserTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self.client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3, debug=True)

    def test_user_properties(self):
        users = self.client.users()
        print(users)
        user = users[0]
        self.assertIsInstance(user, User)

    def test_user_args(self):
        users = self.client.users(name='dennis')
        print(users)

        users = self.client.users(project='learn_kylin')
        print(users)

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

    def test_under_permission(self):
        client = KE('device2', username='test', password='Kyligence@2020', version=3)
        cube = client.cubes('testcube', project='test')
        print(cube)
