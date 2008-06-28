#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, re, StringIO, os
from xml.dom import minidom
from pyRdfa import _process_DOM, Options
from rdflib.Graph import ConjunctiveGraph
from rdflib.FileInputSource import FileInputSource
import rdfdiff
from rdfdiff import compare_from_string

rdfa = """\
<div xmlns:cc="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <div about="http://example.org/gnomophone.mp3" typeof="cc:Work">
    <span property="dc:title" content="Compilers in the Key of C">foo</span>
    <span property="dc:description" content="A lovely classical work on compiling code.">foo</span>
    <span rel="dc:creator"><span typeof="cc:Agent" property="dc:title" content="Yo-Yo Dyne">foo</span></span>
    <span rel="dc:rights"><span typeof="cc:Agent" property="dc:title" content="Gnomophone">foo</span></span>
    <span property="dc:date" content="1842">foo</span>
    <span property="dc:format" content="audio/mpeg">foo</span>
    <a rel="dc:type" href="http://purl.org/dc/dcmitype/Sound">foo</a>
    <a rel="dc:source" href="http://example.net/gnomovision.mov">foo</a>
    <a rel="cc:license" href="http://creativecommons.org/licenses/by-nc-nd/2.0/">foo</a>
    <a rel="cc:license" href="http://artlibre.org/licence/lal/en/">foo</a>
  </div>
  <div about="http://creativecommons.org/licenses/by-nc-nd/2.0/" typeof="cc:License">
    <a rel="cc:permits" href="http://web.resource.org/cc/Reproduction">foo</a>
    <a rel="cc:permits" href="http://web.resource.org/cc/Distribution">foo</a>
    <a rel="cc:requires" href="http://web.resource.org/cc/Notice">foo</a>
    <a rel="cc:requires" href="http://web.resource.org/cc/Attribution">foo</a>
    <a rel="cc:prohibits" href="http://web.resource.org/cc/CommercialUse">foo</a>
  </div>
</div>
"""

rdf = {'plain': """\
<rdf:RDF xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<Work rdf:about="http://example.org/gnomophone.mp3">
  <dc:title>Compilers in the Key of C</dc:title>
  <dc:description>A lovely classical work on compiling code.</dc:description>
  <dc:creator><Agent><dc:title>Yo-Yo Dyne</dc:title></Agent></dc:creator>
  <dc:rights><Agent><dc:title>Gnomophone</dc:title></Agent></dc:rights>
  <dc:date>1842</dc:date>
  <dc:format>audio/mpeg</dc:format>
  <dc:type rdf:resource="http://purl.org/dc/dcmitype/Sound" />
  <dc:source rdf:resource="http://example.net/gnomovision.mov" />
  <license rdf:resource="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
  <license rdf:resource="http://artlibre.org/licence/lal/en/" />
</Work>
<License rdf:about="http://creativecommons.org/licenses/by-nc-nd/2.0/">
  <permits rdf:resource="http://web.resource.org/cc/Reproduction" />
  <permits rdf:resource="http://web.resource.org/cc/Distribution" />
  <requires rdf:resource="http://web.resource.org/cc/Notice" />
  <requires rdf:resource="http://web.resource.org/cc/Attribution" />
  <prohibits rdf:resource="http://web.resource.org/cc/CommercialUse" />
</License>
</rdf:RDF>
"""}
rdf['embedded'] = 'data:application/rdf+xml,' + urllib.quote(rdf['plain'])
rdf['external'] = 'metadata.rdf'

output = {'prefix' : 'units/', 'id' : 0, 'suffix' : '.html'}

