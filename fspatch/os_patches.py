from contextlib import contextmanager
import os
import errno
import sys

from fs.errors import ResourceNotFound, FSError

from .context import Patch


@contextmanager
def oserrors(path):
    try:
        yield
    except ResourceNotFound:
        _error = os.strerror(errno.ENOENT)
        raise OSError(errno.ENOENT, _error, path)
    except FSError as error:
        raise OSError(str(error))


class OSPatch(Patch):
    """Base class for an os module patch."""

    @property
    def fs(self):
        return self.context.filesystem

    def get_path(self, path):
        return self.context.get_path(path)


class Listdir(OSPatch):
    module = os
    attrib = 'listdir'

    def __call__(self, path='.'):
        if self.is_internal:
            return self._method(path)
        path = os.fsdecode(path)
        _path = self.context.get_path(path)
        try:
            dirlist = self.context.filesystem.listdir(_path)
        except ResourceNotFound as error:
            self.not_found(path)
        except FSError as error:
            raise OSError(str(error))
        return dirlist


class Exists(OSPatch):
    module = os.path
    attrib = 'exists'

    def __call__(self, path):
        _path = self.get_path(path)
        with oserrors(_path):
            return self.fs.exists(path)


class Lexists(OSPatch):
    module = os.path
    attrib = 'lexists'

    def __call__(self, path):
        _path = self.get_path(path)
        with oserrors(_path):
            return self.fs.exists(path)


class TimePatch(OSPatch):
    module = os.path
    attrib = ''
    details_key = ''

    def __call__(self, path):
        _path = self.get_path(path)
        with oserrors(_path):
            info = self.gs.getdetails(path)
        try:
            _time = info.raw['details'][self.details_key]
        except KeyError:
            raise OSError('unable to get time')
        return _time


class Getatime(TimePatch):
    attrib = 'getatime'
    details_key = 'accessed'


class Getmtime(TimePatch):
    attrib = 'getctime'
    details_key = 'modified'


class Getctime(TimePatch):
    attrib = 'getctime'
    details_key = (
        'metadata_changed'
        if sys.platform == 'linux' else
        'created'
    )
