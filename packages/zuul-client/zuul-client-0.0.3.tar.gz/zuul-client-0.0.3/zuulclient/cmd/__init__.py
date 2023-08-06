# Copyright 2020 Red Hat, inc
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

import argparse
import configparser
import logging
import os
import prettytable
import sys
import tempfile
import textwrap
import time

from zuulclient.api import ZuulRESTClient
from zuulclient.utils import get_default
from zuulclient.utils import encrypt_with_openssl


class ZuulClient():
    app_name = 'zuul-client'
    app_description = 'Zuul User CLI'
    log = logging.getLogger("zuul-client")
    default_config_locations = ['~/.zuul.conf']

    def __init__(self):
        self.args = None
        self.config = None

    def _get_version(self):
        from zuulclient.version import version_info
        return "Zuul-client version: %s" % version_info.release_string()

    def createParser(self):
        parser = argparse.ArgumentParser(
            description=self.app_description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-c', dest='config',
                            help='specify the config file')
        parser.add_argument('--version', dest='version', action='version',
                            version=self._get_version(),
                            help='show zuul version')
        parser.add_argument('-v', dest='verbose', action='store_true',
                            help='verbose output')
        parser.add_argument('--auth-token', dest='auth_token',
                            required=False,
                            default=None,
                            help='Authentication Token, required by '
                                 'admin commands')
        parser.add_argument('--zuul-url', dest='zuul_url',
                            required=False,
                            default=None,
                            help='Zuul base URL, needed if using the '
                                 'client without a configuration file')
        parser.add_argument('--use-config', dest='zuul_config',
                            required=False,
                            default=None,
                            help='A predefined configuration in .zuul.conf')
        parser.add_argument('--insecure', dest='verify_ssl',
                            required=False,
                            action='store_false',
                            help='Do not verify SSL connection to Zuul '
                                 '(Defaults to False)')
        self.createCommandParsers(parser)
        return parser

    def createCommandParsers(self, parser):
        subparsers = parser.add_subparsers(title='commands',
                                           description='valid commands',
                                           help='additional help')
        self.add_autohold_subparser(subparsers)
        self.add_autohold_delete_subparser(subparsers)
        self.add_autohold_info_subparser(subparsers)
        self.add_autohold_list_subparser(subparsers)
        self.add_enqueue_subparser(subparsers)
        self.add_enqueue_ref_subparser(subparsers)
        self.add_dequeue_subparser(subparsers)
        self.add_promote_subparser(subparsers)
        self.add_encrypt_subparser(subparsers)
        return subparsers

    def parseArguments(self, args=None):
        parser = self.createParser()
        self.args = parser.parse_args(args)
        if not getattr(self.args, 'func', None):
            parser.print_help()
            sys.exit(1)
        if self.args.func == self.enqueue_ref:
            # if oldrev or newrev is set, ensure they're not the same
            if (self.args.oldrev is not None) or \
               (self.args.newrev is not None):
                if self.args.oldrev == self.args.newrev:
                    raise Exception(
                        "The old and new revisions must not be the same.")
            # if they're not set, we pad them out to zero
            if self.args.oldrev is None:
                self.args.oldrev = '0000000000000000000000000000000000000000'
            if self.args.newrev is None:
                self.args.newrev = '0000000000000000000000000000000000000000'
        if self.args.func == self.dequeue:
            if self.args.change is None and self.args.ref is None:
                raise Exception("Change or ref needed.")
            if self.args.change is not None and self.args.ref is not None:
                raise Exception(
                    "The 'change' and 'ref' arguments are mutually exclusive.")

    def readConfig(self):
        safe_env = {
            k: v for k, v in os.environ.items()
            if k.startswith('ZUUL_')
        }
        self.config = configparser.ConfigParser(safe_env)
        if self.args.config:
            locations = [self.args.config]
        else:
            locations = self.default_config_locations
        for fp in locations:
            if os.path.exists(os.path.expanduser(fp)):
                self.config.read(os.path.expanduser(fp))
                return
        raise Exception("Unable to locate config file in %s" % locations)

    def setup_logging(self):
        """Client logging does not rely on conf file"""
        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)

    def _main(self, args=None):
        self.parseArguments(args)
        if not self.args.zuul_url:
            self.readConfig()
        self.setup_logging()
        # TODO make func return specific return codes
        if self.args.func():
            return 0
        else:
            return 1

    def main(self):
        try:
            sys.exit(self._main())
        except Exception as e:
            self.log.error(e)
            sys.exit(1)

    def add_autohold_subparser(self, subparsers):
        cmd_autohold = subparsers.add_parser(
            'autohold', help='hold nodes for failed job')
        cmd_autohold.add_argument('--tenant', help='tenant name',
                                  required=True)
        cmd_autohold.add_argument('--project', help='project name',
                                  required=True)
        cmd_autohold.add_argument('--job', help='job name',
                                  required=True)
        cmd_autohold.add_argument('--change',
                                  help='specific change to hold nodes for',
                                  required=False, default='')
        cmd_autohold.add_argument('--ref', help='git ref to hold nodes for',
                                  required=False, default='')
        cmd_autohold.add_argument('--reason', help='reason for the hold',
                                  required=True)
        cmd_autohold.add_argument('--count',
                                  help='number of job runs (default: 1)',
                                  required=False, type=int, default=1)
        cmd_autohold.add_argument(
            '--node-hold-expiration',
            help=('how long in seconds should the node set be in HOLD status '
                  '(default: scheduler\'s default_hold_expiration value)'),
            required=False, type=int)
        cmd_autohold.set_defaults(func=self.autohold)

    def autohold(self):
        if self.args.change and self.args.ref:
            raise Exception(
                "Change and ref can't be both used for the same request")
        if "," in self.args.change:
            raise Exception("Error: change argument can not contain any ','")

        node_hold_expiration = self.args.node_hold_expiration
        client = self.get_client()
        r = client.autohold(
            tenant=self.args.tenant,
            project=self.args.project,
            job=self.args.job,
            change=self.args.change,
            ref=self.args.ref,
            reason=self.args.reason,
            count=self.args.count,
            node_hold_expiration=node_hold_expiration)
        return r

    def add_autohold_delete_subparser(self, subparsers):
        cmd_autohold_delete = subparsers.add_parser(
            'autohold-delete', help='delete autohold request')
        cmd_autohold_delete.set_defaults(func=self.autohold_delete)
        cmd_autohold_delete.add_argument('--tenant', help='tenant name',
                                         required=True, default=None)
        cmd_autohold_delete.add_argument('id', metavar='REQUEST_ID',
                                         help='the hold request ID')

    def autohold_delete(self):
        client = self.get_client()
        return client.autohold_delete(self.args.id, self.args.tenant)

    def add_autohold_info_subparser(self, subparsers):
        cmd_autohold_info = subparsers.add_parser(
            'autohold-info', help='retrieve autohold request detailed info')
        cmd_autohold_info.set_defaults(func=self.autohold_info)
        cmd_autohold_info.add_argument('--tenant', help='tenant name',
                                       required=True, default=None)
        cmd_autohold_info.add_argument('id', metavar='REQUEST_ID',
                                       help='the hold request ID')

    def autohold_info(self):
        client = self.get_client()
        request = client.autohold_info(self.args.id, self.args.tenant)

        if not request:
            print("Autohold request not found")
            return False

        print("ID: %s" % request['id'])
        print("Tenant: %s" % request['tenant'])
        print("Project: %s" % request['project'])
        print("Job: %s" % request['job'])
        print("Ref Filter: %s" % request['ref_filter'])
        print("Max Count: %s" % request['max_count'])
        print("Current Count: %s" % request['current_count'])
        print("Node Expiration: %s" % request['node_expiration'])
        print("Request Expiration: %s" % time.ctime(request['expired']))
        print("Reason: %s" % request['reason'])
        print("Held Nodes: %s" % request['nodes'])

        return True

    def add_autohold_list_subparser(self, subparsers):
        cmd_autohold_list = subparsers.add_parser(
            'autohold-list', help='list autohold requests')
        cmd_autohold_list.add_argument('--tenant', help='tenant name',
                                       required=True)
        cmd_autohold_list.set_defaults(func=self.autohold_list)

    def autohold_list(self):
        client = self.get_client()
        autohold_requests = client.autohold_list(tenant=self.args.tenant)

        if not autohold_requests:
            print("No autohold requests found")
            return True

        table = prettytable.PrettyTable(
            field_names=[
                'ID', 'Tenant', 'Project', 'Job', 'Ref Filter',
                'Max Count', 'Reason'
            ])

        for request in autohold_requests:
            table.add_row([
                request['id'],
                request['tenant'],
                request['project'],
                request['job'],
                request['ref_filter'],
                request['max_count'],
                request['reason'],
            ])

        print(table)
        return True

    def add_enqueue_subparser(self, subparsers):
        cmd_enqueue = subparsers.add_parser('enqueue', help='enqueue a change')
        cmd_enqueue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_enqueue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_enqueue.add_argument('--project', help='project name',
                                 required=True)
        cmd_enqueue.add_argument('--change', help='change id',
                                 required=True)
        cmd_enqueue.set_defaults(func=self.enqueue)

    def enqueue(self):
        client = self.get_client()
        r = client.enqueue(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            change=self.args.change)
        return r

    def add_enqueue_ref_subparser(self, subparsers):
        cmd_enqueue = subparsers.add_parser(
            'enqueue-ref', help='enqueue a ref',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
            Submit a trigger event

            Directly enqueue a trigger event.  This is usually used
            to manually "replay" a trigger received from an external
            source such as gerrit.'''))
        cmd_enqueue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_enqueue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_enqueue.add_argument('--project', help='project name',
                                 required=True)
        cmd_enqueue.add_argument('--ref', help='ref name',
                                 required=True)
        cmd_enqueue.add_argument(
            '--oldrev', help='old revision', default=None)
        cmd_enqueue.add_argument(
            '--newrev', help='new revision', default=None)
        cmd_enqueue.set_defaults(func=self.enqueue_ref)

    def enqueue_ref(self):
        client = self.get_client()
        r = client.enqueue_ref(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            ref=self.args.ref,
            oldrev=self.args.oldrev,
            newrev=self.args.newrev)
        return r

    def add_dequeue_subparser(self, subparsers):
        cmd_dequeue = subparsers.add_parser('dequeue',
                                            help='dequeue a buildset by its '
                                                 'change or ref')
        cmd_dequeue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_dequeue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_dequeue.add_argument('--project', help='project name',
                                 required=True)
        cmd_dequeue.add_argument('--change', help='change id',
                                 default=None)
        cmd_dequeue.add_argument('--ref', help='ref name',
                                 default=None)
        cmd_dequeue.set_defaults(func=self.dequeue)

    def dequeue(self):
        client = self.get_client()
        r = client.dequeue(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            change=self.args.change,
            ref=self.args.ref)
        return r

    def add_promote_subparser(self, subparsers):
        cmd_promote = subparsers.add_parser('promote',
                                            help='promote one or more changes')
        cmd_promote.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_promote.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_promote.add_argument('--changes', help='change ids',
                                 required=True, nargs='+')
        cmd_promote.set_defaults(func=self.promote)

    def promote(self):
        client = self.get_client()
        r = client.promote(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            change_ids=self.args.changes)
        return r

    def get_client(self):
        if self.args.zuul_url and self.args.zuul_config:
            raise Exception('Either specify --zuul-url or use a config file')
        if self.args.zuul_url:
            self.log.debug(
                'Using Zuul URL provided as argument to instantiate client')
            client = ZuulRESTClient(self.args.zuul_url,
                                    self.args.verify_ssl,
                                    self.args.auth_token)
            return client
        conf_sections = self.config.sections()
        if len(conf_sections) == 1 and self.args.zuul_config is None:
            zuul_conf = conf_sections[0]
            self.log.debug(
                'Using section "%s" found in '
                'config to instantiate client' % zuul_conf)
        elif self.args.zuul_config and self.args.zuul_config in conf_sections:
            zuul_conf = self.args.zuul_config
        else:
            raise Exception('Unable to find a way to connect to Zuul, '
                            'provide the "--zuul-url" argument or set up a '
                            '.zuul.conf file.')
        server = get_default(self.config,
                             zuul_conf, 'url', None)
        verify = get_default(self.config, zuul_conf,
                             'verify_ssl',
                             self.args.verify_ssl)
        # Allow token override by CLI argument
        auth_token = self.args.auth_token or get_default(self.config,
                                                         zuul_conf,
                                                         'auth_token',
                                                         None)
        if server is None:
            raise Exception('Missing "url" configuration value')
        client = ZuulRESTClient(server, verify, auth_token)
        return client

    def add_encrypt_subparser(self, subparsers):
        cmd_encrypt = subparsers.add_parser(
            'encrypt', help='Encrypt a secret to be used in a project\'s jobs')
        cmd_encrypt.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_encrypt.add_argument('--project', help='project name',
                                 required=True)
        cmd_encrypt.add_argument('--no-strip', action='store_true',
                                 help='Do not strip whitespace from beginning '
                                      'or end of input.',
                                 default=False)
        cmd_encrypt.add_argument('--secret-name',
                                 default=None,
                                 help='How the secret should be named. If not '
                                      'supplied, a placeholder will be used.')
        cmd_encrypt.add_argument('--field-name',
                                 default=None,
                                 help='How the name of the secret variable. '
                                      'If not supplied, a placeholder will be '
                                      'used.')
        cmd_encrypt.add_argument('--infile',
                                 default=None,
                                 help='A filename whose contents will be '
                                      'encrypted. If not supplied, the value '
                                      'will be read from standard input.\n'
                                      'If entering the secret manually, press '
                                      'Ctrl+d when finished to process the '
                                      'secret.')
        cmd_encrypt.add_argument('--outfile',
                                 default=None,
                                 help='A filename to which the encrypted '
                                      'value will be written.  If not '
                                      'supplied, the value will be written '
                                      'to standard output.')
        cmd_encrypt.set_defaults(func=self.encrypt)

    def encrypt(self):
        if self.args.infile:
            try:
                with open(self.args.infile) as f:
                    plaintext = f.read()
            except FileNotFoundError:
                raise Exception('File "%s" not found' % self.args.infile)
            except PermissionError:
                raise Exception(
                    'Insufficient rights to open %s' % self.args.infile)
        else:
            plaintext = sys.stdin.read()
        if not self.args.no_strip:
            plaintext = plaintext.strip()
        pubkey_file = tempfile.NamedTemporaryFile(delete=False)
        self.log.debug('Creating temporary key file %s' % pubkey_file.name)
        client = self.get_client()
        try:
            key = client.get_key(self.args.tenant, self.args.project)
            pubkey_file.write(str.encode(key))
            pubkey_file.close()

            self.log.debug('Calling openssl')
            ciphertext_chunks = encrypt_with_openssl(pubkey_file.name,
                                                     plaintext,
                                                     self.log)
            output = textwrap.dedent(
                '''
                - secret:
                    name: {}
                    data:
                      {}: !encrypted/pkcs1-oaep
                '''.format(self.args.secret_name or '<name>',
                           self.args.field_name or '<fieldname>'))

            twrap = textwrap.TextWrapper(width=79,
                                         initial_indent=' ' * 8,
                                         subsequent_indent=' ' * 10)
            for chunk in ciphertext_chunks:
                chunk = twrap.fill('- ' + chunk)
                output += chunk + '\n'

            if self.args.outfile:
                with open(self.args.outfile, "w") as f:
                    f.write(output)
            else:
                print(output)
            return_code = True
        except Exception as e:
            self.log.exception(e)
            return_code = False
        finally:
            self.log.debug('Deleting temporary key file %s' % pubkey_file.name)
            os.unlink(pubkey_file.name)
        return return_code


def main():
    ZuulClient().main()
