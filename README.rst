===========
fs.datalake
===========

`PythonFileSystem <https://www.pyfilesystem.org/>`_ extension for
`Azure Datalake Storage <https://azure.microsoft.com/en-us/services/storage/data-lake-storage/>`_ gen.1.

PyFileSystem is a Filesystem abstraction for Python, that provides the same API on whatever storage backend (Hard drive,
clouds, archive files, ...).

Azure Datalake Store is a cloud storage dedicated at big data Hadoop like operations provided by Microsoft.

.. warning::

   **About Datalake store generation**

   ``fs.datalake`` does not (yet) support Azure Datalake Store Gen. 2 backends as long as the underlying
   ``azure-datalake-store`` Python library doesn't.

Installation
============

.. code:: console

   pip install fs.datalake

Usage
=====

As most backends for FS2, you may create a connection.

Developer notes
===============

Bootstrap the project
---------------------

Please use a dedicated virtualenv to maintain this package, but I should not need to say that.

Grab the source from the SCM repository, then ``cd`` to the root:

.. code:: console

  $ pip install -e .[dev]

Run the tests:

.. code:: console

  $ python setup.py test
  $ python run_tests.py

MIT License
===========

Copyright 2019 Gilles Lenfant

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Links
=====

Misc resources used for development
-----------------------------------

* `PythonFileSystem documentation <https://docs.pyfilesystem.org/>`_
* `Azure Datalake Storage`_
* `azure datalake store Python lib <https://pypi.org/project/azure-datalake-store/>`_
* https://docs.microsoft.com/azure/data-lake-store/data-lake-store-data-operations-python

Source code
-----------

  https://github.com/glenfant/fs.datalake

Issue tracker
-------------

  https://github.com/glenfant/fs.datalake/issues

Known issues and limitations
============================

Python 3.4 and older versions
-----------------------------

The first alpha release will support Python 3.5 and later. Older Python versions won't be supported unless
contributions as PR that don't break the tests with later versions.

As Python 2.7 support by FS2 is planned to be dropped, I won't add Python 2.x complicated compatibility layer, and won't
accept PR for Python 2.7 support.

Token lifetime
--------------

The authentication against Azure services provide a **one hour life token**. This is not a major issue for CLI
applications but could be an issue for long time running processes.

So I must find a way to refresh that token automatically (find what exception - if any - is raised from the lower level
lib when trying to query the server with an outdated token)

Datalake limitations
--------------------

Looking for doc about the various limitations of Datalake, and their consequences on this software.

- What is the encoding of the file / directory names ?
- Are there forbidden characters in the file / directory names
- What's the size limit of file / directory names ?
- Is there a limit of directory levels ?

Cryptography
------------

There are lots of crypto options on Datalake storage. I have to admit that I am somehow stuck in that domain, and didn't
provide specific features to play with encrypted Datalake stores. Any help in that field is welcome.
