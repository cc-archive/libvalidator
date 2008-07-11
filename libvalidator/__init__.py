# -*- coding: utf-8 -*-
import re, urlparse, urllib, os
from xml.dom import minidom
from xml.dom.ext import c14n
from xml.parsers.expat import ExpatError
from BeautifulSoup import BeautifulSoup
from pyRdfa import _process_DOM, Options
from pyRdfa.transform.DublinCore import DC_transform
import rdflib

class URLOpener(urllib.FancyURLopener):
    def http_error_404(*args, **kwargs):
        raise IOError

class libvalidator():
    def __init__(self, *args, **kargs):
        self.namespaces = {'cc': rdflib.Namespace('http://web.resource.org/cc/'),
                           'dc': rdflib.Namespace('http://purl.org/dc/elements/1.1/'),
                           'xhv': rdflib.Namespace('http://www.w3.org/1999/xhtml/vocab#')}
        self.baseURI = ''
        self.result = {'licensedObjects': {}}
    def findBaseDocument(self):
        # FIXME no CURIE support (low priority)
        for e in self.dom.getElementsByTagName('base'):
            if e.hasAttribute('href'):
                self.baseURI = e.getAttribute('href')
                return
        reContentLocation = re.compile('(?:^|\s+)Content\-Location\s*:\s*(\S+)', re.IGNORECASE)
        search = reContentLocation.search(self.headers)
        if search:
            self.baseURI = search.group(1)
        elif self.location:
            self.baseURI = self.location
    def canonicalization(self, code):
        try:
            dom = minidom.parseString(code)
        except ExpatError, err:
            code = str(BeautifulSoup(code))
            # the following can raise ExpatError again
            dom = minidom.parseString(code)
        return c14n.Canonicalize(dom, comments = True)
    def extractLicensedObjects(self, code, base):
        code = self.canonicalization(code)
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(code))
        for row in graph.query('SELECT ?a ?b WHERE { { ?a cc:license ?b } UNION { ?a xhv:license ?b } UNION { ?a dc:rights ?b } UNION { ?a dc:rights.license ?b } }', initNs = dict(cc = self.namespaces['cc'], dc = self.namespaces['dc'], xhv = self.namespaces['xhv'])):
            try:
                self.result['licensedObjects'][str(row[0])]
            except:
                self.result['licensedObjects'][str(row[0])] = []
            # a blank node
            if isinstance(row[1], rdflib.BNode):
                # FIXME fish for interesting data (cc:Agent)
                #triples = []
                #for r in graph.query('SELECT ?a ?b WHERE { '+row[1].n3()+' ?a ?b }'):
                #    triples.append((str(r[0]), str(r[1])))
                #self.result['licensedObjects'][str(row[0])].append(triples)
                pass
            # an RDF URI reference
            elif isinstance(row[1], rdflib.URIRef):
                self.result['licensedObjects'][str(row[0])].append(str(row[1]))
            # a literal
            else:
                self.result['licensedObjects'][str(row[0])].append(str(row[1]))
                
    def parse(self, code, location = None, headers = None):
        if location is not None:
            self.location = location
        if headers is not None:
            self.headers = headers
        self.code = self.canonicalization(code)
        self.dom = minidom.parseString(self.code)
        self.findBaseDocument()
        sources = []
        reRDF = re.compile('<([^\s<>]+)\s+(?:[^>]+\s+)?xmlns(?::[^=]+)?\s*=\s*(?:("http://www\.w3\.org/1999/02/22-rdf-syntax-ns#")|(\'http://www\.w3\.org/1999/02/22\-rdf\-syntax\-ns#\')).*</\\1\s*>')
        for m in re.finditer(reRDF, code):
            sources.append([self.baseURI, m.group(0)])
        dump = _process_DOM(self.dom, self.location, 'xml', Options(warnings = False, transformers = [DC_transform]))
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(dump), format='xml')
        sources.append([self.baseURI, graph.serialize(format='xml')])
        for row in graph.query('SELECT ?b WHERE { ?a xhv:meta ?b . }', initNs = dict(xhv = self.namespaces['xhv'])):
            try:
                # FIXME allows opening local files e.g. /etc/passwd (should not be allowed unless testing)
                f = URLOpener().open(row[0])
                # FIXME no MIME type detection (we assume it must be application/rdf+xml as yet)
                if not unicode(row[0]).startswith('data:'):
                    sources.append([str(row[0]), f.read()])
                else:
                    sources.append([self.baseURI, f.read()])
            except IOError:
                pass
        for (base, source) in sources:
            self.extractLicensedObjects(source, base)
        return self.result
        # aside of the licensed objects, gather information about licenses themselves
