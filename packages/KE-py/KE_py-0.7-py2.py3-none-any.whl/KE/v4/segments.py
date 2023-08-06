# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import
from KE.base import Base
from KE.v4.job import Job
from KE.v4.segment import Segment
from KE.util import danger_action


class Segments(Base):

    def __init__(self, client=None, model=None, segment_list=None):
        """Segments Object, List of Segment
        """
        super(Segments, self).__init__(client=client)
        self.model = model
        self.segment_list = segment_list
        self.segment_id_list = None
        self.segment_id_list = None
        self._segment_range = None
        self.size = None

    @classmethod
    def from_json(cls, client=None, json_obj=None, model=None, project=None):
        """Deserialize the segment json object to a Segment object

        :param client: the KE client
        :param json_obj: the segment json object
        """

        segment_id_list = [s['id'] for s in json_obj]
        segment_name_list = [s['name'] for s in json_obj]
        segments = Segments(client=client, model=model)
        segments.size = len(segment_name_list)
        segments.model = model
        segments.project = project
        segments.segment_id_list = segment_id_list
        segments.segment_name_list = segment_name_list
        segments.segment_list = [Segment.from_json(client=client, model=model, json_obj=s) for s in json_obj]

        return segments

    @classmethod
    def from_segment_list(cls, model, client=None, segment_list=None):
        """
        Parse segment list to a Segments object
        """
        segments = Segments(client=client, model=model, segment_list=segment_list)
        return segments

    def _twoinone(self, build_type):
        if len(self.segment_id_list) == 0:
            # the segments is empty, return
            return
        body = {'type': build_type,
                'ids': self.segment_id_list,
                'project': self.project,
                }

        uri = '/models/{model_name}/segments'.format(model_name=self.model)
        json_obj = self._client.fetch_json(uri=uri, method='PUT', body=body)
        data = json_obj['data']
        return data

    def merge(self, mp_values=None, force=None):
        """合并segment

        :param mp_values:
        :param force:
        :return:
        """
        return self._twoinone('MERGE')

    def refresh(self):
        return self._twoinone('REFRESH')

    @danger_action
    def drop(self, purge=False, force=False):
        """

        :param purge: required boolean，是否清空 Segments。
        :param force: optional boolean，是否强制删除，默认值为 "false"。
        :return:
        """
        if len(self.segment_id_list) == 0:
            # the segments is empty, return
            return
        params = {
                'purge': purge,
                'ids': self.segment_id_list,
                'project': self.project,
                'force': force,
                }

        uri = '/models/{model_name}/segments'.format(model_name=self.model)

        json_obj = self._client.fetch_json(uri=uri, method='DELETE', params=params)
        data = json_obj['data']

        return data

    def list_segments(self):
        """列出 segment

        :return:
        """
        return self.segment_list

    @property
    def segment_range(self):
        """Return the range of Segments. e.g.: 19700101000000_20200206000000

        :return:
        """
        if len(self.segment_list) == 0:
            return []

        if not self._segment_range:
            datetime_list = []
            for name in self.segment_name_list:
                start, end = name.split('_')
                datetime_list.append(start)
                datetime_list.append(end)
            return "%s_%s" % (min(datetime_list), max(datetime_list))
        else:
            return self._segment_range

    @property
    def segment_count(self):
        return len(self.segment_id_list)

    def __repr__(self):
        return '<Segments: %s>' % self.segment_range
