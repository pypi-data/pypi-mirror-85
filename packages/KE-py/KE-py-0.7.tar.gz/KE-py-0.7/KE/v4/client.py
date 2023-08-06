# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.v4.project import Project
from KE.v4.job import Job
from KE.v4.model import Model
from KE.v4.user import User
from KE.v4.query import Query
from KE.v3.client import KE3


class KE4(KE3):
    """Part of API still call the KE3 API"""
    headers = {
        'Accept': 'application/vnd.apache.kylin-v4-public+json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json;charset=utf-8'
    }
    internal_headers = {
        'Accept': 'application/vnd.apache.kylin-v4+json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json;charset=utf-8'
    }

    def __init__(self, host, port=7070, username='ADMIN', password='KYLIN', debug=False, ssl=False, verify=True):
        """创建KE4 Client客户端实例

        :param host: 主机名 或 IP 或 主机的List，如 ['device1','device2'], 此情况会随机选其中一个进行请求, 起到负载均衡作用
        :param port: 端口
        :param username: 用户名
        :param password: 密码
        :param debug: 是否开启Debug模式
        :param ssl: 是否开启SSL
        :param verify: 是否开启SSL的验证，默认为开启
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.version = 4
        self.projects_count = None
        self.debug = debug
        self.ssl = ssl
        self.verify = verify

    def projects(self, name=None, offset=0, size=1000, exact=True):
        """Get projects

        :param name: project name
        :param offset:
        :param size:
        :param exact: 是否对项目名称进行完全匹配，默认为 true
        :return:  Project Object list
        :rtype: Project Object
        """
        params = {'project': name, 'page_offset': offset, 'page_size': size, 'exact': exact}
        json_obj = self.fetch_json('/projects/', params=params)
        self.logger.debug(json_obj)
        projects_json = json_obj['data']['value']
        total = json_obj['data']['total_size']
        self.projects_count = total

        return [Project.from_json(self, json_obj=p) for p in projects_json]

    def jobs(self, time_filter=4, project=None,
             offset=0, size=20, sort_by='last_modify', reverse=True, key=None):
        """Get jobs

        :parameter:
            time_filter:
                最近一天	0
                最近一周	1
                最近一月	2
                最近一年	3
                所有	4

            project: - 可选 string，项目名称
            offset: - 可选 int，每页返回的任务的偏移量，默认值为 "0"
            size: - 可选 int，每页返回的任务数量，默认值为 "10"
            sort_by: - 可选 string，排序字段，默认为 "last_modified"
            reverse: - 可选 boolean，是否倒序，默认为 "true"
            key: 筛选字段，目前支持筛选任务 ID 及任务对象名称

        :return: Job object list
        :rtype: jobs
        """
        params = {'time_filter': time_filter, 'project': project, 'page_offset': offset,
                  'page_size': size, 'sort_by': sort_by, 'reverse': reverse, 'key': key}
        json_obj = self.fetch_json('/jobs/', params=params)
        self.logger.debug(json_obj)
        obj = json_obj['data']['value']
        return [Job.from_json(client=self, json_obj=j) for j in obj]

    def cubes(self, name=None, offset=0, size=20,
              exact_match=True, model_name=None, project=None,
              sort_by='update_time', reverse=True):
        """Attention! KE4 does not have Cube, use Model instead.

        :return:
        """
        print('Attention, KE4 does not have Cube, use Model instead.')

    def models(self, project=None, name=None, offset=0, size=20, exact=True, status=None):
        """Get Models

        :param project: required
        :param name:
        :param offset:
        :param size:
        :param exact: 是否和模型名称完全匹配
        :param status: 模型状态
        :return: Model List
        """
        params = {'model_name': name, 'page_offset': offset, 'page_size': size,
                  'exact': exact, 'project': project, 'status': status}
        json_obj = self.fetch_json('/models/', params=params)
        models_json = json_obj['data']['value']
        return [Model.from_json(client=self, json_obj=m, project=project) for m in models_json]

    def users(self, project=None, case_sensitive=False, offset=0, size=10):
        """Get Users

        :param project:
        :param case_sensitive:
        :param offset:
        :param size:
        :return:
        """
        params = {'project': project, 'isCaseSensitive': case_sensitive,
                  'page_offset': offset, 'page_size': size}
        json_obj = self.fetch_json(uri='/user', params=params, headers=KE4.headers)
        users_json = json_obj['data']['value']
        return [User.from_json(client=self, json_obj=u) for u in users_json]

    def query(self, sql, project, offset=0, limit=100, timeout=120):
        """查询

        :param sql:
        :param project:
        :param offset:
        :param limit:
        :param timeout:
        :return:
        """
        body = {'sql': sql, 'offset': offset, 'limit': limit, 'project': project}
        json_obj = self.fetch_json(uri='/query/', body=body, method='POST', timeout=timeout)
        return Query.from_json(client=self, json_obj=json_obj['data'], project=project)

    def create_project(self, name, maintain_model_type, description=''):
        """Create Project

        :param name:
        :param maintain_model_type: Required. Options:
            AUTO_MAINTAIN
            MANUAL_MAINTAIN表示 AI 增强模式。
        :param description:
        :return:
        """
        body = {'name': name, 'maintain_model_type': maintain_model_type, 'description': description}
        json_obj = self.fetch_json(uri='/projects', method='POST', body=body)
        return Project.from_json(client=self, json_obj=json_obj['data'])

    def create_user(self):
        pass
