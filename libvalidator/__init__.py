# -*- coding: utf-8 -*-
import re, os, urlparse, urllib, hashlib
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from xml.sax._exceptions import SAXParseException
from BeautifulSoup import BeautifulSoup
from pyRdfa import _process_DOM, Options
from pyRdfa.transform.DublinCore import DC_transform
import rdflib, tidy, c14n

class URLOpener(urllib.FancyURLopener):
    def http_error_404(*args, **kwargs):
        raise IOError

class libvalidator():
    def __init__(self, *args, **kargs):
        self.namespaces = {'cc': rdflib.Namespace('http://web.resource.org/cc/'),
                           'dc': rdflib.Namespace('http://purl.org/dc/elements/1.1/'),
                           'xhv': rdflib.Namespace('http://www.w3.org/1999/xhtml/vocab#')}
        self.baseURI = ''
        self.result = {'licensedObjects': {}, 'licenses': {}}
    def findBaseDocument(self):
        # FIXME no CURIE support (low priority)
        # FIXME no xml:base support (low priority)
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
    def findBaseForElement(self, base, element):
        # FIXME no CURIE support (low priority)
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
                search = node.findParent(attrs={'xml:base' : lambda(value): value is not None})
                if search:
                    return search['xml:base']
                node = node.parent
        return base        
    def canonicalization(self, code):
        try:
            dom = minidom.parseString(code)
        except ExpatError, err:
            code = unicode(BeautifulSoup(code)).encode('utf-8')
        try:
            dom = minidom.parseString(code)
        except ExpatError, err:
            options = dict(output_xml=1, numeric_entities=1, quote_nbsp=1,
                           add_xml_decl=1, indent=0, tidy_mark=0,
                           input_encoding='utf8', output_encoding='ascii',
                           hide_comments=0)
            code = unicode(tidy.parseString(code, **options)).encode('utf-8')
        try:
            dom = minidom.parseString(code)
        except ExpatError, err:
            return False
        return c14n.Canonicalize(dom, comments = True)
    def extractLicensedObjects(self, code, base):
        try:
            code = self.canonicalization(code)
        except ExpatError, err:
            return False
        graph = rdflib.ConjunctiveGraph()
        try:
            graph.parse(rdflib.StringInputSource(code))
        except SAXParseException, err:
            return False
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
    def extractLicenseInformation(self, code, base):
        try:
            code = self.canonicalization(code)
        except ExpatError, err:
            return False
        graph = rdflib.ConjunctiveGraph()
        try:
            graph.parse(rdflib.StringInputSource(code))
        except SAXParseException, err:
            return False
        # FIXME body of the method
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
                    # FIXME ignores the Content-Location in the HTTP header
                    sources.append([str(row[0]), f.read()])
                else:
                    sources.append([self.baseURI, f.read()])
            except IOError:
                pass
        for (base, source) in sources:
            self.extractLicensedObjects(source, base)
        return self.result
        # aside of the licensed objects, gather information about licenses themselves
    def parseLicense(self, sample, location):
        # name, external XHTML, external RDF/XML, embedded
        # <link rel="alternate" type="application/rdf+xml" href="rdf" />
        # calculate hashes
        sample = sample.strip()
        headers = ''
        reHyperlink = re.compile('^(?:data:|((ftp|gopher|https?)://))\S+$', re.IGNORECASE)
        if reHyperlink.search(sample) is not None:
            # FIXME cache
            try:
                opener = URLOpener()
                filename, headers = opener.retrieve(sample)
                f = open(filename, 'r')
                code = f.read()
                f.close()
                opener.close()
                externalLocation = sample
            except IOError, err:
                return False
        else:
            code = sample
        soup = BeautifulSoup(code)
        rel = re.compile('(?:^alternate\s+)|(?:\s+alternate\s+)|(?:^alternate$)|(?:\s+alternate$)', re.IGNORECASE)
        links = soup.findAll(re.compile('^(?:a|link)$', re.IGNORECASE),
                             {'rel': rel, 'type': 'application/rdf+xml', 'href': lambda(value): value is not None})
        licenses = []
        if len(links) == 0:
            licenses.append([location, sample])
        else:
            element = soup.find('base', {'href': lambda(value): value is not None})
            reContentLocation = re.compile('(?:^|\s+)Content\-Location\s*:\s*(\S+)', re.IGNORECASE)
            search = reContentLocation.search(unicode(headers))
            if element:
                base = element['href']
            elif search:
                base = search.group(1)
            elif location:
                base = externalLocation
            for link in links:
                try:
                    url = urlparse.urljoin(self.findBaseForElement(base, link), link['href'])
                    f = URLOpener().open(url)
                    if not link['href'].startswith('data:'):
                        # FIXME ignores the Content-Location in the HTTP header
                        licenses.append([url, f.read()])
                    else:
                        licenses.append([base, f.read()])
                    f.close()
                except IOError:
                    pass
            for (base, source) in licenses:
                self.extractLicenseInformation(source, base)
