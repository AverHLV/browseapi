from unittest import TestCase
from json import loads

from ..client import BrowseAPI
from ..containers import BrowseAPIResponse
from ..exceptions import BrowseAPIParamError, BrowseAPIRequestParamError

SECRET_FILENAME = 'browseapi/tests/secret.json'
DATA_FILENAME = 'browseapi/tests/test_data.json'


class ClientTest(TestCase):
    """ Test Browse API initialization and client methods execution """

    def setUp(self) -> None:
        secret = self.load_json_data(SECRET_FILENAME)
        self.data = self.load_json_data(DATA_FILENAME)
        
        self.properties = [
            {'name': 'Year', 'value': '2016'},
            {'name': 'Make', 'value': 'Honda'},
            {'name': 'Model', 'value': 'Fit'},
            {'name': 'Trim', 'value': 'EX-L Hatchback 4-Door'},
            {'name': 'Engine', 'value': '1.5L 1497CC l4 GAS DOHC Naturally Aspirated'}
        ]
        
        self.api = BrowseAPI(secret['eb_app_id'], secret['eb_cert_id'])

    def test_init_params(self):
        self.assertRaises(BrowseAPIParamError, BrowseAPI, 'app_id', 'cert_id', reference_id='ref_id')
        self.assertRaises(BrowseAPIParamError, BrowseAPI, 'app_id', 'cert_id', country='US')
        self.assertRaises(BrowseAPIParamError, BrowseAPI, 'app_id', 'cert_id', zip_code=19026)

    def test_search(self):
        responses = self.api.execute('search', [{'q': 'drone', 'limit': 50}, {'category_ids': 20863}])
        self.assert_responses(responses)

    def test_search_by_image(self):
        responses = self.api.execute('search_by_image', [{'image': self.data['image']}])
        self.assert_responses(responses)

    def test_get_item(self):
        responses = self.api.execute('get_item', [{'item_id': 'v1|202117468662|0', 'fieldgroups': 'PRODUCT'}])
        self.assert_responses(responses)
        responses = self.api.execute('get_item', [{'item_id': 'v1|202117468662|0', 'fieldgroups': 'COMPACT'}])
        self.assert_responses(responses)

    def test_get_item_by_legacy_id(self):
        responses = self.api.execute('get_item_by_legacy_id', [{'legacy_item_id': '262800155662'}])
        self.assert_responses(responses)

        responses = self.api.execute('get_item_by_legacy_id',
                                     [{'legacy_item_id': '262800155662', 'fieldgroups': 'PRODUCT'}])

        self.assert_responses(responses)

    def test_get_items_by_item_group(self):
        responses = self.api.execute('get_items_by_item_group', [{'item_group_id': '351825690866'}])
        self.assert_responses(responses)

    def test_check_compatibility(self):
        responses = self.api.execute('check_compatibility',
                                     [{'item_id': 'v1|182708228929|0', 'compatibility_properties': self.properties}])

        self.assert_responses(responses)

    def test_response_pass_errors(self):
        responses = self.api.execute('get_items_by_item_group', [{'item_group_id': '182708228929'}], pass_errors=True)
        self.assertIsInstance(responses[0], BrowseAPIResponse)
        self.assertIsInstance(responses[0].errors[0], BrowseAPIRequestParamError)

    def assert_responses(self, responses: list) -> None:
        for response in responses:
            self.assertIsInstance(response, BrowseAPIResponse)

    @staticmethod
    def load_json_data(filename: str) -> dict:
        with open(filename) as file:
            return loads(file.read())
