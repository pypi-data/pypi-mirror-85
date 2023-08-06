# Copyright 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import logging
import testtools


class BaseTestCase(testtools.TestCase):
    log = logging.getLogger("zuulclient.test")

    def setUp(self):
        super(BaseTestCase, self).setUp()


class FakeRequestResponse(object):
    def __init__(self, status_code=None, json=None, text=None,
                 exception_msg=None):
        self._json = json
        self.text = text
        self.status_code = status_code
        self.exception_msg = exception_msg or 'Error'

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(self.exception_msg)
