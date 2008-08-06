# -*- coding: utf-8 -*-
import nose.tools
import urllib, re
from libvalidator import libvalidator

class TestLicenseParsing():
    def __init__(self, *args, **kargs):
        self.parser = libvalidator()
        self.license = {'name': 'Creative Commons Attribution-Noncommercial-No Derivative Works 2.0 Generic',
                        'external': 'http://creativecommons.org/licenses/by-nc-nd/2.0/',
                        'external_rdf': 'http://creativecommons.org/licenses/by-nc-nd/2.0/rdf',
                        'plain': re.sub('\s+', ' ', """\
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
""").replace('> <', '><')}
        self.license['embedded'] = 'data:application/rdf+xml,' + urllib.quote(self.license['plain'])
        # FIXME add an XHTML with an alternative RDF/XML test case
    