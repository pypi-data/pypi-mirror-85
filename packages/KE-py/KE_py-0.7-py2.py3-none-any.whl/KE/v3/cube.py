# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from datetime import datetime
from KE.base import Base
from KE.v3.segments import Segments
from KE.v3.job import Job
from KE.util import danger_action
from KE.util import unify_timestamp


class Cube(Base):

    def __init__(self, client=None, cube_id=None, name=None, project_name=None):
        """Cube Object
        """
        super(Cube, self).__init__(client=client)

        self.id = cube_id
        self.name = name
        self.project_name = project_name
        self.segment_count = None

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the cube json object to a Cube object

        :param client: the KE client
        :param json_obj: the cube json object
        """

        cube = Cube(client=client, cube_id=json_obj['uuid'], name=json_obj['name'], project_name=json_obj['project'])
        cube.owner = json_obj.get('owner', '')
        cube.last_modified = json_obj['last_modified']
        cube.last_modified_dt = datetime.utcfromtimestamp(json_obj['last_modified'] / 1000)
        cube.version = json_obj['version']
        cube.name = json_obj['name']
        cube.owner = json_obj['owner']
        cube.descriptor = json_obj['descriptor']
        cube.cost = json_obj['cost']
        cube.status = json_obj['status']
        cube.create_time_utc = json_obj['create_time_utc']
        cube.create_time_dt = datetime.utcfromtimestamp(json_obj['create_time_utc'] / 1000)
        cube.cuboid_bytes = json_obj['cuboid_bytes']
        cube.cuboid_bytes_recommend = json_obj['cuboid_bytes_recommend']
        cube.cuboid_last_optimized = json_obj['cuboid_last_optimized']
        cube.model = json_obj['model']
        cube.input_records_count = json_obj['input_records_count']
        cube.input_records_size = json_obj['input_records_size']
        cube.cuboid_count = json_obj['cuboid_count']

        cube.segments_json = json_obj['segments']

        return cube

    def segments(self, start_time=0, end_time=None, offset=0, size=20, mp_values=''):
        """Get Segments object of the Cube

        This API seems not showing on Official Document, only hooked with the WebUI Ajax Request

        :param start_time: datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :param end_time: datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :param offset:
        :param size:
        :param mp_values:
        :return: Segments object
        """
        # convert date or datetime type to timestamp
        start_time = unify_timestamp(start_time)
        end_time = unify_timestamp(end_time)

        if (start_time is not None) or (end_time is not None):
            params = {'startTime': start_time, 'endTime': end_time,
                      'pageOffset': offset, 'pageSize': size, 'mpValues': mp_values}
            uri = '/cubes/{name}/segments/'.format(name=self.name)
            json_obj = self._client.fetch_json(uri=uri, params=params)
            self.segment_count = json_obj['data']['size']
            return Segments.from_json(self.name, client=self._client, json_obj=json_obj['data']['segments'])
        # construct from cube.segments_json
        return Segments.from_json(self.name, client=self._client, json_obj=self.segments_json)

    def list_segments(self, start_time=0, end_time=None, offset=0, size=20, mp_values=''):
        """List segment

        :param start_time:
        :param end_time:
        :param offset:
        :param size:
        :param mp_values:
        :return: Segment object list
        """
        return

    def build(self, start_time, end_time, mp_values='', build_type='BUILD', force=False, yarn_queue=None):
        """Build the segment of this Cube

        :param start_time:  datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :param end_time:  datetime or date or str/int of timestamp ，如 1388534400000 对应 2014-01-01 00:00:00
        :param build_type: - 必选 string，支持的计算类型，为："BUILD"
        :param mp_values: - 可选 string，对应模型的分区字段值
        :param force: - 可选 boolean，强制提交任务选项，默认值为 false
        :param yarn_queue: - 可选 string，指定该任务使用的 YARN 队列，在系统级别或项目级别设置参数后使用：\
            kylin.engine-yarn.queue.in.task.enabled（是否允许为任务指定 YARN 队列，默认不开启）、 \
            kylin.engine-yarn.queue.in.task.available（可供设置的 YARN 队列，多个队列时用英文逗号分隔）。
        :return: Job object
        """
        start_time = unify_timestamp(start_time)
        end_time = unify_timestamp(end_time)

        body = {'startTime': start_time, 'endTime': end_time,
                'mpValues': mp_values, 'buildType': build_type, 'force': force,
                'yarnQueue': yarn_queue}
        json_obj = self._client.fetch_json('/cubes/{cube_name}/segments/build'
                                           .format(cube_name=self.name), body=body, method='PUT')
        return Job.from_json(client=self._client, json_obj=json_obj['data'])

    def clone(self, new_name=None):
        """克隆Cube

        :param new_name: 新的cube name; 默认加 _clone
        :return: a cloned Cube object
        """
        if not new_name:
            new_name = '%s_clone' % self.name
        body = {'project': self.project_name, 'cubeName': new_name}
        json_obj = self._client.fetch_json('/cubes/{cube_name}/clone'.format(cube_name=self.name),
                                           body=body, method='PUT')
        cube_json = json_obj['data']
        return self.from_json(client=self._client, json_obj=cube_json)

    def enable(self):
        json_obj = self._client.fetch_json('/cubes/{cube_name}/enable'.format(cube_name=self.name), method='PUT')
        cube_json = json_obj['data']
        return self.from_json(client=self._client, json_obj=cube_json)

    def disable(self):
        json_obj = self._client.fetch_json('/cubes/{cube_name}/disable'.format(cube_name=self.name), method='PUT')
        cube_json = json_obj['data']
        return self.from_json(client=self._client, json_obj=cube_json)

    @danger_action
    def purge(self, mp_values=None, mp_values_set=None):
        """Purge the Cube

        :param mp_values: - 可选 string，模型多级分区值，用于指定单个待清理的分区
        :param mp_values_set: - 可选 数组, 模型多级分区值的数组，用于指定多个待清理的分区
        :return: New Cube object
        """
        params = {'project': self.project_name, 'mpValues': mp_values, 'mpValuesSet': mp_values_set}
        json_obj = self._client.fetch_json('/cubes/{cube_name}/purge'.format(cube_name=self.name),
                                           params=params, method='PUT')
        cube_json = json_obj['data']
        return self.from_json(client=self._client, json_obj=cube_json)

    def holes(self, mp_values=None):
        """
        :param mp_values: 可选 string, 多级分区值（只对于多级分区的 Cube 有效）
        :return:
        """
        params = {'cubeName': self.name, 'mpValues': mp_values}
        json_obj = self._client.fetch_json('/cubes/{cube_name}/holes'.format(cube_name=self.name), params=params)
        return json_obj['data']

    def refresh_lookup(self):
        pass

    def get_sql(self):
        """Get the SQL of the model
            Notice: it's internal API, use internal headers instead

        :return: SQL string
        """
        pass

    def __repr__(self):
        return '<Cube %s>' % self.name
