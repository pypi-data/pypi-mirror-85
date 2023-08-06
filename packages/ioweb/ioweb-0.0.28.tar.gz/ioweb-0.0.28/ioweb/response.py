from io import BytesIO
from collections import defaultdict
try:
    import ujson as json
except ImportError:
    import json

import defusedxml.lxml
import lxml.etree # pytype: disable=import-error
from selection import XpathSelector
from cssselect import HTMLTranslator
try:
    import selectolax.parser # pytype: disable=import-error
except ImportError:
    SELECTOLAX_IMPORTED = False
else:
    SELECTOLAX_IMPORTED = True


class CssSelector(XpathSelector):
    __slots__ = ()

    def process_query(self, query):
        xpath_query = HTMLTranslator().css_to_xpath(query)
        return super(CssSelector, self).process_query(xpath_query)


class Response(object):
    __slots__ = (
        '_bytes_body',
        'cert',
        'status',
        'url',
        'error',
        'headers',
        'meta',
        '_cached_lxml_dom',
        '_cached_selectolax_dom',
    )

    def __init__(self):
        self._bytes_body = None#BytesIO()
        self.headers = None
        self.cert = None
        self.status = None
        self.url = None
        self.error = None
        self.meta = {}
        self._cached_lxml_dom = None
        self._cached_selectolax_dom = None

    #def write_bytes_body(self, data):
    #    return self._bytes_body.write(data)

    @property
    def data(self):
        return self.bytes_body

    @property
    def text(self):
        return self.data.decode('utf-8', errors='ignore')

    @property
    def bytes_body(self):
        return self._bytes_body#.getvalue()

    @property
    def json(self):
        return json.loads(self.text)

    def get_content_type(self):
        if self.headers:
            return (
                self.headers.get('content-type', '').split(';')[0].strip()
            )
        else:
            return None

    def dom(self):
        if self._cached_lxml_dom is None:
            clean_data = self.data.replace(b'\x00', b'')
            res = defusedxml.lxml.parse(
                BytesIO(clean_data),
                lxml.etree.HTMLParser()
            )
            self._cached_lxml_dom = res.getroot()
        return self._cached_lxml_dom

    def xpath(self, query):
        return XpathSelector(self.dom()).select(query)

    def css(self, query):
        return CssSelector(self.dom()).select(query)

    def save(self, path):
        with open(path, 'wb') as out:
            out.write(self.data)

    def slax_dom(self):
        if not SELECTOLAX_IMPORTED:
            raise ImportError('Could not import selectolax.parser. Install selectolax package')
        else:
            if self._cached_selectolax_dom is None:
                # pytype: disable=name-error
                self._cached_selectolax_dom = selectolax.parser.HTMLParser(
                    self.data.replace(b'\x00', b'')
                )
                # pytype: enable=name-error
            return self._cached_selectolax_dom

    def slax(self, query):
        return self.slax_dom().css(query)
