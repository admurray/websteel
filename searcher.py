import requests

class WildURL:
    #: The space is very important, since URLs don't accept space.s
    NUM_PLACEHOLDER = ' _num_ '
    WORD_PLACEHOLDER = ' _word_ '

    def __init__(self, url):
        self.url = url

    def generate_padded_number(self, padding, number):
        return number.zfill(padding)


class Searcher:
    def __init__(self):
        pass

    def find_valid_page(self, wild_url):


    def _is_invalid_page(self, url):
        page = requests.get(url)

        return