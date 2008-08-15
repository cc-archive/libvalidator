# -*- coding: utf-8 -*-
__author__ = 'Hugo Dworak <http://hugo.dworak.info>'
__license__ = """Copyright (C) 2008  Hugo Dworak

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import re, os, urlparse, urllib
from xml.dom import minidom
import html5lib
from html5lib import treebuilders
from pyRdfa import _process_DOM, Options
from pyRdfa.transform.DublinCore import DC_transform
import rdflib
import cc.license
from cc.license.lib.exceptions import CCLicenseError

class URLOpener(urllib.FancyURLopener):
    def http_error_404(*args, **kwargs):
        raise IOError

class libvalidator():
    def __init__(self, *args, **kargs):
        self.namespaces = {'cc': rdflib.Namespace('http://web.resource.org/cc/'),
                           'dc': rdflib.Namespace('http://purl.org/dc/elements/1.1/'),
                           'xhv': rdflib.Namespace('http://www.w3.org/1999/xhtml/vocab#')}
        self.baseURI = ''
        self.headers = None
        self.location = None
        self.result = {'licensedObjects': {}, 'licenses': {}, 'deprecated': False}
    def findBaseDocument(self):
        # FIXME no CURIE support (low priority)
        # FIXME no xml:base support (low priority)
        for e in self.dom.getElementsByTagName('base'):
            if e.hasAttribute('href'):
                self.baseURI = e.getAttribute('href')
                return
        if self.headers is not None:
            header = self.headers.get('Content-Type')
            if header is not None:
                self.baseURI = unicode(header)
                return
        self.baseURI = self.location
    def formDocument(self, code):
        dom = None
        try:
            dom = minidom.parseString(code)
        except:
            parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder('dom'))
            dom = parser.parse(code)
        return (dom, dom.toxml())
    def extractLicensedObjects(self, code, base):
        (dom, code) = self.formDocument(code)
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(code.encode('utf-8')))
        for row in graph.query('SELECT ?a ?b WHERE { { ?a cc:license ?b } UNION { ?a xhv:license ?b } UNION { ?a dc:rights ?b } UNION { ?a dc:rights.license ?b } }', initNs = dict(cc = self.namespaces['cc'], dc = self.namespaces['dc'], xhv = self.namespaces['xhv'])):
            if not self.result['licensedObjects'].has_key(str(row[0])):
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
                if not self.result['licenses'].has_key(str(row[1])):
                    license = self.parseLicense(str(row[1]))
                    if license != str(row[1]):
                        self.result['licenses'][str(row[1])] = self.parseLicense(str(row[1]))
            # a literal
            else:
                self.result['licensedObjects'][str(row[0])].append(str(row[1]))
    def parse(self, code, location = None, headers = None, openLocalFiles = False):
        if location is not None:
            self.location = location
        if headers is not None:
            self.headers = headers
        (self.dom, self.code) = self.formDocument(code)
        self.findBaseDocument()
        sources = []
        reRDF = re.compile('<([^\s<>]+)\s+(?:[^>]+\s+)?xmlns(?::[^=]+)?\s*=\s*(?:("http://www\.w3\.org/1999/02/22-rdf-syntax-ns#")|(\'http://www\.w3\.org/1999/02/22\-rdf\-syntax\-ns#\')).*</\\1\s*>')
        for m in re.finditer(reRDF, code):
            sources.append([self.baseURI, m.group(0)])
            self.result['deprecated'] = True
        dump = _process_DOM(self.dom, self.location, 'xml', Options(warnings = False, transformers = [DC_transform]))
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(dump), format='xml')
        sources.append([self.baseURI, graph.serialize(format='xml')])
        for row in graph.query('SELECT ?b WHERE { ?a xhv:meta ?b . }', initNs = dict(xhv = self.namespaces['xhv'])):
            try:
                reHyperlink = re.compile('^(?:data:|((ftp|gopher|https?)://))\S+$', re.IGNORECASE)
                if openLocalFiles == True or reHyperlink.search(row[0]) is not None:
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
    def parseLicense(self, uri):
        try:
            license = cc.license.selectors.choose('standard').by_uri(uri)
        except CCLicenseError, err:
            # a license might be stated using its title
            return uri
        return {'title' : license.title(),
                'description' : license.description(),
                'jurisdiction' : license.jurisdiction,
                'current_version' : license.current_version,
                'version' : license.version,
                'superseded' : license.superseded,
                'deprecated' : license.deprecated,
                'requires' : license.requires,
                'permits' : license.permits,
                #'prohibits' : license.prohibits,
                'libre' : license.libre,
                'license_class' : license.license_class,
                'license_code' : license.license_code,
                'uri' : license.uri}
