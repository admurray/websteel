import os
import errno
import time
import requests
import itertools
import urlparse
import threading
from  websteel_exc import RangeNumericsCountMismatch
from urlparse import urlparse
from urlparse import urljoin
from bs4 import BeautifulSoup
PDF = ['.pdf']
IMAGE = ['.jpg', '.png' '.jpeg', '.gif']
VIDS = ['.mp4', '.avi', '.flv']
MUSIC = ['.mp3', 'ogg']
def getpagelinks(page, filetype=IMAGE):
    parsed_uri = urlparse(page)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    page_links = []
    page_content = requests.get(page)
    pagehtml = page_content.content
    page_content.close()
    all_links = []
    soup = BeautifulSoup(pagehtml)
    for elm in soup():
        all_links += list(elm.attrs.values())
    for link in all_links:
        if link and not isinstance(link, list):
            dot_index = link.rfind('.')
            ext = link[dot_index:]

            if isinstance(filetype, list) and link:
                if ext in filetype:
                    page_links.append(link)
            elif isinstance(filetype, str):
                if ext == filetype:
                    page_links.append(link)
    return base_url, page_links


def get_pages(base_url,links_list, output_dir):
    for link in links_list:
        page_url = urljoin(base_url, link)
        thr = threading.Thread(target=get_page_data, args=(page_url, output_dir, base_url, ))
        thr.start()

#: for direct links
def generate_links(base_link, ranges=[]):
    base_link_segs = base_link.split(' ')
    print(base_link_segs)
    if not len(base_link_segs) -1 == len(ranges):
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

    links_list = get_cross_product_list(url_segments_list)
    return links_list

def get_cross_product_list(url_segments_list):
    links_list = []
    for l in itertools.product(*url_segments_list):
        links_list.append(''.join(l))
    return links_list

def download_pics_from_list(links_list, output_dir):
    for each in links_list:
        get_page_data(each, output_dir)


def get_consecutive_links(page_url, start_img, end_img):
    #: Iterate over files
    digits = page_url[page_url.rfind('%_'):page_url.rfind('_%')]
    page = []



def get_page_data(page_url, output_dir, base_url=None, kill=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    if page_url.startswith('//'):
        page_url = 'http:'+page_url
    elif page_url.startswith('/') and base_url:
        page_url = base_url[:-1]+page_url
    response = requests.get(page_url, headers=headers)
    dirname = output_dir+page_url[page_url.find('/')+1:page_url.rfind('/')]
    try:
        os.makedirs(dirname)
        print 'Created directory - {}'.format(dirname)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise

    filename = page_url[page_url.rfind('/')+1:]
    if not response.status_code == 404 and len(response.content) >= 12000:
        with open('{}/{}'.format(dirname, filename), 'wb') as file_path:
            print('Downloading {} to {}'.format(page_url, dirname))
            file_path.write(response.content)
            time.sleep(0)
    elif response.status_code == 404:
        if not kill:
            print('Retrying link img download before giving up')
            base_url, all_files = getpagelinks(page_url[:-4])
            count = 0
            for each in all_files:
                count = count+1
                if count >= len(all_files):
                    kill = True
                get_page_data(each, output_dir, base_url, kill)
        print('Status - {} Size- {}, link - {} : NOT Downloading\n'.format(response.status_code, len(response.content), page_url))
    else:
        print('Status - {} Size- {}, link - {} : NOT Downloading\n'.format(response.status_code, len(response.content), page_url))

def get_forum_docs(start_page, last_page, forum_link):
    for i in range(start_page, last_page):
        page_link = forum_link.replace(' ', '{}'.format(i))
        base_url, all_files = getpagelinks(page_link)
        print '==============================================================================================\n'
        print 'Getting links from page : {}\n'.format(page_link)
        for each in all_files:
            try:
                get_page_data(each, '~/Downloads/', base_url)
            except:
                pass


def get_direct_links(page_url): #: http://xyz.com/a= &b= &c=img.jpg
    for each in generate_links(page_url, [(5, 1000, 2000),(3, 0, 25)]):
        get_page_data(each, '~/Downloads/')


if __name__ == '__main__':

    #get_forum_docs(forum_link=forum_link, start_page=0, last_page=336)
    '''
    Scenarios : 
    Single page with many links
    Single page single file
    Single file link
    Single page with links leading to links
    Single page 
    '''


