import uuid
from abc import abstractmethod

from django.db import models
from django_mysql.models import Model, JSONField
from acl.default_acl import row_acl


class BaseModel(Model):
    created = models.DateTimeField("创建时间", auto_now_add=True)
    last_modified = models.DateTimeField("最后修改时间", auto_now=True)
    # acl = JSONField(default=get_acl('row', level='sys'))
    acl = JSONField(default=row_acl)
    is_active = models.BooleanField("删除标记", default=True)
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"

    def _to_dict(self):
        # TODO 排除文件类型字段
        FOREIGNKEY_LIKE_KEY = ['ForeignKey', 'TreeForeignKey', 'OneToOneField', ]
        field_map = {i.name: i for i in self._meta.fields}
        # many_to_many_map = {i.name: i for i in self._meta.many_to_many}
        # fields = list(field_map.items()) + list(many_to_many_map.items())
        fields = field_map.items()

        _fields = {}
        for name, field in fields:
            internal_type = field.get_internal_type()
            default = field.get_default()
            if internal_type in FOREIGNKEY_LIKE_KEY:
                name += '_id'
            _fields[name] = dict(internal_type=internal_type, field=field, default=default)

        data = {}

        for field_name, field_config in _fields.items():
            internal_type = field_config['internal_type']
            # if internal_type in FOREIGNKEY_LIKE_KEY + ['ManyToManyField']:
            #     attr = getattr(self, field_name)
            #     value = list(attr.values()) if attr else None
            # else:
            value = self.__dict__[field_name]
            data[field_name] = value
        return data

    def to_dict(self):
        return self._to_dict()

    @staticmethod
    def pagination(query_set, limit=20, offset=0):
        meta = dict(total_count=query_set.count(),
                    limit=limit,
                    offset=offset)
        objects = [o.to_dict() for o in query_set[offset:limit]]
        return dict(meta=meta, objects=objects)
