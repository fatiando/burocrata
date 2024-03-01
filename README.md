# Burocrata: Check and insert copyright and license notices into source code

Part of the [Fatiando a Terra][fatiando] project.

[![Latest release on PyPI](https://img.shields.io/pypi/v/burocrata.svg?style=flat-square)][pypi]
[![Latest release on conda-forge](https://img.shields.io/conda/vn/conda-forge/burocrata.svg?style=flat-square)][conda-forge]
[![Test coverage report](https://img.shields.io/codecov/c/github/fatiando/burocrata/main?style=flat-square)][coverage]
[![Compatible Python versions](https://img.shields.io/pypi/pyversions/burocrata.svg?style=flat-square)][pypi]

## About

*Burocrata* is a small command-line program that can check the existence of
copyright and license notices in source code files and add them when they are
missing.

## Installing

*Burocrata* is available from PyPI:

```
python -m pip install burocrata
```

and conda-forge:

```
conda install burocrata -c conda-forge
```

## Using

Check that very `.py` file in a directory has a license notice:

```
$ burocrata --check --extension=py source_folder
```

Removing the `--check` option will make Burocrata add the license notice to
the files that don't have them:

```
$ burocrata --extension=py source_folder
```

The license and copyright notice can be configured in a `pyproject.toml` file
located in the directory where `burocrata` is run:

```
$ cat pyproject.toml
[tool.burocrata]
notice = '''
# Copyright (c) YYYY Name of Developer.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause'''
```

See a full list of options:

```
$ burocrata --help
```

## Dependencies

We use the following dependencies (see `pyproject.toml` for specific version
constraints):

* [click](https://click.palletsprojects.com) for building the command-line
  interface.
* [tomli](https://github.com/hukkin/tomli) to parse the TOML configuration
  files.
* [pathspec](https://github.com/cpburnz/python-pathspec) to parse `.gitignore`
  files.

## Contacting Us

Find out more about how to reach us at
[fatiando.org/contact][contact]

## Contributing

### Code of conduct

Please note that this project is released with a [Code of Conduct][coc].
By participating in this project you agree to abide by its terms.

### Contributing Guidelines

Please read our
[Contributing Guide][contrib]
to see how you can help and give feedback.

## License

Burocrata is free and open-source software distributed under the
[MIT License][license].

[pypi]: https://pypi.org/project/burocrata/
[conda-forge]: https://github.com/conda-forge/burocrata-feedstock
[coverage]: https://app.codecov.io/gh/fatiando/burocrata
[license]: https://github.com/fatiando/burocrata/blob/main/LICENSE.txt
[contrib]: https://github.com/fatiando/burocrata/blob/main/CONTRIBUTING.md
[coc]: https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md
[fatiando]: https://www.fatiando.org
[contact]: https://www.fatiando.org/contact
