from KE.v4.client import KE4
from KE.v4.segments import Segments
from KE.v4.segment import Segment
from KE.v4.project import Project
from KE.v4.job import Job
from KE.v4.model import Model
from KE.v4.query import Query
from KE.v4.user import User

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


__all__ = ['KE4', 'Segments', 'Segment', 'Project', 'Job', 'Model', 'Query', 'User']
