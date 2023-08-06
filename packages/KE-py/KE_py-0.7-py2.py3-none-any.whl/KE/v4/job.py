# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import
from KE.base import Base
from datetime import datetime


class Job(Base):

    def __init__(self, client=None, job_id=None, name=''):
        """Job Object
        """
        super(Job, self).__init__(client=client)
        self.id = job_id
        self.name = name

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the job json object to a Job object

        :param client: the KE client
        :param json_obj: the job json object
        :return: Job object
        """
        client.logger.debug('job json_obj', json_obj)
        job = Job(client=client, job_id=json_obj['id'], name=json_obj['job_name'])
        job.id = json_obj['id']
        job.owner = json_obj.get('owner', '')
        job.last_modified = json_obj['last_modified']
        job.last_modified_dt = datetime.utcfromtimestamp(json_obj.get('last_modified', 0) / 1000)
        job.name = json_obj['job_name']
        job.status = json_obj['job_status']
        job.progress = json_obj['step_ratio'] * 100  # In KE3, it's called progress
        job.duration = json_obj['duration']
        job.project = json_obj['project']
        job.target_segments = json_obj['target_segments']
        job.exec_start_time = json_obj['exec_start_time']
        job.exec_start_time_dt = datetime.utcfromtimestamp(json_obj.get('exec_start_time', 0) / 1000)
        job.exec_end_time = json_obj['exec_end_time']
        job.exec_end_time_dt = datetime.utcfromtimestamp(json_obj.get('exec_end_time', 0) / 1000)
        job.wait_time = json_obj['wait_time']
        job.steps = json_obj['steps']
        job.step_ratio = json_obj['step_ratio']
        job.target_model = json_obj['target_model']

        return job

    def resume(self):
        self._client.fetch_json(
            '/jobs/{job_id}/resume/'.format(job_id=self.id),
            method='PUT')

    def pause(self):
        self._client.fetch_json(
            '/jobs/{job_id}/pause/'.format(job_id=self.id),
            method='PUT')

    def __repr__(self):
        return '<Job %s>' % self.name.split('-')[0].strip()
