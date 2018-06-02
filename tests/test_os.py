import os
from os import listdir

from fs import open_fs
import fspatch


class TestOS:

    ROOT_DIR = [
        'empty',
        'foo',
        'test.bin',
        'test.txt'
    ]

    BIN_CONTENTS = b'\x00\x01\x02'
    TEXT_CONTENTS = 'Where there is a will'

    def setup_method(self, method):
        self.fs = open_fs('temp://fspatch')
        self.fs.makedirs('foo/bar/baz')
        self.fs.touch('empty')
        self.fs.setbytes('test.bin', self.BIN_CONTENTS)
        self.fs.settext('test.txt', self.TEXT_CONTENTS)

    def teardown_method(self, method):
        self.fs.close()
        self.fs = None

    def test_listdir(self):
        with fspatch.patch(self.fs):
            assert sorted(os.listdir('/')) == sorted(self.ROOT_DIR)