license = {'name' : 'Creative Commons Attribution-Noncommercial-No Derivative Works 2.0 Generic',
           'plain' : """\
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
  xmlns:cc='http://creativecommons.org/ns#'
  xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  xmlns:dc='http://purl.org/dc/elements/1.1/'
  xmlns:dcq='http://purl.org/dc/terms/'
>
  <cc:License rdf:about="http://creativecommons.org/licenses/by-nc-nd/2.0/">
    <cc:prohibits rdf:resource="http://creativecommons.org/ns#CommercialUse"/>
    <dc:title xml:lang="pt-pt">Atribuição-Uso Não-Comercial-Proibição de realização de Obras Derivadas</dc:title>
    <dc:title xml:lang="bg">Признание-Некомерсиално-Без производни</dc:title>
    <dc:title xml:lang="hr">Imenovanje-Nekomercijalno-Bez prerada</dc:title>
    <dc:title xml:lang="fr-ch">Paternité - Pas d'Utilisation Commerciale - Pas de Modification</dc:title>

    <dc:title xml:lang="en-gb">Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-cl">Atribución-NoComercial-SinDerivadas</dc:title>
    <dc:title xml:lang="pt">Atribuição-Uso Não-Comercial-Não a obras derivadas</dc:title>
    <dc:title xml:lang="zh-tw">姓名標示-非商業性-禁止改作</dc:title>
    <dc:title xml:lang="nl">Naamsvermelding-NietCommercieel-GeenAfgeleideWerken</dc:title>
    <dc:title xml:lang="it">Attribuzione - Non commerciale - Non opere derivate</dc:title>

    <dc:title xml:lang="nso">Tsebagatšo-E sego ya Kgwebo-Tše sa fetolwego</dc:title>
    <dc:title xml:lang="hu">Nevezd meg! - Ne add el! - Ne változtasd!</dc:title>
    <dc:title xml:lang="zu">Qaphela Umnikazi-Ungayisebenziseli Ezentengiselwano-Ungasuseli lutho kulokhu</dc:title>
    <dc:title xml:lang="pl">Uznanie autorstwa-Użycie niekomercyjne-Bez utworów zależnych</dc:title>
    <dc:title xml:lang="ja">表示 - 非営利 - 改変禁止</dc:title>
    <dc:title xml:lang="da">Navngivelse-IkkeKommerciel-IngenBearbejdelse</dc:title>

    <dc:title xml:lang="de">Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="en-us">Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="gl">Recoñecemento-NonComercial-SenObraDerivada</dc:title>
    <dc:title xml:lang="st">Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-ar">Atribución-NoComercial-SinDerivadas</dc:title>
    <dc:title xml:lang="fr-lu">Paternité - Pas d'Utilisation Commerciale - Pas de Modification</dc:title>

    <dc:title xml:lang="sl">Priznanje avtorstva-Nekomercialno-Brez predelav</dc:title>
    <dc:title xml:lang="af">Erkenning-NieKommersieel-GeenAfleidings</dc:title>
    <dc:title xml:lang="es">Reconocimiento-NoComercial-SinObraDerivada</dc:title>
    <dc:title xml:lang="es-pe">Reconocimiento-NoComercial-SinObraDerivada</dc:title>
    <dc:title xml:lang="fr">Paternité - Pas d'Utilisation Commerciale - Pas de Modification</dc:title>
    <dc:title xml:lang="sv">Erkännande-Ickekommersiell-IngaBearbetningar</dc:title>

    <dc:title xml:lang="ca">Reconeixement-NoComercial-SenseObraDerivada</dc:title>
    <dc:title xml:lang="ko">저작자표시-비영리-변경금지</dc:title>
    <dc:title xml:lang="ms">Pengiktirafan-BukanKomersial-TiadaTerbitan</dc:title>
    <dc:title xml:lang="mk">НаведиИзвор-Некомерцијално-БезАдаптираниДела</dc:title>
    <dc:title xml:lang="de-at">Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="it-ch">Attribuzione - Non commerciale - Non opere derivate</dc:title>

    <dc:title xml:lang="de-ch">Namensnennung-NichtKommerziell-KeineBearbeitung</dc:title>
    <dc:title xml:lang="en">Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="zh">署名-非商业性使用-禁止演绎</dc:title>
    <dc:title xml:lang="eo">Atribuo-nekomerca-neniu derivaĵo</dc:title>
    <dc:title xml:lang="en-ca">Attribution-NonCommercial-NoDerivs</dc:title>
    <dc:title xml:lang="es-co">Reconocimiento-NoComercial-SinObraDerivada</dc:title>

    <dc:title xml:lang="fr-ca">Paternité - Pas d'Utilisation Commerciale - Pas de Modification</dc:title>
    <dc:title xml:lang="he">ייחוס-שימוש לא מסחרי-איסור יצירות נגזרות</dc:title>
    <dc:title xml:lang="fi">Nimeä-Ei muutoksia-Epäkaupallinen</dc:title>
    <dc:title xml:lang="eu">Aitortu-EzKomertziala-LanEratorririkGabe</dc:title>
    <dc:title xml:lang="es-mx">Atribución-No Comercial-No Derivadas</dc:title>
    <dc:creator rdf:resource="http://creativecommons.org"/>

    <cc:requires rdf:resource="http://creativecommons.org/ns#Notice"/>
    <cc:requires rdf:resource="http://creativecommons.org/ns#Attribution"/>
    <cc:permits rdf:resource="http://creativecommons.org/ns#Distribution"/>
    <cc:permits rdf:resource="http://creativecommons.org/ns#Reproduction"/>
    <cc:legalcode rdf:resource="http://creativecommons.org/licenses/by-nc-nd/2.0/legalcode"/>
    <dcq:hasVersion>2.0</dcq:hasVersion>
    <dcq:isReplacedBy rdf:resource="http://creativecommons.org/licenses/by-nc-nd/2.5/"/>
  </cc:License>

</rdf:RDF>
"""}
license['embedded'] = 'data:application/rdf+xml,' + urllib.quote(license['plain'])
license['external'] = 'http://creativecommons.org/licenses/by-nc-nd/2.0/'
license['external_rdf'] = 'http://creativecommons.org/licenses/by-nc-nd/2.0/rdf'

metadata = [{'DC.rights.accessRights' : 'Available to subscribers only.',
             'DC.rights.license' : license['external'],
             'DC.rights' : 'Available to subscribers only under ' + license['name'],
             'DC.rightsHolder' : 'Joe Bloggs'},
            {'DC.rights.accessRights' : 'Available to subscribers only.',
             'DC.rights.license' : license['external'],
             'DC.rightsHolder' : 'http://www.example.com/Staff/JoeBloggs'}]

template = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>foobar</title>
  </head>
  <body>
    <div>foo</div>
  </body>
</html>
"""

template = re.sub('\s+', ' ', template).replace('> <', '><')

if not os.path.exists(output['prefix']):
    os.mkdir(output['prefix'])

f = open(output['prefix']+rdf['external'], 'w')
f.write(rdf['plain'])
f.close()

d = minidom.parseString(template)

""" append """
def append(elementName, mountPoint='head', attributes={}, textContent=None):
    global d
    element = d.createElement(elementName)
    for attributeName in attributes.keys():
        element.setAttribute(attributeName, attributes[attributeName])
    if textContent is not None:
        element.appendChild(d.createTextNode(textContent))
    elif elementName == 'a':
        element.appendChild(d.createTextNode('bar'))
    d.getElementsByTagName(mountPoint).item(0).appendChild(element)
    return element

""" dispatch """
def dispatch():
    global output, d, template
    output['id'] += 1
    f = open(output['prefix']+str(output['id']).zfill(3)+output['suffix'], 'w')
    f.write(d.toprettyxml(indent="  ", encoding='UTF-8')+"\n")
    f.close()
    d = minidom.parseString(template)

""" enhance with the Dublin Core profile """
def dc():
    global d
    d.getElementsByTagName('head').item(0).setAttribute('profile', 'http://dublincore.org/documents/dcq-html/')
    append('link', 'head', {'rel' : 'schema.DC', 'href' : 'http://purl.org/dc/elements/1.1/'})

""" shorthand """
def s(*args, **kw):
    append(*args, **kw)
    dispatch()

"""
Assuming:
<head profile="http://dublincore.org/documents/dcq-html/">
<link rel="schema.DC" href="http://purl.org/dc/elements/1.1/" />
we have:
<meta name="DC.rights" scheme="DCTERMS.URI" href="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
<meta name="DC.rights.license" scheme="DCTERMS.URI" href="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
<link rel="DC.rights" href="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
<link rel="DC.rights.license" href="http://creativecommons.org/licenses/by-nc-nd/2.0/" />

What is possible:
<meta name="License" value="Creative Commons Attribution 2.5 Poland" />
<meta name="License" value="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
<meta name="License_URI" value="http://creativecommons.org/licenses/by-nc-nd/2.0/" />
"""

# rel="meta" and an external RDF
s('link', 'head', {'rel' : 'meta', 'type' : 'application/rdf+xml', 'href' : rdf['external']})
s('a', 'div', {'rel' : 'meta', 'type' : 'application/rdf+xml', 'href' : rdf['external']})

# rel="meta" and the "data:" URL scheme
s('link', 'head', {'rel' : 'meta', 'type': 'application/rdf+xml', 'href' : rdf['embedded']})
s('a', 'div', {'rel' : 'meta', 'type' : 'application/rdf+xml', 'href' : rdf['embedded']})

# rel="license" and an external Web page
s('link', 'head', {'rel' : 'license', 'href' : license['external']})
s('a', 'div', {'rel' : 'license', 'href' : license['external']})

# rel="license" and an external RDF
s('link', 'head', {'rel' : 'license', 'type' : 'application/rdf+xml', 'href' : license['external_rdf']})
s('a', 'div', {'rel' : 'license', 'type' : 'application/rdf+xml', 'href' : license['external_rdf']})

# rel="license" and the "data:" URL scheme
s('link', 'head', {'rel' : 'license', 'type' : 'application/rdf+xml', 'href' : license['embedded']})
s('a', 'div', {'rel' : 'license', 'type' : 'application/rdf+xml', 'href' : license['embedded']})

# RDF in an object
s('object', 'div', {'type' : 'application/rdf+xml', 'href' : rdf['external']})
s('object', 'div', {'type' : 'application/rdf+xml', 'href' : rdf['embedded']})

# RDF in a comment
d.appendChild(d.createComment(rdf['plain']))
dispatch()

# RDF embedded directly
element = re.sub('\s+', ' ', rdf['plain']).replace('> <', '><')
d.getElementsByTagName('head').item(0).appendChild(d.importNode(minidom.parseString(element).documentElement, True))
dispatch()
d.getElementsByTagName('div').item(0).appendChild(d.importNode(minidom.parseString(element).documentElement, True))
dispatch()

# RDFa
d.getElementsByTagName('div').item(0).appendChild(d.importNode(minidom.parseString(rdfa).documentElement, True))
dispatch()

"""
Check the isomorphism

d.getElementsByTagName('div').item(0).appendChild(d.importNode(minidom.parseString(rdfa).documentElement, True))
rdfa = d.toxml(encoding='UTF-8')+"\n"

store = ConjunctiveGraph()
store.load(FileInputSource(StringIO.StringIO(rdf['plain']))) 
rdf01 = store.serialize(format='nt')

options = Options(warnings=True)
rdf02 = _process_DOM(d, '', 'nt', options)

print rdfdiff.compare_from_string(rdf01, rdf02)
"""
