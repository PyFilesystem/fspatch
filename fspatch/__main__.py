from __future__ import unicode_literals

from fs import open_fs
from . import patch


from os.path import exists
fs = open_fs('mem://')
foo = fs.makedir('foo')
foo.touch('bar1')
foo.touch('bar2')

fs.tree()

with patch(fs):
    import os
    from os import listdir
    print(os.path.exists('foo'))
    d = os.listdir('/')
    print(d)
    print(listdir('/'))

print(os.listdir('/'))
print(listdir('/'))