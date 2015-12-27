#! /usr/bin/python
import requests
from Download import Download
from Parser import Parser

class DownloadNowVideo (Download):

    def __init__ (self):
        Download.__init__ (self)
        self._parser = Parser ()

    def getVideoLink (self, totalLines):
        for line in totalLines:
            if 'file: "http://' in line:
                return line.split ('"')[1]

    def downloadVideo (self, link, name):
        print '  -> going to ' + link

        url = link.replace ('video/', 'mobile/video.php?id=')
        r = requests.get (url, headers={ "user-agent": "Mozilla/5.0" })
        data = self._parser.feed (r.text)

        sources = data.get_by (tag = 'source')

        for s in sources:
            try:
                self.downloadVideoFile (s.attrs['src'][0], name)
                return
            except Exception as e:
                pass
