from unittest import TestCase
from json import loads

from ..client import BrowseAPI
from ..containers import BrowseAPIResponse
from ..exceptions import BrowseAPIParamError

SECRET_FILENAME = 'browseapi/tests/secret.json'
DATA_FILENAME = 'browseapi/tests/test_data.json'


class ClientTest(TestCase):
    """ Test Browse API initialization and client methods execution """

    def setUp(self) -> None:
        secret = self.load_json_data(SECRET_FILENAME)
        self.data = self.load_json_data(DATA_FILENAME)
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

    def assert_responses(self, responses):
        for response in responses:
            self.assertIsInstance(response, BrowseAPIResponse)
            self.assertTrue(len(response.itemSummaries))

    @staticmethod
    def load_json_data(filename):
        with open(filename) as file:
            return loads(file.read())
