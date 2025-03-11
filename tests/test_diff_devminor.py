# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffDevminor(TardiffTestCase):
    def test_diff_devminor(self) -> None:
        fentry = tarfile.TarInfo(name='container/dev-entry')
        fentry.type = tarfile.CHRTYPE
        fentry.devmajor = 1
        fentry.devminor = 3

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.addfile(fentry)
        self.assertTrue(example1.is_file())

        fentry = tarfile.TarInfo(name='container/dev-entry')
        fentry.type = tarfile.CHRTYPE
        fentry.devmajor = 1
        fentry.devminor = 4

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.addfile(fentry)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # should be difference with two different devmodes
        diffed, _ = tardiff(files)
        self.assertTrue(diffed)
