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


# Docker based tests for algorithms and analyzers

import json
import os
import shutil

import nose.tools
import pkg_resources

from beat.backend.python.hash import hashDataset
from beat.backend.python.hash import toPath
from beat.core.database import Database
from beat.core.test.utils import slow

from . import core
from . import prefix
from . import tmp_prefix

instructions_dir = pkg_resources.resource_filename(__name__, "instructions")


def index_db_from_instructions(input_field):
    database = Database(prefix, input_field["database"])
    view = database.view(input_field["protocol"], input_field["set"])
    filename = toPath(
        hashDataset(
            input_field["database"], input_field["protocol"], input_field["set"]
        ),
        suffix=".db",
    )
    view.index(os.path.join(tmp_prefix, filename))


class TestDockerAlgorithmExecution(core.AssetBaseTest):

    asset_type = "algorithm"

    @slow
    def test_algorithm_using_database(self):
        instructions = os.path.join(instructions_dir, "algo_using_database.json")
        with open(instructions) as instruction_file:
            instructions_data = json.load(instruction_file)
        input_field = instructions_data["inputs"]["in"]
        index_db_from_instructions(input_field)

        exit_code, outputs = self.call("execute", instructions, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, msg=outputs)

    @slow
    def test_algorithm_using_cached_files(self):
        cache_dir = os.path.join(tmp_prefix, "ab", "cd", "ef")

        os.makedirs(cache_dir)
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum",
            ),
            cache_dir,
        )

        instructions = os.path.join(instructions_dir, "algo_using_cached_files.json")

        exit_code, outputs = self.call("execute", instructions, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, msg=outputs)

    @slow
    def test_algorithm_using_database_and_cached_files(self):
        cache_dir = os.path.join(tmp_prefix, "ab", "cd", "ef")

        os.makedirs(cache_dir)
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum",
            ),
            cache_dir,
        )

        instructions = os.path.join(
            instructions_dir, "algo_using_database_and_cached_files.json"
        )

        with open(instructions) as instruction_file:
            instructions_data = json.load(instruction_file)
        input_field = instructions_data["inputs"]["in1"]
        index_db_from_instructions(input_field)

        exit_code, outputs = self.call("execute", instructions, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, msg=outputs)

    @slow
    def test_analyzer(self):
        cache_dir = os.path.join(tmp_prefix, "ab", "cd", "ef")

        os.makedirs(cache_dir)
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index",
            ),
            cache_dir,
        )
        shutil.copy(
            os.path.join(
                instructions_dir,
                "0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum",
            ),
            cache_dir,
        )

        instructions = os.path.join(instructions_dir, "analyzer.json")

        exit_code, outputs = self.call("execute", instructions, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, msg=outputs)


class TestDockerExperimentRun(core.AssetBaseTest):
    asset_type = "experiment"

    @slow
    def test_run_single_error_1(self):
        # When running on docker, the module is loaded in the docker
        # container and the local process will return '1'.
        obj = "user/user/single/1/single_error"
        exit_code, outputs = self.call("run", obj, "--docker", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)

    @slow
    def test_run_single_error_twice(self):
        # This one makes sure our output reset is working properly. Both tries should
        # give out the same error.
        obj = "user/user/single/1/single_error"
        exit_code, outputs = self.call("run", obj, "--docker", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)
        exit_code, outputs = self.call("run", obj, "--docker", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)

    def run_database_sharing(self, share_databases, expected_output):
        """Test that the database sharing works"""

        db = Database(prefix, "integers_db/1")
        nose.tools.assert_true(db.valid, db.errors)

        data_sharing_path = db.data["root_folder"]

        offset = 12
        with open(os.path.join(data_sharing_path, "datafile.txt"), "wt") as data_file:
            data_file.write("{}".format(offset))

        obj = "user/user/integers_addition/1/shared_datasets"

        args = ["run", obj, "--docker"]
        if share_databases:
            args.append("--share-databases")

        exit_code, outputs = self.call(*args, cache=tmp_prefix)

        nose.tools.eq_(exit_code, expected_output, outputs)

    @slow
    def test_run_database_sharing(self):
        for share, result in [(False, 1), (True, 0)]:
            yield self.run_database_sharing, share, result
