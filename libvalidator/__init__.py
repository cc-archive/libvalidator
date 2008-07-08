# -*- coding: utf-8 -*-
import re, urlparse
#from tidy import parseString
from BeautifulSoup import BeautifulSoup

class libvalidator():
    def __init__(self, *args, **kargs):
        pass
    """
    No CURIE support
    """
    def findBaseDocument(self):
        soup = BeautifulSoup(self.code)
        element = soup.find('base', {'href': lambda(value): value is not None})
        reContentLocation = re.compile('(?:^|\s+)Content\-Location\s*:\s*(\S+)', re.IGNORECASE)
        search = reContentLocation.search(self.headers)
        if element:
            self.baseURI = element['href']
        elif search:
            self.baseURI = search.group(1)
        elif location:
            self.baseURI = self.location
    def findBaseElement(self, element):
        if element.name.lower() == 'object':
            try:
                return element['codebase']
            except:
                pass
        try:
            return element['xml:base']
        except:
            node = element
            while node:
                search = node.findParent(attrs={'xml:base': lambda(value): value is not None})
                if search:
                    return search['xml:base']
                node = node.parent
        return self.baseURI
    def parse(self, code, location = None, headers = None):
        self.code = code
        if location is not None:
            self.location = location
        if headers is not None:
            self.headers = headers
        self.findBaseDocument()
        # incomplete
