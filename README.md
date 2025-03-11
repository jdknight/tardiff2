# tardiff2

Provides a utility to compare two (or more) tar files. This is aimed to
be a helper when comparing evolving tar files, allowing sanity checks to
expected file lists, modes, ownerships and more.

## Installation

This tool can be installed using [pip][pip] or [pipx][pipx]:

```shell
pipx install tardiff2
 (or)
pip install -U tardiff2
 (or)
python -m pip install -U tardiff2
```

## Usage

This tool can be invoked from a command line using:

```shell
tardiff2 --help
 (or)
python -m tardiff2 --help
```

For example:

```shell
tardiff2 libfoo-1.0.0.tar.gz libfoo-1.1.0.tar.gz
```


[pip]: https://pip.pypa.io/
[pipx]: https://pipx.pypa.io/
