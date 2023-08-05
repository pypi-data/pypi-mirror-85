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


# Basic tests for the command line beat program: environments

import nose.tools
import simplejson as json

from beat.core.test.utils import slow

from . import core


class TestOnline(core.OnlineTestCase):
    asset_type = "environments"  # give command group as environments are not assets

    @slow
    @core.skip_disconnected
    def test_all_list(self):
        exit_code, output = self.call("list", "-t", "all")
        nose.tools.eq_(exit_code, 0, msg=output)

        output_data = json.loads(output)

        nose.tools.assert_true(all(key in output_data for key in ["remote", "docker"]))
        nose.tools.assert_not_equals(len(output_data["remote"]), 0)
        nose.tools.assert_not_equals(len(output_data["docker"]), 0)

    @slow
    @core.skip_disconnected
    def test_remote_list(self):
        exit_code, output = self.call("list", "-t", "remote")
        nose.tools.eq_(exit_code, 0, msg=output)

        output_data = json.loads(output)

        nose.tools.assert_true("remote" in output_data)
        nose.tools.assert_not_equals(len(output_data["remote"]), 0)


class TestDockerEnvironments(core.AssetBaseTest):
    asset_type = "environments"  # give command group as environments are not assets

    @slow
    def test_docker_list(self):
        exit_code, output = self.call("list", "-t", "docker")
        nose.tools.eq_(exit_code, 0, msg=output)

        output_data = json.loads(output)

        nose.tools.assert_true("docker" in output_data)
        nose.tools.assert_not_equals(len(output_data["docker"]), 0)
