# walrus

[![PyPI - Downloads](https://pepy.tech/badge/python-walrus)](https://pepy.tech/count/python-walrus)
[![PyPI - Version](https://img.shields.io/pypi/v/python-walrus.svg)](https://pypi.org/project/python-walrus)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-walrus.svg)](https://pypi.org/project/python-walrus)

[![Travis CI - Status](https://img.shields.io/travis/pybpc/walrus.svg)](https://travis-ci.com/pybpc/walrus)
[![Codecov - Coverage](https://codecov.io/gh/pybpc/walrus/branch/master/graph/badge.svg)](https://codecov.io/gh/pybpc/walrus)
[![Documentation Status](https://readthedocs.org/projects/bpc-walrus/badge/?version=latest)](https://bpc-walrus.readthedocs.io/en/latest/)
<!-- [![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE) -->

> Write *assignment expressions* in Python 3.8 flavour, and let `walrus` worry about back-port issues :beer:

&emsp; Since [PEP 572](https://www.python.org/dev/peps/pep-0572/), Python introduced *assignment expressions*
syntax in version __3.8__. For those who wish to use *assignment expressions* in their code, `walrus` provides an
intelligent, yet imperfect, solution of a **backport compiler** by replacing *assignment expressions* syntax with
old-fashioned syntax, which guarantees you to always write *assignment expressions* in Python 3.8 flavour then
compile for compatibility later.

## Documentation

&emsp; See [documentation](https://bpc-walrus.readthedocs.io/en/latest/) for usage and more details.

## Contribution

&emsp; Contributions are very welcome, especially fixing bugs and providing test cases.
Note that code must remain valid and reasonable.

## See Also

- [`pybpc`](https://github.com/pybpc/bpc) (formerly known as `python-babel`)
- [`f2format`](https://github.com/pybpc/f2format)
- [`poseur`](https://github.com/pybpc/poseur)
- [`vermin`](https://github.com/netromdk/vermin)
