import json
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class DtnWebsiteSale(WebsiteSale):

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(DtnWebsiteSale, self).product(product, category, search, **kwargs)
        if len(product.attribute_line_ids) != 1:
            return res
        stock_map = {}
        for variant in product.product_variant_ids:
            if len(variant.product_template_attribute_value_ids) == 1:
                ptav_id = variant.product_template_attribute_value_ids.id
                is_in_stock = variant.virtual_available > 0
                stock_map[ptav_id] = is_in_stock
        res.qcontext['dtn_stock_map_json'] = json.dumps(stock_map)
        return res