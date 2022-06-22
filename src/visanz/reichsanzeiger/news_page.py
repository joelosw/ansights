import requests
import html2text
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
if True:
    from utils.logger import get_logger
logger = get_logger('FESS')

class News_Page:
    def __init__(self, url, init_keywords=None, timestamp=None):
        self.url: str = url
        self.keywords: set = set()
        if isinstance(init_keywords, str):
            init_keywords = init_keywords.split(' ')
        else:
            init_keywords = init_keywords
        self.keywords.update(init_keywords)
        self.name = '-'.join(self.url.split('/')[-3:])
        self.timestamp = timestamp

    def add_keywords(self, additional_keywords):
        self.keywords.update(additional_keywords)

    def context(self):
        """return text of Newspage
        """
        data = requests.get(self.url)
        text = html2text.html2text(data.text)
        return text

    @property
    def date(self):
        if not self.timestamp:
            return ''
        date = datetime.strptime(
            self.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        return datetime.strftime(date, '%b %Y')

    @property
    def scan_url(self):
        data = requests.get(self.url).content
        soup = BeautifulSoup(data, 'html.parser')
        link = soup.a
        if link:
            return 'https://digi.bib.uni-mannheim.de' + link.get('href')
        else:
            logger.warning('Could not find scan for url {}'.format(self.url))
            return self.url

    def __eq__(self, other):
        other.url == self.url

    def common_keywords(self, other):
        return self.keywords.intersection(other.keywords)

    def __str__(self) -> str:
        return f'\n ========== \n Newspaper Page  from URL: \n {self.url} with keywords {self.keywords} \n and name {self.name} ====== \n'

    def __repr__(self) -> str:
        return self.__str__()
