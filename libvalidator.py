# -*- coding: utf-8 -*-
import re, urlparse
from BeautifulSoup import BeautifulSoup

"""
f=open('tests/units/001.html', 'r')
htmlSource = f.read()
f.close()

htmlSource = htmlSource.replace('"meta"', '"alternate meta"')
"""

htmlSource = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
  PUBLIC '-//W3C//DTD XHTML+RDFa 1.0//EN'
  'http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd'>
<html xmlns="http://www.w3.org/1999/xhtml" xml:base="http://www2.example.org/">
  <head xml:base="http://www.example.org/">
    <title>
      foobar
    </title>
    <link href="metadata1.rdf" rel="meta" type="application/rdf+xml"/>
    <lINk href="" rel="meta" type="application/rdf+xml" xml:base="http://www3.example.org/"/>
    <link href="metadata1b.rdf" REl="meta" type="application/rdf+xml"/>
    <LINK HREF="#foo" REL="meta" type="application/rdf+xml">
    <link step rel="meta" type="application/rdf+xml"/>
    <link href="metadata2.rdf" rel="bookmark" type="application/rdf+xml"/>
    <link href="metadata3.rdf" rel="alternate meta" type="application/rdf+xml"/>
    <link href="metadata4.rdf" rel="meta alternate" type="application/rdf+xml"/>
  </head>
  <body>
    <div>
      foo
    </div>
  </body>
</html>
"""
headers, location = '', ''

#htmlSource = BeautifulSoup(htmlSource).prettify()
soup = BeautifulSoup(htmlSource)

"""
Find a document wide base URI (highest priority to lowest):
* the base URI is set by the BASE element - not in XHTML 2.0
* Content-Location in the HTTP header - must be passed to the library
* the location of the document itself - must be passed to the library

http://www.w3.org/TR/REC-html40/struct/links.html#h-12.4.1
http://www.w3.org/TR/xhtml2/mod-hyperAttributes.html
http://www.ietf.org/rfc/rfc2396.txt
http://www.ietf.org/rfc/rfc1808.txt
"""
element = soup.find('base', {'href': lambda(value): value is not None})
reContentLocation = re.compile('(?:^|\s+)Content\-Location\s*:\s*(\S+)', re.IGNORECASE)
search = reContentLocation.search(headers)
if element:
    base = element['href']
elif search:
    base = search.group(1)
elif location:
    base = location

"""
Find the base URI of an element (highest priority to lowest):
* the value of the codebase attribute - XHTML 1.1 and older
* the value of the xml:base attribute - XHTML 2.0
* the closest parent element that has the xml:base attribute set - XHTML 2.0
* global base URI

http://www.w3.org/TR/REC-html40/struct/objects.html#adef-codebase-OBJECT
http://www.w3.org/TR/2008/WD-html5-diff-20080610/#absent-attributes
http://www.ietf.org/rfc/rfc2396.txt
"""
def findBaseLocation(element):
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
    global base
    return base

metadataURI = []

rel = '(?:^relation)\s+|(?:^relation$)|\s+(?:relation$)'
reMeta = re.compile(rel.replace('relation', 'meta'), re.IGNORECASE)
reLicense = re.compile(rel.replace('relation', 'license'), re.IGNORECASE)
for (elements, attribute) in (
  (soup.findAll(re.compile('^(?:a|link)$', re.IGNORECASE),
                {'rel': reMeta, 'href': lambda(value): value is not None}), 'href'),
  (soup.findAll('object',
                {'data': lambda(value): value is not None}), 'data')):
    for element in elements:
        url = urlparse.urljoin(findBaseLocation(element), element[attribute])
        # check the "about" attribute of parents (RDFa)
        # actually all link and meta belong to RDFa, so this should handle
        # the object only
        if url not in metadataURI:
            metadataURI.append(url)

# migrate to minidom?

print metadataURI
