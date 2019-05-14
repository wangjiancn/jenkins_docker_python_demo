from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_mysql.models import JSONField

from utils.base_model import BaseModel

from .default_acl import write_acl, update_acl, delte_acl, read_acl

# Create your models here.


class Acl(BaseModel):
    scope = models.CharField("类型(表/视图/操作..)", max_length=50, db_index=True)
    name = models.CharField("名称", max_length=50, db_index=True)
    # read = JSONField(default=get_acl('read', level='sys'))
    # write = JSONField(default=get_acl('write', level='sys'))
    # update = JSONField(default=get_acl('update', level='sys'))
    # delete = JSONField(default=get_acl('delete', level='sys'))

    read = JSONField(default=read_acl)
    write = JSONField(default=write_acl)
    update = JSONField(default=update_acl)
    delete = JSONField(default=delte_acl)


class Role(BaseModel):
    name = models.CharField("角色名", max_length=50, db_index=True)
    desc = models.CharField("描述", max_length=50)


class Group(BaseModel):
    name = models.CharField("权限组", max_length=50, db_index=True)
    desc = models.CharField("描述", max_length=50)
    roles = models.ManyToManyField(Role)


class UserProfile(AbstractUser, BaseModel):

    mobile_validator = RegexValidator(
        regex=r'^1\d{10}$', message='Mobile format error!')

    mobile = models.CharField(
        '手机号码',
        max_length=16,
        validators=[mobile_validator])

    nickname = models.CharField(
        _('nickname'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer. \
            Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    roles = models.ManyToManyField(Role)
    groups = models.ManyToManyField(Group)

    @property
    def token(self):
        return self._generate_jwt()

    def _generate_jwt(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow(),
            'data': {
                'username': self.username,
                'is_active': self.is_active,
                'nickname': self.nickname
            }
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

    def to_dict(self):
        return dict(
            username=self.username,
            nickname=self.nickname,
        )
