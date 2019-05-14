DEFAULT_READ_ACL = {
    'all': 1,
    'role_admin': 1,
}

DEFAULT_WRITE_ACL = {
    'all': 0,
    'role_admin': 1
}

DEFAULT_UPDATE_ACL = {
    'all': 0,
    'role_admin': 1
}

DEFAULT_DELETE_ACL = {
    'all': 0,
    'role_admin': 1
}

DEFAULT_ROW_ACL = {
    'read': DEFAULT_READ_ACL,
    'write': DEFAULT_WRITE_ACL
}


def read_acl():
    return DEFAULT_READ_ACL


def write_acl():
    return DEFAULT_WRITE_ACL


def update_acl():
    return DEFAULT_UPDATE_ACL


def delte_acl():
    return DEFAULT_DELETE_ACL


def row_acl():
    return DEFAULT_ROW_ACL


def get_acl(permisson_name, level='default'):
    def acl():
        acl_map = {
            'read': DEFAULT_READ_ACL,
            'write': DEFAULT_WRITE_ACL,
            'update': DEFAULT_UPDATE_ACL,
            'delete': DEFAULT_DELETE_ACL,
            'row': DEFAULT_ROW_ACL
        }
        acl_item = acl_map.get(permisson_name, {})
        if level == 'sys' and permisson_name == 'row':
            acl_item['read'].update({'all': 0})
            acl_item['write'].update({'all': 0})
        elif level == 'sys':
            acl_item.update({'*': 0})
        return acl_item
    return acl
