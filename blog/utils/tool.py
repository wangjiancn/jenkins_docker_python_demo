import uuid
from collections import namedtuple
from django.http import QueryDict
from typing import Tuple, NamedTuple


def is_uuid(arg):
    uuid_str = str(arg)
    try:
        uuid.UUID(uuid_str)
    except Exception:
        return False
    else:
        return True


def parse_query_string(queryDict: QueryDict) -> NamedTuple(
        'query', pagination=dict, order_by=list, filters=dict, defer=list):
    """从请求中解析查询参数

    Args:
        queryDict ([django.http.QueryDict]): 接受request.GET作为参数,
             官方链接:https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.QueryDict

    Returns:
        NamedTuple: NamedTuple('query', pagination=dict, order_by=list, filters=dict)
    """

    _clone = queryDict.copy()

    Query = namedtuple('Query', 'pagination, order_by, filters, defer')

    order_by = _clone.pop('order_by', [])
    pagination = {
        'limit': int(_clone.pop('limit', [10])[-1]),
        'offset': int(_clone.pop('offset', [0])[-1]),
    }

    defer = []
    defer_query = _clone.pop('defer', [])
    for i in defer_query:
        defer.extend(i.split(','))

    filters = _clone.dict()

    query = Query(pagination, order_by, filters, defer)
    return query
