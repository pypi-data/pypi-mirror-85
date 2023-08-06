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


# Basic tests for the command line beat program: databases

import nose
import nose.tools

from beat.backend.python.protocoltemplate import Storage as PTStorage
from beat.backend.python.test.test_database import INTEGERS_DBS
from beat.core.database import Database
from beat.core.database import Storage
from beat.core.database import get_first_procotol_template

from . import core
from . import prefix
from . import tmp_prefix


class TestLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "database"
    object_map = {
        "valid": "integers_db/1",
        "invalid": "invalid/1",
        "create": "new_database/1",
        "new": "new_database/2",
        "fork": "forked_database/1",
    }

    def setUp(self):
        super().setUp()

        obj = get_first_procotol_template(prefix)
        storage = PTStorage(tmp_prefix, obj)
        if not storage.exists():
            exit_code, outputs = self.call(
                "create", obj, prefix=tmp_prefix, asset_type=storage.asset_type
            )
            nose.tools.eq_(exit_code, 0, outputs)


class TestOnline(core.OnlineAssetTestCase):
    asset_type = "database"
    storage_cls = Storage
    object_map = {
        "create": "new_database/1",
        "pull": "simple/1",
        "diff": "simple/1",
        "push": "simple/1",
    }

    def setUp(self):
        super().setUp()
        obj = get_first_procotol_template(prefix)
        storage = PTStorage(tmp_prefix, obj)
        if not storage.exists():
            exit_code, outputs = self.call(
                "create", obj, prefix=tmp_prefix, asset_type=storage.asset_type
            )
            nose.tools.eq_(exit_code, 0, outputs)

    def _modify_asset(self, asset_name):
        """Re-imp"""

        database = Database(tmp_prefix, asset_name)
        nose.tools.eq_(
            len(database.errors),
            0,
            "Failed to load Database: \n%s" % "\n".join(database.errors),
        )
        database.data["root_folder"] = "/a/different/path"
        database.write()

    @core.skip_disconnected
    def test_push_and_delete(self):
        asset_name = self.object_map["push"]

        exit_code, output = self.call("push", asset_name)
        nose.tools.eq_(exit_code, 1, output)
        exit_code, output = self.call("rm", "--remote", asset_name)
        nose.tools.eq_(exit_code, 2, output)

    @core.skip_disconnected
    def test_push_different_versions(self):
        raise nose.SkipTest("Databases don't allow push")

    @core.skip_disconnected
    def test_push_different_forks(self):
        raise nose.SkipTest("Databases don't allow push")

    @core.skip_disconnected
    def test_fail_push_invalid(self):
        raise nose.SkipTest("Databases don't allow push")

    @core.skip_disconnected
    def test_fail_not_owner_push(self):
        """No owner so not need to test"""

        raise nose.SkipTest("Database have no owner")


class TestView(core.AssetBaseTest):
    asset_type = "database"

    def setUp(self):
        self.index_integer_db()

    def index_integer_db(self):
        self.call("index", "integers_db/1")

    def test_view_good(self):
        exit_code, outputs = self.call("view", "integers_db/1/double/double")
        nose.tools.eq_(exit_code, 0, outputs)

    def test_view_unknown_protocol(self):
        exit_code, outputs = self.call("view", "integers_db/1/single/double")
        nose.tools.eq_(exit_code, 1, outputs)

    def test_view_unknown_set(self):
        exit_code, outputs = self.call("view", "integers_db/1/double/single")
        nose.tools.eq_(exit_code, 1, outputs)

    def test_view_bad(self):
        exit_code, outputs = self.call("view", "integers_db/1/two_sets")
        nose.tools.eq_(exit_code, 1, outputs)

    def test_view_invalid(self):
        exit_code, outputs = self.call("view", "invalid/1/default/set")
        nose.tools.eq_(exit_code, 1, outputs)


class TestIndex(core.AssetBaseTest):
    asset_type = "database"

    def test_index_unknown_database(self):
        exit_code, outputs = self.call("index", "foobar/1")
        nose.tools.eq_(exit_code, 1, outputs)

    def test_index_method(self):
        for db_name in INTEGERS_DBS:
            yield self.index_good, db_name

    def index_good(self, db_name):
        exit_code, outputs = self.call("index", db_name)
        nose.tools.eq_(exit_code, 0, outputs)

    def test_list_index_good(self):
        for db_name in INTEGERS_DBS:
            yield self.list_index_good, db_name

    def list_index_good(self, db_name):
        exit_code, outputs = self.call("index", db_name)
        nose.tools.eq_(exit_code, 0, outputs)
        exit_code, outputs = self.call("index", "--list", db_name)
        nose.tools.eq_(exit_code, 0, outputs)

    def test_delete_index_good(self):
        for db_name in INTEGERS_DBS:
            yield self.delete_index_good, db_name

    def delete_index_good(self, db_name):
        exit_code, outputs = self.call("index", db_name)
        nose.tools.eq_(exit_code, 0, outputs)
        exit_code, outputs = self.call("index", "--delete", db_name)
        nose.tools.eq_(exit_code, 0, outputs)

    def test_index_all(self):  # bad and good, return != 0
        expected_errors = 16
        existing_errors, outputs = self.call("index")
        nose.tools.assert_true(
            existing_errors >= expected_errors,
            (
                "There should be at least %d "
                "errors on installed databases, but I've found only %d"
                % (expected_errors, existing_errors)
            ),
        )

    def test_index_error_invalid_env(self):
        db_name = "integers_db_invalid_env/1"
        with nose.tools.assert_raises(RuntimeError) as context:
            self.call("index", "--docker", db_name)
        print(context.exception)
        nose.tools.assert_true(
            "Environment Does not exist (1.4.0) not found for the database"
            in context.exception.args[0]
        )
