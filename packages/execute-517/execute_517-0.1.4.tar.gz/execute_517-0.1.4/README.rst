Run a command in a PEP 517 env
------------------------------

This package allows you to run any Python command inside the build environment specified by the ``pyproject.toml`` file. This may be useful for executing specific ``setup.py`` commands inside an env where all the dependencies are available.

For example to get the version of a package run the following command in the root of the repository::

  $ execute-517 "setup.py --version"

License
-------

This project is Copyright (c) Stuart Mumford and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

Lots of the code in this repository is adapted from the
`build <https://github.com/pypa/build>`__ package which is licensed under the
terms of the MIT license.
