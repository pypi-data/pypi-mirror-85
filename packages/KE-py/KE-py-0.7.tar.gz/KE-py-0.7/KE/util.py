# coding=u8
import time
import warnings
from functools import wraps
from datetime import date, datetime, timedelta
from six.moves import input


def danger_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        answer = input('Are you sure to run Yes/No: ')
        if answer.lower() == 'yes':
            return func(*args, **kwargs)
        else:
            return
    return wrapper


def unify_timestamp(d):
    """Convert date, datetime to timestamp

    :param d: date or datetime
    :return: timestamp
    """
    if isinstance(d, datetime):
        timestamp = d.strftime('%s000')
        return timestamp
    if isinstance(d, date):
        dt = datetime.fromordinal(d.toordinal())
        timestamp = dt.strftime('%s000')
        return timestamp
    else:
        return d
