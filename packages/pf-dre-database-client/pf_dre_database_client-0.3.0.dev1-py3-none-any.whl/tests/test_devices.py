from unittest import TestCase

# Project Specific Modules
from mms import MMSClient
from tests.helpers import get_db_client_kwargs


class TestDevices(TestCase):
    def setUp(self):
        self.clientArgs = get_db_client_kwargs()

    def test_mock_meter(self):
        ids = MMSClient(**self.clientArgs).get_device_ids_for_codes(['42.8355'])
        self.assertEqual(ids, {'42.8355': '353'})

    def test_inverted_meter(self):
        c = MMSClient(**self.clientArgs)
        ids = c.get_device_ids_for_codes(['42.8355', '8300.11'])
        self.assertEqual(ids, {'42.8355': '353', '8300.11': '1997'})
        self.assertEqual(0, c.device_inverted(ids['42.8355']))
        self.assertEqual(1, c.device_inverted(ids['8300.11']))

    def test_codes_for_service(self):
        c = MMSClient(**self.clientArgs)
        codes = c.get_device_codes_for_service('NEMWEB')
        self.assertEqual(3, len(codes))
        self.assertCountEqual(
            ['NEM.predispatch_5', 'NEM.predispatch', 'NEM.dispatch_pre_ap'],
            codes
        )

