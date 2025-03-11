# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffSameName(TardiffTestCase):
    def test_diff_same_name(self) -> None:
        sample1 = Path('container-1') / 'contents.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'contents.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is another example file.\n')
        self.assertTrue(sample2.is_file())

        example1 = Path('dist-1') / 'example.tgz'
        example1.parent.mkdir()
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1)
        self.assertTrue(example1.is_file())

        example2 = Path('dist-2') / 'example.tgz'
        example2.parent.mkdir()
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        opts = TarDiffOpts()
        opts.detailed = 2

        diffed, _ = tardiff(files, opts=opts)
        self.assertTrue(diffed)
