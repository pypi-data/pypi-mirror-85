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


"""
Base class for asset testing
"""

import os
import shutil

from collections import namedtuple
from functools import wraps

import click
import nose.tools

from click.testing import CliRunner

from beat.cmdline.scripts import main_cli
from beat.core.test.utils import cleanup
from beat.core.test.utils import skipif
from beat.core.test.utils import slow

from .. import common
from . import disconnected
from . import platform
from . import prefix
from . import tmp_prefix
from . import token
from . import user

if not disconnected:
    from django.contrib.staticfiles.testing import LiveServerTestCase
else:

    class LiveServerTestCase:
        """Dummy shell class"""

        live_server_url = None

        @classmethod
        def setUpClass(cls):
            pass

        def setUp(self):
            pass


# ----------------------------------------------------------
# decorators

# Make skip on disconnected a decorator, this will make tests easier to read and write
skip_disconnected = skipif(disconnected, "missing test platform (%s)" % platform)


def skip_no_version(method):
    """Skip test is asset does not support versioning"""

    @wraps(method)
    def _impl(self, *args, **kwargs):
        with common.Selector(tmp_prefix) as selector:
            if not selector.has_versions(self.asset_type):
                raise nose.SkipTest(
                    "{} does not support versions".format(self.asset_type)
                )
        return method(self, *args, **kwargs)

    return _impl


def skip_no_fork(method):
    """Skip test if asset does not support forking"""

    @wraps(method)
    def _impl(self, *args, **kwargs):
        with common.Selector(tmp_prefix) as selector:
            if not selector.can_fork(self.asset_type):
                raise nose.SkipTest("{} does not support forks".format(self.asset_type))
        return method(self, *args, **kwargs)

    return _impl


# ----------------------------------------------------------
# helper

# Used for making direct calls
MockConfig = namedtuple("MockConfig", ["platform", "user", "token"])


# ----------------------------------------------------------


class BaseTest:
    asset_type = None

    def setUp(self):
        pass

    def tearDown(self):
        cleanup()

    @classmethod
    def get_cmd_group(cls, asset_type):
        try:
            cmd_group = common.TYPE_PLURAL[asset_type]
        except KeyError:
            return asset_type

        if "/" in cmd_group:
            cmd_group = cmd_group.split("/")[-1]
        return cmd_group

    @classmethod
    def call(cls, *args, **kwargs):
        """A central mechanism to call the main routine with the right parameters"""

        use_prefix = kwargs.get("prefix", prefix)
        use_platform = kwargs.get("platform", platform)
        use_cache = kwargs.get("cache", "cache")
        asset_type = kwargs.get("asset_type", cls.asset_type)
        remote_user = kwargs.get("user", user)

        cmd_group = cls.get_cmd_group(asset_type)

        parameters = [
            "--test-mode",
            "--prefix",
            use_prefix,
            "--token",
            token,
            "--user",
            remote_user,
            "--cache",
            use_cache,
            "--platform",
            use_platform,
        ]

        if cmd_group:
            parameters.append(cmd_group)

        parameters += list(args)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(main_cli.main, parameters, catch_exceptions=False)

        if result.exit_code != 0:
            click.echo(result.output)
        return result.exit_code, result.output


# ----------------------------------------------------------


