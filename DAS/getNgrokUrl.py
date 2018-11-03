from bs4 import BeautifulSoup
import urllib.request


# Ngrok uses port 4040 as default
link = 'http://127.0.0.1:4040/status'


def getNgrokUrl():
    raw = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(raw, features='lxml')
    htmlTextList = soup.text.split('"')
    i = 0
    while i < len(htmlTextList):
        if htmlTextList[i] == 'URL\\':
            return htmlTextList[i+2][:-1]
        i += 1
