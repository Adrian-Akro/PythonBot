from bs4 import BeautifulSoup
import requests

class Wikipedia:
    def __init__(self, language_two_digit, lookup_term):
        self.lookup_term = lookup_term
        self.__set_language(language_two_digit)
        self.__set_page_soup(self.__get_page_url_from_search())

    def get_summary(self):
        summary_container = self.page_soup.find(id='mw-content-text')
        text = summary_container.find('p').text
        if len(text) > 247:
            return text[0:247] + '...'
        return text

    def get_image(self):
        summary_container = self.page_soup.find(id='mw-content-text')
        # First try to get image from a.image
        try:
            try:
                src = summary_container.find('a',{'class': 'image'}).find('img').get('src')

            # Then get image from img.thumbimage
            except AttributeError:
                src = summary_container.find('img',{'class': 'thumbimage'}).get('src')
        except AttributeError:
            return ''

        if src[0:4] != 'https':
            src = 'https:' + src
        return src

    def get_title(self):
        title_h1 = self.page_soup.find(id='firstHeading')
        return title_h1.text
        
    def __set_language(self, language_two_digit):
        if language_two_digit == 'ES':
            self.url = Wikipedia.url_es()
        elif language_two_digit == 'EN':
            self.url = Wikipedia.url_en()
        else:
            self.url = 'https://' + language_two_digit + '.wikipedia.org'

    def __get_page_url_from_search(self):
        url = self.url + '/wiki/w/index.php?search=' + '+'.join(self.lookup_term.split(' '))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            li_result = soup.find('li', {'class': 'mw-search-result'})
            return self.url + li_result.find('a').get('href')
        except AttributeError:
            print('The lookup term query did not return any valid pages, attempting get soup of url (', url, ') directly')
        return url

    def __set_page_soup(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        assert soup.find(id='ooui-php-1') == None, ('Could not get soup from url and search result were found', url)
        # TODO: Check for ambiguous pages
        self.page_url = url
        self.page_soup = soup

    @staticmethod
    def url_en():
        return 'https://en.wikipedia.org'

    @staticmethod
    def url_es():
        return 'https://es.wikipedia.org'