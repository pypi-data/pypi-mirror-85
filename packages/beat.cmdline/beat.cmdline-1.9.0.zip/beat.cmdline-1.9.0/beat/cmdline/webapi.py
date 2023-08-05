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


from urllib.parse import urlparse

import requests
import simplejson as json


class WebAPIError(RuntimeError):
    def __init__(self, cmd, url, answer):
        message = "{cmd} error {status}: {url}\nError:{text}".format(
            cmd=cmd, status=answer.status_code, url=url, text=answer.text
        )
        super().__init__(message)


class WebAPI(object):
    """Central class for all remote service related calls"""

    API_VERSION = "v1"
    API_PATH = "/api/{}".format(API_VERSION)

    def __init__(self, platform, user, token=None):
        self.platform = platform
        self.parsed = urlparse(self.platform)
        self.user = "**anonymous**" if token is None else user
        self.token = token

    def is_anonymous(self):
        return self.token is None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return

    def _make_authorization(self):
        return "Token {}".format(self.token)

    def _make_headers(self):
        if self.token is None:
            return None

        return {
            "Authorization": self._make_authorization(),
            "Content-Type": "application/json",
        }

    def __build_url(self, path):
        platform = self.parsed.geturl()
        if platform.endswith("/"):
            platform = platform[:-1]

        if path.startswith("/"):
            path = path[1:]

        url = "{platform}/{path}".format(platform=platform, path=path)
        return url

    def get(self, path):
        url = self.__build_url(path)
        answer = requests.get(url, headers=self._make_headers())

        # if answer.status_code < 200 or answer.status_code >= 300:
        if answer.status_code not in [200, 204]:
            raise WebAPIError("GET", url, answer)

        return answer.json()

    def post(self, path, data=None):
        url = self.__build_url(path)
        answer = requests.post(url, json=data, headers=self._make_headers())

        if answer.status_code not in [200, 201]:
            raise WebAPIError("POST", url, answer)

        try:
            return answer.json()
        except json.JSONDecodeError:
            return answer.text

    def upload(self, path, data):
        url = self.__build_url(path)
        answer = requests.post(
            url, files=data, headers={"Authorization": self._make_authorization()}
        )

        if answer.status_code not in [200, 201, 204]:
            raise WebAPIError("POST", url, answer)

        try:
            return answer.json()
        except json.JSONDecodeError:
            return answer.text

    def download(self, path):
        url = self.__build_url(path)
        answer = requests.get(
            url, headers={"Authorization": self._make_authorization()}
        )

        if answer.status_code not in [200, 204]:
            raise WebAPIError("GET", url, answer)

        return answer.content

    def put(self, path, data=None):
        url = self.__build_url(path)
        answer = requests.put(url, json=data, headers=self._make_headers())

        if answer.status_code not in [200, 204]:
            raise WebAPIError("PUT", url, answer)

        try:
            return answer.json()
        except json.JSONDecodeError:
            return answer.text

    def delete(self, path):
        url = self.__build_url(path)
        answer = requests.delete(url, headers=self._make_headers())

        # Should respond a 204 status and an empty body
        if answer.status_code not in [200, 204]:
            raise WebAPIError("DELETE", url, answer)
