# -*- coding: utf-8 -*-
"""Query the https://opac.sbn.it service for Italian ISBN metadata.
We always ask for the first hit of the search, so if an ISBN has two
different editions (different entries in SBN with same ISBN), we will
only get the first/older one."""

import logging
import re
from isbnlib.dev import stdmeta
from isbnlib.dev._bouth23 import u
from isbnlib.dev.webquery import query as wquery

UA = 'isbnlib (gzip)'
SERVICE_URL = 'https://opac.sbn.it/sbn3.0/opaclib?db=solr_iccu&select_db=solr_iccu'\
    '&nentries=1&from=1&searchForm=opac/iccu/error.jsp&resultForward=opac/iccu/full_uni.jsp'\
    '&do_cmd=search_show_cmd&format=unimarc&rpnlabel=+ISBN+%3D+{isbn}+%28parole+in+AND%29+'\
    '&rpnquery=%40attrset+bib-1++%40attr+1%3D7+%40attr+4%3D6+%22{isbn}%22&totalResult=1&fname=none'

LOGGER = logging.getLogger(__name__)

# DICT { ISO 8859-1 char entity : HTML entity }
DICT_ISO8859_TO_HTML = {
    'À': "&Agrave;",
    'Á': "&Aacute;",
    'Â': "&Acirc;",
    'Ã': "&Atilde;",
    'Ä': "&Auml;",
    'Å': "&Aring;",
    'Æ': "&AElig;",
    'Ç': "&Ccedil;",
    'È': "&Egrave;",
    'É': "&Eacute;",
    'Ê': "&Ecirc;",
    'Ë': "&Euml;",
    'Ì': "&Igrave;",
    'Í': "&Iacute;",
    'Î': "&Icirc;",
    'Ï': "&Iuml;",
    'Ñ': "&Ntilde;",
    'Ò': "&Ograve;",
    'Ó': "&Oacute;",
    'Ô': "&Ocirc;",
    'Õ': "&Otilde;",
    'Ö': "&Ouml;",
    'Ø': "&Oslash;",
    'Ù': "&Ugrave;",
    'Ú': "&Uacute;",
    'Û': "&Ucirc;",
    'Ü': "&Uuml;",
    'Ý': "&Yacute;",
    'ß': "&szlig;",
    'à': "&agrave;",
    'á': "&aacute;",
    'â': "&acirc;",
    'ã': "&atilde;",
    'ä': "&auml;",
    'å': "&aring;",
    'æ': "&aelig;",
    'ç': "&ccedil;",
    'è': "&egrave;",
    'é': "&eacute;",
    'ê': "&ecirc;",
    'ë': "&euml;",
    'ì': "&igrave;",
    'í': "&iacute;",
    'î': "&icirc;",
    'ï': "&iuml;",
    'ð': "&eth;",
    'ñ': "&ntilde;",
    'ò': "&ograve;",
    'ó': "&oacute;",
    'ô': "&ocirc;",
    'õ': "&otilde;",
    'ö': "&ouml;",
    'ø': "&oslash;",
    'ù': "&ugrave;",
    'ú': "&uacute;",
    'û': "&ucirc;",
    'ü': "&uuml;",
    'ý': "&yacute;",
    'þ': "&thorn;",
    'ÿ': "&yuml;",
}


def cleanup_title(title):
    """Find and format title and subtitle, if present"""
    # sometimes they add spurious &lt; and &gt; html symbols:
    title = title.replace('&lt;', '').replace('&gt;', '')
    if '$e' in title:  # make first letter capital after $e
        frag = re.findall(r'\$e\D', title)[0]
        title = title.replace(frag, '$e' + frag[2].upper())
    title = title.replace('$a', '').replace('$e', '. ')
    return title


