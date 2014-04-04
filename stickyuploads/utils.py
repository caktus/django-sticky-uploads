from __future__ import unicode_literals

import os

from django.core import signing
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject


def serialize_upload(name, storage, url):
    """
    Serialize uploaded file by name and storage. Namespaced by the upload url.
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
    }, salt=url)


def deserialize_upload(value, url):
    """
    Restore file and name and storage from serialized value and the upload url.
    """
    result = {'name': None, 'storage': None}
    try:
        result = signing.loads(value, salt=url)
    except signing.BadSignature:
        # TODO: Log invalid signature
        pass
    else:
        try:
            result['storage'] = get_storage_class(result['storage'])
        except (ImproperlyConfigured, ImportError):
            # TODO: Log invalid class
            result = {'name': None, 'storage': None}
    return result


def open_stored_file(value, url):
    """
    Deserialize value for a given upload url and return open file.
    Returns None if deserialization fails.
    """
    upload = None
    result = deserialize_upload(value, url)
    filename = result['name']
    storage_class = result['storage']
    if storage_class and filename:
        storage = storage_class()
        if storage.exists(filename):
            upload = storage.open(filename)
            upload.name = os.path.basename(filename)
    return upload