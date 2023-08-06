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


# Basic tests for the command line beat program: dataformats

from beat.core.dataformat import DataFormat
from beat.core.dataformat import Storage

from . import core
from . import prefix
from . import tmp_prefix


class TestOnline(core.OnlineAssetTestCase):

    asset_type = "dataformat"
    storage_cls = Storage
    object_map = {
        "pull": "system/bounding_box_video/1",
        "diff": "system/integer/1",
        "create": "user/newobject/1",
        "fork_from": "user/composed/1",
        "fork": "user/forked_obj/1",
        "push": "user/composed/1",
        "not_owner_push": "system/chart/1",
        "push_invalid": "errors/description_too_long/1",
    }

    def _modify_asset(self, asset_name):
        """Re-imp"""

        dataformat = DataFormat(tmp_prefix, asset_name)
        dataformat.data["value"] = "int64"
        dataformat.write()

    def _prepare_fork_dependencies(self, asset_name):
        super()._prepare_fork_dependencies(asset_name)

        dataformat = DataFormat(prefix, asset_name)

        for df in dataformat.referenced.keys():
            if df.startswith("user"):
                src_storage = Storage(prefix, df)
                dst_storage = Storage(tmp_prefix, df)
                dst_storage.save(*src_storage.load())


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "dataformat"
    object_map = {
        "valid": "user/3d_array_of_dataformat/1",
        "invalid": "user/invalid/1",
        "create": "user/new_dataformat/1",
        "new": "user/new_dataformat/2",
        "fork": "user/forked_dataformat/1",
    }
