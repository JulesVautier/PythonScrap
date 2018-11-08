import lxml.etree
import lxml.html
import requests
from requests.auth import HTTPBasicAuth

JSON_URL = 'https://s3-eu-west-1.amazonaws.com/legalstart/thumbscraper_input_tampered.hiring-env.json'
ROOT_URL = 'https://yolaw-tokeep-hiring-env.herokuapp.com/'


class Scraper:

    def __init__(self, json_url=JSON_URL, root_url=ROOT_URL):
        self.json_url = json_url
        self.root_url = root_url
        pass

    def getJSON(self):
        resp = requests.get(url=self.json_url)
        data = resp.json()
        return data

    def readPage(self, pageURL, jsonURL, data, nbPage):
        print('Move to page', nbPage)
        page = data[jsonURL]
        req = requests.get(url=pageURL, auth=HTTPBasicAuth('Thumb', 'Scraper'))
        root = lxml.html.fromstring(req.content)
        button = root.xpath(page['xpath_button_to_click'])
        button = button[0].attrib['href'][1:]
        query = root.xpath(page['xpath_test_query'])
        result = page['xpath_test_result']
        if (query == result):
            self.readPage(self.root_url + button, page['next_page_expected'], data, nbPage + 1)
        else:
            print('ALERT - Can’t move to page ', nbPage + 1, ': page ', nbPage,' link has been malevolently tampered with!!', sep='')
            pass

    def start(self):
        data = self.getJSON()
        self.readPage(self.root_url, '0', data, 1)
        pass