import lxml.etree
import lxml.html
import requests
from requests.auth import HTTPBasicAuth

JSON_URL = 'https://s3-eu-west-1.amazonaws.com/legalstart/thumbscraper_input_tampered.hiring-env.json'
FIRST_URL = 'https://yolaw-tokeep-hiring-env.herokuapp.com/'


class Scraper:

    def __init__(self, url = JSON_URL):
        self.url = url
        pass

    def getJSON(self):
        resp = requests.get(url=self.url)
        data = resp.json()
        return data

    def readPage(self, pageURL, jsonURL, data, nbPage):
        page = data[jsonURL]
        req = requests.get(url=pageURL, auth=HTTPBasicAuth('Thumb', 'Scraper'))
        root = lxml.html.fromstring(req.content)
        button = root.xpath(page['xpath_button_to_click'])
        button = button[0].attrib['href'][1:]
        query = root.xpath(page['xpath_test_query'])
        result = page['xpath_test_result']
        if (query == result):
            print('Move to page', nbPage)
            self.readPage(FIRST_URL + button, page['next_page_expected'], data, nbPage + 1)
        else:
            print('ALERT - Can’t move to page ', nbPage + 1, ': page ', nbPage,' link has been malevolently tampered with!!', sep='')

    def start(self):
        data = self.getJSON()
        self.readPage(FIRST_URL, '0', data, 0)