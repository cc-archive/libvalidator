# -*- coding: utf-8 -*-
"""The core of the library.

Copyright (C) 2008, 2009, 2010 Robert Gust‐Bardon and Creative Commons.
Originally contributed by Robert Gust‐Bardon.

This file is a part of the License Validation Library.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Robert Gust‐Bardon and Creative Commons"
__copyright__ = ("Copyright 2008, 2009, 2010 "
                 "Robert Gust‐Bardon and Creative Commons")
__credits__ = ["Robert Gust‐Bardon", "Asheesh Laroia"]
__license__ = ("GNU Lesser General Public License Version 3 "
               "or any later version")
__version__ = "0.1.0"
__maintainer__ = "Robert Gust‐Bardon"
__status__ = "Beta"

import re, os, urlparse, urllib
from xml.dom import minidom
import html5lib
from html5lib import treebuilders
from pyRdfa import _process_DOM, Options
from pyRdfa.transform.DublinCore import DC_transform
import rdflib
import cc.license

class URLOpener(urllib.FancyURLopener):
    """Prevent the validation of Web pages that serve as an HTTP 404
       message."""

    def http_error_404(*args, **kwargs):
        raise IOError


class libvalidator(object):
    """Extract license information."""

    def __init__(self, *args, **kargs):
        """The constructor."""
        # Namespaces that will be used in the SPARQL queries
        self.namespaces = {
            'old': rdflib.Namespace('http://web.resource.org/cc/'),
            'cc': rdflib.Namespace('http://creativecommons.org/ns#'),
            'dc': rdflib.Namespace('http://purl.org/dc/elements/1.1/'),
            'xhv': rdflib.Namespace('http://www.w3.org/1999/xhtml/vocab#')
        }
        # The base IRI of the document that is being parsed
        self.base = ''
        # The headers that were sent along with the document that is
        # being parsed
        self.headers = None
        # The location of the document that is being parsed
        self.location = None
        # The outcome of parsing
        self.result = {
            'licensedObjects': {}, # FIXME misleading name (subject)
            'licenses': {},
            'deprecated': False
        }

    def findBaseDocument(self):
        """Establish the IRI that will be used when the translation of
           a relative IRI into an absolute IRI will occur."""
        # FIXME There is no support for CURIEs.
        # FIXME There is no support for ``xml:base``.
        for e in self.dom.getElementsByTagName('base'):
            if e.hasAttribute('href'):
                self.base = e.getAttribute('href')
                return
        if self.headers is not None:
            header = self.headers.get('Content-Location')
            if header is not None:
                self.base = unicode(header)
                return
        self.base = self.location

    def formDocument(self, code):
        """Parse the source code written in RDF/XML, HTML, or XHTML in
           order to obtain a DOM tree."""
        # Translate CDATA blocks into PCDATA blocks.
        reCDATA = re.compile(r'<!\[CDATA\[((?:[^\]]+|\](?!\]>))*)\]\]>')
        for m in re.finditer(reCDATA, code):
            code = code.replace(m.group(0), m.group(1).replace('&', '&amp;') \
                                                      .replace('<', '&lt;') \
                                                      .replace('>', '&gt;'))
        # Try to construct a DOM tree using xml.dom.minidom and, if
        # that fails, fall back to using html5lib.HTMLParser to
        # accomplish the goal.
        dom = None
        try:
            dom = minidom.parseString(code)
        except:
            parser = html5lib.HTMLParser(
                         tree=treebuilders.getTreeBuilder('dom')
                     )
            dom = parser.parse(code)
        return (dom, dom.toxml())

    def extractLicensedObjects(self, code, base):
        """Extract licensed object from documents written in RDF/XML."""
        # FIXME When it comes to RDF, the name of method is misleading,
        #       because subjects are licensed, not objects (cf. the RDF
        #       triple).
        # FIXME The base IRI is not used at all in this method.
        # Obtain a DOM tree and a well-formed document given a
        # document written in RDF/XML.
        (dom, code) = self.formDocument(code)
        # Obtain a graph from the DOM tree.
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(code.encode('utf-8')))
        # Perform a SPARQL query looking for relations which state that
        # a subject is licensed.
        # FIXME Should dc:license be supported?
        for row in graph.query(
            'SELECT ?a ?b WHERE {'
              '{ ?a old:license ?b }'
            ' UNION '
              '{ ?a cc:license ?b }'
            ' UNION '
              '{ ?a xhv:license ?b }'
            ' UNION '
              '{ ?a dc:rights ?b }'
            ' UNION '
              '{ ?a dc:rights.license ?b }'
            '}',
            initNs = dict(
                         old = self.namespaces['old'],
                         cc = self.namespaces['cc'],
                         dc = self.namespaces['dc'],
                         xhv = self.namespaces['xhv'])
                     ):
            # Each row (the result) contains a pair consisting of a
            # subject and an object.
            # Create an empty list for the licensing information on a
            # given subject, should no information already exist.
            if not self.result['licensedObjects'].has_key(str(row[0])):
                self.result['licensedObjects'][str(row[0])] = []
            # Case 1: the object is a blank node.
            if isinstance(row[1], rdflib.BNode):
                # FIXME Fish for interesting data (e.g. cc:Agent).
                """
                triples = []
                for r in graph.query('SELECT ?a ?b WHERE { '+
                                     row[1].n3()+' ?a ?b }'):
                    triples.append((str(r[0]), str(r[1])))
                self.result['licensedObjects'][str(row[0])].append(triples)
                """
                pass
            # Case 2: the object is an RDF URI reference.
            elif isinstance(row[1], rdflib.URIRef):
                # Check if the information has not already appeared.
                if str(row[1]) not in \
                   self.result['licensedObjects'][str(row[0])]:
                    self.result['licensedObjects'][str(row[0])].\
                         append(str(row[1]))
                    # Retrieve information about the license stated
                    # using the object, if this license has not
                    # appeared earlier.
                    if not self.result['licenses'].has_key(str(row[1])):
                        license = self.parseLicense(str(row[1]))
                        # Check if any information about the license
                        # stated by the object has been retrieved
                        if license != str(row[1]):
                            # Store the information about the retrieved
                            # license
                            self.result['licenses'][str(row[1])] = \
                                self.parseLicense(str(row[1]))
            # Case 3: the object is a literal.
            else:
                self.result['licensedObjects'][str(row[0])].\
                     append(str(row[1]))

    def parse(self, code, location = None, headers = None,
              openLocalFiles = False):
        """Parse the source code in order to retrieve statements
           referring to licensed subjects."""
        # Use the default location, if none is given.
        if location is not None:
            self.location = location
        # Use the default headers, if none are given.
        if headers is not None:
            self.headers = headers
        # Parse the source code and obtains a DOM tree and well-formed
        # source code without any CDATA blocks.
        (self.dom, self.code) = self.formDocument(code)
        # Establish the base IRI for the document.
        self.findBaseDocument()
        # The following list stores all the documents written in
        # RDF/XML that are meant to be processed in order to retrieve
        # license information.
        sources = []
        # Find parts of the document (be it elements or comments) that
        # contain RDF/XML.
        reRDF = re.compile(
            # <rdf:RDF
            '<([^\s<>]+)'
            # xmlns:dc="http://purl.org/dc/elements/1.1/"
            '\s+(?:[^>]+\s+)?'
            # xmlns
            'xmlns'
            # :rdf
            '(?::[^=]+)?'
            # =
            '\s*=\s*'
            # "http://www\.w3\.org/1999/02/22-rdf-syntax-ns#"
            '(?:'
              '("http://www\.w3\.org/1999/02/22-rdf-syntax-ns#")'
            '|'
              '(\'http://www\.w3\.org/1999/02/22\-rdf\-syntax\-ns#\')'
            ')'
            # ><Work rdf:about="http://foo.bar/">...</Work>
            '.*?'
            # </rdf:RDF>
            '</\\1\s*>'
            , re.DOTALL)
        for m in re.finditer(reRDF, code):
            sources.append([self.base, m.group(0)])
            # FIXME The element should only be classified as
            #       deprecated in case it actually contains license
            #       information.
            # Note: this bug was discovered in February 2009 thanks to
            #       Mr. Hans Loepfe.
            self.result['deprecated'] = True
        # Obtain the RDF triples (written in RDF/XML) from the original
        # document.
        dump = _process_DOM(self.dom, self.location, 'xml',
                            Options(warnings = False,
                                    transformers = [DC_transform]))
        # Obtain a graph from the document written using the RDF/XML
        # notation.
        graph = rdflib.ConjunctiveGraph()
        graph.parse(rdflib.StringInputSource(dump), format='xml')
        # Append the document written in RDF/XML to the list of
        # documents to be processed.
        sources.append([self.base, graph.serialize(format='xml')])
        # Iterate over the objects that provide metadata about the
        # document that is being analysed.
        for row in graph.query('SELECT ?b WHERE { ?a xhv:meta ?b . }',
                               initNs = dict(xhv = self.namespaces['xhv'])):
            # Try to retrieve the resource.
            try:
                reHyperlink = re.compile(
                                  '^(?:data:|((ftp|gopher|https?)://))\S+$',
                                  re.IGNORECASE
                              )
                if openLocalFiles == True or \
                   reHyperlink.search(row[0]) is not None:
                    f = URLOpener().open(row[0])
                    # FIXME No Internet media type detection is
                    #       performed (it is assumed that the document
                    #       is written using the RDF/XML notation).
                    if not unicode(row[0]).startswith('data:'):
                        # FIXME The Content-Location HTTP header is
                        #       ignored.
                        sources.append([str(row[0]), f.read()])
                    else:
                        sources.append([self.base, f.read()])
            except IOError:
                pass
        # Extract the license information from all the collected
        # documents written in RDF/XML.
        for (base, source) in sources:
            self.extractLicensedObjects(source, base)
        return self.result

    def parseLicense(self, iri):
        """Employ cc.license in order to obtain additional information
           about a license that is stated using an IRI."""
        try:
            license = cc.license.selectors.choose('standard').by_uri(iri)
        except cc.license.CCLicenseError, err:
            # Return the original IRI, should no data on the license
            # be available through cc.license.
            return iri
        # Note: ``requires``, ``permits``, and ``prohibits`` were
        #       originally not used due to a bug in cc.license.
        return {'title' : license.title(),
                'description' : license.description(),
                'jurisdiction' : license.jurisdiction,
                'current_version' : license.current_version,
                'version' : license.version,
                'superseded' : license.superseded,
                'deprecated' : license.deprecated,
                'requires' : license.requires,
                'permits' : license.permits,
                'prohibits' : license.prohibits,
                'libre' : license.libre,
                'license_class' : license.license_class,
                'license_code' : license.license_code,
                'uri' : license.uri}

