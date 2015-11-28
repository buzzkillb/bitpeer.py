# bitpeer.py - Bitcoin protocol and node

A pure Python3 bitcoin protocol and node implementation with pycoin.

You can support this project and other bitcoin-related projects by donating BTC to: **129k6fDTd66j1LMY5RAdFSQozeBe58nfxE**


## Features

- Bitcoin protocol data serialization / deserialization
- Customizable clients for single node connections
- Network support for different coins (bitcoin, namecoin, litecoin)
- Customizable node:
  - DNS seed bootstrap
  - Multiple connections
  - Mempool and transaction broadcast
  - Automatic syncronization with storage capabilities (the storage abstraction allows different storage types)
  - Storage types: shelve and memory
  - Peer reconnection handling



## Getting started

To install bitpeer.py, use `pip` (recommended method) or `easy_install`::

```bash
	pip3 install bitpeer.py
```

Or if pip is an alias of pip3:

```bash
	pip install bitpeer.py
```	

## Examples

Some samples are available in samples directory.

