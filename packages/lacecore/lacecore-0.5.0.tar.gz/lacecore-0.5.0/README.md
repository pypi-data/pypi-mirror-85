# lacecore

[![version](https://img.shields.io/pypi/v/lacecore.svg?style=flat-square)][pypi]
[![python versions](https://img.shields.io/pypi/pyversions/lacecore.svg?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/lacecore.svg?style=flat-square)][pypi]
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square)][coverage]
[![build](https://img.shields.io/circleci/project/github/lace/lacecore/master.svg?style=flat-square)][build]
[![code style](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square)][black]

Polygonal mesh library optimized for cloud computation.

Relies on the scientific-computing package [NumPy][], the cloud-ready
computational geometry library [polliwog][] and the linear-algebra toolbelt
[vg][].

Similar libraries in the problem space are [Trimesh][] which is large,
full-featured, batteries included, and a better choice for rapid prototyping,
and [Lace][], also batteries included, which is the spiritual predecessor of
this library.

The goals of this project are:

- Keep dependencies light and deployment flexible.
- Ensure high performance.
- Maintain 100% coverage and production code quality.
- Provide a complete core which can be augmented through additional modules.
- Respond to community contributions.

[pypi]: https://pypi.org/project/lacecore/
[coverage]: https://github.com/lace/lacecore/blob/master/.coveragerc#L2
[build]: https://circleci.com/gh/lace/lacecore/tree/master
[docs build]: https://lacecore.readthedocs.io/en/latest/
[black]: https://black.readthedocs.io/en/stable/
[trimesh]: https://trimsh.org/
[numpy]: https://numpy.org/
[lace]: https://github.com/lace/lace
[polliwog]: https://github.com/lace/polliwog
[vg]: https://github.com/lace/vg

## Contribute

- Issue Tracker: https://github.com/lace/lacecore/issues
- Source Code: https://github.com/lace/lacecore

Pull requests welcome!


## Support

If you are having issues, please let us know.


## Acknowledgements

This library was developed by [Paul Melnikow][] and [Jake Beard][].

Its spiritual predecessor is [Lace][], which was refactored from legacy code
at Body Labs by [Alex Weiss][], with portions by [Eric Rachlin][],
[Paul Melnikow][], [Victor Alvarez][], and others. Later it was extracted
from the Body Labs codebase and open-sourced by [Guillaume Marceau][]. In
2018 it was [forked by Paul Melnikow][fork] and published as
[metabolace][fork pypi]. Thanks to a repository and package transfer from
Body Labs, the fork has been merged back into the original.

[paul melnikow]: https://github.com/paulmelnikow
[jake beard]: https://github.com/jbeard4
[alex weiss]: https://github.com/algrs
[eric rachlin]: https://github.com/eerac
[victor alvarez]: https://github.com/yangmillstheory
[guillaume marceau]: https://github.com/gmarceau
[fork]: https://github.com/metabolize/lace
[fork pypi]: https://pypi.org/project/metabolace/

## License

The project is licensed under the two-clause BSD license.

### Install with support for loading OBJ 

In order to keep the package lightweight, support for loading obj is an optional dependency:

`pip install lacecore[obj]`
