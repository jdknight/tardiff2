# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffDetaileds(TardiffTestCase):
    def test_diff_detailed(self) -> None:
        sample1 = Path('container-1') / 'sample.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'sample.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is another example file.\n')
        self.assertTrue(sample2.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1)
        self.assertTrue(example1.is_file())

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        opts = TarDiffOpts()
        opts.detailed = 2

        # at this time, this run is mainly to check if a detailed request
        # runs as expected (no explicit output check at this time)
        diffed, _ = tardiff(files, opts=opts)
        self.assertTrue(diffed)
