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


# Basic tests for the command line beat program: plotterparameters

import nose.tools

from beat.core.plotterparameter import Plotterparameter
from beat.core.plotterparameter import Storage
from beat.core.test.utils import slow

from . import core
from . import tmp_prefix


class TestOnline(core.OnlineAssetTestCase):

    asset_type = "plotterparameter"
    storage_cls = Storage
    object_map = {
        "pull": "plot/bar/1",
        "diff": "plot/bar/1",
        "create": "user/newobject/1",
        "push": "plot/bar/1",
        "not_owner_push": "plot/bar/1",
    }

    def _modify_asset(self, asset_name):
        """Re-imp"""

        plotterparameter = Plotterparameter(tmp_prefix, asset_name)
        plotterparameter.data["value"] = {"dummy": "int64"}
        plotterparameter.write()

    @slow
    @core.skip_disconnected
    def test_push_and_delete(self):
        asset_name = self.object_map["push"]

        exit_code, output = self.call("push", asset_name)
        nose.tools.eq_(exit_code, 2, output)
        exit_code, output = self.call("rm", "--remote", asset_name)
        nose.tools.eq_(exit_code, 2, output)

    @core.skip_disconnected
    def test_push_different_versions(self):
        raise nose.SkipTest("Plotterparameters don't allow push")

    @core.skip_disconnected
    def test_push_different_forks(self):
        raise nose.SkipTest("Plotterparameters don't allow push")

    @core.skip_disconnected
    def test_fail_push_invalid(self):
        raise nose.SkipTest("Plotterparameters don't allow push")

    @core.skip_disconnected
    def test_fail_not_owner_push(self):
        """No owner so not need to test"""

        raise nose.SkipTest("Plotterparameters don't allow push")


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "plotterparameter"
    object_map = {
        "valid": "plot/config/1",
        "invalid": "user/invalid/1",
        "create": "user/new_plotterparameter/1",
        "new": "user/new_plotterparameter/2",
        "fork": "user/forked_plotterparameter/1",
    }
