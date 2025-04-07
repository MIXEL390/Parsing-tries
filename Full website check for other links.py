from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup 

import re
import random

pages = set()

allExtLinks = []
allIntLinks = []

def GetLinks(pageURL):
    html = urlopen(f'https://github.com{pageURL}')
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        bodyContent = bs.find('div', {'id' : 'bodyContent'}).find_all('p')
        if len(bodyContent):
            print(bodyContent[0])
        print(bs.find(id = 'ca-edit').find('a').attrs['href'])## same for p and everything else
    except AttributeError:
        print('Page misses')

    for link in bs.find_all('a', href=re.compile('^(/MIXEL390/)')):
        if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    
                    newPage = link.attrs['href']
                    print('-'*20)
                    print(newPage)
                    pages.add(newPage)
                    GetLinks(newPage)

def getExternalLinks(bs, url):
    netloc = urlparse(url).netloc
    externalLinks = set()
    for link in bs.find_all('a'): 
        if not link.attrs.get('href'):
            continue
        parsed = urlparse(link.attrs['href'])
        if parsed.netloc != '' and parsed.netloc != netloc:
            externalLinks.add(link.attrs['href'])
    return list(externalLinks)


def getInternalLinks(bs, url):
    netloc = urlparse(url).netloc
    scheme = urlparse(url).scheme
    internalLinks = set()
    for link in bs.find_all('a'):
        if not link.attrs.get('href'):
            continue
        parsed = urlparse(link.attrs['href'])
        if parsed.netloc == '':
            internalLinks.add(f'{scheme}://{netloc}/{link.attrs["href"].strip("/")}')
        elif parsed.netloc == netloc:
            internalLinks.add(link.attrs['href'])
    return list(internalLinks)

def getAllExternalLinks(url):
    bs = BeautifulSoup(urlopen(url), 'html.parser')
    internalLinks = getInternalLinks(bs, url)
    externalLinks = getExternalLinks(bs, url)
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.append(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.append(link)
            getAllExternalLinks(link)

def getRandomExternalLink(startingPage):
    bs = BeautifulSoup(urlopen(startingPage), 'html.parser')
    externalLinks = getExternalLinks(bs, startingPage)
    if not len(externalLinks):
        print('No other external links, trying to find others')
        internalLinks = getInternalLinks(bs, startingPage)
        return getRandomExternalLink(random.choice(internalLinks))
    else:
        return random.choice(externalLinks)
    
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print(f'Random external link is: {externalLink}')
    followExternalOnly(externalLink)


followExternalOnly('https://github.com/')
allIntLinks.append('https://github.com')
getAllExternalLinks('https://github.com/')

GetLinks('/MIXEL390/Parsing-tries')
