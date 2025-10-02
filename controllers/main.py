import json
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class DtnWebsiteSale(WebsiteSale):

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(DtnWebsiteSale, self).product(product, category, search, **kwargs)

        stock_map = {}
        if product.attribute_line_ids:
            variants_with_sudo = product.product_variant_ids.sudo()
            for variant in variants_with_sudo:
                if len(variant.product_template_attribute_value_ids) == 1:
                    ptav_id = variant.product_template_attribute_value_ids.id
                    is_in_stock = variant.virtual_available > 0
                    stock_map[ptav_id] = is_in_stock
        
        res.qcontext['dtn_stock_map_json'] = json.dumps(stock_map)
        return res