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

import click
import simplejson as json

from beat.core.dock import Host

from . import common
from .click_helper import AliasedGroup

logger = logging.getLogger(__name__)


def get_remote_environments(ctx):
    config = ctx.meta.get("config")
    try:
        with common.make_webapi(config) as webapi:
            return webapi.get("/api/v1/backend/environments/")
    except Exception as e:
        logger.error("Failed to connect to platform: {}".format(e))
        return {}


def get_docker_environments():
    host = Host(raise_on_errors=False)
    return host.images_cache


@click.group(cls=AliasedGroup)
@click.pass_context
def environments(ctx):
    """Execution environment related commands"""


@environments.command()
@click.option(
    "--type",
    "-t",
    "type_",
    type=click.Choice(["docker", "remote", "all"], case_sensitive=False),
    default="all",
)
@click.option("--output", "-o", type=click.Path(), default=None)
@click.pass_context
def list(ctx, type_, output):
    """List available execution environments"""

    data = {}
    if type_ in ["remote", "all"]:
        data["remote"] = get_remote_environments(ctx)

    if type_ in ["docker", "all"]:
        data["docker"] = get_docker_environments()

    data_str = json.dumps(data, indent=4)

    if output is not None:
        with open(output, "wt") as file:
            click.echo(data_str, file=file)
    else:
        click.echo(data_str)
