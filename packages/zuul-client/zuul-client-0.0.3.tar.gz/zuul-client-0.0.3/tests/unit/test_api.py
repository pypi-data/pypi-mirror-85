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

from tests.unit import BaseTestCase
from tests.unit import FakeRequestResponse

from unittest.mock import MagicMock

from zuulclient.api import ZuulRESTClient
from zuulclient.api import ZuulRESTException


class TestApi(BaseTestCase):

    def test_client_init(self):
        """Test initialization of a client"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        self.assertEqual('https://fake.zuul/', client.url)
        self.assertEqual('https://fake.zuul/api/', client.base_url)
        self.assertEqual(False, client.session.verify)
        self.assertFalse('Authorization' in client.session.headers)
        client = ZuulRESTClient(url='https://fake.zuul')
        self.assertEqual('https://fake.zuul/', client.url)
        self.assertEqual('https://fake.zuul/api/', client.base_url)
        client = ZuulRESTClient(url='https://fake.zuul/with/path/')
        self.assertEqual('https://fake.zuul/with/path/', client.url)
        self.assertEqual('https://fake.zuul/with/path/api/', client.base_url)
        token = 'aiaiaiai'
        client = ZuulRESTClient(url='https://fake.zuul/', verify=True,
                                auth_token=token)
        self.assertEqual('https://fake.zuul/', client.url)
        self.assertEqual('https://fake.zuul/api/', client.base_url)
        self.assertEqual(True, client.session.verify)
        self.assertEqual('Bearer %s' % token,
                         client.session.headers.get('Authorization'))

    def _test_status_check(self, client, verb, func, *args, **kwargs):
        # validate request errors
        for error_code, regex in [(401, 'Unauthorized'),
                                  (403, 'Insufficient privileges'),
                                  (500, 'Unknown error')]:
            with self.assertRaisesRegex(ZuulRESTException,
                                        regex):
                req = FakeRequestResponse(error_code)
                if verb == 'post':
                    client.session.post = MagicMock(return_value=req)
                elif verb == 'get':
                    client.session.get = MagicMock(return_value=req)
                elif verb == 'delete':
                    client.session.delete = MagicMock(return_value=req)
                else:
                    raise Exception('Unknown HTTP "verb" %s' % verb)
                func(*args, **kwargs)

    def test_autohold(self):
        """Test autohold"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.autohold(
                'tenant', 'project', 'job', 1, None, 'reason', 1, 3600)

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'post', client.autohold,
            'tenant', 'project', 'job', 1, None, 'reason', 1, 3600)
        # test REST call
        req = FakeRequestResponse(200, True)
        client.session.post = MagicMock(return_value=req)
        ah = client.autohold(
            'tenant', 'project', 'job', 1, None, 'reason', 1, 3600)
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant/project/project/autohold',
            json={'reason': 'reason',
                  'count': 1,
                  'job': 'job',
                  'change': 1,
                  'ref': None,
                  'node_hold_expiration': 3600}
        )
        self.assertEqual(True, ah)

    def test_autohold_list(self):
        """Test autohold-list"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # test status checks
        self._test_status_check(
            client, 'get', client.autohold_list, 'tenant1')

        fakejson = [
            {'id': 123,
             'tenant': 'tenant1',
             'project': 'project1',
             'job': 'job1',
             'ref_filter': '.*',
             'max_count': 1,
             'current_count': 0,
             'reason': 'because',
             'nodes': ['node1', 'node2']}
        ]
        req = FakeRequestResponse(200, fakejson)
        client.session.get = MagicMock(return_value=req)
        ahl = client.autohold_list('tenant1')
        client.session.get.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/autohold')
        self.assertEqual(fakejson, ahl)

    def test_autohold_delete(self):
        """Test autohold-delete"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.autohold_delete(123, 'tenant1')

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'delete', client.autohold_delete,
            123, 'tenant1')

        # test REST call
        req = FakeRequestResponse(204)
        client.session.delete = MagicMock(return_value=req)
        ahd = client.autohold_delete(123, 'tenant1')
        client.session.delete.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/autohold/123'
        )
        self.assertEqual(True, ahd)

    def test_autohold_info(self):
        """Test autohold-info"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # test status checks
        self._test_status_check(
            client, 'get', client.autohold_info, 123, 'tenant1')

        fakejson = {
            'id': 123,
            'tenant': 'tenant1',
            'project': 'project1',
            'job': 'job1',
            'ref_filter': '.*',
            'max_count': 1,
            'current_count': 0,
            'reason': 'because',
            'nodes': ['node1', 'node2']
        }
        req = FakeRequestResponse(200, fakejson)
        client.session.get = MagicMock(return_value=req)
        ahl = client.autohold_info(tenant='tenant1', id=123)
        client.session.get.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/autohold/123')
        self.assertEqual(fakejson, ahl)

    def test_enqueue(self):
        """Test enqueue"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.enqueue('tenant1', 'check', 'project1', '1,1')

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'post', client.enqueue,
            'tenant1', 'check', 'project1', '1,1')

        # test REST call
        req = FakeRequestResponse(200, True)
        client.session.post = MagicMock(return_value=req)
        enq = client.enqueue('tenant1', 'check', 'project1', '1,1')
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/project/project1/enqueue',
            json={'change': '1,1',
                  'pipeline': 'check'}
        )
        self.assertEqual(True, enq)

    def test_enqueue_ref(self):
        """Test enqueue ref"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.enqueue_ref(
                'tenant1', 'check', 'project1', 'refs/heads/stable', '0', '0')

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'post', client.enqueue_ref,
            'tenant1', 'check', 'project1', 'refs/heads/stable', '0', '0')

        # test REST call
        req = FakeRequestResponse(200, True)
        client.session.post = MagicMock(return_value=req)
        enq_ref = client.enqueue_ref(
            'tenant1', 'check', 'project1', 'refs/heads/stable', '0', '0')
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/project/project1/enqueue',
            json={'ref': 'refs/heads/stable',
                  'oldrev': '0',
                  'newrev': '0',
                  'pipeline': 'check'}
        )
        self.assertEqual(True, enq_ref)

    def test_dequeue(self):
        """Test dequeue"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.dequeue('tenant1', 'check', 'project1', '1,1')

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'post', client.dequeue,
            'tenant1', 'check', 'project1', '1,1')

        # test conditions on ref and change
        with self.assertRaisesRegex(Exception, 'need change OR ref'):
            client.dequeue(
                'tenant1', 'check', 'project1', '1,1', 'refs/heads/stable')

        # test REST call
        req = FakeRequestResponse(200, True)
        client.session.post = MagicMock(return_value=req)
        deq = client.dequeue('tenant1', 'check', 'project1', change='1,1')
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/project/project1/dequeue',
            json={'change': '1,1',
                  'pipeline': 'check'}
        )
        self.assertEqual(True, deq)
        deq = client.dequeue(
            'tenant1', 'check', 'project1', ref='refs/heads/stable')
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/project/project1/dequeue',
            json={'ref': 'refs/heads/stable',
                  'pipeline': 'check'}
        )
        self.assertEqual(True, deq)

    def test_promote(self):
        """Test promote"""
        client = ZuulRESTClient(url='https://fake.zuul/')
        # token required
        with self.assertRaisesRegex(Exception, 'Auth Token required'):
            client.promote('tenant1', 'check', ['1,1', '2,1'])

        client = ZuulRESTClient(url='https://fake.zuul/',
                                auth_token='aiaiaiai')
        # test status checks
        self._test_status_check(
            client, 'post', client.promote,
            'tenant1', 'check', ['1,1', '2,1'])

        # test REST call
        req = FakeRequestResponse(200, True)
        client.session.post = MagicMock(return_value=req)
        prom = client.promote('tenant1', 'check', ['1,1', '2,1'])
        client.session.post.assert_called_with(
            'https://fake.zuul/api/tenant/tenant1/promote',
            json={'changes': ['1,1', '2,1'],
                  'pipeline': 'check'}
        )
        self.assertEqual(True, prom)

    def test_get_key(self):
        """Test getting a project's public key"""
        pubkey = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqiwMzHBCMu8Nsz6LH5Rr
