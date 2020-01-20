from bs4 import BeautifulSoup
import requests

class Wikipedia:
    def __init__(self, lookup_term):
        self.lookup_term = lookup_term
        self.url = Wikipedia.url_es() + self.lookup_term
        page = requests.get(self.url)
        self.__soup = BeautifulSoup(page.content, 'html.parser')

    def get_summary(self):
        summary_container = self.__soup.find(id='mw-content-text')
        text = summary_container.find('p').text
        if len(text) > 247:
            return text[0:247] + '...'
        return text

    def get_image(self):
        summary_container = self.__soup.find(id='mw-content-text')
        src = summary_container.find('img').get('src')
        return src

    @staticmethod
    def url_en():
        return 'https://en.wikipedia.org/wiki/'

    @staticmethod
    def url_es():
        return 'https://es.wikipedia.org/wiki/'