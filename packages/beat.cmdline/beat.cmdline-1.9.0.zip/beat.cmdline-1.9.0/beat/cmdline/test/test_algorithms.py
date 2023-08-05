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


# Basic tests for the command line beat program: algorithms

import nose.tools

from beat.core.algorithm import Algorithm
from beat.core.algorithm import Storage
from beat.core.dataformat import Storage as DFStorage
from beat.core.library import Storage as LibStorage

from . import core
from . import prefix
from . import tmp_prefix


class TestOnline(core.OnlineAssetTestCase):

    asset_type = "algorithm"
    storage_cls = Storage
    object_map = {
        "pull": "user/integers_add/1",
        "diff": "user/integers_add/1",
        "create": "user/newobject/1",
        "fork_from": "user/unknown/1",
        "fork": "user/forked_obj/1",
        "push": "user/db_input_loop_processor/1",
        "not_owner_push": "v1/integers_add/1",
        "push_invalid": "errors/description_too_long/1",
    }

    def _modify_asset(self, asset_name):
        """Re-imp"""

        storage = self.storage_cls(tmp_prefix, asset_name)
        storage.code.save("class Algorithm:\n  pass")

    def _prepare_fork_dependencies(self, asset_name):
        super()._prepare_fork_dependencies(asset_name)

        algorithm = Algorithm(prefix, asset_name)

        for lib in algorithm.libraries.keys():
            src_storage = LibStorage(prefix, lib)
            dst_storage = LibStorage(tmp_prefix, lib)
            dst_storage.save(*src_storage.load())

        for dataformat in algorithm.dataformats.keys():
            if dataformat.startswith("user"):
                src_storage = DFStorage(prefix, dataformat)
                dst_storage = DFStorage(tmp_prefix, dataformat)
                dst_storage.save(*src_storage.load())


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "algorithm"
    object_map = {
        "valid": "legacy/valid_algorithm/1",
        "invalid": "user/invalid/1",
        "create": "legacy/new_algorithm/1",
        "new": "legacy/new_algorithm/2",
        "fork": "legacy/forked_algorithm/1",
    }

    def setup(self):
        obj = "user/integers/1"
        storage = DFStorage(tmp_prefix, obj)
        if not storage.exists():
            exit_code, outputs = self.call(
                "create", obj, prefix=tmp_prefix, asset_type="dataformat"
            )
            nose.tools.eq_(exit_code, 0, outputs)
