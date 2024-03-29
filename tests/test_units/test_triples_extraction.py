# -*- coding: utf-8 -*-
"""Unit tests.

Copyright (C) 2008, 2009, 2010 Robert Gust‐Bardon and Creative Commons.
Originally contributed by Robert Gust‐Bardon.

This file is part of the License Validation Library.

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
__credits__ = ["Robert Gust-Bardon"]
__license__ = ("GNU Lesser General Public License Version 3 "
               "or any later version")
__version__ = "0.1.0"
__maintainer__ = "Robert Gust‐Bardon"
__status__ = "Beta"

import nose.tools
import urllib, re, os
from urlparse import urljoin
from libvalidator import libvalidator
from xml.dom import minidom
from pyRdfa import _process_DOM, Options

class TestTriplesExtraction():

    def __init__(self, *args, **kargs):
        self.parser = libvalidator()
        self.baseURI = 'tests/test_units/test.html'
        self.rdfa = re.sub('\s+', ' ', """\
<div xmlns:cc="http://web.resource.org/cc/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <div about="http://example.org/gnomophone.mp3" typeof="cc:Work">
    <span property="dc:title"
          content="Compilers in the Key of C">foo</span>
    <span property="dc:description"
          content="A lovely classical work on compiling code."
    >foo</span>
    <span rel="dc:creator"><span typeof="cc:Agent" property="dc:title"
                                 content="Yo-Yo Dyne">foo</span></span>
    <span rel="dc:rights"><span typeof="cc:Agent" property="dc:title"
                                 content="Gnomophone">foo</span></span>
    <span property="dc:date" content="1842">foo</span>
    <span property="dc:format" content="audio/mpeg">foo</span>
    <a rel="dc:type" href="http://purl.org/dc/dcmitype/Sound">foo</a>
    <a rel="dc:source"
       href="http://example.net/gnomovision.mov">foo</a>
    <a rel="cc:license"
       href="http://creativecommons.org/licenses/by-nc-nd/2.0/">foo</a>
    <a rel="cc:license"
       href="http://artlibre.org/licence/lal/en/">foo</a>
  </div>
  <div about="http://creativecommons.org/licenses/by-nc-nd/2.0/"
       typeof="cc:License">
    <a rel="cc:permits"
       href="http://web.resource.org/cc/Reproduction">foo</a>
    <a rel="cc:permits"
       href="http://web.resource.org/cc/Distribution">foo</a>
    <a rel="cc:requires"
       href="http://web.resource.org/cc/Notice">foo</a>
    <a rel="cc:requires"
       href="http://web.resource.org/cc/Attribution">foo</a>
    <a rel="cc:prohibits"
       href="http://web.resource.org/cc/CommercialUse">foo</a>
  </div>
</div>
""").replace('> <', '><')
        self.rdf = {'external': 'metadata.rdf',
                    'plain': re.sub('\s+', ' ', """\
<rdf:RDF xmlns="http://web.resource.org/cc/"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <Work rdf:about="http://example.org/gnomophone.mp3">
    <dc:title>Compilers in the Key of C</dc:title>
    <dc:description
      >A lovely classical work on compiling code.</dc:description>
    <dc:creator><Agent><dc:title
      >Yo-Yo Dyne</dc:title></Agent></dc:creator>
    <dc:rights><Agent><dc:title
      >Gnomophone</dc:title></Agent></dc:rights>
    <dc:date>1842</dc:date>
    <dc:format>audio/mpeg</dc:format>
    <dc:type rdf:resource="http://purl.org/dc/dcmitype/Sound" />
    <dc:source rdf:resource="http://example.net/gnomovision.mov" />
    <license
      rdf:resource="http://creativecommons.org/licenses/by-nc-nd/2.0/"
    />
    <license rdf:resource="http://artlibre.org/licence/lal/en/" />
  </Work>
  <License
    rdf:about="http://creativecommons.org/licenses/by-nc-nd/2.0/">
    <permits rdf:resource="http://web.resource.org/cc/Reproduction" />
    <permits rdf:resource="http://web.resource.org/cc/Distribution" />
    <requires rdf:resource="http://web.resource.org/cc/Notice" />
    <requires rdf:resource="http://web.resource.org/cc/Attribution" />
    <prohibits
      rdf:resource="http://web.resource.org/cc/CommercialUse" />
  </License>
