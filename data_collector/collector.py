'''
This file is the base for collecting all the data from a source
The source may be a
    link or a list of links (A file address may be local or remote.)
'''

import logging
import utils
import websteel_exc
import xlrd


COLLECTION_LOG = 'data_collection'

logger = logging.getLogger('data_collection')
log_fle_handle = logging.FileHandler('collection.log')


class DataCollector:
    def __init__(self, source):
        if not source:
            raise websteel_exc.NoSourceSpecified('Please specify a valid data source')
        self.source = source
        self.logger = logging.getLogger('data_collection')


class SpreadSheetDataCollector(DataCollector):

    def __init__(self):
        # super(SpreadSheetDataCollector, self).__init__()
        pass

    def parse_source_file(self):
        book = xlrd.open_workbook(self.source, logging=log_fle_handle)
        sheet = book.sheet_by_index(0)
        sheet_data = {}
        for row_index in xrange(1, sheet.nrows):
            sheet.row(0) = 


if __name__=='__main__':
    x = utils.get_project_dir()
    print(x)