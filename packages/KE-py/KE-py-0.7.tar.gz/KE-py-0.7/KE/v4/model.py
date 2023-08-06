# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import
from KE.base import Base
from KE.v4.segments import Segments
from KE.v4.job import Job
from datetime import datetime
from KE.util import unify_timestamp


class Model(Base):

    def __init__(self, client=None, name=None, project=None):
        """Model Object"""
        super(Model, self).__init__(client=client)

        self.name = name
        self.project = project

    @classmethod
    def from_json(cls, client=None, json_obj=None, project=None):
        """Deserialize the project json object to a Model object

        :param client: the KE client
        :param json_obj: the model json object
        :param project: project name
        :return: Model object
        """
        client.logger.debug(json_obj)
        _project = json_obj['project']
        if not _project:
            #  sometime project is None in json_obj
            _project = project

        model = Model(client=client, project=_project, name=json_obj['name'])
        model.id = json_obj['uuid']
        model.lookups = json_obj['lookups']
        model.is_streaming = json_obj['is_streaming']
        model.size_kb = json_obj['size_kb']
        model.input_records_count = json_obj['input_records_count']
        model.input_records_size = json_obj['input_records_size']
        model.last_modified = json_obj['last_modified']
        model.create_time = json_obj['create_time']
        model.create_time_dt = datetime.utcfromtimestamp(json_obj.get('create_time', 0) / 1000)
        model.version = json_obj['version']
        model.owner = json_obj['owner']
        model.alias = json_obj['alias']
        model.description = json_obj['description']
        model.fact_table = json_obj['fact_table']
        model.all_named_columns = json_obj['all_named_columns']
        model.storage = json_obj['storage']
        model.all_measures = json_obj['all_measures']
        model.expansion_rate = json_obj['expansion_rate']
        # model.segments = json_obj['segments']
        model.capacity = json_obj['capacity']
        model.computed_columns = json_obj['computed_columns']
        model.partition_desc = json_obj['partition_desc']
        model.status = json_obj['status']

        return model

    def segments(self, start_time=1, end_time=9223372036854775806, offset=0, size=20):
        """Get segments of the model

        :parameter
            offset: - optional int，分页页面，默认为 0。
            size: - optional int，分页大小，默认为 20。
            start_time: - optional string，Segments 开始时间，默认为 1, 时间戳类型，毫秒。
            end_time: - optional string，Segments 结束时间，默认为9223372036854775806，时间戳类型，毫秒。

        :return: Segments Object
        """
        import KE.v4.client as client_v4 # avoid mutual top-level imports
        start_time = unify_timestamp(start_time)
        end_time = unify_timestamp(end_time)

        params = {'project': self.project, 'start': start_time, 'end': end_time, 'page_offset': offset,
                  'page_size': size}
        uri = '/models/{model}/segments'.format(model=self.name)
        json_obj = self._client.fetch_json(uri=uri, params=params, headers=client_v4.KE4.headers)
        self.logger.debug(json_obj)
        return Segments.from_json(client=self._client, json_obj=json_obj['data']['value'],
                                  model=self.name, project=self.project)

    def build(self, start_time, end_time):
        """构建

        加载数据（AI 增强模式）
        :param start_time:  datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :param end_time:  datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :return: json_obj
        """
        import KE.v4.client as client_v4
        start_time = unify_timestamp(start_time)
        end_time = unify_timestamp(end_time)

        body = {'project': self.project, 'start': start_time, 'end': end_time}
        uri = '/models/{model}/segments'.format(model=self.name)
        json_obj = self._client.fetch_json(uri=uri, body=body, headers=client_v4.KE4.headers, method='POST')

        return json_obj

    def indexes(self):
        """构建索引

        :return:
        """
        uri = '/models/{model_name}/indexes'.format(model_name=self.name)
        body = {'project': self.project}
        json_obj = self._client.fetch_json(uri=uri, method='POST', body=body)
        return json_obj

    def describe(self):
        uri = '/models/{project}/{model_name}/model_desc'.format(project=self.project, model_name=self.name)
        json_obj = self._client.fetch_json(uri=uri)
        return json_obj['data']

    def validation(self, sqls):
        uri = '/models/model_validation'
        body = {'project': self.project, 'sqls': sqls}
        json_obj = self._client.fetch_json(uri=uri, method='POST', body=body)
        return json_obj['data']

    def get_sql(self):
        """Get the SQL of the model
            Notice: it's internal API, use internal headers instead

        :return: SQL string
        """
        import KE.v4.client as client_v4  # avoid mutual top-level imports
        params = {'model': self.id, 'project': self.project}
        uri = 'models/{model_id}/sql'.format(model_id=self.id)
        json_obj = self._client.fetch_json(uri=uri, params=params, headers=client_v4.KE4.internal_headers)
        return json_obj['data']

    def rule(self):
        params = {'model': self.id, 'project': self.project}
        uri = 'index_plans/rule'
        json_obj = self._client.fetch_json(uri=uri, params=params)
        return json_obj['data']

    def __repr__(self):
        return "<Model: {name}>".format(name=self.name)
