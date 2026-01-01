# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class DtnWebsiteSale(WebsiteSale):

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        # 1. Виклик батьківського методу
        res = super(DtnWebsiteSale, self).product(product, category, search, **kwargs)

        # Перевірка, чи це рендер сторінки
        if not hasattr(res, 'qcontext'):
            return res

        # 2. Логіка АВТО-ВИБОРУ (Серверний редирект)
        if not request.params.get('product_id'):
            current_variant = res.qcontext.get('product_variant')
            
            # ВИПРАВЛЕНО: Використовуємо free_qty (реально доступна кількість), а не virtual_available (прогноз)
            # Якщо поточного варіанту немає в наявності (або він зарезервований)
            if current_variant and current_variant.sudo().free_qty <= 0:
                # Шукаємо варіанти, де free_qty > 0
                available_variants = product.product_variant_ids.sudo().filtered(lambda v: v.free_qty > 0)
                
                if available_variants:
                    first_available = available_variants[0]
                    if first_available.id != current_variant.id:
                        product_url = f"/shop/product/{product.id}?product_id={first_available.id}"
                        return request.redirect(product_url)

        # 3. Збір даних для візуалізації (Frontend)
        stock_map = {}
        if product.attribute_line_ids:
            variants_with_sudo = product.product_variant_ids.sudo()
            for variant in variants_with_sudo:
                # ВИПРАВЛЕНО: Варіант вважається "в наявності", тільки якщо він реально є (free_qty > 0)
                # PO, що їдуть, тепер ігноруються
                is_in_stock = variant.free_qty > 0
                
                if is_in_stock:
                    for ptav in variant.product_template_attribute_value_ids:
                        stock_map[ptav.id] = True

        res.qcontext['dtn_stock_map_json'] = json.dumps(stock_map)
        return res