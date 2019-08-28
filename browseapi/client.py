import asyncio

from aiohttp import client_exceptions, ClientSession, ClientTimeout

from base64 import b64encode
from urllib.parse import urlencode

from . import exceptions
from .containers import BrowseAPIResponse

TIMEOUT = 10


class BrowseAPI(object):
    """ Client class for eBay Browse API """

    _uri = 'https://api.ebay.com/buy/browse/v1'
    _auth_uri = 'https://api.ebay.com/identity/v1/oauth2/token'
    _search_uri = _uri + '/item_summary/search?'
    _search_by_image_uri = _uri + '/item_summary/search_by_image?'

    # Client Credential Grant Type

    _credentials_grant_type = 'client_credentials'
    _scope_public_data = 'https://api.ebay.com/oauth/api_scope'

    supported_methods = (
        'search',
        'search_by_image'
    )

    marketplaces = (
        'EBAY_US',
        'EBAY_AT',
        'EBAY_AU',
        'EBAY_BE',
        'EBAY_CA',
        'EBAY_CH',
        'EBAY_DE',
        'EBAY_ES',
        'EBAY_FR',
        'EBAY_GB',
        'EBAY_HK',
        'EBAY_IE',
        'EBAY_IN',
        'EBAY_IT',
        'EBAY_MY',
        'EBAY_NL',
        'EBAY_PH',
        'EBAY_PL',
        'EBAY_SG',
        'EBAY_TH',
        'EBAY_TW',
        'EBAY_VN',
        'EBAY_MOTORS_US'
    )

    def __init__(self,
                 app_id: str,
                 cert_id: str,
                 marketplace_id='EBAY_US',
                 partner_id=None,
                 reference_id=None,
                 country=None,
                 zip_code=None):
        """
        Client initialization

        :param app_id: eBay developer client id
        :param cert_id: ebay developer client secret
        :param marketplace_id: eBay marketplace identifier
        :param partner_id: eBay Network Partner ID
        :param reference_id: any value to identify item or purchase order can be used only with partner_id
        :param country: country code, needed for the calculated shipping information
        :param zip_code: used only with a country for getting shipping information
        """

        if marketplace_id not in self.marketplaces:
            raise exceptions.BrowseAPIParamError('marketplace_id')

        if reference_id is not None and partner_id is None:
            raise exceptions.BrowseAPIParamError('partner_id. For reference_id partner_id is required')

        if (country is None and zip_code is not None) or (zip_code is None and country is not None):
            raise exceptions.BrowseAPIParamError('country or zip_code. These parameters can only both None or filled')

        self._session = None
        self._oauth_session = None
        self._possible_requests = None

        self._responses = []
        self._timeout = ClientTimeout(total=TIMEOUT)

        self._oauth_headers = {
            'Authorization': 'Basic {}'.format(str(b64encode((app_id + ':' + cert_id).encode('utf8')))[2:-1]),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        self._headers = {
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'Authorization': 'Bearer {}',
            'X-EBAY-C-MARKETPLACE-ID': marketplace_id
        }

        # check data and form ctx header

        ctx_header = ''

        if partner_id is not None:
            ctx_header = 'affiliateCampaignId=' + str(partner_id)

            if reference_id is not None:
                ctx_header += ',affiliateReferenceId=' + str(reference_id)

        if country is not None:
            if len(ctx_header):
                ctx_header += ','

            ctx_header += self._encode_params({'contextualLocation': 'country={0},zip={1}'.format(country, zip_code)})

        if len(ctx_header):
            self._headers['X-EBAY-C-ENDUSERCTX'] = ctx_header

    async def _create_session(self):
        """ Create requests session """

        if self._session is not None:
            await self._session.close()

        self._session = ClientSession(headers=self._headers, timeout=self._timeout)

    async def _request(self, uri: str, request_type=0, data=None, oauth=False) -> dict:
        """
        Make async request

        :param uri: request uri
        :param request_type: int, request type:
            0 - GET
            1 - POST
        :param data: json data in dictionary for POST request or None
        :param oauth: oauth request or another request
        :return: json response
        """

        try:
            if not request_type:
                async with self._session.get(uri) as response:
                    return await response.json()

            elif request_type == 1:
                if oauth:
                    async with self._oauth_session.post(uri, data=data) as response:
                        return await response.json()

                else:
                    async with self._session.post(uri, json=data) as response:
                        return await response.json()

            else:
                raise exceptions.BrowseAPIParamError('request_type')

        except client_exceptions.InvalidURL:
            raise exceptions.BrowseAPIInvalidUri('Invalid uri', uri)

        except client_exceptions.ServerTimeoutError:
            raise exceptions.BrowseAPITimeoutError('Timeout occurred', uri)

        except client_exceptions.ClientConnectorError:
            raise exceptions.BrowseAPIConnectionError('Connection error', uri)

        except client_exceptions.ClientOSError:
            raise exceptions.BrowseAPIConnectionError('Connection reset', uri)

        except client_exceptions.ServerDisconnectedError:
            raise exceptions.BrowseAPIConnectionError('Server refused the request', uri)

        except client_exceptions.ClientResponseError:
            raise exceptions.BrowseAPIMimeTypeError('Response has unexpected mime type', uri)

    async def _oauth(self, grant_type=0):
        """
        OAuth request

        :param grant_type: integer, grant type:
            0 - client credentials grant type
        :return: json response
        """

        if not grant_type:
            grant_type = self._credentials_grant_type
            scope = self._scope_public_data

        else:
            raise exceptions.BrowseAPIParamError('grant_type')

        data = self._encode_params(locals(), ('self',))
        return await self._request(self._auth_uri, request_type=1, data=data, oauth=True)

    async def _search(self,
                      q=None,
                      gtin=None,
                      charity_ids=None,
                      fieldgroups='MATCHING_ITEMS',
                      compatibility_filter=None,
                      category_ids=None,
                      filter=None,
                      sort=None,
                      limit=200,
                      offset=0,
                      aspect_filter=None,
                      epid=None) -> dict:
        """
        Browse API search method

        :param q: a string consisting of one or more keywords that are used to search for items
        :param gtin: search by the Global Trade Item Number of the item
        :param charity_ids: limits the results to only items associated with the specified charity ID
        :param fieldgroups: comma separated list of values that lets you control what is returned in the response
        :param compatibility_filter: specifies the attributes used to define a specific product
        :param category_ids: the category ID is used to limit the results
        :param filter: multiple field filters that can be used to limit/customize the result set
        :param sort: specifies the order and the field name to use to sort the items
        :param limit: the number of items, from the result set, returned in a single page
        :param offset: the number of items to skip in the result set
        :param aspect_filter: this field lets you filter by item aspects
        :param epid: eBay product identifier of a product from the eBay product catalog
        :return: json response
        """

        uri = self._search_uri + self._encode_params(locals(), ('self',))
        return await self._request(uri)

    async def _search_by_image(self,
                               image: str,
                               category_ids=None,
                               filter=None,
                               sort=None,
                               limit=200,
                               offset=0,
                               aspect_filter=None,
                               epid=None) -> dict:
        """
        Browse API searchByImage method

        :param image: base64 encoded image
        :param category_ids: the category ID is used to limit the results
        :param filter: multiple field filters that can be used to limit/customize the result set
        :param sort: specifies the order and the field name to use to sort the items
        :param limit: the number of items, from the result set, returned in a single page
        :param offset: the number of items to skip in the result set
        :param aspect_filter: this field lets you filter by item aspects
        :param epid: eBay product identifier of a product from the eBay product catalog
        :return: json response
        """

        uri = self._search_by_image_uri + self._encode_params(locals(), ('self', 'image'))
        return await self._request(uri, request_type=1, data={'image': image})

    async def _send_oauth_request(self):
        """ Send OAuth request for getting application token """

        oauth_response = await self._oauth()

        try:
            app_token = oauth_response['access_token']
            expires_in = oauth_response['expires_in']

        except KeyError:
            raise exceptions.BrowseAPIOAuthError(oauth_response)

        self._possible_requests = expires_in // TIMEOUT
        self._headers['Authorization'] = self._headers['Authorization'].format(app_token)

    async def _send_requests(self, method: str, params: list, pass_errors: bool) -> None:
        """
        Send async requests

        :param method: Browse API method name in lowercase
        :param params: list of params dictionaries for every request
        :param pass_errors: exceptions in the tasks are treated the same as successful results, bool
        """

        self._responses = []

        # load specified api method

        if method not in self.supported_methods:
            raise exceptions.BrowseAPIMethodError('This method is not supported: {}'.format(method))

        method_name = method
        method = getattr(self, '_' + method)

        try:
            # get oauth token

            self._oauth_session = ClientSession(headers=self._oauth_headers, timeout=self._timeout)
            await self._send_oauth_request()
            await self._create_session()

            # send requests

            params = self._split_list(params, self._possible_requests)

            for part_number, param_part in enumerate(params):
                responses = await asyncio.gather(
                    *[method(**param) for param in param_part],
                    return_exceptions=pass_errors
                )

                self._responses += [BrowseAPIResponse(response, method_name) if isinstance(response, dict) else response
                                    for response in responses]

                if part_number != len(params):
                    await self._send_oauth_request()
                    await self._create_session()

        finally:
            await self._oauth_session.close()

            if self._session is not None:
                await self._session.close()

    def execute(self, method: str, params: list, pass_errors=False) -> list:
        """
        Start event loop and make requests

        :param method: Browse API method name in lowercase
        :param params: list of params dictionaries for every request
        :param pass_errors: exceptions in the tasks are treated the same as successful results, bool
        :return: list of responses
        """

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._send_requests(method, params, pass_errors))

        finally:
            loop.close()

        return self._responses

    @staticmethod
    def _encode_params(params: dict, to_delete=('',)) -> str:
        """
        Encode uri parameters

        :param params: request parameters dictionary
        :param to_delete: iterable, what params needs to be deleted
        :return: string with encoded parameters
        """

        return urlencode({
            param: str(params[param]) for param in params if params[param] is not None and param not in to_delete
        })

    @staticmethod
    def _split_list(array: list, n: int):
        """ Split list into parts with n elements """

        return [array[i:i + n] for i in range(0, len(array), n)]