class AssetBaseTest(BaseTest):
    """Base class that ensures that the asset_type is set before calling click"""

    object_map = {}
    storage_cls = None

    @classmethod
    def create(cls, obj=None):
        obj = obj or cls.object_map["create"]
        exit_code, outputs = cls.call("create", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        storage = cls.storage_cls(tmp_prefix, obj)
        nose.tools.assert_true(storage.exists())
        return storage

    @classmethod
    def delete(cls, obj):
        exit_code, outputs = cls.call("rm", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        storage = cls.storage_cls(tmp_prefix, obj)
        nose.tools.assert_false(storage.exists())

    @classmethod
    def call(cls, *args, **kwargs):
        nose.tools.assert_is_not_none(cls.asset_type, "Missing value for asset_type")
        return super().call(*args, **kwargs)


class AssetLocalTest(AssetBaseTest):
    """Base class for local tests"""

    def __init__(self):
        super().__init__()
        nose.tools.assert_true(self.object_map)
        nose.tools.assert_is_not_none(self.storage_cls)

    def test_local_list(self):
        exit_code, outputs = self.call("list")
        nose.tools.eq_(exit_code, 0, outputs)

    def test_check_valid(self):
        exit_code, outputs = self.call("check", self.object_map["valid"])
        nose.tools.eq_(exit_code, 0, outputs)

    def test_check_invalid(self):
        exit_code, outputs = self.call("check", self.object_map["invalid"])
        nose.tools.eq_(exit_code, 1, outputs)

    def test_create(self, obj=None):
        self.create(self.object_map["create"])

    @skip_no_version
    def test_new_version(self):
        obj = self.object_map["create"]
        obj2 = self.object_map["new"]
        self.create(obj)
        exit_code, outputs = self.call("version", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        s = self.storage_cls(tmp_prefix, obj2)
        nose.tools.assert_true(s.exists())

        # check version status
        with common.Selector(tmp_prefix) as selector:
            nose.tools.eq_(selector.version_of(self.asset_type, obj2), obj)

    def test_fork(self):
        obj = self.object_map["create"]
        obj2 = self.object_map["fork"]
        self.create(obj)
        with common.Selector(tmp_prefix) as selector:
            if selector.can_fork(self.asset_type):
                exit_code, outputs = self.call("fork", obj, obj2, prefix=tmp_prefix)
                nose.tools.eq_(exit_code, 0, outputs)
                selector.load()
                s = self.storage_cls(tmp_prefix, obj2)
                nose.tools.assert_true(s.exists())
                nose.tools.eq_(selector.forked_from(self.asset_type, obj2), obj)
            else:
                exit_code, outputs = self.call("fork", obj, obj2, prefix=tmp_prefix)
                nose.tools.assert_not_equal(exit_code, 0)

    def test_delete_local(self):
        obj = self.object_map["create"]
        self.create(obj)
        self.delete(obj)

    def test_delete_local_unexisting(self):
        obj = self.object_map["create"]
        storage = self.storage_cls(tmp_prefix, obj)
        nose.tools.assert_false(storage.exists())

        exit_code, outputs = self.call("rm", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)
        nose.tools.assert_false(storage.exists())


# ----------------------------------------------------------


class AssetRemoteTest(AssetBaseTest):
    """Base class for remote tests"""

    def __init__(self):
        super().__init__()
        nose.tools.assert_true(self.object_map)
        nose.tools.assert_is_not_none(self.storage_cls)

    def _modify_asset(self, asset_name):
        """Modify an asset"""

        raise NotImplementedError

    def _prepare_fork_dependencies(self, asset_name):
        """Prepare prefix content with fork dependencies"""

        src_storage = self.storage_cls(prefix, asset_name)
        dst_storage = self.storage_cls(tmp_prefix, asset_name)
        dst_storage.save(*src_storage.load())

    @slow
    @skip_disconnected
    def test_remote_list(self):
        exit_code, output = self.call("list", "--remote")
        nose.tools.eq_(exit_code, 0, output)

    @slow
    @skip_disconnected
    def test_pull_one(self, obj=None):
        obj = obj or self.object_map["pull"]
        exit_code, output = self.call("pull", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)
        storage = self.storage_cls(tmp_prefix, obj)
        nose.tools.assert_true(storage.exists())
        return storage

    @slow
    @skip_disconnected
    def test_pull_all(self):
        exit_code, output = self.call("pull", prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)

    @slow
    @skip_disconnected
    def test_diff(self):
        obj = self.object_map["diff"]
        exit_code, output = self.call("pull", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)

        # quickly modify the user library by emptying it
        self._modify_asset(obj)

        exit_code, output = self.call("diff", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)

    @slow
    @skip_disconnected
    def test_status(self):
        self.test_diff()
        self.test_pull_one()
        exit_code, output = self.call("status", prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, output)

    @slow
    @skip_disconnected
    @skip_no_version
    def test_push_different_versions(self):
        asset_name = self.object_map["create"]
        self.create(asset_name)

        number_of_versions = 5
        version_pos = asset_name.rindex("/") + 1
        original_name = asset_name[:version_pos]
        original_version = int(asset_name[version_pos:])

        for i in range(number_of_versions):
            asset_name = original_name + str(original_version + i)
            exit_code, outputs = self.call("version", asset_name, prefix=tmp_prefix)
            nose.tools.eq_(exit_code, 0, outputs)

        asset_name = original_name + str(original_version + number_of_versions)

        exit_code, output = self.call("push", asset_name, prefix=tmp_prefix)

        nose.tools.eq_(exit_code, 0, output)

        config = MockConfig(self.live_server_url, user, token)
        with common.make_webapi(config) as webapi:
            asset_list = common.retrieve_remote_list(webapi, self.asset_type, ["name"])
            aoi_list = [
                asset for asset in asset_list if asset["name"].startswith(original_name)
            ]
            nose.tools.assert_equal(len(aoi_list), number_of_versions + 1)

    @slow
    @skip_disconnected
    @skip_no_fork
    def test_push_different_forks(self):
        asset_name = self.object_map["fork"]

        if "fork_from" in self.object_map:
            original = self.object_map["fork_from"]
        else:
            original = self.object_map["pull"]

        self._prepare_fork_dependencies(original)

        number_of_forks = 1
        if asset_name.count("/") != 4:
            version_pos = asset_name.rindex("/") + 1
            original_name = asset_name[: version_pos - 1]
        else:
            original_name = asset_name

        for i in range(number_of_forks):
            fork_name = "{}_{}".format(original_name, i)
            if asset_name.count("/") != 4:
                fork_name += "/1"

            exit_code, outputs = self.call(
                "fork", original, fork_name, prefix=tmp_prefix
            )
            nose.tools.eq_(exit_code, 0, outputs)
            asset_name = fork_name

        asset_name = "{}_{}".format(original_name, number_of_forks - 1)
        if asset_name.count("/") != 4:
            asset_name += "/1"

        exit_code, output = self.call("push", asset_name, prefix=tmp_prefix)

        nose.tools.eq_(exit_code, 0, output)

        config = MockConfig(self.live_server_url, user, token)
        with common.make_webapi(config) as webapi:
            asset_list = common.retrieve_remote_list(webapi, self.asset_type, ["name"])
            aoi_list = [
                asset for asset in asset_list if asset["name"].startswith(original_name)
            ]
            nose.tools.assert_equal(len(aoi_list), number_of_forks)

    @slow
    @skip_disconnected
    def test_push_and_delete(self):
        asset_name = self.object_map["push"]

        # now push the new object and then delete it remotely
        exit_code, output = self.call("push", asset_name)
        nose.tools.eq_(exit_code, 0, output)
        exit_code, output = self.call("rm", "--remote", asset_name)
        nose.tools.eq_(exit_code, 0, output)

    @slow
    @skip_disconnected
    def test_fail_push_invalid(self):
        asset_name = self.object_map["push_invalid"]

        with nose.tools.assert_raises(RuntimeError) as assertion:
            self.call("push", asset_name, user="errors")
        exc = assertion.exception
        text = exc.args[0]
        nose.tools.assert_true(text.startswith("Invalid "))

    @slow
    @skip_disconnected
    def test_fail_not_owner_push(self):
        asset_name = self.object_map["not_owner_push"]

        exit_code, output = self.call("push", asset_name)
        nose.tools.eq_(exit_code, 1, output)


class OnlineTestMixin:
    """Mixin for using Django's live server"""

    def setUp(self):
        """Cache a copy of the database to avoid the need to call make install
        on each tests.
        """

        if not disconnected:
            from django.conf import settings

            database_path = settings.DATABASES["default"]["TEST"]["NAME"]
            db_backup = os.path.join(prefix, "django_test_database.sqlite3")

            if not os.path.exists(db_backup):
                shutil.copyfile(database_path, db_backup)
            else:
                shutil.copyfile(db_backup, database_path)

    @classmethod
    def call(cls, *args, **kwargs):
        """Re-implement for platform URL handling"""

        kwargs["platform"] = cls.live_server_url

        return super().call(*args, **kwargs)


class OnlineTestCase(LiveServerTestCase, OnlineTestMixin, BaseTest):
    """Test case using django live server for test of remote functions"""

    def setUp(self):
        for base in OnlineTestCase.__bases__:
            base.setUp(self)


class OnlineAssetTestCase(LiveServerTestCase, OnlineTestMixin, AssetRemoteTest):
    """Test case using django live server for asset related remote tests"""

    def setUp(self):
        for base in OnlineTestCase.__bases__:
            base.setUp(self)
