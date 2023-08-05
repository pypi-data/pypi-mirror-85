from xml.dom.minidom import parseString
import dicttoxml

from .base import ApiBling


class Order(ApiBling):

    def __init__(self, api_key):
        self.api = super(Order, self).__init__(api_key)
        self.order = {}
        self.items = []
        self.client = {}
        self.shipping = {}

    def add_item(self, **kwargs):
        self.items.append(kwargs)

    def get_xml(self):
        obj = self.order
        obj.update({
            'cliente': self.client,
            'itens': self.items,
            'transporte': self.shipping
        })
        item_dict = {
            'volumes': 'volume',
            'itens': 'item'
        }

        xml_snippet = dicttoxml.dicttoxml(
            obj,
            item_func=lambda x: item_dict.get(x),
            custom_root='pedido',
            attr_type=False)
        dom = parseString(xml_snippet)
        return dom.toprettyxml()

    def create_order(self, gen_nfe=False):
        uri = '/pedido'
        payload = {
            'xml': self.get_xml(),
            'gerarnfe': gen_nfe
        }
        return self._make_request('POST', uri, data=payload)
