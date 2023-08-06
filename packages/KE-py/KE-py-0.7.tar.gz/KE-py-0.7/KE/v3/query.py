# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import, division
from KE.base import Base
import pandas as pd


class Query(Base):

    def __init__(self, client=None, query_id=None):
        """Query Object
        """
        super(Query, self).__init__(client=client)

        self.id = query_id

    @classmethod
    def from_json(cls, client=None, json_obj=None, project=None):
        """Deserialize the job json object to a Job object

        :client: the KE client
        :json_obj: the job json object
        """
        client.logger.debug(json_obj)
        query = Query(client=client, query_id=json_obj['queryId'])
        column_metas = json_obj['columnMetas']

        query.affectedRowCount = json_obj['affectedRowCount']
        query.isException = json_obj['isException']
        query.exceptionMessage = json_obj['exceptionMessage']
        query.duration = json_obj['duration']
        query.totalScanCount = json_obj['totalScanCount']
        query.totalScanBytes = json_obj['totalScanBytes']
        query.hitExceptionCache = json_obj['hitExceptionCache']
        query.storageCacheUsed = json_obj.get('storageCacheUsed')
        query.server = json_obj['server']
        query.sparderUsed = json_obj['sparderUsed']
        query.timeout = json_obj['timeout']
        query.pushDown = json_obj['pushDown']
        query.cube = json_obj['cube']
        query.results = json_obj['results']
        query.df = cls._to_pandas(query.results, column_metas)
        query.project = project
        query.realizations = json_obj.get('realizations')
        return query

    @staticmethod
    def _to_pandas(results, column_metas):
        if results:
            cols = [c['name'] for c in column_metas]
            df = pd.DataFrame(results, columns=cols)
            return df
        else:
            return pd.DataFrame()

    def __repr__(self):
        return '<Query %s>' % self.id
