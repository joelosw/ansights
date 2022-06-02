import requests
import html2text
class News_Page:
    keywords: set = set()
    url: str

    def __init__(self, url, init_keywords=None):
        self.url = url
        if isinstance(init_keywords, str):
            init_keywords = init_keywords.split(' ')
        else:
            init_keywords = init_keywords
        self.keywords.update(init_keywords)

    def add_keywords(self, additional_keywords):
        self.keywords.update(additional_keywords)

    def context(self):
        """return text of Newspage
        """
        data = requests.get(self.url)
        text = html2text.html2text(data.text)
        return text

    def __eq__(self, other):
        other.url == self.url

    def common_keywords(self, other):
        return self.keywords.intersection(other.keywords)

    def __str__(self) -> str:
        return f'\n ========== \n Newspaper Page  from URL: \n {self.url} with keywords {self.keywords} ====== \n'

    def __repr__(self) -> str:
        return self.__str__()