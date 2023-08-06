# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from KE.v3.client import KE3


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
        user.locked = json_obj['locked']
        user.wrong_time = json_obj['wrong_time']
        user.id = json_obj['uuid']
        user.last_modified = json_obj['last_modified']
        user.version = json_obj['version']

        return user

    def update(self, password, disabled, authorities):
        body = {'password': password, 'disabled': disabled, 'authorities': authorities}
        uri = '/kap/user/{name}'.format(name=self.name)
        json_obj = self._client.fetch_json(uri=uri, body=body)
        return User.from_json(client=self._client, json_obj=json_obj)

    def list_access(self):
        """
        Notice: it's from API v2

        :return:
        """
        uri = '/access/{user}'.format(user=self.name)
        json_obj = self._client.fetch_json(uri=uri, headers=KE3.headers)
        return json_obj['data']

    def list_row_access(self, project, table):
        """
        Notice: it's from API v2

        :return:
        """
        uri = '/access/{user}/{project}/{table}/row'.format(
            user=self.name, project=project, table=table)
        json_obj = self._client.fetch_json(uri=uri, headers=KE3.headers)
        return json_obj['data']

    def list_col_access(self, project, table):
        """
        Notice: it's from API v2
        :return:
        """
        uri = '/access/{user}/{project}/{table}/column'.format(user=self.name, project=project, table=table)
        json_obj = self._client.fetch_json(uri=uri, headers=KE3.headers)
        return json_obj['data']

    def __repr__(self):
        return "<User: {name}>".format(name=self.name)
