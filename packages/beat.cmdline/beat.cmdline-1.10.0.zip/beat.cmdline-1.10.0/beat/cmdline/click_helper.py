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

"""Click based helper classes"""

import click


class AliasedGroup(click.Group):
    """ Class that handles prefix aliasing for commands """

    def get_command(self, ctx, cmd_name):
        """Re-imp"""

        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


class MutuallyExclusiveOption(click.Option):
    """Class implementing mutually exclusive option

    From https://stackoverflow.com/a/37491504/5843716
    """

    def __init__(self, *args, **kwargs):
        """Initialize"""

        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help_ = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = (
                "{}\n"
                "NOTE: This argument is mutually exclusive with arguments: [{}].".format(
                    help_, ex_str
                )
            )

        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """Re-imp"""

        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super().handle_parse_result(ctx, opts, args)


class AssetInfo:
    """ Information needed by the command to properly call local and remote
        commands
    """

    def __init__(
        self, asset_type=None, diff_fields=None, push_fields=None, get_dependencies=None
    ):
        self.asset_type = asset_type
        self.diff_fields = diff_fields
        self.push_fields = push_fields
        self.get_dependencies = get_dependencies

    def __repr__(self):
        return "{}\n{}\n{}\n{}".format(
            self.asset_type, self.diff_fields, self.push_fields, self.get_dependencies
        )


class AssetCommand(click.Command):
    """ Custom click command that will update the context with asset information
        related to the command called.
    """

    asset_info = AssetInfo()

    def invoke(self, ctx):
        """Re-imp"""

        ctx.meta["asset_info"] = self.asset_info
        return super().invoke(ctx)
