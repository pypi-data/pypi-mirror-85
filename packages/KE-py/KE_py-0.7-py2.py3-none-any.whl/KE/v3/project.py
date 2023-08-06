# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from KE.util import danger_action
from datetime import datetime


class Project(Base):

    def __init__(self, client=None, project_id=None, name=''):
        """Project Object"""
        super(Project, self).__init__(client=client)
        self.id = project_id
        self.name = name

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the project json object to a Project object

        :param client: the KE client
        :param json_obj: the project json object
        :return: Project object
        """

        project = Project(client=client, project_id=json_obj['uuid'], name=json_obj['name'])

        project.last_modified = json_obj['last_modified']
        project.status = json_obj['status']
        project.create_time_utc = json_obj['create_time_utc']
        if project.create_time_utc:
            project.create_time_utc_dt = datetime.utcfromtimestamp(json_obj.get('create_time_utc') / 1000)
        project.last_update_time = json_obj['last_update_time']
        if project.last_update_time:
            project.last_update_time_dt = datetime.utcfromtimestamp(json_obj.get('last_update_time') / 1000)
        project.description = json_obj['description']
        project.realizations = json_obj['realizations']
        project.owner = json_obj['owner']
        project.last_modified = json_obj['last_modified']
        project.override_kylin_properties = json_obj['override_kylin_properties']
        project.version = json_obj['version']
        project.name = json_obj['name']
        project.tables = json_obj['tables']

        return project

    def cubes(self, name=None, offset=0, size=20,
              exact_match=True, model_name=None,
              sort_by='update_time', reverse=True):
        """Get Cubes

        :param offset: - 可选 int，返回数据起始下标，默认为 0
        :param size: - 可选 int，分页返回对应每页返回多少，默认为10
        :param name: - 可选 string， Cube 名称
        :param exact_match: - 可选 boolean，是否根据 Cube 名称完全匹配，默认为 true
        :param model_name: - 可选 string，返回对应模型名称等于该关键字的 Cube
        :param sort_by: - 可选 string，指定排序字段，默认为 update_time
        :param reverse: - 可选 boolean，是否倒序，默认为 true
        :return: List of Cube object
        """
        return self._client.cubes(project=self.name, name=name, offset=offset,
                                  size=size, exact_match=exact_match, model_name=model_name,
                                  sort_by=sort_by, reverse=reverse)

    def models(self):
        # TODO
        pass

    def jobs(self, time_filter=0, status=None, offset=0, size=20, sort_by=None):
        """Get jobs of the project

        Parameters:
            time_filter:
                最近一天	0
                最近一周	1
                最近一月	2
                最近一年	3
                所有	4
            status:
                NEW	0
                PENDING	1
                RUNNING	2
                FINISHED	4
                ERROR	8
                DISCARDED	16
                STOPPED	32
            sort_by:
                排序字段
            offset:
            size:
            
        :return: Job object list
        :rtype: jobs
        """
        return self._client.jobs(project=self.name, time_filter=time_filter, status=status,
                                 offset=offset, size=size, sort_by=sort_by)

    @danger_action
    def delete(self):
        """Delete the project; 删除Project

        :return:
        """
        json_obj = self._client.fetch_json(uri='/projects/{project}'.format(project=self.name), method='DELETE')
        return json_obj['data']

    def __repr__(self):
        return '<Project %s>' % self.name
