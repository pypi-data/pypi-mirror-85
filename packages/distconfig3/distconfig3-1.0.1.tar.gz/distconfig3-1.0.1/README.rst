.. image:: https://travis-ci.com/alexferl/distconfig.svg?branch=master
  :target: https://travis-ci.com/alexferl/distconfig

.. image:: https://readthedocs.org/projects/distconfig/badge/?version=latest
  :target: https://readthedocs.org/projects/distconfig/?badge=latest
  :alt: Documentation Status

distconfig3
===========

This is a fork of `distconfig <https://github.com/deliveryhero/distconfig>`_ removing Python 2.7 support as well as six
and ujson dependencies.

Library to manage distributed configuration using either `ZooKeeper <https://zookeeper.apache.org/>`_ or
`Etcd <https://github.com/coreos/etcd>`_ or `Consul <http://www.consul.io/>`_.

Rational
--------

When you have to manage configuration of a given services that are distributed across nodes, you may want
to consider using either one of the distributed configuration managers e.g. zookeeper, etcd, consul ..., this
library goal is to give developers an easy access to configuration stored in the previous backends.

Installation:
-------------

To use **ZooKeeper** as backend you should install ``distconfig3`` using ::

    $ pip install distconfig3[zookeeper]

with **etcd**::

    $ pip install distconfig3[etcd]

with **consul**::

    $ pip install distconfig3[consul]

Usage:
------

Example using zookeeper as a backend ::

    from kazoo import client

    from distconfig import Proxy

    client = client.KazooClient()
    # The user must call ``KazooClient.start()`` before using this particular
    # backend
    client.start()

    proxy = Proxy.configure(
        'distconfig.backends.zookeeper.ZooKeeperBackend',
        client=client,
    )

    # config is a read only mapping-like object.
    config = proxy.get_config('/distconfig/service_name/config')

    print(config['key'])

    # Getting nested values works by supplying key seperated by '/' char.
    print(config['key/inner'])

    # You can assert key value type by using typed get function e.g.
    # get_int, get_float, get_unicode, get_bytes ... .
    print(config.get_int('key/inner/int_key'))

    # Getting a inner config.
    print(config.get_config('key/inner/dict_key'))


Development:
------------

Start by installing dependencies ::

    $ pip install -r requirements/dev.txt

To run unit test use tox ::

    $ tox

To run integration test, we recommend you to install `docker <https://www.docker.com/>`_ and then run ::

    $ ./run-tests.sh

The above script will setup docker container for each of the backend
and run the integration tests on them.


TODO:
-----

- Add file as a backend (use https://pypi.python.org/pypi/watchdog)
