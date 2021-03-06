#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DownloadStreamCloud import DownloadStreamCloud
from DownloadNowVideo import DownloadNowVideo
from DownloadStreamin import DownloadStreamin
from DownloadStreamPlay import DownloadStreamPlay

from InfoProviderImdb import InfoProviderImdb

#from LinksProviderSeriesFlv import LinksProviderSeriesFlv
from LinksProviderSeriesPepito import LinksProviderSeriesPepito
from LinksProviderSeriesAdicto import LinksProviderSeriesAdicto
from LinksProviderPordede import LinksProviderPordede

from Season import Link
from Tools import isNumber

from threading import Thread
import time
from Queue import Queue

class CtrlProviders():

    def __init__ (self, tmpPath):

        self.TMP_PATH = tmpPath
        self._infoProviderImdb = InfoProviderImdb ()

        #self._linkProviders = [LinksProviderPordede(), LinksProviderSeriesAdicto(), LinksProviderSeriesFlv(), LinksProviderSeriesPepito()]
        #self._linkProviders = [LinksProviderPordede(), LinksProviderSeriesAdicto(), LinksProviderSeriesPepito()]
        self._linkProviders = [LinksProviderPordede(), LinksProviderSeriesPepito()]

    def downloadVideo (self, url, host, name):
        if 'streamcloud' in host.lower():
            d = DownloadStreamCloud ()
            downloadErr = d.downloadVideo (url, self.TMP_PATH + '/' + name)

        elif 'nowvideo' in host.lower():
            d = DownloadNowVideo ()
            downloadErr = d.downloadVideo (url, self.TMP_PATH + '/' + name)
        elif 'streamplay' in host.lower():
            d =  DownloadStreamPlay ()
            downloadErr = d.downloadVideo (url, self.TMP_PATH + '/' + name)
        elif 'streamin' in host.lower() or 'streaminto' in host.lower():
            d =  DownloadStreamin ()
            downloadErr = d.downloadVideo (url, self.TMP_PATH + '/' + name)
        else:
            print '  -> host "' + host + '" not defined for download'

    def loadSerie (self, serieName):
        data = self._infoProviderImdb.loadSerie (serieName)
        if data == None:
			#data = self._infoProviderAnime.loadSerie (serieName)
			#if data == None:
				#...
            raise Exception ('Serie "' + serieName + '" not found')
        return data

    def printSuggerencies (self):
        print ''
        print ' -> suggerencies:'
        self._infoProviderImdb.printSuggerencies ()
        #self._infoProviderAnime.printSuggerencies ()
        print ''

    def getMainInfo (self, serieName):
        q = Queue()

        threads = []

        for linkProvider in self._linkProviders:
            threads.append(Thread(target=linkProvider.getMainPageLink, args=(serieName, q)))

        for thread in threads: thread.start()
        for thread in threads: thread.join()

        mainPages = []

        while q.qsize() > 0:
            mainPages.append(q.get())

        return mainPages

    def getChapterUrls (self, mainPagesLinks, seasonNumber, chapterNumber):
        q = Queue()

        threads = []
        print ''
        for mainPage, linkProvider in [(x[1], y) for x in mainPagesLinks for y in self._linkProviders if x[0] == y._name]:
            threads.append(Thread(target=linkProvider.getChapterUrls, args=(mainPage, seasonNumber, chapterNumber, q)))

        for thread in threads: thread.start()
        for thread in threads: thread.join()

        data = []

        while q.qsize() > 0:
            data.append(q.get()[1])

        return data
