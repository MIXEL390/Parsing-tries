from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin

import re


class Website:

    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Content:

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = {}

    def getPage(url):
        try:
            html = urlopen(url)
        except Exception as e:
            print(e)
            return None
        return BeautifulSoup(html, 'html.parser')

    def safeGet(bs, selector):
        selectedElems = bs.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def getContent(self, url):
        bs = Crawler.getPage(url)
        if bs is not None:
            title = Crawler.safeGet(bs, self.site.titleTag)
            body = Crawler.safeGet(bs, self.site.bodyTag)
            return Content(url, title, body)
        return Content(url, '', '')

    def crawl(self):
        bs = Crawler.getPage(self.site.url)
        if bs is None:
            return
        
        targetPages = bs.findAll('a', href=re.compile(self.site.targetPattern))
        
        for targetPage in targetPages:
            url = targetPage.attrs['href']
            if not self.site.absoluteUrl:
                from urllib.parse import urljoin 
                url = urljoin(self.site.url, url)
            if url not in self.visited:
                self.visited[url] = self.getContent(url)
                self.visited[url].print()
                
            if not self.site.absoluteUrl:
                url = urljoin(self.site.url, url)



quotes_site = Website(
    name='Quotes to Scrape',
    url='https://quotes.toscrape.com',
    targetPattern='\/page\/\d+\/', 
    absoluteUrl=False, 
    titleTag='span.text', 
    bodyTag='span small.author'
)

crawler = Crawler(quotes_site)
crawler.crawl()
