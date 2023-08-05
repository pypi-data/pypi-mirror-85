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


Toolchains
----------

The commands available for toolchains are:

.. command-output:: beat toolchains --help

For instance, a list of the toolchains available locally can
be obtained as follows:

.. command-output:: beat toolchains list
   :cwd: ..

A list of the toolchains available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

  $ beat toolchains list --remote

.. _beat-cmdline-toolchains-checkscript:

How to check that a toolchain is correctly declared?
....................................................

To check that a toolchain declaration file is correctly written, the command
line tool can be used.

For example, we check a correct file (found in
``src/beat.core/beat/core/test/toolchains/integers_addition.json``):

.. code-block:: sh

    $ beat --prefix=src/beat.core/beat/core/test/ toolchains check \
      integers_addition
    The toolchain is executable!

Here, the ``--prefix`` option is used to tell the scripts where all our data
formats, toolchains and algorithms are located, and ``integers_addition`` is the
name of the toolchain we want to check (note that we don't add the ``.json``
extension, as this is the name of the toolchain, not the filename!).

Now we check a file that isn't a correctly formatted JSON file:

``src/beat.core/beat/core/test/toolchains/invalid/invalid.json``:


.. code-block:: json

   {
       "invalid": true,
   }


.. code-block:: sh

   $ beat --prefix=src/beat.core/beat/core/test/ toolchains check invalid/invalid
   The toolchain isn\'t valid, due to the following errors:
       Failed to decode the JSON file \'beat/src/beat.core/beat/core/test/toolchains/invalid/invalid.json\':
           Expecting property name enclosed in double quotes: line 3 column 1 (char 23)


Here we are told that something is wrong JSON-wise around the line 3, column 1
of the JSON file. The error is the ``,`` (comma) character: in JSON, the last
field of an object (``{}``) or the last element of an array (``[]``) cannot be
followed by a comma.  This is the corrected version:

.. code-block:: json

    {
        "invalid": true
    }

Also note that since we tell the script that all our toolchain declaration
files are located in ``src/beat.core/beat/core/test/toolchains/``, the
subfolders in that location are considered as part of the name of the data
formats they contains (like here ``invalid/invalid``).

As a last example, here is the result of the script when the toolchain
references unknown inputs and outputs (see the following sections for
explanations about the content of the declaration file):

``src/beat.core/beat/core/test/toolchains/invalid/empty_blocks_list.json``:

.. code-block:: json

    {
        "blocks": [],
        "databases": [ {
                "name": "integers",
                "outputs": {
                    "values": "single_integer"
                }
            }
        ],
        "connections": [ {
                "from": "integers.values",
                "to": "echo.in"
            }
        ],
        "results": [
            "echo.out"
        ]
    }


.. code-block:: sh

    $ beat --prefix=src/beat.core/beat/core/test/ toolchains check invalid/empty_blocks_list
    The toolchain isn\'t valid, due to the following errors:
        Unknown inputs: echo.in
        Unknown result outputs: echo.out