E0hUJvuHhEfGF2S+1Y7ux7MtrE7zFsKK3JYZLbJuuQ62w5UsDtjRCQ8A4RhDVItZ
lPzEIvrz3SVnOX61cAkc3FOZq3GG+vXZHzbyZUgQV6eh7cvvxKACaI10WLNTKvD2
0Hb8comVtrFFG333x+9MxGQIKhoaBFGDcBnTsWlSVFxyWFxkvmlmFfglR2IV7c5O
YAKWItpRYDCfZMvptwsDm8fRnafW7ADvMsFhKgSkQX0YnXBwVDIjywYMiaz9zzo6
zOfxhwe8fGWxUtaQObpnJ7uAiXrFBEefXdTR+5Zh5j0mR1MB0W0VupK7ezVOQ6LW
JNKtggslhDR/iPUbRaMMILWUJtLAin4I6ZOP05wNrau0zoYp5iW3hY4AV4+i+oYL
Rcl2SNzPYnZXMTvfsZV1f4J6fu1vLivRS6ynYWjYZWucK0C2NpD0NTMfP5jcUU3K
uM10zi/xzsPZ42xkVQFv0OfznwJVBDVMovQFOCBVKFP52wT44mmcMcTZQjyMBJLR
psLogzoSlPF9MfewbYwStYcA1HroexMPifQ7unvdzdb0S9y/RiN2WJgt8meXGrWU
JHyRBXb/ZW7Hy5CEMEkPY8+DcwvyNfN6cdTni8htcDZA/N1hzhaslKoUYcdCS8dH
GuS6/ewjS+arA1Iyeg/IxmECAwEAAQ==
-----END PUBLIC KEY-----"""
        req = FakeRequestResponse(200, text=pubkey)
        client = ZuulRESTClient(url='https://fake.zuul/')
        client.session.get = MagicMock(return_value=req)
        key = client.get_key('tenant1', 'project1')
        self.assertEqual(pubkey, key)
