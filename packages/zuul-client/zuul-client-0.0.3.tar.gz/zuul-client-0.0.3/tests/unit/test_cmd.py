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


import os
import tempfile
from tests.unit import BaseTestCase
from tests.unit import FakeRequestResponse

from unittest.mock import MagicMock, patch

from zuulclient.cmd import ZuulClient


chunks = [
    'V+Q+8Gq7u7YFq6mbmM+vM/4Z7xCx+qy3YHilYYSN6apJeqSjU2xyJVuNYI680kwBEFFXt'
    'QmEqDlVIOG3yYTHgGbDq9gemMj2lMTzoTyftaE8yfK2uGZqWGwplh8PcGR67IhdH2UdDh'
    '8xD5ehKwX9j/ZBoSJ0LQCy4KBvpB6sccc8wywGvNaJZxte8StLHgBxUFFxmO96deNkhUS'
    '7xcpT+aU86uXYspJXmVrGOpy1/5QahIdi171rReRUToTO850M7JYuqcNrDm5rNiCdtwwT'
    'BnEJbdXa6ZMvyD9UB4roXi8VIWp3laueh8qoE2INiZtxjOrVIJkhm2HASqZ13ROyycv1z'
    '96Cr7UxH+LjrCm/yNfRMJpk00LZMwUOGUCueqH244e96UX5j6t+S/atkO+wVpG+9KDLhA'
    'BQ7pyiW/CDqK9Z1ZpQPlnFM5PX4Mu7LemYXjFH+7eSxp+N/T5V0MrVt41MPv0h6al9vAM'
    'sVJIQYeBNagYpjFSkEkMsJMXNAINJbfoT6vD4AS7pnCqiTaMgDC/6RQPwP9fklF+dJWq/'
    'Au3QSQb7YIrjKiz2A75xQLxWoz9T+Lz4qZkF00zh5nMPUrzJQRPaBwxH5I0wZG0bYi9AJ'
    '1tlAuq+vIhlY3iYlzVtPTiIOtF/6V+qPHnq1k6Tiv8YzJms1WyOuw106Bzl9XM=']


