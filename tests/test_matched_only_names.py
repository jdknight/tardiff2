# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestMatchedOnlyNames(TardiffTestCase):
    def test_matched_only_names(self) -> None:
        sample1 = Path('container-1') / 'sample.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'sample.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        def mode644(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.mode = 0o644
            return tarinfo

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1, filter=mode644)
        self.assertTrue(example1.is_file())

        def mode654(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
            tarinfo.mode = 0o654
            return tarinfo

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2, filter=mode654)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        opts = TarDiffOpts()
        opts.only_names = True

        # while different modes, we are only comparing file names here
        diffed, _ = tardiff(files, opts=opts)
        self.assertFalse(diffed)
