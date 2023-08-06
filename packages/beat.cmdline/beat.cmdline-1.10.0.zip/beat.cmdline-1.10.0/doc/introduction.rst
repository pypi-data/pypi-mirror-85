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


.. _beat-cmdline-introduction:

Introduction
============
The user objects (data formats, toolchains, experiments, etc) are stored
locally in a directory with specific structure that is commonly referred to as
a **prefix** (see "The Prefix" in section "A Hands-On-Tutorial" of `BEAT documentation`_). The user objects on the web platform are
also stored in a similar directory structure. It is possible to extract a
representation from the objects on the BEAT web server and interact with them
locally. Local object copies contain the same amount of information that is
displayed through the web interface.

The BEAT command-line utility can be used for simple functionalities (e.g.
deleting an existing algorithm or making small modifications) or advanced
tasks (e.g. database development, experiment debugging) both for local objects
and remote objects. In order to make this possible for the remote objects, the
web platform provides a RESTful API which third-party applications can use to
list, query and modify existing remote objects.


The ``beat`` command-line utility bridges user interaction with a remote BEAT
web platform and locally available objects in a seamless way:

.. command-output:: beat --help

The command-line interface is separated in subcommands, for acting on specific
objects. Actions can be driven to operate on locally installed
or remotely available objects. You'll find detailed information about
sub-commands on specific sub-sections of this documentation dedicated to that
particular type of object. In :ref:`beat-cmdline-configuration`, we cover basic usage and
configuration only.

.. include:: links.rst
