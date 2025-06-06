# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffUid(TardiffTestCase):
    def test_diff_uid(self) -> None:
        sample1 = Path('container-1') / 'sample.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'sample.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        def uid1000(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.uid = 1000
            return tarinfo

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1, filter=uid1000)
        self.assertTrue(example1.is_file())

        def uid1001(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.uid = 1001
            return tarinfo

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2, filter=uid1001)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # should be difference with two different uids
        diffed, _ = tardiff(files)
        self.assertTrue(diffed)
