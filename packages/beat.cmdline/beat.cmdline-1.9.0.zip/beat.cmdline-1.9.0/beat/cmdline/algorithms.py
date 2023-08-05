#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import logging
import os

import click
import simplejson as json

from beat.backend.python.algorithm import Storage as AlgorithmStorage
from beat.core import algorithm
from beat.core import hash
from beat.core.dock import Host
from beat.core.execution import DockerExecutor

from . import commands
from . import common
from .click_helper import AliasedGroup
from .click_helper import AssetCommand
from .click_helper import AssetInfo
from .decorators import raise_on_error

logger = logging.getLogger(__name__)


def pull_impl(webapi, prefix, names, force, indentation, format_cache, lib_cache):
    """Copies algorithms (and required libraries/dataformats) from the server.

  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to retrieve objects. If the list is empty, then we pull all
      available objects of a given type. If no user is set, then pull all
      public objects of a given type.

    force (bool): If set to ``True``, then overwrites local changes with the
      remotely retrieved copies.

    indentation (int): The indentation level, useful if this function is called
      recursively while downloading different object types. This is normally
      set to ``0`` (zero).

    format_cache (dict): A dictionary containing all dataformats already
      downloaded.

    lib_cache (dict): A dictionary containing all libraries already
      downloaded.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    from .dataformats import pull_impl as dataformats_pull
    from .libraries import pull_impl as libraries_pull

    status, names = common.pull(
        webapi,
        prefix,
        "algorithm",
        names,
        ["declaration", "code", "description"],
        force,
        indentation,
    )

    if status != 0:
        return status

    # see what dataformats one needs to pull
    if indentation == 0:
        indentation = 4

    dataformats = []
    libraries = []
    for name in names:
        obj = algorithm.Algorithm(prefix, name)
        dataformats.extend(obj.dataformats.keys())
        libraries.extend(obj.libraries.keys())

    # downloads any formats to which we depend on
    df_status = dataformats_pull(
        webapi, prefix, dataformats, force, indentation, format_cache
    )

    lib_status = libraries_pull(
        webapi, prefix, libraries, force, indentation, lib_cache
    )

    return status + df_status + lib_status


def print_examples():
    print(
        """
To feed data from a database to an algorithm:
=============================================

{
    "algorithm": "<username>/<algorithm>/<version>",
    "channel": "main",
    "inputs": {
        "<input_name>": {
            "database": "<database>/<version>",
            "protocol": "<protocol>",
            "set": "<set>",
            "output": "<output_name>",
            "channel": "main"
        }
    },
    "outputs": {
        "<output_name>": {
          "channel": "main"
        }
    },
    "parameters": {
      "<parameter_name>": <value>
    },
    "environment": {
        "name": "<environment_name>",
        "version": "<environment_version>"
    }
}


To feed data from a file in the cache:
======================================

{
    "algorithm": "<username>/<algorithm>/<version>",
    "channel": "main",
    "inputs": {
        "<input_name>": {
            "hash": "<hash>",
            "channel": "main"
        }
    },
    "outputs": {
        "<output_name>": {
          "channel": "main"
        }
    },
    "parameters": {
      "<parameter_name>": <value>
    },
    "environment": {
        "name": "<environment_name>",
        "version": "<environment_version>"
    }
}


To execute an analyzer:
=======================

