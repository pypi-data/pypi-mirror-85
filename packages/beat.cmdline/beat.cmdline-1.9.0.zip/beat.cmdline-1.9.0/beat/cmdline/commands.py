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

import types

import click

from . import common
from .decorators import raise_on_error
from .scripts import main_cli


def copy_func(f, name=None):
    """
    based on https://stackoverflow.com/a/30714299/5843716

    return a function with same code, globals, defaults, closure, doc, and
    name (or provide a new name)
    """
    fn = types.FunctionType(
        f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__
    )
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    fn.__doc__ = f.__doc__

    return fn


@click.option(
    "--remote", help="Only acts on the remote copy of the list.", is_flag=True
)
@click.pass_context
@raise_on_error
def list_impl(ctx, remote):
    """Lists the assets of this type available on the platform.

    To list all existing asset of a type on your local prefix:

    $ beat <asset_type> list
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    if remote:
        with common.make_webapi(config) as webapi:
            return common.display_remote_list(webapi, asset_info.asset_type)
    else:
        return common.display_local_list(config.path, asset_info.asset_type)


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def path_impl(ctx, names):
    """Displays local path of asset files

  Example:
    $ beat <asset_type> path xxx
  """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.display_local_path(config.path, asset_info.asset_type, names)


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def edit_impl(ctx, name):
    """Edit local asset file

  Example:
    $ beat <asset_type> edit xxx
  """
    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.edit_local_file(
        config.path, config.editor, asset_info.asset_type, name
    )


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def check_impl(ctx, names):
    """Checks a local asset for validity.

    Example:
      $ beat <asset_type> check xxx
    """
    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.check(config.path, asset_info.asset_type, names)


@click.pass_context
@raise_on_error
def status_impl(ctx):
    """Shows (editing) status for all available items of asset type

  Example:
    $ beat <asset_type> status
  """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    with common.make_webapi(config) as webapi:
        return common.status(webapi, config.path, asset_info.asset_type)[0]


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def create_impl(ctx, names):
    """Creates a new local asset.

    Example:
      $ beat <asset_type> create xxx
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.create(config.path, asset_info.asset_type, names)


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def version_impl(ctx, name):
    """Creates a new version of an existing asset

    Example:
      $ beat <asset_type> version xxx
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.new_version(config.path, asset_info.asset_type, name)


@click.argument("src", nargs=1)
@click.argument("dst", nargs=1)
@click.pass_context
@raise_on_error
def fork_impl(ctx, src, dst):
    """Forks a local asset

    Example:
      $ beat <asset_type> fork xxx yyy
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.fork(config.path, asset_info.asset_type, src, dst)


@click.argument("name", nargs=-1)
@click.option(
    "--remote", help="Only acts on the remote copy of the algorithm", is_flag=True
)
@click.pass_context
@raise_on_error
def rm_impl(ctx, name, remote):
    """Deletes a local asset (unless --remote is specified)

    Example:
      $ beat <asset_type> rm xxx
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    if remote:
        with common.make_webapi(config) as webapi:
            return common.delete_remote(webapi, asset_info.asset_type, name)
    else:
        return common.delete_local(config.path, asset_info.asset_type, name)


@click.argument("name", nargs=-1)
@click.pass_context
@raise_on_error
def rm_local_impl(ctx, name):
    """Deletes a local asset

    Example:
      $ beat <asset_type> rm xxx
    """
    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    return common.delete_local(config.path, asset_info.asset_type, name)


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def diff_impl(ctx, name):
    """Shows changes between the local asset and the remote version

    Example:
      $ beat toolchains diff xxx
    """

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]

    with common.make_webapi(config) as webapi:
        return common.diff(
            webapi, config.path, asset_info.asset_type, name, asset_info.diff_fields
        )


@click.argument("names", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.option(
    "--dry-run",
    help="Doesn't really perform the task, just " "comments what would do",
    is_flag=True,
)
@click.pass_context
@raise_on_error
def push_impl(ctx, names, force, dry_run):
    """Uploads asset to the server

    Example:
        $ beat algorithms push --dry-run yyy
    """

    def do_push(ctx, dependency_type, names):
        push_cmd = main_cli.main.get_command(ctx, dependency_type).get_command(
            ctx, "push"
        )
        ctx.meta["asset_info"] = push_cmd.asset_info
        return ctx.invoke(push_cmd, names=names, force=force, dry_run=dry_run)

    config = ctx.meta["config"]
    asset_info = ctx.meta["asset_info"]
    mappings = ctx.meta.get("mappings", {})

    for name in names:
        validator = common.TYPE_VALIDATOR[asset_info.asset_type](config.path, name)
        if not validator.valid:
            raise RuntimeError(
                "Invalid {} {}".format(asset_info.asset_type, validator.errors)
            )

        with common.Selector(config.path) as selector:
            dependency_type = common.TYPE_PLURAL[asset_info.asset_type]
            fork = selector.forked_from(asset_info.asset_type, name)
            if fork:
                status = do_push(ctx, dependency_type, [fork])
                if status != 0:
                    return status
            version = selector.version_of(asset_info.asset_type, name)
            if version:
                status = do_push(ctx, dependency_type, [version])
                if status != 0:
                    return status

        if asset_info.get_dependencies is not None:
            dependencies = asset_info.get_dependencies(ctx, name)
            for dependency_type, dependency_list in dependencies.items():
                status = do_push(ctx, dependency_type, dependency_list)
                if status != 0:
                    return status

    with common.make_webapi(config) as webapi:
        return common.push(
            webapi=webapi,
            prefix=config.path,
            asset_type=asset_info.asset_type,
            names=names,
            fields=asset_info.push_fields,
            mappings=mappings,
            force=force,
            dry_run=dry_run,
            indentation=0,
        )


CMD_TABLE = {
    "list": list_impl,
    "path": path_impl,
    "edit": edit_impl,
    "check": check_impl,
    "status": status_impl,
    "create": create_impl,
    "version": version_impl,
    "fork": fork_impl,
    "rm": rm_impl,
    "rm_local": rm_local_impl,
    "diff": diff_impl,
    "push": push_impl,
}


def command(name):
    """Returns a copy of the method to be decorated.

    This allows to reuse the same commands. Using directly the original method
    would allow to only use it once.

    Parameters:
        name str: Name of the desired command
    """

    return copy_func(CMD_TABLE[name])


def initialise_asset_commands(click_cmd_group, cmd_list, cmd_cls):
    """Initialize a command group adding all the commands from cmd_list to it

    Parameters:
        click_cmd_group obj: click command to group
        cmd_list list: list of string or tuple of the commands to add
        cmd_cls: subclass of click Command to use
    """

    for item in cmd_list:
        if isinstance(item, tuple):
            click_cmd_group.command(cls=cmd_cls, name=item[0])(command(item[1]))
        else:
            click_cmd_group.command(cls=cmd_cls, name=item)(command(item))
