import logging
import os
import unittest
import utils

# Project module imports
import data_collector.collector as coll
import websteel_exc

# Logger setup
logger = logging.getLogger('unit_tests')
test_logger = logging.FileHandler('unit_test.log')

# Constants
TEST_FILE = 'NYSEGROUP_US_REF_SECURITYMASTER_EQUITY_SAMPLE.xls'
TEST_FILE_KEYS = []

class TestDataCollector(unittest.TestCase):

    def setUp(self):
        proj_dir = utils.get_project_dir()
        self.source_file = os.path.join(proj_dir, 'tests', 'resources', TEST_FILE)

    def test_data_collector_instatiation_no_source(self):
        with self.assertRaises(websteel_exc.NoSourceSpecified):
            coll.DataCollector(None)

    def test_data_collector_intantiation(self):
        collector = coll.DataCollector(self.source_file)
        self.assertIsNotNone(collector.source)
        self.assertEqual(collector.source, self.source_file)

class TestSpreadSheetDataCollector(unittest.TestCase):

    def setUp(self):
        proj_dir = utils.get_project_dir()
        self.source_file = os.path.join(proj_dir, 'tests', 'resources', TEST_FILE)

    def test_get_sheet_keys(self):
        pass