{
    "algorithm": "<username>/<algorithm>/<version>",
    "channel": "main",
    "inputs": {
        "<input_name>": {
            "hash": "<hash>",
            "channel": "main"
        }
    },
    "parameters": {
      "<parameter_name>": <value>
    },
    "environment": {
        "name": "<environment_name>",
        "version": "<environment_version>"
    }
}
"""
    )


def execute_impl(prefix, cache, instructions_file):
    try:
        # Load the JSON configuration
        if not os.path.exists(instructions_file):
            raise IOError("JSON instructions file `%s' not found" % instructions_file)

        with open(instructions_file, "r") as f:
            configuration = json.load(f)

        # Add missing configuration fields
        configuration["queue"] = "unused"
        configuration["nb_slots"] = 1

        if "parameters" not in configuration:
            configuration["parameters"] = {}

        for name, cfg in configuration["inputs"].items():
            cfg["endpoint"] = name
            suffix = ""
            if "database" in cfg:  # Connected to a database output
                cfg["hash"] = hash.hashDataset(
                    cfg["database"], cfg["protocol"], cfg["set"]
                )
                suffix = ".db"

            cfg["path"] = hash.toPath(cfg["hash"], suffix=suffix)

        algo = AlgorithmStorage(prefix, configuration["algorithm"])

        if "outputs" in configuration:  # Standard algorithm
            for name, cfg in configuration["outputs"].items():
                cfg["endpoint"] = name
                cfg["hash"] = hash.hashBlockOutput(
                    "block",
                    configuration["algorithm"],
                    algo.hash(),
                    configuration["parameters"],
                    configuration["environment"],
                    dict([(k, v["hash"]) for k, v in configuration["inputs"].items()]),
                    name,
                )
                cfg["path"] = hash.toPath(cfg["hash"], "")

        else:  # Analyzer
            configuration["result"] = {}
            configuration["result"]["hash"] = hash.hashAnalyzer(
                "block",
                configuration["algorithm"],
                algo.hash(),
                configuration["parameters"],
                configuration["environment"],
                dict([(k, v["hash"]) for k, v in configuration["inputs"].items()]),
            )
            configuration["result"]["path"] = hash.toPath(
                configuration["result"]["hash"], ""
            )

        # Sets up the execution
        dataformat_cache = {}
        database_cache = {}
        algorithm_cache = {}

        host = Host(raise_on_errors=False)

        executor = DockerExecutor(
            host,
            prefix,
            configuration,
            cache,
            dataformat_cache,
            database_cache,
            algorithm_cache,
        )

        if not executor.valid:
            logger.error(
                "Invalid configuration:\n  * %s" % "\n  * ".join(executor.errors)
            )
            return 1

        # Execute the algorithm
        with executor:
            result = executor.process()
            if result["status"] != 0:
                print("STDERR:")
                print(result["stderr"])

        # Display the results
        if "outputs" in configuration:  # Standard algorithm
            print("Outputs of the algorithms available at:")
            for name, cfg in configuration["outputs"].items():
                print("  - %s: %s" % (name, cfg["path"]))
        else:
            print(
                "Results of the analyzer available at: %s"
                % configuration["result"]["path"]
            )

    except Exception:
        import traceback

        logger.error(traceback.format_exc())
        return 1

    return 0


def get_dependencies(ctx, asset_name):
    prefix = ctx.meta["config"].path
    alg = algorithm.Algorithm(prefix, asset_name)

    dependencies = {}

    libraries = list(alg.libraries.keys())
    if libraries:
        dependencies["libraries"] = libraries

    dataformats = list(alg.dataformats.keys())
    if dataformats:
        dependencies["dataformats"] = dataformats

    return dependencies


class AlgorithmCommand(AssetCommand):
    asset_info = AssetInfo(
        asset_type="algorithm",
        diff_fields=["declaration", "code", "description"],
        push_fields=["name", "declaration", "code", "description"],
        get_dependencies=get_dependencies,
    )


@click.group(cls=AliasedGroup)
@click.pass_context
def algorithms(ctx):
    """Configuration and manipulation of algorithms"""


CMD_LIST = [
    "list",
    "path",
    "edit",
    "check",
    "status",
    "create",
    "version",
    "fork",
    "rm",
    "diff",
    "push",
]

commands.initialise_asset_commands(algorithms, CMD_LIST, AlgorithmCommand)


@algorithms.command()
@click.argument("name", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.pass_context
@raise_on_error
def pull(ctx, name, force):
    """Downloads the specified algorithms from the server

  Example:
    $ beat algorithms pull --force yyy
  """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        return pull_impl(webapi, ctx.meta["config"].path, name, force, 0, {}, {})


@algorithms.command()
@click.argument("instructions", nargs=1)
@click.option(
    "--example", help="Display some example JSON instruction files", is_flag=True
)
@click.pass_context
@raise_on_error
def execute(ctx, instructions, example):
    """Execute an algorithm following instructions in a JSON file

  Example:
    $ beat algorithms execute <instructions>
    $ beat algorithms execute --examples
  """
    if example:
        print_examples()
        return 0

    return execute_impl(ctx.meta["config"].path, ctx.meta["config"].cache, instructions)
