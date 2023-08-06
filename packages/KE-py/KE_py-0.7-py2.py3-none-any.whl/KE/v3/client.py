# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import BaseClient
from KE.v3.project import Project
from KE.v3.job import Job
from KE.v3.cube import Cube
from KE.v3.user import User
from KE.v3.query import Query
from KE.v3.model import Model


class KE3(BaseClient):
    headers = {
        'Accept': 'application/vnd.apache.kylin-v2+json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json;charset=utf-8'
    }

    def __init__(self, host, port=7070, username='ADMIN', password='KYLIN', debug=False, ssl=False):
        """创建KE3 Client客户端实例

        :param host: 主机名 或 IP 或 主机的List，如 ['device1','device2'], 此情况会随机选其中一个进行请求, 起到负载均衡作用
        :param port: 端口
        :param username: 用户名
        :param password: 密码
        :param debug: 是否开启Debug模式
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.version = 3
        self.projects_count = None
        super(KE3, self).__init__(debug=debug, ssl=ssl)

    def projects(self, name=None, offset=0, size=1000, exact=True):
        """Get projects

        :param name: project name
        :param offset: 默认为0
        :param size: 默认为1000
        :param exact: 可选 boolean，是否根据 Cube 名称完全匹配，默认为 true
        :return: Project List
        :rtype: list of Project Object
        """
        params = {'pageOffset': offset, 'pageSize': size, 'exact': exact}
        json_obj = self.fetch_json('/projects/', params=params)
        obj = json_obj['data']['projects']
        total = json_obj['data']['size']
        self.projects_count = total
        if name:
            # The original API seems not to support name param, weired.
            for p in obj:
                if p['name'] == name:
                    return Project.from_json(self, json_obj=p)
            return
        return [Project.from_json(self, json_obj=p) for p in obj]

    def jobs(self, time_filter=4, name=None, project=None,
             status=None, offset=0, size=20, sort_by='last_modify', reverse=True):
        """Get jobs

        :param name: Job name
        :param project: project
        :param time_filter:
                最近一天	0
                最近一周	1
                最近一月	2
                最近一年	3
                所有	4
        :param status:
                NEW	0
                PENDING	1
                RUNNING	2
                FINISHED	4
                ERROR	8
                DISCARDED	16
                STOPPED	32
        :param sort_by: 排序字段
        :param offset:
        :param size:
        :return: Job object list
        :rtype: jobs
        """
        params = {'timeFilter': time_filter, 'pageOffset': offset,
                  'pageSize': size, 'sort_by': sort_by, 'reverse': reverse}
        if name:
            params['jobName'] = name
        if project:
            params['projectName'] = project
        if status:
            params['status'] = status

        json_obj = self.fetch_json('/jobs/', params=params)
        obj = json_obj['data']['jobs']
        return [Job.from_json(self, json_obj=j) for j in obj]

    def cubes(self, name=None, offset=0, size=20,
              exact_match=True, model_name=None, project=None,
              sort_by='update_time', reverse=True):
        """Get Cubes

        :param offset: - 可选 int，返回数据起始下标，默认为 0
        :param size: - 可选 int，分页返回对应每页返回多少，默认为10
        :param name: - 可选 string， Cube 名称
        :param exact_match: - 可选 boolean，是否根据 Cube 名称完全匹配，默认为 true
        :param model_name: - 可选 string，返回对应模型名称等于该关键字的 Cube
        :param project: - 可选 string，项目名称
        :param sort_by: - 可选 string，指定排序字段，默认为 update_time
        :param reverse: - 可选 boolean，是否倒序，默认为 true
        :return: List of Cube object
        """
        params = {'pageOffset': offset, 'pageSize': size, 'sortby': sort_by, 'reverse': reverse}
        if name:
            params['cubeName'] = name
        if exact_match:
            params['exactMatch'] = exact_match
        if model_name:
            params['modelName'] = model_name
        if project:
            params['projectName'] = project

        json_obj = self.fetch_json('/cubes/', params=params)
        cubes_json = json_obj['data']['cubes']

        return [Cube.from_json(client=self, json_obj=c) for c in cubes_json]

    def models(self, name=None, offset=0, size=20,
               exact_match=True, project=None):
        """Get Models; 获取 Models

        :param offset: - 可选 int，返回数据起始下标，默认为 0
        :param size: - 可选 int，每页返回多少，默认为 20
        :param name: - 可选 string，模型名称
        :param exact_match: - 可选 boolean，是否对模型名称进行完全匹配，默认为 true
        :param project: - 可选 string， 项目名称
        :return: list of Model Object
        """
        params = {'pageOffset': offset, 'pageSize': size, 'modelName': name, 'projectName': project}
        json_obj = self.fetch_json('/models/', params=params)['data']['models']
        return [Model.from_json(client=self, json_obj=m) for m in json_obj]

    def query(self, sql, project, offset=0, limit=100, timeout=120):
        """查询

        :param sql: SQL
        :param project: 项目
        :param offset: 默认0
        :param limit: 默认100
        :param timeout: timeout
        :return: Pandas DataFrame
        """
        body = {'sql': sql, 'offset': offset, 'limit': limit, 'project': project}
        json_obj = self.fetch_json(uri='/query/', body=body, method='POST', timeout=timeout)
        return Query.from_json(client=self, json_obj=json_obj['data'], project=project)

    def users(self, name=None, project=None, case_sensitive=False, offset=0, size=10):
        """获取User

        :param name: user name
        :param project:
        :param case_sensitive:
        :param offset: 默认0
        :param size: 默认10
        :return: User object
        """
        params = {'name': name, 'project': project, 'isCaseSensitive': case_sensitive,
                  'pageOffset': offset, 'pageSize': size}
        json_obj = self.fetch_json(uri='/kap/user/users/', params=params, headers=KE3.headers)
        users_json = json_obj['data']['users']

        return [User.from_json(client=self, json_obj=u) for u in users_json]

    def create_user(self):
        pass

    def create_project(self):
        pass

