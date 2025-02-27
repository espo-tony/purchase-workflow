# Copyright 2015-17 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Purchase Order Analytic Search",
    "summary": """Search purchase orders by analytic account. New menu entry in
                Purchasing to list purchase order lines.""",
    "version": "15.0.1.0.0",
    "website": "https://github.com/OCA/purchase-workflow",
    "category": "Purchase Workflow",
    "author": "ForgeFlow, Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["analytic", "purchase"],
    "data": ["views/purchase_order_view.xml"],
}
