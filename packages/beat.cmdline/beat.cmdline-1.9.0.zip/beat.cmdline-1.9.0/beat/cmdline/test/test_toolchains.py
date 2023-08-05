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


# Basic tests for the command line beat program: toolchains

import os

import nose.tools

from beat.core.toolchain import Storage
from beat.core.toolchain import Toolchain

from . import core
from . import tmp_prefix


class TestOnline(core.OnlineAssetTestCase):

    asset_type = "toolchain"
    storage_cls = Storage
    object_map = {
        "pull": "user/single/1",
        "diff": "user/single/1",
        "create": "user/newobject/1",
        "fork_from": "user/unknown/1",
        "fork": "user/forked_obj/1",
        "push": "user/two_loops/1",
        "not_owner_push": "other_user/somechain/1",
        "push_invalid": "errors/invalid/1",
    }

    def _modify_asset(self, asset_name):
        """Re-imp"""

        toolchains = Toolchain(tmp_prefix, asset_name)
        toolchains.data["representation"]["blocks"]["echo"]["height"] = 2
        toolchains.write()

    @core.skip_disconnected
    def test_draw(self):
        obj = "user/double_triangle/1"
        self.test_pull_one(obj)

        # now push the new object and then delete it remotely
        exit_code, output = self.call(
            "draw", "--path=%s" % tmp_prefix, prefix=tmp_prefix
        )
        nose.tools.eq_(exit_code, 0, output)

        nose.tools.assert_true(
            os.path.exists(os.path.join(tmp_prefix, "toolchains", obj + ".png"))
        )
        nose.tools.assert_true(
            os.path.exists(os.path.join(tmp_prefix, "toolchains", obj + ".dot"))
        )


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "toolchain"
    object_map = {
        "valid": "user/double_triangle/1",
        "invalid": "user/invalid/1",
        "create": "user/new_toolchain/1",
        "new": "user/new_toolchain/2",
        "fork": "user/forked_toolchain/1",
    }
