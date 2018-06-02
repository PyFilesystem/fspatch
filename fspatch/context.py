import inspect
import gc
from os.path import dirname, join

import fs
FS_PATH = dirname(fs.__file__) + '/'


class Patch:
    module = None
    attrib = None

    def __init__(self, context):
        self.context = context
        self._method = getattr(
            self.module,
            self.attrib
        )

    def __repr__(self):
        return 'patched: %r' % self._method

    def __str__(self):
        return 'patched: %s' % self._method

    @property
    def is_internal(self):
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        caller_path = dirname(module.__file__) + '/'
        return caller_path.startswith(FS_PATH)

    def __call__(self):
        return None


class Context:

    def __init__(self, filesystem, patches, cwd='/', auto_close=False):
        self.filesystem = filesystem
        self.patch_classes = patches
        self.cwd = cwd
        self.auto_close = auto_close

        self.file_handles = {}
        self.patches = set()

    def get_path(self, path):
        path = join(self.cwd, path)
        return path

    def __enter__(self):
        for patch_cls in self.patch_classes:
            patch = patch_cls(self)
            method = patch._method
            namespaces = gc.get_referrers(method)
            for namespace in namespaces:
                if not isinstance(namespace, dict):
                    continue
                if 'OSFS' in namespace:
                    print(namespace)
                    continue
                for k, v in list(namespace.items()):
                    if v is method and k != '_method':
                        namespace[k] = patch
                        self.patches.add(patch)

    def __exit__(self, exc_type, exc_value, tb):
        for patch in self.patches:
            method = patch._method
            namespaces = gc.get_referrers(patch)
            for namespace in namespaces:
                if not isinstance(namespace, dict):
                    continue
                if 'OSFS' in namespace:
                    print(namespace)
                    continue
                for k, v in list(namespace.items()):
                    if v is patch:
                        namespace[k] = method
        self.patches.clear()
