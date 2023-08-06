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


Databases
---------

The commands available for databases are:

.. command-output:: beat databases --help

For instance, a list of the databases available locally can
be obtained as follows:

.. command-output:: beat databases list
   :cwd: ..

A list of the databases available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

   $ beat databases list --remote


Creating a new database
=======================

To create a new database locally, create the necessary files (see "Databases" in section "Getting Started with BEAT" in `BEAT documentation`_) and place them on your prefix.
Once done, use the following command to index the database:

.. code-block:: sh

   $ beat database index <db>/1

and if you wan to upload it to the web server issue the following command:

.. code-block:: sh

   $ beat -p prefix -m <platform> -t <your-token> databases push <db>/1


Replace the string ``<db>`` with the fully qualified name of your database. For
example, ``mynewdatabase``. Replace ``<platform>`` by the address of the BEAT
platform you're trying to interact with. Replace ``<your-token>`` by your user
token (you can get that information via your settings window on the platform
itself).


.. note::

   To create a **new** version of an existing database, you must use the
   command-line tool slightly differently, as explained below. The above
   instructions will not work in this particular case.


Creating a new version of an existing database
==============================================

To create a new version of database locally, first download the current version
and locally create a new version from the current instance. Modify the new
version to fit your needs using a text editor of your choice and then upload
the new version.

.. code-block:: sh

   $ beat -p prefix -m <platform> -t <your-token> databases pull <db>/1
   ...
   $ beat -p prefix databases version <db>
   ...
   $ vim prefix/databases/<db>/2.*
   # once you're happy, upload the new version
   $ beat -p prefix -m <platform> -t <your-token> databases push <db>/2


Replace the string ``<db>`` with the name of your database. For example,
``mynewdatabase``. Replace ``<platform>`` by the address of the BEAT platform
you're trying to interact with. Replace ``<your-token>`` by your user token
(you can get that information via your settings window on the platform itself).

.. note::

   At the moment only users with administrative privilege can push databases to the web serve however all users can create and modify databases locally.

.. include:: links.rst
