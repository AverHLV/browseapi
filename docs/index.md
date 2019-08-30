# Welcome to Browse API client documentation

This package is a Python client for eBay Browse API.
It is asynchronous and designed to send a large number of requests by
one function call.

For more information about this API visit official [documentation](https://developer.ebay.com/api-docs/buy/browse/overview.html).

## Installation
Install from PyPI by `pip install browseapi`

## Supported methods
Only these methods are now implemented (names changed to lowercase notation):

* [search](https://developer.ebay.com/api-docs/buy/browse/resources/item_summary/methods/search)
* [search_by_image](https://developer.ebay.com/api-docs/buy/browse/resources/search_by_image/methods/searchByImage)
* [get_item](https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItem)
* [get_item_by_legacy_id](https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItemByLegacyId)
* [get_items_by_item_group](https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItemsByItemGroup)
* [check_compatibility](https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/checkCompatibility)

## Quickstart
Create a BrowseAPI instance with your application id (app_id)
and application secret (cert_id) and start sending requests:

```python
from browseapi import BrowseAPI

app_id = '<your_app_id>'
cert_id = '<your_cert_id>'

api = BrowseAPI(app_id, cert_id)
responses = api.execute('search', [{'q': 'drone', 'limit': 50}, {'category_ids': 20863}])

# this will make 'search' request two times with parameters
# q=drone and limit=50 for the first time and
# category_ids=20863 for the second time

print(responses[0].itemSummaries[0])
```

All response fields have similar names and types as those mentioned
in official docs.

## Tests
For running tests put your `secret.json` file with fields `'eb_app_id'`
and `'eb_cert_id'` to the `browseapi/tests` directory,
then run a command from the parent browseapi directory:

`python -m unittest browseapi.tests.test_client`

You may get warnings like this:

```ResourceWarning: unclosed transport```

[Just ignore it](https://github.com/aio-libs/aiohttp/issues/1115).

## Requirements
* Python >= 3.5.3
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)