from django.core import signing
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject


def serialize_upload(name, storage):
    """
    Serialize uploaded file by name and storage.
    """
    if isinstance(storage, LazyObject):
        # Unwrap lazy storage class
        storage._setup()
        cls = storage._wrapped.__class__
    else:
        cls = storage.__class__
    return signing.dumps({
        'name': name,
        'storage': '%s.%s' % (cls.__module__, cls.__name__)
    })


def deserialize_upload(value):
    """
    Restore file and name and storage from serialized value.
    """
    result = {'name': None, 'storage': None}
    try:
        result = signing.loads(value)
    except signing.BadSignature:
        # TODO: Log invalid signature
        pass
    else:
        result['storage'] = get_storage_class(result['storage'])
    return result


def open_stored_file(value):
    """
    Deserialize value and return open file. Returns None if deserialization fails.
    """
    upload = None
    result = deserialize_upload(value)
    filename = result['name']
    storage_class = result['storage']
    if storage_class and filename:
        storage = storage_class()
        upload = storage.open(filename)
    return upload