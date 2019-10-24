Test Wrapper for Interactive Environments
=========================================

This document describes the usage of the `TestWrapper` submodule in the `test_framework` module of the functional test framework.

The TestWrapper submodule extends the `BitcoinTestFramework` functionality to external interactive environments for prototyping and educational purposes. Just like `BitcoinTestFramework`, the TestWrapper allows the user to:

* Manage regtest bitcoind subprocesses.
* Access RPC interfaces of these bitcoind instances.
* Log events to functional test logging utility.

The `TestWrapper` can be useful in interactive environments such as the Python3 command-line interpreter or [Jupyter](https://jupyter.org/) notebooks running a Python3 kernel, where is is necessary to extend the object lifetime of the underlying `BitcoinTestFramework` between user inputs.

## 1. Requirements

* Python3
* `bitcoind` built in the same bitcoin repository as the TestWrapper.

## 2. Importing TestWrapper from the Bitcoin Core repository

We can import the TestWrapper by adding the path of the Bitcoin Core `test_framework` module to the beginning of the PATH variable, and then importing the `TestWrapper` class from the `test_wrapper` sub-package.

```
>>> import sys
>>> sys.path.insert(0, "/path/to/bitcoin/test/functional/test_framework")
>>> from test_framework.test_wrapper import TestWrapper
```

The following TestWrapper methods manage the lifetime of the underlying bitcoind processes and logging utilities.

* `TestWrapper.setup()`
* `TestWrapper.shutdown()`

The TestWrapper inherits all BitcoinTestFramework members and methods, such as:
* `TestWrapper.nodes[index].rpc_method()`
* `TestWrapper.log.info("Custom log message")`

The following sections demonstrate how to initialize, run and shutdown a TestWrapper object in an interactive Python3 environment.

## 3. Initializing a TestWrapper object

```
>>> test = TestWrapper()
>>> test.setup("num_nodes"=2)
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Initializing test directory /path/to/bitcoin_func_test_XXXXXXX
```
The TestWrapper supports all functional test parameters of the Bitcoin TestFramework class. The full set of argument keywords which can be used to initialize the TestWrapper can be found [here](../test/functional/test_framework/test_wrapper.py).

**Note: Running multiple instances of TestWrapper is not allowed.**
This also ensures that logging remains consolidated in the same temporary folder. If you need more bitcoind nodes than set by default (1), simply increase the `num_nodes` parameter during setup.

```
>>> test2 = TestWrapper()
>>> test2.setup()
TestWrapper is already running!
```

## 4. Interacting with the TestWrapper

Unlike the BitcoinTestFramework class, the TestWrapper keeps the underlying Bitcoind subprocesses (nodes) and logging utilities running, until the user explicitly shuts down the TestWrapper object.

During the time between the `setup` and `shutdown` calls, all `bitcoind` node processes and BitcoinTestFramework convenience methods can be accessed interactively.

**Example: Mining a regtest chain**

By default, the TestWrapper nodes are initialized with a clean chain. This means that each node has at block height 0 after initialization of the TestWrapper.

```
>>> test.nodes[0].getblockchaininfo()["blocks"]
0
```

We now generate 101 regtest blocks, and send these to a wallet address owned by the first node.

```
>>> address = test.nodes[0].getnewaddress()
>>> test.nodes[0].generatetoaddress(101, address)
['2b98dd0044aae6f1cca7f88a0acf366a4bfe053c7f7b00da3c0d115f03d67efb', ...
```
Since the two nodes are each initialized to establish a connection to the other during `setup`, the second node will receive the newly mined blocks after they propagate.

```
>>> test.nodes[1].getblockchaininfo()["blocks"]
101
```
The block rewards of the first block are now spendable by the wallet of the first node.

```
>>> test.nodes[0].getbalance()
Decimal('50.00000000')
```

We can also log custom events to the logger.

```
>>> TestWrapper.log.info("Successfully mined regtest chain!")
```

**Note: Please also consider the functional test [readme](../test/functional/README.md), which provides an overview of the test-framework**. Modules such as [key.py](../test/functional/test_framework/key.py), [script.py](../test/functional/test_framework/script.py) and [messages.py](../test/functional/test_framework/messages.py) are especially useful in constructing objects which can be passed to the bitcoind nodes managed by a running TestWrapper object.

## 5. Shutting the TestWrapper down

Shutting down the TestWrapper will safely tear down all running bitcoind instances and remove all temporary data and logging directories.

```
>>> test.shutdown()
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Stopping nodes
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Cleaning up /path/to/bitcoin_func_test_XXXXXXX on exit
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Tests successful
```
To prevent the logs from being removed after a shutdown, simply set the `TestWrapper.options.nocleanup` member to `True`.
```
>>> test.options.nocleanup = True
>>> test.shutdown()
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Stopping nodes
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Not cleaning up dir /path/to/bitcoin_func_test_XXXXXXX on exit
20XX-XX-24TXX:XX:XX.XXXXXXX TestFramework (INFO): Tests successful
```

The following utility consolidates logs from the bitcoind nodes and the underlying BitcoinTestFramework:

* `/path/to/bitcoin/test/functional/combine_logs.py '/path/to/bitcoin_func_test_XXXXXXX'`