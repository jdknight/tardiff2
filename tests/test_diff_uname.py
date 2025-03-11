# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffUname(TardiffTestCase):
    def test_diff_uname(self) -> None:
        sample1 = Path('container-1') / 'sample.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'sample.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        def uname_alpha(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.uname = 'alpha'
            return tarinfo

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1, filter=uname_alpha)
        self.assertTrue(example1.is_file())

        def uname_bravo(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.uname = 'bravo'
            return tarinfo

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2, filter=uname_bravo)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # should be difference with two different unames
        diffed, _ = tardiff(files)
        self.assertTrue(diffed)
