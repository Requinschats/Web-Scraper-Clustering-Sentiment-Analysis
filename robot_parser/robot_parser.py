import time
from urllib import parse
from urllib import robotparser


class RobotParser:
    AGENT_NAME = '40074024'
    robot_file_name = 'robots.txt'

    def __init__(self, base_url):
        self.value = None
        self.base_url = base_url
        self.parser = self.initialize_robot()
        self.crawl_delay = self.get_crawl_delay()
        self.request_rate = self.get_request_rate

    def initialize_robot(self):
        # https://www.tutorialspoint.com/urllib-robotparser-parser-for-robots-txt-in-python
        parser = robotparser.RobotFileParser()
        parser.set_url(parse.urljoin(self.base_url, self.robot_file_name))
        parser.read()
        return parser

    def can_fetch_url(self, url):
        return self.parser.can_fetch(self.AGENT_NAME, url)

    def get_crawl_delay(self):
        parser_delay = self.parser.crawl_delay(self.AGENT_NAME)
        if parser_delay:
            return parser_delay
        return 0

    def get_request_rate(self):
        request_delay = self.parser.request_rate(self.AGENT_NAME)
        if request_delay: return request_delay
        return 0

    def get_is_crawlable(self, url):
        if not self.can_fetch_url(url): return False
        if self.crawl_delay: time.sleep(self.crawl_delay)
        return True
