Browse API client
=================

|coverage| |build_status| |Documentation Status| |PyPI version|

This package is a Python client for eBay Browse API. It is asynchronous
and designed to send a large number of requests by one function call.

For more information about this API visit official
`documentation <https://developer.ebay.com/api-docs/buy/browse/overview.html>`__.

Installation
------------

Install from PyPI by ``pip install browseapi``

Supported methods
-----------------

Only these methods are now implemented (names changed to lowercase
notation):

-  `search <https://developer.ebay.com/api-docs/buy/browse/resources/item_summary/methods/search>`__
-  `search\_by\_image <https://developer.ebay.com/api-docs/buy/browse/resources/search_by_image/methods/searchByImage>`__
-  `get\_item <https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItem>`__
-  `get\_item\_by\_legacy\_id <https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItemByLegacyId>`__
-  `get\_items\_by\_item\_group <https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItemsByItemGroup>`__
-  `check\_compatibility <https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/checkCompatibility>`__

Quickstart
----------

Create a BrowseAPI instance with your application id (app\_id) and
application secret (cert\_id) and start sending requests:

.. code:: python

    from browseapi import BrowseAPI

    app_id = '<your_app_id>'
    cert_id = '<your_cert_id>'

    api = BrowseAPI(app_id, cert_id)
    responses = api.execute('search', [{'q': 'drone', 'limit': 50}, {'category_ids': 20863}])

    # this will make 'search' request two times with parameters
    # q=drone and limit=50 for the first time and
    # category_ids=20863 for the second time

    print(responses[0].itemSummaries[0])

All response fields have similar names and types as those mentioned in
official docs.

Tests
-----

For running tests put your ``secret.json`` file with fields
``'eb_app_id'`` and ``'eb_cert_id'`` to the ``browseapi/tests``
directory, then run a command from the parent browseapi directory:

``python -m unittest browseapi.tests.test_client``

You may get warnings like this:

``ResourceWarning: unclosed transport``

`Just ignore it. <https://github.com/aio-libs/aiohttp/issues/1115>`__

Requirements
------------

-  Python >= 3.5.3
-  `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`__

Documentation
-------------

Documentation built with `mkdocs <https://www.mkdocs.org/>`__.

`browseapi.readthedocs.io <https://browseapi.readthedocs.io/en/latest/>`__

.. |coverage| image:: https://img.shields.io/codecov/c/github/AverHLV/browseapi.svg
.. |build_status| image:: https://img.shields.io/gitlab/pipeline/AverHLV/browseapi/dev.svg
   :target: https://gitlab.com/AverHLV/browseapi/pipelines
.. |Documentation Status| image:: https://readthedocs.org/projects/browseapi/badge/?version=latest
   :target: https://browseapi.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/browseapi.svg
   :target: https://badge.fury.io/py/browseapi
