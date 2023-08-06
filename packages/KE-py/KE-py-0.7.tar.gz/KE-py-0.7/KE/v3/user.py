# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base


class User(Base):

    def __init__(self, client=None, name=''):
        """User Object
        """
        super(User, self).__init__(client=client)
        self.name = name

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the user json object to a User object

        :param client: the KE client
        :param json_obj: the user json object
        """
        client.logger.debug(json_obj)
        user = User(client=client, name=json_obj['username'])
        user.authorities = json_obj['authorities']
        user.disabled = json_obj['disabled']
        user.defaultPassword = json_obj['defaultPassword']
        user.locked = json_obj['locked']
        user.lockedTime = json_obj['lockedTime']
        user.wrongTime = json_obj['wrongTime']
        user.id = json_obj['uuid']
        user.last_modified = json_obj['last_modified']
        user.version = json_obj['version']

        return user

    def update(self, password, disabled, authorities):
        """更改用户属性

        :param password: 必选 string，用户密码
        :param disabled: 必选 boolean，是否启用，可填内容 true（代表该用户处于禁用状态），false（代表该用户处于启用状态）
        :param authorities: 必选 string[]，用户所属用户组
        :return: New User object
        """
        body = {'password': password, 'disabled': disabled, 'authorities': authorities}
        uri = '/kap/user/{name}'.format(name=self.name)
        json_obj = self._client.fetch_json(uri=uri, body=body)
        return User.from_json(client=self._client, json_obj=json_obj)

    def list_access(self):
        """返回用户拥有的项目及表权限

        :return:
        """
        uri = '/access/{user}'.format(user=self.name)
        json_obj = self._client.fetch_json(uri=uri)
        return json_obj['data']

    def list_row_access(self, project, table):
        """返回用户拥有的行级权限

        :param project: 必选 string，项目名称
        :param table: 必选 string，表名称
        :return:
        """
        uri = '/access/{user}/{project}/{table}/row'.format(
            user=self.name, project=project, table=table)
        json_obj = self._client.fetch_json(uri=uri)
        return json_obj['data']

    def list_col_access(self, project, table):
        """返回用户拥有的列级权限

        :param project:
        :param table:
        :return:
        """
        uri = '/access/{user}/{project}/{table}/column'.format(user=self.name, project=project, table=table)
        json_obj = self._client.fetch_json(uri=uri)
        return json_obj['data']

    def __repr__(self):
        return "<User: {name}>".format(name=self.name)
