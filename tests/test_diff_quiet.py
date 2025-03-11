# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tardiff2.tardiff import tardiff
from tests import TardiffTestCase
import tarfile


class TestDiffQuiet(TardiffTestCase):
    def test_diff_quiet(self) -> None:
        sample1 = Path('container-1') / 'alpha.txt'
        sample1.parent.mkdir()
        sample1.write_text('This is an example file.\n')
        self.assertTrue(sample1.is_file())

        sample2 = Path('container-2') / 'bravo.txt'
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

        # ensure a diff scenario generates output
        stdout = StringIO()
        with redirect_stdout(stdout):
            diffed, _ = tardiff(files)
        self.assertTrue(diffed)
        self.assertNotEqual(stdout.getvalue(), '')

        # re-run the same thing in quiet mode and ensure no output is generated
        stdout = StringIO()
        with redirect_stdout(stdout):
            diffed, _ = tardiff(files, quiet=True)
        self.assertTrue(diffed)
        self.assertEqual(stdout.getvalue(), '')
