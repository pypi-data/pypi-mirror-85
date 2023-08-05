# pylint: disable=broad-except
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from booknot.crawler.crawler import Crawler
from booknot.crawler.metadata import Metadata


class HttpCrawler(Crawler):

    def __init__(self, session: requests.Session):
        self.session = session

    def fetch(self, url: str) -> Metadata:
        r = self.session.get(url)
        content = r.content
        return self.parse_content(url, content)

    def parse_content(self, url: str, content: str) -> Metadata:
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.head.title.string
        description = self.extract_description(soup)

        now = datetime.now()
        return Metadata(url=url, title=title, description=description, capture_date=now)

    def extract_description(self, soup: BeautifulSoup):
        description = ''
        try:
            description_node = soup.head.find('meta', property="og:description")
            if description_node is None:
                description_node = soup.head.find(attrs={"name": re.compile(r'Description', re.I)})

            description = description_node["content"]
        except Exception as exception:
            logging.exception(exception)

        return description
