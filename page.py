import re
import os
import urllib.request
from urllib import parse
from urllib.error import HTTPError
from utils import PageUtils

class Page:
    def __init__(self, page_url):
        self.page_url = page_url
        self.is_valid = False
        self.response = self.get_page_response()
        self.info = self.response.info()
        self.page_type = self.info.get_content_maintype()
        self.page_file_ext = self.info.get_content_subtype()
        self.page_content = self.response.read()
        self.filename = self.get_filename()

    def get_page_response(self):
        try:
            req = urllib.request.Request(self.page_url, headers=PageUtils.HEADERS)
            response = urllib.request.urlopen(req)
            return response
        except HTTPError as he:
            print('Connection failed : {}'.format(he))
            return None

    def is_valid_page(self, type, size):
        #: A page is valid when its size is above a certain specified limit and is of type
        if len(self.response.content) >= size and self.page_type() in type:
            return True
        else:
            return False

    def get_filename(self):
        filepath = self.get_url_filepath()
        return os.path.basename(filepath.path)

    def get_url_filepath(self):
        filepath = parse.urlparse(self.page_url)
        print('The filepath is : {}'.format(filepath.path))
        return filepath

    def create_file_on_disk(self, location):
        full_location = os.path.join(location, self.filename)
        with open(full_location, 'wb') as datafile:
            datafile.write(self.page_content)



if __name__ == '__main__':
    url = ''
    page = Page(url)
    print(page.page_type)
    print(page.page_file_ext)
    print(page.info)
    print(page.filename)
    page.create_file_on_disk('~/Downloads')
