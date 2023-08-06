# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from datetime import datetime


class Model(Base):

    def __init__(self, client=None, name=None, project_name=None):
        """Model Object
        """
        super(Model, self).__init__(client=client)

        self.name = name
        self.project_name = project_name

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the project json object to a Model object

        :param client: the KE client
        :param json_obj: the model json object
        :return: Model object
        """
        client.logger.debug(json_obj)
        model = Model(client=client, project_name=json_obj['project'], name=json_obj['name'])
        model.id = json_obj['uuid']
        model.last_modified = json_obj['last_modified']
        if model.last_modified:
            model.last_modified_dt = datetime.utcfromtimestamp(json_obj['last_modified']/1000)
        model.version = json_obj['version']
        model.owner = json_obj['owner']
        model.description = json_obj['description']
        model.lookups = json_obj['lookups']
        model.fact_table = json_obj['fact_table']
        model.dimensions = json_obj['dimensions']
        model.metrics = json_obj['metrics']
        model.partition_desc = json_obj['partition_desc']
        model.capacity = json_obj['capacity']
        model.computed_columns = json_obj['computed_columns']
        model.smart_model = json_obj['smart_model']
        model.smart_model_sqls = json_obj['smart_model_sqls']

        return model

    def __repr__(self):
        return '<Model %s>' % self.name
