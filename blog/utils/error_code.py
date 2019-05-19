"""
code < 0 系统级别错误
code = 0 返回正常
code > 0 业务错误
"""


_code = {
    -1: dict(
        en='Unkown Error',
        zh="未知错误"
    ),
    # success
    0: dict(
        en='OK',
        zh="成功"
    ),

    # system level code
    10001: dict(
        en="require login",
        zh='需要登录'),
    10003: dict(
        en="missing argument",
        zh='参数错误'),
    10004: dict(
        en="articel not exist",
        zh='资源不存在'),
    10005: dict(
        en="user authenticate failed",
        zh='用户名或密码错误'),
    10006: dict(
        en="Invlid token",
        zh='无效的Token')

    # server level code
}

BLANK_MSG = dict(en="No Msg", zh="无错误详细信息")


def get_msg(code=0, lang='zh'):
    msgs = _code.get(code) or BLANK_MSG
    msg = msgs.get(lang, '')
    return msg
