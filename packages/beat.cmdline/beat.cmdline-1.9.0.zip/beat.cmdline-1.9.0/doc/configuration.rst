.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.backend.python module of the BEAT platform.  ..
..                                                                            ..
.. Redistribution and use in source and binary forms, with or without
.. modification, are permitted provided that the following conditions are met:

.. 1. Redistributions of source code must retain the above copyright notice, this
.. list of conditions and the following disclaimer.

.. 2. Redistributions in binary form must reproduce the above copyright notice,
.. this list of conditions and the following disclaimer in the documentation
.. and/or other materials provided with the distribution.

.. 3. Neither the name of the copyright holder nor the names of its contributors
.. may be used to endorse or promote products derived from this software without
.. specific prior written permission.

.. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
.. ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
.. WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
.. DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
.. FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
.. DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
.. SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
.. CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
.. OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
.. OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


.. _beat-cmdline-configuration:

Configuration
-------------

The ``beat`` command-line utility can operate independently of any initial
configuration. By runig for example the following command:

.. code-block:: sh

   $ beat dataformats list --remote

By default, ``beat`` is pre-configured to access the `main BEAT
website`_ anonymously, but it can be configured to use secret keys for any of
its users and/or access an alternative website installed somewhere else. This
allows users to push modified objects into the platform, completing the
development loop:

1. Pull objects of interest locally.
2. Develop new objects or modify existing ones.
3. Test locally, on an environment similar to the one available at the remote platform. (If the user wants to run the experiment locally without pushing it back to the platform they can use their own environment)
4. Push back modifications and then scale-up experiment running to explore more databases and more parameter combinations.

In order to properly configure a working prefix and memorize access options on
that directory, do the following from your shell:

.. code-block:: sh

   $ beat config set user myname token thistoken
   ...

You can verify your username and token have been memorized on that working
directory with:

.. command-output:: beat config show


By default, the command-line program considers the ``prefix`` directory on your
current working directory as your prefix. You can override this setting using the
``--prefix`` flag:

.. code-block:: sh

   $ beat --prefix=/Users/myname/work/beat config show
   ...


Note that it is also possible to set a different code editor

.. code-block:: sh

   $ beat config set editor vim


So we can imagine using the ``edit`` command to edit locally any object.

For example editing an algorithm named ``user/integers_echo/1`` can be done
using the following command:

.. code-block:: sh

   $ beat algorithm edit user/integers_echo/1

You can also use the ``path`` command on all your objects to identify all
the files and local paths for any given object.

For example we can get the files path associated with the algorithm
named ``user/integers_echo/1`` using the following command:

.. code-block:: sh

   $ beat algorithm path user/integers_echo/1


Local Overrides
===============

If you use the ``config set`` flag ``--local``, then the configuration values
are not set on the default configuration file (``~/.beatrc``), but instead in
the **current** working directory (``./.beatrc``). Configuration values found
the local directory take **precedence** over values configured on the global
file. Values from the command-line (such as those passed with ``--prefix`` as
explained above) take precedence over both settings.

You can set a variable on the local directory to override the global settings
like this:

.. code-block:: sh

   # set a different prefix when operating from the current directory
   $ beat config set --local prefix `pwd`/other_prefix
   $ beat config show
   ...


Database Root Directories
=========================

When running an experiment in the BEAT ecosystem using the local
executor (the default executor, also behind the ``--local`` flag), ``beat``
will look into your configuration for any options set by the user that follow
the format ``database/<db name>/<db version>``. ``beat`` expects that this
option points to a string representing the path to the root folder of the
actual database files for the given database.

For example, the AT&T "Database of Faces" is available on the BEAT platform
as the "atnt" database. The third version of the "atnt" database would be
referenced as "atnt/3". The object "atnt/3" has a root folder defined on
the BEAT platform already, and changing this locally would mean creating a
new version of the database.
Instead, you may override that path by setting the configuration option
``database/atnt/3`` to your local path to the database files.
Assuming your username is "user" and you extracted the database files to
``~/Downloads/atnt_db``, you can set ``database/atnt/3`` to
``/home/user/Downloads/atnt_db``, and BEAT will find the database files.

You may explore different configuration options with the ``--help`` flag of
``beat config``:

.. command-output:: beat config --help

.. include:: links.rst
