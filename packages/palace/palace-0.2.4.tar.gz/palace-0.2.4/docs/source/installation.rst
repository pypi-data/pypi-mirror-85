Installation
============

Prerequisites
-------------

Palace requires CPython_ version 3.6 or above for runtime
and pip_ for installation.

Via PyPI
--------

Palace can be installed from PyPI::

   pip install palace

Wheel distributions are built exclusively for GNU/Linux on amd64.
If you want to help packaging for other platforms, please reach out
on our `mailing list`_.

From source
-----------

Aside from the build dependencies listed in ``pyproject.toml``,
one will additionally need compatible Python headers, alure_,
a C++14 compiler, CMake_ 2.6+ (and probably git_ for fetching the source).
Palace can then be compiled and installed by running::

   git clone https://git.sr.ht/~cnx/palace
   pip install palace/

.. _CPython: https://www.python.org/
.. _pip: https://pip.pypa.io/en/latest/
.. _mailing list: https://lists.sr.ht/~cnx/palace
.. _alure: https://github.com/kcat/alure
.. _CMake: https://cmake.org/
.. _git: https://git-scm.com/
