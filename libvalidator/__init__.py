# -*- coding: utf-8 -*-
import re, urlparse, urllib
from xml.dom import minidom
from xml.dom.ext import c14n
from xml.parsers.expat import ExpatError
from BeautifulSoup import BeautifulSoup
from pyRdfa import _process_DOM, Options
import rdflib

class URLOpener(urllib.FancyURLopener):
    def http_error_404(*args, **kwargs):
        raise IOError

class libvalidator():
    def __init__(self, *args, **kargs):
        self.reRDF = re.compile('<([^\s<>]+)\s+(?:[^>]+\s+)?xmlns(?::[^=]+)?\s*=\s*(?:("http://www\.w3\.org/1999/02/22-rdf-syntax-ns#")|(\'http://www\.w3\.org/1999/02/22\-rdf\-syntax\-ns#\')).*</\\1\s*>')
    """
    No CURIE support
    Should be rewritten to utilise DOM instead of the BeautifulSoup parsing
    findBaseElement MUST be rewritten to use DOM
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
        elif self.location:
            self.baseURI = self.location
    """
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
    """
    def parse(self, code, location = None, headers = None):
        if location is not None:
            self.location = location
        if headers is not None:
            self.headers = headers
        try:
            dom = minidom.parseString(code)
        except ExpatError, err:
            code = str(BeautifulSoup(code))
            # the following can raise ExpatError again
            dom = minidom.parseString(code)
        self.code = c14n.Canonicalize(dom, comments=True)
        self.dom = minidom.parseString(self.code)
        self.findBaseDocument()
        sources = []
        for m in re.finditer(self.reRDF, code):
            sources.append([self.baseURI, m.group(0)])
        n3 = _process_DOM(self.dom, self.location, 'n3', Options(warnings=False))
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(nt), format='n3')
        for row in graph.query('SELECT ?b WHERE { ?a xhv:meta ?b . }', initNs=dict(xhv=rdflib.Namespace("http://www.w3.org/1999/xhtml/vocab#"))):
            try:
                f = URLOpener().open(row[0])
                if not unicode(row[0]).startswith('data:'):
                    sources.append([str(row[0]), f.read()])
                else:
                    sources.append([self.baseURI, f.read()])
            except IOError:
                pass
