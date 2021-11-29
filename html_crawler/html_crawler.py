import requests
from bs4 import BeautifulSoup

from html_crawler.selectors import select_concordia_internal_links
from robot_parser.robot_parser import RobotParser


class HtmlCrawler:
    HTML_SEPARATOR = ";"

    def __init__(self, base_url):
        self.links = select_concordia_internal_links()
        self.documents = []
        self.robot_parser = RobotParser(base_url)

    def fetch_url_html(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser").get_text(separator=self.HTML_SEPARATOR)

    def fetch_concordia_internal_links_html(self, max_document_count=100):
        print("Fetching " + str(max_document_count) + " Concordia html pages...")
        for url in self.links[0: max_document_count]:
            html = self.fetch_url_html(url)
            self.documents.append(html)
        return self.documents
