#!/usr/bin/env python3
# Copyright (c) 2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import argparse
from os import getpid
from os.path import abspath, join

from test_framework.test_framework import BitcoinTestFramework

class TestWrapper:
    """Wrapper Class for BitcoinTestFramework.

    The TestWrapper class extends the BitcoinTestFramework
    rpc & daemon process management functionality to external
    python environments.

    It is a singleton class, which ensures that users only
    start a single TestWrapper at a time."""

    class __TestWrapper(BitcoinTestFramework):
        def set_test_params(self):
            pass

        def run_test(self):
            pass

        def setup(self, **kwargs):
            if self.running:
                print("TestWrapper is already running!")
                return

            self.setup_clean_chain = kwargs.get('setup_clean_chain',True)
            self.num_nodes = kwargs.get('num_nodes', 1)
            self.network_thread = kwargs.get('network_thread', None)
            self.rpc_timeout = kwargs.get('rpc_timeout', 60)
            self.supports_cli = kwargs.get('supports_cli', False)
            self.bind_to_localhost_only = kwargs.get('bind_to_localhost_only', True)

            self.options = argparse.Namespace
            self.options.nocleanup = kwargs.get('nocleanup', False)
            self.options.noshutdown = kwargs.get('noshutdown', False)
            self.options.cachedir = kwargs.get('cachedir', abspath(join(__file__ ,"../../../..") + "/test/cache"))
            self.options.tmpdir = kwargs.get('tmpdir', None)
            self.options.loglevel = kwargs.get('loglevel', 'INFO')
            self.options.trace_rpc = kwargs.get('trace_rpc', False)
            self.options.port_seed = kwargs.get('port_seed', getpid())
            self.options.coveragedir = kwargs.get('coveragedir', None)
            self.options.configfile = kwargs.get('configfile', abspath(join(__file__ ,"../../../..") + "/test/config.ini"))
            self.options.pdbonfailure = kwargs.get('pdbonfailure', False)
            self.options.usecli = kwargs.get('usecli', False)
            self.options.perf = kwargs.get('perf', False)
            self.options.randomseed = kwargs.get('randomseed', None)

            self.options.bitcoind = kwargs.get('bitcoind', abspath(join(__file__ ,"../../../..") +  "/src/bitcoind"))
            self.options.bitcoincli = kwargs.get('bitcoincli', None)

            super().setup()
            self.running = True

        def shutdown(self):
            if not self.running:
                print("TestWrapper is not running!")
            else:
                super().shutdown()
                self.running = False

    instance = None

    def __new__(cls):
        # Implementation enforces singleton pattern,
        # and will return existing instance if available.
        if not TestWrapper.instance:
            TestWrapper.instance = TestWrapper.__TestWrapper()
            TestWrapper.instance.running = False
        return TestWrapper.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
