# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import
from KE.base import Base
from datetime import datetime


class Job(Base):

    def __init__(self, client=None, job_id=None, name=''):
        """Job Object"""
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

        job = Job(client=client, job_id=json_obj['uuid'], name=json_obj['name'])

        job.id = json_obj['uuid']
        job.owner = json_obj.get('owner', '')
        job.last_modified = json_obj['last_modified']
        job.last_modified_dt = datetime.utcfromtimestamp(json_obj['last_modified'] / 1000)
        job.version = json_obj['version']
        job.name = json_obj['name']
        job.status = json_obj.get('job_status')
        if not job.status:
            job.status = json_obj.get('status')
        job.type = json_obj.get('type')
        job.duration = json_obj.get('duration')
        job.project_name = json_obj['project_name']
        job.related_segment = json_obj['related_segment']
        job.exec_start_time = json_obj['exec_start_time']
        job.exec_start_time_dt = datetime.utcfromtimestamp(json_obj.get('exec_start_time', 0) / 1000)
        job.exec_end_time = json_obj['exec_end_time']
        job.exec_end_time_dt = datetime.utcfromtimestamp(json_obj.get('exec_end_time', 0) / 1000)
        job.exec_interrupt_time = json_obj['exec_interrupt_time']
        job.mr_waiting = json_obj['mr_waiting']
        job.steps = json_obj['steps']
        job.progress = round(json_obj['progress'], 2)

        return job

    def resume(self):
        """继续任务

        :return:
        """
        json_obj = self._client.fetch_json(
            '/jobs/{job_id}/resume/'.format(job_id=self.id),
            method='PUT')
        return Job.from_json(client=self._client, json_obj=json_obj['data'])

    def pause(self):
        """暂停任务

        :return:
        """
        json_obj = self._client.fetch_json(
            '/jobs/{job_id}/pause/'.format(job_id=self.id),
            method='PUT')
        return Job.from_json(client=self._client, json_obj=json_obj['data'])

    def cancel(self):
        """取消任务

        :return:
        """
        json_obj = self._client.fetch_json(
            '/jobs/{job_id}/cancel/'.format(job_id=self.id),
            method='PUT')
        return Job.from_json(client=self._client, json_obj=json_obj['data'])

    def drop(self):
        """删除任务

        :return:
        """
        json_obj = self._client.fetch_json(
            '/jobs/{job_id}/drop/'.format(job_id=self.id),
            method='DELETE')
        return Job.from_json(client=self._client, json_obj=json_obj['data'])

    def refresh(self, inplace=False):
        """Get the latest stats of the Job object

        :param inplace: Whether to return a new Job. Default is False
        :return: Job object
        """
        jobs = self._client.jobs(name=self.name)
        if len(jobs) > 0:
            if inplace:
                job = jobs[0]
                self._update_props(job)
                return self
            else:
                return jobs[0]

    def _update_props(self, new_job):
        for prop, value in self.__dict__.items():
            self.__setattr__(prop, getattr(new_job, prop))

    def __str__(self):
        return '<Job %s>' % self.name.split('-')[0].strip()

    def __repr__(self):
        return '<Job %s>' % self.name.split('-')[0].strip()
