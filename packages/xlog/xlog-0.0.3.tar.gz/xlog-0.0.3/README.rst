.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="Xlog logo" src="https://www.xbiome.cn/images/logo.png">
        </a>
    </p>
    <p align="center">
        <a href="https://pypi.org/project/xlog/"><img alt="Pypi version" src="https://img.shields.io/pypi/v/loguru.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="Python versions" src="https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="Documentation" src="https://img.shields.io/readthedocs/loguru.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="Build status" src="https://img.shields.io/travis/Delgan/loguru/master.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="Coverage" src="https://img.shields.io/codecov/c/github/delgan/loguru/master.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="Code quality" src="https://img.shields.io/codacy/grade/4d97edb1bb734a0d9a684a700a84f555.svg"></a>
        <a href="https://pypi.org/project/xlog/"><img alt="License" src="https://img.shields.io/github/license/delgan/loguru.svg"></a>
    </p>

=========

**Xlog** Xbime logging Frame in Python.


.. end-of-readme-intro

Installation
------------

::

    pip3 install xlog


Features
--------

* `Format the pipeline logging.

Take the tour
-------------

.. highlight:: python3

.. |logger| replace:: ``logger``
.. _logger: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger

.. |add| replace:: ``add()``
.. _add: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add

.. |remove| replace:: ``remove()``
.. _remove: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.remove

.. |complete| replace:: ``complete()``
.. _complete: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete

.. |catch| replace:: ``catch()``
.. _catch: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.catch

.. |bind| replace:: ``bind()``
.. _bind: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.bind

.. |contextualize| replace:: ``contextualize()``
.. _contextualize: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.contextualize

.. |patch| replace:: ``patch()``
.. _patch: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.patch

.. |opt| replace:: ``opt()``
.. _opt: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.opt

.. |trace| replace:: ``trace()``
.. _trace: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.trace

.. |success| replace:: ``success()``
.. _success: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.success

.. |level| replace:: ``level()``
.. _level: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.level

.. |configure| replace:: ``configure()``
.. _configure: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure

.. |disable| replace:: ``disable()``
.. _disable: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.disable

.. |enable| replace:: ``enable()``
.. _enable: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.enable

.. |parse| replace:: ``parse()``
.. _parse: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.parse

.. _sinks: https://loguru.readthedocs.io/en/stable/api/logger.html#sink
.. _record dict: https://loguru.readthedocs.io/en/stable/api/logger.html#record
.. _log messages: https://loguru.readthedocs.io/en/stable/api/logger.html#message
.. _easily configurable: https://loguru.readthedocs.io/en/stable/api/logger.html#file
.. _markup tags: https://loguru.readthedocs.io/en/stable/api/logger.html#color
.. _fixes it: https://loguru.readthedocs.io/en/stable/api/logger.html#time
.. _No problem: https://loguru.readthedocs.io/en/stable/api/logger.html#env
.. _logging levels: https://loguru.readthedocs.io/en/stable/api/logger.html#levels

.. |better_exceptions| replace:: ``better_exceptions``
.. _better_exceptions: https://github.com/Qix-/better-exceptions

.. |notifiers| replace:: ``notifiers``
.. _notifiers: https://github.com/notifiers/notifiers


Ready to use it with simple method.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    from xlog import xlog

	xlog.init('ProjectName','LogPath','LogLevel')

	xlog.logger('YourMessage')

OutPut Example:
-----------------

	