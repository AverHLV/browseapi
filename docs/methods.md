## BrowseAPI
Client class.

* app_id: eBay developer client id
* cert_id: ebay developer client secret
* marketplace_id: eBay marketplace identifier
* partner_id: eBay Network Partner ID
* reference_id: any value to identify item or purchase order can be used only with partner_id
* country: country code, needed for the calculated shipping information
* zip_code: used only with a country for getting shipping information

Only app_id and cert_id always required. Marketplace id set to 'US'
by default. If you are a user of eBay Network Partner, pass your
ID to partner_id. For better calculation of shipping information,
you may want to specify your country and zip code.

Supported methods and available marketplaces can be shown by client attributes:
```python
from browseapi import BrowseAPI

print(BrowseAPI.supported_methods)
print(BrowseAPI.marketplaces)
```

## execute
Public method for running API requests.

* method: Browse API method name in lowercase
* params: list of params dictionaries for every request
* pass_errors: exceptions in the tasks are treated the same as successful results, bool
* return: list of responses

Pass_errors set to False by default.