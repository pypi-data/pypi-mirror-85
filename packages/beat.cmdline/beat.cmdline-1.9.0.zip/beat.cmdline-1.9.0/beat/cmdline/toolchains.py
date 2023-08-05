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


class ToolchainCommand(AssetCommand):
    asset_info = AssetInfo(
        asset_type="toolchain",
        diff_fields=["declaration", "description"],
        push_fields=["name", "declaration", "description"],
    )


@click.group(cls=AliasedGroup)
@click.pass_context
def toolchains(ctx):
    """toolchains commands"""


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

commands.initialise_asset_commands(toolchains, CMD_LIST, ToolchainCommand)


@toolchains.command()
@click.argument("names", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    """Downloads the specified toolchains from the server.

       $ beat toolchains pull xxx.
    """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        status, downloaded = common.pull(
            webapi,
            ctx.meta["config"].path,
            "toolchain",
            names,
            ["declaration", "description"],
            force,
            indentation=0,
        )
        return status


@toolchains.command()
@click.argument("names", nargs=-1)
@click.option(
    "--path",
    help="Use path to write files to disk (instead of the " "current directory)",
    type=click.Path(),
)
@click.pass_context
@raise_on_error
def draw(ctx, names, path):
    """Creates a visual representation of the toolchain"""
    return common.dot_diagram(ctx.meta["config"].path, "toolchain", names, path, [])
