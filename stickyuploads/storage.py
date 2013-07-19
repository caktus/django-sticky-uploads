import tempfile

from django.core.files.storage import FileSystemStorage


class TempFileSystemStorage(FileSystemStorage):
    """Storage class to store files in the system /tmp."""

    def __init__(self):
        super(TempFileSystemStorage, self).__init__(
            location=tempfile.gettempdir(), base_url=None)

    def url(self, name):
        """Files are not accessable via url."""
        raise NotImplementedError()