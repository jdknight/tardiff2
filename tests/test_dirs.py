# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDirs(TardiffTestCase):
    def test_dirs_diff_flag(self) -> None:
        sample1 = Path('container-1') / 'nested' / 'sample.txt'
        sample1.parent.mkdir(parents=True)
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'nested' / 'sample.txt'
        sample2.parent.mkdir(parents=True)
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1.parent, recursive=False)
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

        # should be difference with missing directory entry on second
        diffed, _ = tardiff(files)
        self.assertTrue(diffed)

    def test_dirs_diff_ignore(self) -> None:
        sample1 = Path('container-1') / 'nested' / 'sample.txt'
        sample1.parent.mkdir(parents=True)
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'nested' / 'sample.txt'
        sample2.parent.mkdir(parents=True)
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1.parent, recursive=False)
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
        opts.ignore_dirs = True

        # while directories are different, we have flagged to ignore any
        # differences in directories
        diffed, _ = tardiff(files, opts=opts)
        self.assertFalse(diffed)

    def test_dirs_match(self) -> None:
        sample1 = Path('container-1') / 'nested' / 'sample.txt'
        sample1.parent.mkdir(parents=True)
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'nested' / 'sample.txt'
        sample2.parent.mkdir(parents=True)
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1.parent, recursive=False)
            tar.add(sample1)
        self.assertTrue(example1.is_file())

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2.parent, recursive=False)
            tar.add(sample2)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # match with same directory and file entries
        diffed, _ = tardiff(files)
        self.assertFalse(diffed)
