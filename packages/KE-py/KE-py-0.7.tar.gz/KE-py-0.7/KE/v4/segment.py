# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from datetime import datetime


class Segment(Base):

    def __init__(self, model, client=None, segment_id=None, name=None):
        """Segment Object
        """
        super(Segment, self).__init__(client=client)
        self.id = segment_id
        self.name = name
        self.model = model

    @classmethod
    def from_json(cls, model=None, client=None, json_obj=None):
        """Deserialize the segment json object to a Segment object

        :param client: the KE client
        :param json_obj: the segment json object
        """

        segment = Segment(model, client=client, segment_id=json_obj['id'], name=json_obj['name'])
        segment.name = json_obj.get('name', '')
        segment.model = model
        segment.date_range_start = json_obj.get('date_range_start', '')
        segment.date_range_end = json_obj.get('date_range_end', '')
        segment.source_offset_start = json_obj.get('source_offset_start', '')
        segment.source_offset_end = json_obj.get('source_offset_end', '')
        segment.status = json_obj.get('status', '')
        segment.column_source_bytes = json_obj.get('column_source_bytes', '')
        segment.input_records = json_obj.get('input_records', '')
        segment.input_records_size = json_obj.get('input_records_size', '')
        segment.last_build_time = json_obj.get('last_build_time', '')
        segment.last_build_time_dt = datetime.utcfromtimestamp(json_obj.get('last_build_time', 0) / 1000)
        segment.last_build_job_id = json_obj.get('last_build_job_id', '')
        segment.create_time_utc = json_obj.get('create_time_utc', '')
        segment.create_time_utc_dt = datetime.utcfromtimestamp(json_obj.get('create_time_utc', 0) / 1000)
        segment.cuboid_shard_nums = json_obj.get('cuboid_shard_nums', '')
        segment.total_shards = json_obj.get('total_shards', '')
        segment.dictionaries = json_obj.get('dictionaries', '')
        segment.snapshots = json_obj.get('snapshots', '')
        segment.additionalInfo = json_obj.get('additionalInfo', '')
        segment.project_dictionaries = json_obj.get('project_dictionaries', '')

        return segment

    def export(self, hdfsPath, mkdirOnHdfs=False):
        self._client

    def __repr__(self):
        return "<{name}>".format(name=self.name)