</rdf:RDF>
""").replace('> <', '><')}
        self.rdf['embedded'] = 'data:application/rdf+xml,' + \
                               urllib.quote(self.rdf['plain'])
        self.license = {
            'name':
                 'Creative Commons Attribution-Noncommercial-'
                 'No Derivative Works 2.0 Generic',
            'external':
                 'http://creativecommons.org/licenses/by-nc-nd/2.0/',
            'external_rdf':
                 'http://creativecommons.org/licenses/by-nc-nd/2.0/rdf',
            'plain': re.sub('\s+', ' ', """\
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
  xmlns:cc='http://creativecommons.org/ns#'
  xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  xmlns:dc='http://purl.org/dc/elements/1.1/'
  xmlns:dcq='http://purl.org/dc/terms/'
>
  <cc:License
    rdf:about="http://creativecommons.org/licenses/by-nc-nd/2.0/">
    <cc:prohibits
      rdf:resource="http://creativecommons.org/ns#CommercialUse"/>
    <dc:title xml:lang="pt-pt"
      >Atribuição-Uso Não-Comercial-Proibição de realização <!--
      -->de Obras Derivadas</dc:title>
    <dc:title xml:lang="bg"
      >Признание-Некомерсиално-Без производни</dc:title>
    <dc:title xml:lang="hr"
      >Imenovanje-Nekomercijalno-Bez prerada</dc:title>
    <dc:title xml:lang="fr-ch"
      >Paternité - Pas d'Utilisation Commerciale - <!--
      -->Pas de Modification</dc:title>

    <dc:title xml:lang="en-gb"
      >Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-cl"
      >Atribución-NoComercial-SinDerivadas</dc:title>
    <dc:title xml:lang="pt"
      >Atribuição-Uso Não-Comercial-Não a obras derivadas</dc:title>
    <dc:title xml:lang="zh-tw">姓名標示-非商業性-禁止改作</dc:title>
    <dc:title xml:lang="nl"
      >Naamsvermelding-NietCommercieel-GeenAfgeleideWerken</dc:title>
    <dc:title xml:lang="it"
      >Attribuzione - Non commerciale - Non opere derivate</dc:title>

    <dc:title xml:lang="nso"
      >Tsebagatšo-E sego ya Kgwebo-Tše sa fetolwego</dc:title>
    <dc:title xml:lang="hu"
      >Nevezd meg! - Ne add el! - Ne változtasd!</dc:title>
    <dc:title xml:lang="zu"
      >Qaphela Umnikazi-Ungayisebenziseli <!--
      -->Ezentengiselwano-Ungasuseli lutho kulokhu</dc:title>
    <dc:title xml:lang="pl"
      >Uznanie autorstwa-Użycie niekomercyjne-<!--
      -->Bez utworów zależnych</dc:title>
    <dc:title xml:lang="ja">表示 - 非営利 - 改変禁止</dc:title>
    <dc:title xml:lang="da"
      >Navngivelse-IkkeKommerciel-IngenBearbejdelse</dc:title>

    <dc:title xml:lang="de"
      >Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="en-us"
      >Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="gl"
      >Recoñecemento-NonComercial-SenObraDerivada</dc:title>
    <dc:title xml:lang="st"
      >Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-ar"
      >Atribución-NoComercial-SinDerivadas</dc:title>
    <dc:title xml:lang="fr-lu"
      >Paternité - Pas d'Utilisation Commerciale - <!--
      -->Pas de Modification</dc:title>

    <dc:title xml:lang="sl"
      >Priznanje avtorstva-Nekomercialno-Brez predelav</dc:title>
    <dc:title xml:lang="af"
      >Erkenning-NieKommersieel-GeenAfleidings</dc:title>
    <dc:title xml:lang="es"
      >Reconocimiento-NoComercial-SinObraDerivada</dc:title>
    <dc:title xml:lang="es-pe"
      >Reconocimiento-NoComercial-SinObraDerivada</dc:title>
    <dc:title xml:lang="fr"
      >Paternité - Pas d'Utilisation Commerciale - <!--
      -->Pas de Modification</dc:title>
    <dc:title xml:lang="sv"
      >Erkännande-Ickekommersiell-IngaBearbetningar</dc:title>

    <dc:title xml:lang="ca"
      >Reconeixement-NoComercial-SenseObraDerivada</dc:title>
    <dc:title xml:lang="ko">저작자표시-비영리-변경금지</dc:title>
    <dc:title xml:lang="ms"
      >Pengiktirafan-BukanKomersial-TiadaTerbitan</dc:title>
    <dc:title xml:lang="mk"
      >НаведиИзвор-Некомерцијално-БезАдаптираниДела</dc:title>
    <dc:title xml:lang="de-at"
      >Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="it-ch"
      >Attribuzione - Non commerciale - Non opere derivate</dc:title>

    <dc:title xml:lang="de-ch"
      >Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="en"
      >Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="zh">署名-非商业性使用-禁止演绎</dc:title>
    <dc:title xml:lang="eo">Atribuo-nekomerca-neniu derivaĵo</dc:title>
    <dc:title xml:lang="en-ca"
      >Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-co"
      >Reconocimiento-NoComercial-SinObraDerivada</dc:title>

    <dc:title xml:lang="fr-ca"
      >Paternité - Pas d'Utilisation Commerciale - <!--
      -->Pas de Modification</dc:title>
    <dc:title
      xml:lang="he">ייחוס-שימוש לא מסחרי-איסור יצירות נגזרות</dc:title>
    <dc:title xml:lang="fi"
      >Nimeä-Ei muutoksia-Epäkaupallinen</dc:title>
    <dc:title xml:lang="eu"
      >Aitortu-EzKomertziala-LanEratorririkGabe</dc:title>
    <dc:title xml:lang="es-mx"
      >Atribución-No Comercial-No Derivadas</dc:title>
    <dc:creator rdf:resource="http://creativecommons.org"/>

    <cc:requires rdf:resource="http://creativecommons.org/ns#Notice"/>
    <cc:requires
      rdf:resource="http://creativecommons.org/ns#Attribution"/>
    <cc:permits
      rdf:resource="http://creativecommons.org/ns#Distribution"/>
    <cc:permits
      rdf:resource="http://creativecommons.org/ns#Reproduction"/>
    <cc:legalcode rdf:resource=
      "http://creativecommons.org/licenses/by-nc-nd/2.0/legalcode"/>
    <dcq:hasVersion>2.0</dcq:hasVersion>
    <dcq:isReplacedBy rdf:resource=
      "http://creativecommons.org/licenses/by-nc-nd/2.5/"/>
  </cc:License>

