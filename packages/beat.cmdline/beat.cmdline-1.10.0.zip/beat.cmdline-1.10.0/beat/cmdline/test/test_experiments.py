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


# Basic tests for the command line beat program: experiments

import logging
import os

import nose.tools

from beat.core.algorithm import Storage as AlgStorage
from beat.core.dataformat import Storage as DFStorage
from beat.core.experiment import Experiment
from beat.core.experiment import Storage
from beat.core.test.test_execution import clear_conda_environment
from beat.core.test.test_execution import create_conda_environment
from beat.core.test.utils import slow
from beat.core.toolchain import Storage as TCStorage

from . import core
from . import prefix
from . import tmp_prefix
from .utils import MockLoggingHandler
from .utils import index_experiment_dbs


def setup_experiments():
    index_experiment_dbs("user/user/double_triangle/1/double_triangle")
    index_experiment_dbs("user/user/integers_addition/1/integers_addition")


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "experiment"
    object_map = {
        "valid": "user/user/single/1/single",
        "invalid": "user/user/single/1/does_not_exist",
        "create": "user/user/single/1/single",
        "fork": "user/user/unknown/1/forked_obj",
    }

    @classmethod
    def create(cls, obj=None):
        """Can't create from scratch so copy an object of the tests"""

        src_storage = cls.storage_cls(prefix, obj)
        dst_storage = cls.storage_cls(tmp_prefix, obj)
        dst_storage.save(*src_storage.load())

    def test_create(self, obj=None):
        nose.SkipTest("Experiment can't be created")

    @slow
    def test_plot_non_image_local_results(self):
        obj = "user/user/single/1/no_image_plotter"
        cache_path = os.path.join(tmp_prefix, "cache")

        index_experiment_dbs(obj)

        exit_code, outputs = self.call("run", obj, prefix=prefix, cache=cache_path)
        nose.tools.eq_(exit_code, 0, outputs)

        # now push the new object and then delete it remotely
        exit_code, outputs = self.call(
            "plot",
            "--output-folder=%s" % tmp_prefix,
            obj,
            prefix=prefix,
            cache=cache_path,
        )
        nose.tools.eq_(exit_code, 0, outputs)
        generated_files = [
            file_ for file_ in os.listdir(tmp_prefix) if file_.endswith(".json")
        ]
        nose.tools.assert_true(generated_files)


class TestOnline(core.OnlineAssetTestCase):

    asset_type = "experiment"
    storage_cls = Storage
    object_map = {
        "pull": "user/user/single/1/single",
        "diff": "user/user/single/1/single",
        "push": "user/user/unknown/1/unknown",
        "fork_from": "user/user/unknown/1/unknown",
        "fork": "user/user/unknown/1/forked_obj",
        "not_owner_push": "other_user/user/single/1/someexp",
        "push_invalid": "errors/user/single/1/description_too_long",
    }

    def _modify_asset(self, asset_name):
        """Re-imp"""

        experiment = Experiment(tmp_prefix, asset_name)
        experiment.data["globals"]["queue"] = "another_queue"
        experiment.write()

    def _prepare_fork_dependencies(self, asset_name):
        super()._prepare_fork_dependencies(asset_name)
        assets = [
            (DFStorage, ["user/single_integer/1"]),
            (AlgStorage, ["user/unknown/1", "user/integers_echo_analyzer_v2/1"]),
            (TCStorage, ["user/unknown/1"]),
            (Storage, ["user/user/unknown/1/unknown"]),
        ]

        for item in assets:
            storage_cls, asset_list = item
            for asset in asset_list:
                src_storage = storage_cls(prefix, asset)
                dst_storage = storage_cls(tmp_prefix, asset)
                dst_storage.save(*src_storage.load())

        # The remote database dataformats is not the same as the local version
        # hence download it to ensure we can push experiments using it properly
        self.call("pull", "simple/1", asset_type="databases", prefix=tmp_prefix)

    @slow
    @core.skip_disconnected
    def test_push_and_delete(self):
        asset_name = self.object_map["push"]
        self._prepare_fork_dependencies(asset_name)

        exit_code, output = self.call("push", asset_name, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)
        exit_code, output = self.call("rm", "--remote", asset_name)
        nose.tools.eq_(exit_code, 0, output)

    @core.skip_disconnected
    def test_draw(self):
        obj = "user/user/double_triangle/1/double_triangle"
        self.test_pull_one(obj)

        # now push the new object and then delete it remotely
        exit_code, outputs = self.call(
            "draw", "--path=%s" % tmp_prefix, prefix=tmp_prefix
        )
        nose.tools.eq_(exit_code, 0, outputs)

        nose.tools.assert_true(
            os.path.exists(os.path.join(tmp_prefix, "experiments", obj + ".dot"))
        )
        nose.tools.assert_true(
            os.path.exists(os.path.join(tmp_prefix, "experiments", obj + ".png"))
        )

    @slow
    @core.skip_disconnected
    def test_start(self):
        obj = "user/user/double_triangle/1/double_triangle"
        exit_code, outputs = self.call("start", obj)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    @core.skip_disconnected
    def test_cancel(self):
        obj = "user/user/double_triangle/1/double_triangle"
        exit_code, outputs = self.call("cancel", obj)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    @core.skip_disconnected
    def test_reset(self):
        obj = "user/user/double_triangle/1/double_triangle"
        exit_code, outputs = self.call("reset", obj)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    @core.skip_disconnected
    def test_runstatus(self):
        obj = "user/user/double_triangle/1/double_triangle"
        exit_code, outputs = self.call("runstatus", obj)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    @core.skip_disconnected
    def test_plot_local_results(self):
        obj = "user/user/single/1/single"
        cache_path = os.path.join(tmp_prefix, "cache")

        self.test_pull_one(obj)
        index_experiment_dbs(obj)

        exit_code, outputs = self.call("run", obj, prefix=tmp_prefix, cache=cache_path)
        nose.tools.eq_(exit_code, 0, outputs)

        plotters = ["plot/scatter/1", "plot/bar/1", "plot/isoroc/1"]
        for plotter in plotters:
            exit_code, outputs = self.call(
                "pull",
                plotter,
                prefix=tmp_prefix,
                asset_type="plotter",
                cache=cache_path,
            )
            nose.tools.eq_(exit_code, 0, outputs)

        # now push the new object and then delete it remotely
        exit_code, outputs = self.call(
            "plot",
            "--output-folder=%s" % tmp_prefix,
            obj,
            prefix=tmp_prefix,
            cache=cache_path,
        )
        nose.tools.eq_(exit_code, 0, outputs)
        generated_files = [
            file_ for file_ in os.listdir(tmp_prefix) if file_.endswith(".png")
        ]
        nose.tools.assert_true(generated_files)


