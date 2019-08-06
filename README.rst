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

Direct API
----------

.. code:: python

   from fs.datalake import DatalakeFS

   tenant_id = "xxx"           # Provided by your Azure dashboard
   storage_name = "mystorage"  # Created through the Azure dashboard
   username = "myself"         # Your Azure dashboard credentials
   password = "my-secret"

   datalake_storage = DatalakeFS(tenant_id, storage_name, username=username, password=password)

   # Play with your storage using the usual FS API
   print(datalake_storage.listdir("."))

Using the ``open_fs`` factory
-----------------------------

As most backends for FS2, you may create a connection using the ``open_fs`` factory.

https://docs.pyfilesystem.org/en/latest/reference/opener.html#fs.opener.registry.Registry.open_fs

Example:

.. code:: python

   from fs import open_fs

   url = f"datalake://{username}:{password}@{tenant_id}/{storage_name}"
   datalake_storage = open_fs(url)

   # Play with your storage using the usual FS API
   print(datalake_storage.listdir("."))

.. warning::

   You may need to url_quote your username and password if these contain special characters like "/", "=", space
   and some others.

You can read in the doc that the ``open_fs`` may take additional parameters after the URL. Note that with the
``dtalake://...`` URLs, ``writable``, ``create`` and ```default_protocol`` are ignore. Though you may provide the
``cwd`` keyword parameter.

Authenticating with ``client_id`` and ``client_secret``
-------------------------------------------------------

If you do not want to let your username and password in your scripts or configuration files, you may prefer to create
a couple ``client_id`` and ``client_secret`` in your Azure dashboard and use these to authenticate in your app.

With the storage API:

.. code:: python

   client_id = "xxxx..."      # Credentials hashes created in your Azure dashboard
   client_secret = "yyyy..."

   datalake_storage = DatalakeFS(tenant_id, storage_name, client_id=client_id,
                                 client_secret=client_secret)

With the FS2 factory:

.. code:: python

   url = f"datalake://{tenant_id}/{storage_name}?client_id={client_id)&client_secret={client_secret}

.. warning::

   For the same reasons as above mentioned about special characters, you may need to "url_quote" ``client_id`` and
   ``client_secret`` when inserting them in the query of an URL.

Developer notes
===============

Bootstrap the project
---------------------

Please use a dedicated virtualenv to maintain this package, but I should not need to say that.

Grab the source from the SCM repository, then ``cd`` to the root:

.. code:: console

  $ pip install -e .[testing]

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