def parser_sbn(data):
    """Parse the response from the SBN service. The input data is the
    result webpage in html from the search. We request the Unimarc
    record, which contains html entities (accents such as &ograve;)
    We need to use the above dictionary to convert the html entity to
    an iso-8859-1 character.
    The Unimarc entry tends to be more complete than the MARC21 result
    in the tests we ran on SBN, that is why we chose it.
    The document link below gives the Unimarc architecture:
    https://archive.ifla.org/VI/8/unimarc-concise-bibliographic-format-2008.pdf"""

    recs = {}
    recs['Authors'] = []
    try:
        data = data.replace('\n', ' ').replace('\t', '')
        data = re.findall('<li>LEADER(.*)</ul', data)[0]
        data = re.split('<li>', data)  # split into lines for loop
        for line in data:
            # Convert html entities (like accents) to iso-8859-1:
            for isoent, htmlent in DICT_ISO8859_TO_HTML.items():
                line = line.replace(htmlent, isoent)

            # Author:
            # <li>700  1$aDi Matteo$b, Nino$3IT\ICCU\CAGV\748340</li>
            # <li>701  1$aLodato$b, Saverio$3IT\ICCU\CFIV\025147</li>
            if (re.search(r"^70", line) and len(recs['Authors']) == 0):
                # do a lazy match from $a until the first $ sign:
                surname = re.findall(r'\$a(.+?)\$', line)[0]
                name = re.findall(r'\$b(.+?)\$', line)[0]
                author = u(surname + name)
                recs['Authors'].append(author)
            # Publisher and Publication year::
            # <li>210   $aMilano$cChiarelettere$d2018</li>
            elif re.search(r"^210", line):
                publisher = re.findall(r'\$c(.+?)\$', line)[0]
                recs['Publisher'] = u(publisher)
                # sometimes there is a space between $d and the year:
                year = re.findall(r'\$d.*(\d{4})', line)[0]
                recs['Year'] = u(year)
            # Title:
            # 200 1 $aGiuro che non avrò piu fame$el'Italia della ricostruzione$fAldo Cazzullo
            # $a is the main title, $e is a subtitle and $f is author
            elif re.search(r"^200", line):
                title = re.findall(r'\$a(.*)\$f', line)[0]
                recs['Title'] = u(cleanup_title(title))
            # When the book is part of a bigger opus, the main title appears in 461, not in 200
            # 461 1$1001IT\ICCU\UBO\0079398$12001 $aIstituzioni di diritto romano$fEnzo Nardi$v1$
            elif re.search(r"^461", line):
                mtitle = re.findall(r'\$a(.+?)\$f', line)[0]
                recs['Title'] = u(cleanup_title(mtitle) + '. ' + recs['Title'])
                # Sometimes there is no author in 70X, but in 461:
                # 461 1$1001IT\ICCU\CFI\0053061$12001 $aCommedia$fDante Alighieri$ga cura di Emilio Pasquini e Antonio Quaglio$v1$1700 1$aAlighieri$b, Dante$3IT\ICCU\CFIV\008732$4070$1702 1$aPasquini$b, Emilio$f <1935- >$3IT\ICCU\CFIV\011735$1702 1$aQuaglio$b, Antonio Enzo$3IT\ICCU\CFIV\033998
                if (len(recs['Authors']) == 0
                        and re.search(r"700 1\$a", line)):
                    surname = re.findall(r'1\$a(.+?)\$b', line)
                    name = re.findall(r'\$b(.+?)\$', line)
                    for s, n in zip(surname, name):
                        recs['Authors'].append(u(s + n))
            # Language:
            # <li>101   $aita</li>
            # Sometimes there are two main languages: 101 $alat$aita
            elif re.search(r"^101", line):
                langs = re.findall(r'\$a\D\D\D', line)
                lang = ''
                for l in langs:
                    lang = l if l == langs[0] else lang + ',' + l
                lang = lang.replace('$a', '')
                recs['Language'] = u(lang)
            elif line == '':
                continue

    except IndexError:
        LOGGER.debug('Check the parsing for Italian SBN (possible error!)')
    try:
        # delete almost empty records
        if not recs['Title'] and not recs['Authors']:
            recs = {}
    except KeyError:
        recs = {}
    return recs


def _mapper(isbn, records):
    """Make records canonical.
    canonical: ISBN-13, Title, Authors, Publisher, Year, Language
    """
    # handle special case
    if not records:  # pragma: no cover
        return {}
    # add ISBN-13
    records['ISBN-13'] = u(isbn)
    # call stdmeta for extra cleaning and validation
    return stdmeta(records)


def query(isbn):
    """Query the Italian SBN service for metadata. """
    data = wquery(SERVICE_URL.format(isbn=isbn),
                  user_agent=UA,
                  parser=parser_sbn)
    if not data:  # pragma: no cover
        LOGGER.debug('No data from SBN for isbn %s', isbn)
        return {}
    return _mapper(isbn, data)
