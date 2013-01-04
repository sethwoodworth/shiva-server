import re
import urllib2

import requests

from shiva.api.lyrics.base import LyricScraper


class AZLyrics(LyricScraper):
    """
    """

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.lyrics = None
        self.source = None

        self.search_url = 'http://search.azlyrics.com/search.php?q=%s'
        self.lyric_url_re = re.compile(r'http://www\.azlyrics\.com/lyrics/'
                                       r'[a-z0-9]+/[a-z0-9]+\.html')
        self.lyric_re = re.compile(r'<!-- start of lyrics -->(.*)'
                                   r'<!-- end of lyrics -->', re.M + re.S)

    def fetch(self):
        self.search()
        if not self.source:
            return None

        print(self.source)
        response = requests.get(self.source)
        lyrics = self.lyric_re.findall(response.text)[0]

        lyrics = re.sub(r'<br[ /]+>', '\r', lyrics)
        lyrics = re.sub(r'<.*?>', '', lyrics)

        self.lyrics = lyrics.strip()

    def search(self):
        query = urllib2.quote('%s %s' % (self.artist, self.title))
        print(self.search_url % query)
        response = requests.get(self.search_url % query)
        results = self.lyric_url_re.findall(response.text)

        if results:
            self.source = results[0]
