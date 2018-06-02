from fs import open_fs
from fs.base import FS

from .context import Context
from . import os_patches

PATCHES = [
    os_patches.Listdir,
    os_patches.Exists,
    os_patches.Lexists,
    os_patches.Getatime,
    os_patches.Getmtime,
    os_patches.Getctime
]


def patch(fs_url, patches=None, cwd='/'):
    """
    Patch a filesystem over Python builtins.

    """

    if isinstance(fs_url, FS):
        filesystem = fs_url
        auto_close = True
    else:
        filesystem = open_fs(fs_url)
        auto_close = False

    return Context(
        filesystem,
        patches or PATCHES,
        cwd=cwd,
        auto_close=auto_close
    )