</rdf:RDF>
""").replace('> <', '><')}
        self.license['embedded'] = \
            'data:application/rdf+xml,' + \
            urllib.quote(self.license['plain'])
        self.metadata = \
            [{'DC.rights.accessRights': 'Available to subscribers only.',
              'DC.rights.license': self.license['external'],
              'DC.rights': 'Available to subscribers only under ' + \
                           self.license['name'],
              'DC.rightsHolder': 'Joe Bloggs'},
             {'DC.rights.accessRights': 'Available to subscribers only.',
              'DC.rights.license': self.license['external'],
              'DC.rightsHolder': 'http://www.example.com/Staff/JoeBloggs'}]
        self.template = re.sub('\s+', ' ', """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN"
                      "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>foobar</title>
  </head>
  <body>
    <div>foo</div>
  </body>
</html>
""").replace('> <', '><')
        f = open(urljoin(self.baseURI, self.rdf['external']), 'w')
        f.write(self.rdf['plain'])
        f.close()

    def __del__(self):
        path = urljoin(self.baseURI, self.rdf['external'])
        if os.path.exists(path):
            os.remove(path)

    def document_reset(self):
        self.document = minidom.parseString(self.template)

    def document_append(self, elementName, mountPoint='head',
                              attributes={}, textContent=None):
        element = self.document.createElement(elementName)
        for attributeName in attributes.keys():
            element.setAttribute(attributeName, attributes[attributeName])
        if textContent is not None:
            element.appendChild(self.document.createTextNode(textContent))
        elif elementName == 'a':
            element.appendChild(self.document.createTextNode('bar'))
        self.document.getElementsByTagName(mountPoint).item(0).\
             appendChild(element)
        return element

    def document_profile(self):
        head = self.document.getElementsByTagName('head').item(0)
        head.setAttribute('profile',
                          'http://dublincore.org/documents/dcq-html/')
        link = self.document.createElement('link')
        link.setAttribute('rel', 'schema.DC')
        link.setAttribute('href', 'http://purl.org/dc/elements/1.1/')
        children = head.getElementsByTagName('*')
        if (children.length > 0):
            head.insertBefore(link, children.item(0))
        else:
            head.appendChild(link)

    def parse(self):
        self.result = self.parser.parse(self.document.toxml(), self.baseURI,
                                        None, True)

    def assert_external(self):
        assert 'http://artlibre.org/licence/lal/en/' in \
               self.result['licensedObjects']\
                          ['http://example.org/gnomophone.mp3'] \
           and 'http://creativecommons.org/licenses/by-nc-nd/2.0/' in \
               self.result['licensedObjects']\
                          ['http://example.org/gnomophone.mp3']

    def test_a_meta_embedded(self):
        self.document_reset()
        self.document_append('a', 'div', 
                             {'rel': 'meta', 'type': 'application/rdf+xml',
                              'href': self.rdf['embedded']})
        self.parse()
        self.assert_external()

    def test_a_meta_external(self):
        self.document_reset()
        self.document_append('a', 'div',
                             {'rel': 'meta', 'type': 'application/rdf+xml',
                              'href': self.rdf['external']})
        self.parse()
        self.assert_external()

    def test_link_meta_embedded(self):
        self.document_reset()
        self.document_append('link', 'head',
                             {'rel': 'meta', 'type': 'application/rdf+xml',
                              'href': self.rdf['embedded']})
        self.parse()
        self.assert_external()

    def test_link_meta_external(self):
        self.document_reset()
        self.document_append('link', 'head',
                             {'rel': 'meta', 'type': 'application/rdf+xml',
                              'href': self.rdf['external']})
        self.parse()
        self.assert_external()

    def test_meta_dc_meta_name(self):
        self.document_reset()
        self.document_profile()
        for k, v in self.metadata[0].iteritems():
            options = {'name': k, 'content': v}
            if v.startswith('http://'):
                options['scheme'] = 'DCTERMS.URI'
            self.document_append('meta', 'head', options)
        self.parse()
        assert 'Available to subscribers only under Creative Commons '
               'Attribution-Noncommercial-No Derivative Works 2.0 '
               'Generic' in self.result['licensedObjects'][self.baseURI] \
           and 'http://creativecommons.org/licenses/by-nc-nd/2.0/' in \
               self.result['licensedObjects'][self.baseURI]

    def test_meta_dc_link_link(self):
        self.document_reset()
        self.document_profile()
        for k, v in self.metadata[1].iteritems():
            if v.startswith('http://'):
                options = {'rel': k, 'href': v}
                self.document_append('link', 'head', options)
            else:
                options = {'name': k, 'content': v}
                self.document_append('meta', 'head', options)
        self.parse()
        assert 'http://creativecommons.org/licenses/by-nc-nd/2.0/' in \
               self.result['licensedObjects'][self.baseURI]

    def test_rdfxml_element(self):
        self.document_reset()
        self.document.getElementsByTagName('head').item(0).\
             appendChild(self.document.importNode(
                 minidom.parseString(self.rdf['plain']).documentElement, True)
             )
        self.parse()
        self.assert_external()

    def test_rdfxml_comment(self):
        self.document_reset()
        self.document.appendChild(
            self.document.createComment(self.rdf['plain'])
        )
        self.parse()
        self.assert_external()

    def test_rdfa(self):
        self.document_reset()
        self.document.getElementsByTagName('div').item(0).\
             appendChild(self.document.importNode(
                 minidom.parseString(self.rdfa).documentElement, True)
             )
        self.parse()
        self.assert_external()

