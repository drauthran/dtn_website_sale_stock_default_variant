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
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
        # Мы получаем варианты с правами суперпользователя, чтобы обойти проверку прав доступа для гостей
        variants_with_sudo = product.product_variant_ids.sudo()
        
        # Теперь итерируем по вариантам, полученным через .sudo()
        for variant in variants_with_sudo:
            if len(variant.product_template_attribute_value_ids) == 1:
                ptav_id = variant.product_template_attribute_value_ids.id
                # Теперь это поле будет вычислено без ошибок доступа
                is_in_stock = variant.virtual_available > 0
                stock_map[ptav_id] = is_in_stock
        
        res.qcontext['dtn_stock_map_json'] = json.dumps(stock_map)
        return res