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

            # Num_nodes parameter must be set
            # by BitcoinTestFramework child class.
            self.num_nodes = kwargs.get('num_nodes', 1)
            kwargs.pop('num_nodes', None)

            # User parameters override default values.
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                elif hasattr(self.options, key):
                    setattr(self.options, key, value)
                else:
                    raise KeyError(key + " not a valid parameter key")

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
