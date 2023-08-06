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


"""Usage:
  %(prog)s libraries list [--remote]
  %(prog)s libraries path [<name>]...
  %(prog)s libraries edit <name>...
  %(prog)s libraries check [<name>]...
  %(prog)s libraries pull [--force] [<name>]...
  %(prog)s libraries push [--force] [--dry-run] [<name>]...
  %(prog)s libraries diff <name>
  %(prog)s libraries status
  %(prog)s libraries create <name>...
  %(prog)s libraries version <name>
  %(prog)s libraries fork <src> <dst>
  %(prog)s libraries rm [--remote] <name>...
  %(prog)s libraries --help


Commands:
  list      Lists all the libraries available on the platform
  path      Displays local path of libraries files
  edit      Edit local library file
  check     Checks a local library for validity
  pull      Downloads the specified libraries from the server
  push      Uploads libraries to the server
  diff      Shows changes between the local library and the remote version
  status    Shows (editing) status for all available libraries
  create    Creates a new local library
  version   Creates a new version of an existing library
  fork      Forks a local library
  rm        Deletes a local library (unless --remote is specified)


Options:
  --force    Performs operation regardless of conflicts
  --dry-run  Doesn't really perform the task, just comments what would do
  --remote   Only acts on the remote copy of the library
  --help     Display this screen

"""

import logging

import click

from beat.core import library

from . import commands
from . import common
from .click_helper import AliasedGroup
from .click_helper import AssetCommand
from .click_helper import AssetInfo
from .decorators import raise_on_error

logger = logging.getLogger(__name__)


def pull_impl(webapi, prefix, names, force, indentation, cache):
    """Copies libraries (and dependent libraries) from the server.

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

    cache (dict): A dictionary containing all libraries already downloaded.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    libraries = set(names)  # what is being request
    download = libraries - set(cache.keys())  # what we actually need

    if not download:
        return 0

    if indentation == 0:
        indentation = 4

    status, downloaded = common.pull(
        webapi,
        prefix,
        "library",
        download,
        ["declaration", "code", "description"],
        force,
        indentation,
    )

    if status != 0:
        return status

    # see what else one needs to pull
    for name in downloaded:
        try:
            obj = library.Library(prefix, name)
            cache[name] = obj
            if not obj.valid:
                cache[name] = None

            # downloads any dependencies
            libraries |= obj.libraries.keys()

        except Exception as e:
            logger.error("loading `%s': %s...", name, str(e))
            cache[name] = None

    # recurse until done
    return pull_impl(webapi, prefix, libraries, force, indentation, cache)


def get_dependencies(ctx, asset_name):
    prefix = ctx.meta["config"].path
    lib = library.Library(prefix, asset_name)

    dependencies = {}

    libraries = list(lib.uses.values())
    if libraries:
        dependencies["libraries"] = libraries

    return dependencies


class LibraryCommand(AssetCommand):
    asset_info = AssetInfo(
        asset_type="library",
        diff_fields=["declaration", "code", "description"],
        push_fields=["name", "declaration", "code", "description"],
        get_dependencies=get_dependencies,
    )


@click.group(cls=AliasedGroup)
@click.pass_context
def libraries(ctx):
    """Configuration and manipulation of libraries"""


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

commands.initialise_asset_commands(libraries, CMD_LIST, LibraryCommand)


@libraries.command()
@click.argument("names", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    """Downloads the specified libraries from the server

  Example:
    $ beat libraries pull --force yyy
  """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        return pull_impl(webapi, ctx.meta["config"].path, names, force, 0, {})
