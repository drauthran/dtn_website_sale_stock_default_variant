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

        # Перевірка, чи це рендер сторінки (щоб уникнути помилок при редиректах чи JSON відповідях)
        if not hasattr(res, 'qcontext'):
            return res

        # 2. Логіка АВТО-ВИБОРУ (Серверний редирект)
        # Працює тільки, якщо користувач НЕ вибрав конкретний варіант вручну (немає product_id в URL)
        if not request.params.get('product_id'):
            # Отримуємо варіант, який Odoo вибрала за замовчуванням
            current_variant = res.qcontext.get('product_variant')
            
            # Важливо: використовуємо sudo(), оскільки у гостя сайту може не бути прав на читання складу
            if current_variant and current_variant.sudo().virtual_available <= 0:
                # Шукаємо всі варіанти цього товару, які є в наявності
                available_variants = product.product_variant_ids.sudo().filtered(lambda v: v.virtual_available > 0)
                
                if available_variants:
                    # Беремо перший доступний
                    first_available = available_variants[0]
                    
                    # Якщо це інший варіант - робимо редирект
                    if first_available.id != current_variant.id:
                        product_url = f"/shop/product/{product.id}?product_id={first_available.id}"
                        return request.redirect(product_url)

        # 3. Збір даних для візуалізації (Frontend)
        stock_map = {}
        if product.attribute_line_ids:
            variants_with_sudo = product.product_variant_ids.sudo()
            for variant in variants_with_sudo:
                is_in_stock = variant.virtual_available > 0
                if is_in_stock:
                    for ptav in variant.product_template_attribute_value_ids:
                        stock_map[ptav.id] = True

        res.qcontext['dtn_stock_map_json'] = json.dumps(stock_map)
        return res