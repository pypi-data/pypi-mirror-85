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


.. _beat-cmdline-plotters:

Plotters
--------

The commands available for plotterparameters are:

.. command-output:: beat plotters --help

For instance, a list of the plotters available locally can
be obtained as follows:

.. command-output:: beat plotters list
   :cwd: ..

A list of the plotters available on the remote platform can
be obtained by running the following command:

.. code-block:: sh

   $ beat plotters list --remote

How to plot a figure?
.........................

The command ``beat plotters plot <name>`` can be used to plot data using a
specific plotter.

There a many ways to plot data:

* Using sample data:

.. code-block:: sh

  $ beat plotter plot --sample_data plottername

* passing some private input data (no sample_data required here), specific plotterparameter and output image name

.. code-block:: sh

  $ beat plotter plot plottername --inputdata inputdata.json --outputimage outputimage.png --plotterparameter plotterparameter

  * inputdata.json is the filename containing data
  * outputimage is the name of the saved image
  * plotter the name of the plotter (e.g.: plot/bar/1)
  * plotterparameter the name of the plotterparameter (e.g.: plot/bar/1)

* without specifing the output image:

.. code-block:: sh

  $ beat plotter plot plottername --inputdata inputdata.json --plotterparameter plotterparameter

  * The image gets saved under the plotter path with default name "output_image.png"

Take into account that some extra options are available such as '--show' which will pop out the generated plots on your screen.