class TestCmd(BaseTestCase):

    def test_client_args_errors(self):
        """Test bad CLI arguments when instantiating client"""
        ZC = ZuulClient()
        with self.assertRaisesRegex(Exception,
                                    'Either specify --zuul-url or '
                                    'use a config file'):
            ZC._main(['--zuul-url', 'https://fake.zuul',
                      '--use-config', 'fakezuul',
                      'autohold',
                      '--tenant', 'tenant1', '--project', 'project1',
                      '--job', 'job1', '--change', '3',
                      '--reason', 'some reason',
                      '--node-hold-expiration', '3600'])

    def test_autohold(self):
        """Test autohold via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.post = MagicMock(
                return_value=FakeRequestResponse(200, True))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'autohold',
                 '--tenant', 'tenant1', '--project', 'project1',
                 '--job', 'job1', '--change', '3', '--reason', 'some reason',
                 '--node-hold-expiration', '3600'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/autohold',
                json={'reason': 'some reason',
                      'count': 1,
                      'job': 'job1',
                      'change': '3',
                      'ref': '',
                      'node_hold_expiration': 3600}
            )
            self.assertEqual(0, exit_code)

    def test_autohold_args_errors(self):
        """Test wrong arguments for autohold"""
        ZC = ZuulClient()
        with self.assertRaisesRegex(Exception,
                                    "Change and ref can't be both used "
                                    "for the same request"):
            ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'autohold',
                 '--tenant', 'tenant1', '--project', 'project1',
                 '--job', 'job1', '--change', '3', '--reason', 'some reason',
                 '--ref', '/refs/heads/master',
                 '--node-hold-expiration', '3600'])
        with self.assertRaisesRegex(Exception,
                                    "Error: change argument can not "
                                    "contain any ','"):
            ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'autohold',
                 '--tenant', 'tenant1', '--project', 'project1',
                 '--job', 'job1', '--change', '3,2', '--reason', 'some reason',
                 '--node-hold-expiration', '3600'])

    def test_parse_arguments(self):
        """ Test wrong arguments in parseArguments precheck"""
        ZC = ZuulClient()
        with self.assertRaisesRegex(Exception,
                                    "The old and new revisions must "
                                    "not be the same."):
            ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue-ref',
                 '--tenant', 'tenant1', '--project', 'project1',
                 '--pipeline', 'check',
                 '--ref', '/refs/heads/master',
                 '--oldrev', '1234', '--newrev', '1234'])
        with self.assertRaisesRegex(Exception,
                                    "The 'change' and 'ref' arguments are "
                                    "mutually exclusive."):
            ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'dequeue',
                 '--tenant', 'tenant1', '--project', 'project1',
                 '--pipeline', 'post', '--change', '3,2',
                 '--ref', '/refs/heads/master'])

    def test_autohold_delete(self):
        """Test autohold-delete via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.delete = MagicMock(
                return_value=FakeRequestResponse(204))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'autohold-delete',
                 '--tenant', 'tenant1', '1234'])
            session.delete.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/autohold/1234')
            self.assertEqual(0, exit_code)

    def test_autohold_info(self):
        """Test autohold-info via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.get = MagicMock(
                return_value=FakeRequestResponse(
                    200,
                    json={'id': 1234,
                          'tenant': 'tenant1',
                          'project': 'project1',
                          'job': 'job1',
                          'ref_filter': '.*',
                          'max_count': 1,
                          'current_count': 0,
                          'node_expiration': 0,
                          'expired': 0,
                          'reason': 'some_reason',
                          'nodes': ['node1', 'node2']}))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul', 'autohold-info',
                 '--tenant', 'tenant1', '1234'])
            session.get.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/autohold/1234')
            self.assertEqual(0, exit_code)
            session.get = MagicMock(
                return_value=FakeRequestResponse(404,
                                                 exception_msg='Not found'))
            with self.assertRaisesRegex(Exception, 'Not found'):
                ZC._main(
                    ['--zuul-url', 'https://fake.zuul', 'autohold-info',
                     '--tenant', 'tenant1', '1234'])

    def test_enqueue(self):
        """Test enqueue via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.post = MagicMock(
                return_value=FakeRequestResponse(200, True))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--change', '3,1',
                 '--project', 'project1'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/enqueue',
                json={'change': '3,1',
                      'pipeline': 'check'}
            )
            self.assertEqual(0, exit_code)

    def test_enqueue_ref(self):
        """Test enqueue-ref via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.post = MagicMock(
                return_value=FakeRequestResponse(200, True))
            # ensure default revs are set
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue-ref',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--ref', 'refs/heads/stable',
                 '--project', 'project1'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/enqueue',
                json={'ref': 'refs/heads/stable',
                      'pipeline': 'check',
                      'oldrev': '0000000000000000000000000000000000000000',
                      'newrev': '0000000000000000000000000000000000000000'}
            )
            self.assertEqual(0, exit_code)
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue-ref',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--ref', 'refs/heads/stable',
                 '--project', 'project1',
                 '--oldrev', 'ababababab'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/enqueue',
                json={'ref': 'refs/heads/stable',
                      'pipeline': 'check',
                      'oldrev': 'ababababab',
                      'newrev': '0000000000000000000000000000000000000000'}
            )
            self.assertEqual(0, exit_code)
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue-ref',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--ref', 'refs/heads/stable',
                 '--project', 'project1',
                 '--newrev', 'ababababab'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/enqueue',
                json={'ref': 'refs/heads/stable',
                      'pipeline': 'check',
                      'newrev': 'ababababab',
                      'oldrev': '0000000000000000000000000000000000000000'}
            )
            self.assertEqual(0, exit_code)
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'enqueue-ref',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--ref', 'refs/heads/stable',
                 '--project', 'project1',
                 '--oldrev', 'ababababab',
                 '--newrev', 'bababababa'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/enqueue',
                json={'ref': 'refs/heads/stable',
                      'pipeline': 'check',
                      'oldrev': 'ababababab',
                      'newrev': 'bababababa'}
            )
            self.assertEqual(0, exit_code)

    def test_dequeue(self):
        """Test dequeue via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.post = MagicMock(
                return_value=FakeRequestResponse(200, True))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'dequeue',
                 '--pipeline', 'tag',
                 '--tenant', 'tenant1', '--ref', 'refs/heads/stable',
                 '--project', 'project1'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/dequeue',
                json={'ref': 'refs/heads/stable',
                      'pipeline': 'tag'}
            )
            self.assertEqual(0, exit_code)
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'dequeue',
                 '--pipeline', 'check',
                 '--tenant', 'tenant1', '--change', '3,3',
                 '--project', 'project1'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/'
                'project/project1/dequeue',
                json={'change': '3,3',
                      'pipeline': 'check'}
            )
            self.assertEqual(0, exit_code)

    def test_promote(self):
        """Test promote via CLI"""
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.post = MagicMock(
                return_value=FakeRequestResponse(200, True))
            exit_code = ZC._main(
                ['--zuul-url', 'https://fake.zuul',
                 '--auth-token', 'aiaiaiai', 'promote',
                 '--pipeline', 'gate',
                 '--tenant', 'tenant1',
                 '--changes', '3,3', '4,1', '5,3'])
            session.post.assert_called_with(
                'https://fake.zuul/api/tenant/tenant1/promote',
                json={'changes': ['3,3', '4,1', '5,3'],
                      'pipeline': 'gate'}
            )
            self.assertEqual(0, exit_code)

    def test_encrypt(self):
        """Test encrypting a secret via CLI"""
        infile = tempfile.NamedTemporaryFile(delete=False)
        infile.write(b'my little secret')
        infile.close()
        outfile = tempfile.NamedTemporaryFile(delete=False)
        outfile.close()
        ZC = ZuulClient()
        with patch('requests.Session') as mock_sesh:
            session = mock_sesh.return_value
            session.get = MagicMock(
                return_value=FakeRequestResponse(200, text='aaa'))
            with patch('zuulclient.cmd.encrypt_with_openssl') as m_encrypt:
                m_encrypt.return_value = chunks
                exit_code = ZC._main(
                    ['--zuul-url', 'https://fake.zuul', '-v',
                     'encrypt', '--tenant', 'tenant1', '--project', 'project1',
                     '--infile', infile.name, '--outfile', outfile.name])
                self.assertEqual(0, exit_code)
                session.get.assert_called()
                m_encrypt.assert_called()
                secret = '''
- secret:
    name: <name>
    data:
      <fieldname>: !encrypted/pkcs1-oaep
        - V+Q+8Gq7u7YFq6mbmM+vM/4Z7xCx+qy3YHilYYSN6apJeqSjU2xyJVuNYI680kwBEFFXt
          QmEqDlVIOG3yYTHgGbDq9gemMj2lMTzoTyftaE8yfK2uGZqWGwplh8PcGR67IhdH2UdDh
          8xD5ehKwX9j/ZBoSJ0LQCy4KBvpB6sccc8wywGvNaJZxte8StLHgBxUFFxmO96deNkhUS
          7xcpT+aU86uXYspJXmVrGOpy1/5QahIdi171rReRUToTO850M7JYuqcNrDm5rNiCdtwwT
          BnEJbdXa6ZMvyD9UB4roXi8VIWp3laueh8qoE2INiZtxjOrVIJkhm2HASqZ13ROyycv1z
          96Cr7UxH+LjrCm/yNfRMJpk00LZMwUOGUCueqH244e96UX5j6t+S/atkO+wVpG+9KDLhA
          BQ7pyiW/CDqK9Z1ZpQPlnFM5PX4Mu7LemYXjFH+7eSxp+N/T5V0MrVt41MPv0h6al9vAM
          sVJIQYeBNagYpjFSkEkMsJMXNAINJbfoT6vD4AS7pnCqiTaMgDC/6RQPwP9fklF+dJWq/
          Au3QSQb7YIrjKiz2A75xQLxWoz9T+Lz4qZkF00zh5nMPUrzJQRPaBwxH5I0wZG0bYi9AJ
          1tlAuq+vIhlY3iYlzVtPTiIOtF/6V+qPHnq1k6Tiv8YzJms1WyOuw106Bzl9XM=
'''
                with open(outfile.name) as f:
                    self.assertEqual(secret, f.read())
        os.unlink(infile.name)
        os.unlink(outfile.name)