class TestCache(core.AssetBaseTest):
    asset_type = "experiment"

    def setUp(self):
        super().setUp()
        setup_experiments()

    @slow
    def test_list_integers_addition_1_cache(self):
        obj = "user/user/integers_addition/1/integers_addition"
        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        exit_code, outputs = self.call("caches", "--list", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    def test_checksum_integers_addition_1_cache(self):
        obj = "user/user/integers_addition/1/integers_addition"
        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        exit_code, outputs = self.call("caches", "--checksum", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    def test_delete_integers_addition_1_cache(self):
        obj = "user/user/integers_addition/1/integers_addition"
        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        exit_code, outputs = self.call("caches", "--delete", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)


class TestRun(core.AssetBaseTest):
    asset_type = "experiment"

    def setUp(self):
        super().setUp()
        setup_experiments()

    @slow
    def test_run_integers_addition_1(self):
        obj = "user/user/integers_addition/1/integers_addition"
        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    def test_run_integers_addition_1_different_environment(self):
        environment_path = create_conda_environment(["beat.backend.python"])

        obj = "user/user/integers_addition/1/integers_addition"
        exit_code, status = self.call(
            "run",
            obj,
            cache=tmp_prefix,
            environment=os.path.join(environment_path, "bin", "python"),
        )

        clear_conda_environment(environment_path)

        nose.tools.eq_(exit_code, 0)

    @slow
    def test_run_integers_addition_1_twice(self):
        log_handler = MockLoggingHandler(level="DEBUG")
        logging.getLogger().addHandler(log_handler)
        log_messages = log_handler.messages

        obj = "user/user/integers_addition/1/integers_addition"

        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

        info_len = len(log_messages["info"])
        nose.tools.assert_greater(info_len, 4)
        nose.tools.assert_true(
            log_messages["info"][info_len - 1].startswith("  Results")
        )

        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

        info_len = len(log_messages["info"])
        nose.tools.assert_greater(info_len, 6)
        nose.tools.assert_true(
            log_messages["info"][info_len - 1].startswith("  Results")
        )

    @slow
    def test_run_double_triangle_1(self):
        obj = "user/user/double_triangle/1/double_triangle"
        exit_code, outputs = self.call("run", obj, cache=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)

    @slow
    def test_run_single_error_1_local(self):
        # When running locally, the module with the error is loaded
        # inside the currently running process and will return '1'.
        obj = "user/user/single/1/single_error"
        exit_code, outputs = self.call("run", obj, "--local", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)

    @slow
    def test_run_single_error_twice_local(self):
        # This one makes sure our output reset is working properly. Both tries should
        # give out the same error.
        obj = "user/user/single/1/single_error"
        exit_code, outputs = self.call("run", obj, "--local", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)
        exit_code, outputs = self.call("run", obj, "--local", cache=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)
