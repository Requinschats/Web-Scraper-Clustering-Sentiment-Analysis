from urllib import parse
from urllib import robotparser


class RobotParser:
    AGENT_NAME = '40074024'
    robot_file_name = 'robots.txt'

    def __init__(self, base_url):
        self.value = None
        self.base_url = base_url
        self.parser = self.initialize_robot()

    def initialize_robot(self):
        # https://www.tutorialspoint.com/urllib-robotparser-parser-for-robots-txt-in-python
        parser = robotparser.RobotFileParser()
        parser.set_url(parse.urljoin(self.base_url, self.robot_file_name))
        parser.read()
        return parser
