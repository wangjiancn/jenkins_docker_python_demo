import uuid


def is_uuid(arg):
    uuid_str = str(arg)
    try:
        uuid.UUID(uuid_str)
    except Exception:
        return False
    else:
        return True
