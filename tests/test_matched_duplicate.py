# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import shutil
import tarfile


class TestMatchedDuplicate(TardiffTestCase):
    def test_matched_duplicate(self) -> None:
        files = [
            'example.tar',
            'this-file-does-not-exist',
        ]

        sample = Path('container') / 'contents.txt'
        sample.parent.mkdir()
        sample.write_text('This is an example file.\n')
        self.assertTrue(sample.is_file())

        example1 = Path('example1.tgz')
        with tarfile.open(example1, 'w') as tar:
            tar.add(sample)
        self.assertTrue(example1.is_file())

        example2 = Path('example2.tgz')
        shutil.copyfile(example1, example2)
        self.assertTrue(example2.is_file())

        files = [
            example1,
            example2,
        ]

        # same tar file copied; should be a perfect match
        diffed, _ = tardiff(files)
        self.assertFalse(diffed)
