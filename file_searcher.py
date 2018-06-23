import itertools
from websteel_exc import *

#: The space is very important, since URLs don't accept space.s
NUM_PLACEHOLDER = ' _num_ '
WORD_PLACEHOLDER = ' _word_ '

class FileSearcher:
    #: There can be two ways to collect data
    #  get data from page
    #: follow links and get data from links.
    #:

    def __init__(self):
        pass

class UrlIterator:

    def __init__(self, wild_url):
        self.wild_url = wild_url

    def generate_url_list(self, wild_url, ranges):
        if '_word_' in wild_url:
            raise NotSupportedFunctionality('This functionality is not yet supported,'\
                                            ' Please stick to just numeric wildcards')
        base_link_segs = wild_url.split(' _num_ ')
        print(base_link_segs)
        if not len(base_link_segs) - 1 == len(ranges):
            raise RangeNumericsCountMismatch('Number of ranges and spaces in the url must be equal')
        url_segments_list = []
        for idx, val in enumerate(base_link_segs[:-1]):
            segment_list = []
            padding, start, end = ranges[idx]
            for i in range(start, end):
                num = str(i).zfill(padding)
                segment = '{}{}'.format(val, num)
                segment_list.append(segment)
            url_segments_list.append(segment_list)
        url_segments_list.append(base_link_segs[-1:])

        links_list = self.get_cross_product_list(url_segments_list)
        return links_list

    def get_cross_product_list(self, url_segments_list):
        links_list = []
        for l in itertools.product(*url_segments_list):
            links_list.append(''.join(l))
        return links_list

  