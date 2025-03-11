# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import platform
import tarfile


class TestMatchedLinkname(TardiffTestCase):
    def test_matched_linkname(self) -> None:
        if platform.system() != 'Linux':
            msg = 'symlink test skipped for non-Linux'
            raise self.skipTest(msg)

        sample1 = Path('container-1') / 'sample.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample1_link = Path('container-1') / 'sample-link'
        sample1_link.symlink_to('sample.txt')
        self.assertTrue(sample1_link.is_symlink())

        sample2 = Path('container-2') / 'sample.txt'
        sample2.parent.mkdir()
        sample2.write_text('This is an example file.\n')
        self.assertTrue(sample2.is_file())

        sample2_link = Path('container-2') / 'sample-link'
        sample2_link.symlink_to('sample.txt')
        self.assertTrue(sample2_link.is_symlink())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample1)
            tar.add(sample1_link)
        self.assertTrue(example1.is_file())

        example2 = Path('example2.tgz')
        with tarfile.open(example2, 'w') as tar:
            tar.add(sample2)
            tar.add(sample2_link)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # should be difference with two different sized content
        diffed, _ = tardiff(files)
        self.assertFalse(diffed)
