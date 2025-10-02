# -*- coding: utf-8 -*-
{
    'name': 'DTN Website Sale: Stock Variants Style',
    'version': '18.0.9.0.0', # Финальная версия
    'category': 'Website/eCommerce',
    'summary': 'Visually marks out-of-stock variants and auto-selects the first available one.',
    'author': 'Drauthran',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'website.assets_frontend': [
            'dtn_website_sale_stock_default_variant/static/src/scss/product_page_stock_style.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}