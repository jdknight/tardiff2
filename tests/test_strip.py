# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestStrip(TardiffTestCase):
    def test_strip_two(self) -> None:
        sample1a = Path('container-1') / 'contents.txt'
        sample1a.parent.mkdir()
        sample1a.write_text('This is an example file.\n')
        self.assertTrue(sample1a.is_file())

        sample1b = Path('container-1') / 'nested-1' / 'contents.txt'
        sample1b.parent.mkdir()
        sample1b.write_text('This is an example file.\n')
        self.assertTrue(sample1b.is_file())

        sample2a = Path('container-2') / 'contents.txt'
        sample2a.parent.mkdir()
        sample2a.write_text('This is an example file.\n')
        self.assertTrue(sample2a.is_file())

        sample2b = Path('container-2') / 'nested-2' / 'contents.txt'
        sample2b.parent.mkdir()
        sample2b.write_text('This is an example file.\n')
        self.assertTrue(sample2b.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1a)
            tar.add(sample1b)
        self.assertTrue(example1.is_file())

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2a)
            tar.add(sample2b)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        opts = TarDiffOpts()
        opts.strip = 2

        # should match the same even if we have different nested content
        # since we are stripping two levels
        diffed, _ = tardiff(files, opts=opts)
        self.assertFalse(diffed)

    def test_strip_zero(self) -> None:
        sample1 = Path('container-1') / 'contents.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'contents.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is an example file.\n')
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
        opts.strip = 0

        # should be difference since we are not stripping and the base
        # container names are unique
        diffed, _ = tardiff(files, opts=opts)
        self.assertTrue(diffed)
