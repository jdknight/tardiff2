# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from dataclasses import dataclass
from dataclasses import field
from tardiff2.defs import DEFAULT_ATTRIBS


@dataclass
class TarDiffOpts:
    attribs: list[str] = field(default_factory=lambda: DEFAULT_ATTRIBS)
    detailed: bool = False
    ignore_dirs: bool = False
    only_names: bool = False
    strip: int = 1
