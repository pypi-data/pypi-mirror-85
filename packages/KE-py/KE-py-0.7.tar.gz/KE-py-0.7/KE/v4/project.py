# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from KE.util import danger_action
from datetime import datetime


class Project(Base):

    def __init__(self, client=None, project_id=None, name=''):
        """Project Object
        """
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
        project.create_time_dt = datetime.utcfromtimestamp(json_obj.get('create_time_utc', 0) / 1000)
        project.description = json_obj['description']
        project.owner = json_obj['owner']
        project.last_modified = json_obj['last_modified']
        project.override_kylin_properties = json_obj['override_kylin_properties']
        project.version = json_obj['version']
        project.name = json_obj['name']
        project.segment_config = json_obj['segment_config']

        return project

    def models(self, name=None, offset=0, size=20, exact=True, status=None):
        """Get Models

        :param name:
        :param offset:
        :param size:
        :param exact: 是否和模型名称完全匹配
        :param status: 模型状态
        :return: Model List
        """
        return self._client.models(project=self.name, name=name, offset=offset, size=size, exact=exact, status=status)

    def jobs(self, time_filter=4, offset=0, size=20, sort_by='last_modify', reverse=True, key=None):
        """Get jobs

        :parameter:
            time_filter:
                最近一天	0
                最近一周	1
                最近一月	2
                最近一年	3
                所有	4

            offset: - 可选 int，每页返回的任务的偏移量，默认值为 "0"
            size: - 可选 int，每页返回的任务数量，默认值为 "20"
            sort_by: - 可选 string，排序字段，默认为 "last_modified"
            reverse: - 可选 boolean，是否倒序，默认为 "true"
            key: 筛选字段，目前支持筛选任务 ID 及任务对象名称

        :return: Job object list
        :rtype: jobs
        """
        return self._client.jobs(project=self.name, time_filter=time_filter,
                                 offset=offset, size=size, sort_by=sort_by,
                                 reverse=reverse, key=key)

    def export_models(self, models, dest_path=None):
        """模型元数据导出

        :param models:  必填, list，模型名称列表。比如 ['model1','model2']
        :param dest_path: 导出的文件绝对路径。默认为当前目录的{project}_{models}.zip。
        :return: None
        :rtype: None
        """
        if isinstance(models, str):
            models = [models]
        if not dest_path:
            dest_path = "{project}_{models}.zip".format(project=self.name, models=str(models))
        res = self._client.fetch_file(uri='/metastore/backup/models', params={'project': self.name},
                                      body={'names': models}, method='POST', dest_path=dest_path)
        return

    def import_models(self, models, dest_path):
        """
        导入模型
        :param models: 模型列表；比如：['model1','model2']
        :param dest_path: zip文件的绝对路径比如 '/tmp/xxx.zip'
        :return:
        """
        headers = {
            'Accept': 'application/vnd.apache.kylin-v4+json',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'en',
        }

        if isinstance(models, str):
            models = [models]
        if not dest_path:
            dest_path = "{project}_{models}.zip".format(project=self.name, models=str(models))

        res = self.upload_and_check_model_metadata(dest_path)
        signature = res['data']['signature']
        model_ids = [m['uuid'] for m in res['data']['models']]
        payload = {
            'signature': signature,
            'ids': model_ids
        }

        with open(dest_path, 'rb') as f:
            file_ = [('file', f)]

            res = self._client.upload_file(uri='/metastore/models', params={'project': self.name}, files=file_,
                                           data=payload, headers=headers, method='POST')

    def upload_and_check_model_metadata(self, file_path):
        """
        check imported zip file is validate
        :param file_path: string, full path of zip file
        :return:
        """
        headers = {
            'Accept': 'application/vnd.apache.kylin-v4+json',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'en',
        }

        with open(file_path, 'rb') as f:
            file_ = [('file', f)]
            res = self._client.upload_file(
                uri='/metastore/validation/models?project={project_name}'.format(project_name=self.name), method='POST',
                headers=headers,
                files=file_)

            return res

    def push_down_config(self):
        pass

    @danger_action
    def delete(self):
        json_obj = self._client.fetch_json(uri='/projects/{project}'.format(project=self.name), method='DELETE')
        return json_obj['data']

    def __repr__(self):
        return '<Project %s>' % self.name
