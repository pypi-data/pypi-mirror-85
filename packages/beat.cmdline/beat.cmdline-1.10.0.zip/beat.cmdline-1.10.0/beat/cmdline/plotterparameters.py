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


import click

from . import commands
from . import common
from .click_helper import AliasedGroup
from .click_helper import AssetCommand
from .click_helper import AssetInfo
from .decorators import raise_on_error


def pull_impl(webapi, prefix, names, force, indentation, format_cache):
    """Copies plotterparameters from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (list): A list of strings, each representing the unique relative
        path of the objects to retrieve or a list of usernames from which to
        retrieve objects. If the list is empty, then we pull all available
        objects of a given type. If no user is set, then pull all public
        objects of a given type.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).


    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    # download required plotterparameter
    status, names = common.pull(
        webapi,
        prefix,
        "plotterparameter",
        names,
        ["data", "short_description", "plotter"],
        force,
        indentation,
    )
    return status


class PlotterparametersCommand(AssetCommand):
    asset_info = AssetInfo(asset_type="plotterparameter", diff_fields=["data"])


@click.group(cls=AliasedGroup)
@click.pass_context
def plotterparameters(ctx):
    """Plotterparameters commands"""


CMD_LIST = [
    "list",
    "path",
    "edit",
    "check",
    "status",
    "create",
    "version",
    "fork",
    "diff",
    ("rm", "rm_local"),
]

commands.initialise_asset_commands(
    plotterparameters, CMD_LIST, PlotterparametersCommand
)


@plotterparameters.command()
@click.argument("names", nargs=-1)
@click.option("--force", help="Force", is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    """Downloads the specified plotterparameters from the server.

       $ beat plotterparameters pull xxx.
    """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        name = common.make_up_remote_list(webapi, "plotterparameter", names)
        if name is None:
            return 1  # error
        return pull_impl(webapi, ctx.meta["config"].path, name, force, 0, {})
