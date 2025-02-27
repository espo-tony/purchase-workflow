# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import Form, TransactionCase


class TestPurchaseWorkAcceptance(TransactionCase):
    def setUp(self):
        super().setUp()
        self.service_product = self.env.ref("product.product_product_1")
        self.service_product.purchase_method = "purchase"
        self.product_product = self.env.ref("product.product_product_6")
        self.res_partner = self.env.ref("base.res_partner_3")
        self.employee = self.env.ref("base.user_demo")
        self.main_company = self.env.ref("base.main_company")
        self.date_now = fields.Datetime.now()
        # Enable and Config WA
        self.env["res.config.settings"].create(
            {"group_enable_wa_on_po": True}
        ).execute()

        self.picking_type_return = self.env["stock.picking.type"].search(
            [
                ("code", "=", "incoming"),
                ("return_picking_type_id", "=", False),
                ("company_id", "=", self.main_company.id),
            ],
            limit=1,
        )

    def _create_purchase_order(self, qty, product):
        purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.res_partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom": product.uom_id.id,
                            "name": product.name,
                            "price_unit": product.standard_price,
                            "date_planned": self.date_now,
                            "product_qty": qty,
                        },
                    )
                ],
            }
        )
        return purchase_order

    def _create_multi_purchase_order(self, qty, multi):
        purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.res_partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_product.id,
                            "product_uom": self.product_product.uom_id.id,
                            "name": self.product_product.name,
                            "price_unit": self.product_product.standard_price,
                            "date_planned": self.date_now,
                            "product_qty": qty,
                        },
                    )
                    for x in range(multi)
                ],
            }
        )
        return purchase_order

    def _create_work_acceptance(self, qty, po=False):
        work_acceptance = self.env["work.acceptance"].create(
            {
                "purchase_id": po and po.id or False,
                "partner_id": self.res_partner.id,
                "responsible_id": self.employee.id,
                "date_due": self.date_now,
                "date_receive": self.date_now,
                "company_id": self.main_company.id,
                "wa_line_ids": [
                    (
                        0,
                        0,
                        {
                            "purchase_line_id": po and po.order_line[0].id or False,
                            "product_id": po
                            and po.order_line[0].product_id.id
                            or self.service_product.id,
                            "name": po
                            and po.order_line[0].name
                            or self.service_product.name,
                            "price_unit": po
                            and po.order_line[0].price_unit
                            or self.service_product.standard_price,
                            "product_uom": po
                            and po.order_line[0].product_uom.id
                            or self.service_product.uom_id.id,
                            "product_qty": qty,
                        },
                    )
                ],
            }
        )
        return work_acceptance

    def _create_multi_work_acceptance(self, qty, purchase_order, multi):
        work_acceptance = self.env["work.acceptance"].create(
            {
                "purchase_id": purchase_order.id,
                "partner_id": self.res_partner.id,
                "responsible_id": self.employee.id,
                "date_due": self.date_now,
                "date_receive": self.date_now,
                "company_id": self.main_company.id,
                "wa_line_ids": [
                    (
                        0,
                        0,
                        {
                            "purchase_line_id": purchase_order.order_line[x].id,
                            "product_id": purchase_order.order_line[x].product_id.id,
                            "name": purchase_order.order_line[x].name,
                            "price_unit": purchase_order.order_line[x].price_unit,
                            "product_uom": purchase_order.order_line[x].product_uom.id,
                            "product_qty": qty,
                        },
                    )
                    for x in range(multi)
                ],
            }
        )
        return work_acceptance

    def test_00_wa_button(self):
        qty = 3.0
        work_acceptance = self._create_work_acceptance(qty)
        work_acceptance.button_accept()
        self.assertEqual(work_acceptance.state, "accept")
        work_acceptance.button_cancel()
        self.assertEqual(work_acceptance.state, "cancel")
        work_acceptance.button_draft()
        self.assertEqual(work_acceptance.state, "draft")
        # Test open wizard
        wizard = self.env.ref("purchase_work_acceptance.view_work_accepted_date_wizard")
        res = work_acceptance.with_context(manual_date_accept=True).button_accept()
        self.assertEqual(res["res_model"], "work.accepted.date.wizard")
        self.assertEqual(res["view_id"], wizard.id)
        ctx = {
            "active_ids": [work_acceptance.id],
            "active_id": work_acceptance.id,
            "active_model": work_acceptance._name,
        }
        WorkAcceptanceWizard = self.env["work.accepted.date.wizard"]
        with Form(WorkAcceptanceWizard.with_context(**ctx)) as f:
            f.date_accept = self.date_now
        wa_wizard = f.save()
        wa_wizard.button_accept()

    def test_01_action_view_wa(self):
        # Create Purchase Order
        qty = 42.0
        purchase_order = self._create_purchase_order(qty, self.product_product)
        purchase_order.button_confirm()
        self.assertEqual(purchase_order.state, "purchase")

        res = purchase_order.with_context(create_wa=True).action_view_wa()
        ctx = res.get("context")
        work_acceptance = Form(self.env["work.acceptance"].with_context(**ctx))
        self.assertEqual(work_acceptance.state, "draft")
        # Open with 1 WA
        work_acceptance1 = self._create_work_acceptance(1, purchase_order)
        res = purchase_order.action_view_wa()
        self.assertEqual(res["res_id"], work_acceptance1.id)
        work_acceptance1.button_accept()
        purchase_order._compute_wa_accepted()
        # Open with 2 WA
        work_acceptance2 = self._create_work_acceptance(2, purchase_order)
        purchase_order._compute_wa_ids()
        res = purchase_order.action_view_wa()
        res_domain = ast.literal_eval(res["domain"])
        wa_ids = (work_acceptance1 + work_acceptance2).ids
        self.assertEqual(res_domain[0][2], wa_ids)

    def test_02_flow_product(self):
        # Create Purchase Order
        qty = 42.0
        purchase_order = self._create_purchase_order(qty, self.product_product)
        purchase_order.button_confirm()
        self.assertEqual(purchase_order.state, "purchase")
        self.assertEqual(purchase_order.incoming_picking_count, 1)
        # Create Work Acceptance
        work_acceptance = self._create_work_acceptance(qty, purchase_order)
        work_acceptance.button_accept()
        self.assertEqual(work_acceptance.state, "accept")
        self.assertEqual(purchase_order.wa_count, 1)
        # Received Products
        picking = purchase_order.picking_ids[0]
        self.assertEqual(len(picking.move_ids_without_package), 1)
        with Form(picking) as p:
            p.wa_id = work_acceptance
        p.save()
        with self.assertRaises(ValidationError):
            picking.move_ids_without_package[0].quantity_done = 30.0
            picking.button_validate()
        picking.move_ids_without_package[0].quantity_done = 42.0
        picking.button_validate()
        # Can't set to draft wa when you validate picking
        with self.assertRaises(UserError):
            work_acceptance.button_draft()
        # Create Vendor Bill
        f = Form(self.env["account.move"].with_context(default_move_type="in_invoice"))
        f.partner_id = purchase_order.partner_id
        f.purchase_id = purchase_order
        # f.wa_id = work_acceptance
        invoice = f.save()
        invoice.wa_id = work_acceptance
        invoice_line = invoice.invoice_line_ids[0]
        with self.assertRaises(ValidationError):
            invoice_line.with_context(check_move_validity=False).write(
                {"quantity": 6.0}
            )
            invoice.action_post()  # Warn when quantity not equal to WA
        invoice_line.quantity = qty
        self.assertEqual(invoice.state, "draft")
        invoice.invoice_date = invoice.date
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_03_flow_service(self):
        qty = 30.0
        # Create Purchase Order
        purchase_order = self._create_purchase_order(qty, self.service_product)
        purchase_order.button_confirm()
        self.assertEqual(purchase_order.state, "purchase")
        # Create Work Acceptance
        work_acceptance = self._create_work_acceptance(qty, purchase_order)
        work_acceptance.button_accept()
        self.assertEqual(work_acceptance.state, "accept")
        self.assertEqual(purchase_order.wa_count, 1)
        # Create Vendor Bill
        f = Form(self.env["account.move"].with_context(default_move_type="in_invoice"))
        f.partner_id = purchase_order.partner_id
        f.purchase_id = purchase_order
        # f.wa_id = work_acceptance
        invoice = f.save()
        invoice.wa_id = work_acceptance
        self.assertEqual(invoice.state, "draft")
        invoice.invoice_date = invoice.date
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_04_enable_config_flow(self):
        qty = 2.0
        # Create Purchase Order
        purchase_order = self._create_purchase_order(qty, self.service_product)
        purchase_order.button_confirm()
        # Create Work Acceptance
        work_acceptance = self._create_work_acceptance(qty, purchase_order)
        work_acceptance.button_accept()
        self.env["res.config.settings"].create(
            {"group_enable_wa_on_invoice": True}
        ).execute()
        res = purchase_order.with_context(create_bill=True).action_create_invoice()
        self.assertEqual(res.get("res_model"), "select.work.acceptance.wizard")
        wizard = self.env[res.get("res_model")].create({"wa_id": work_acceptance.id})
        wizard = wizard.with_context(active_id=purchase_order.id)
        self.assertEqual(wizard.wa_ids, work_acceptance)
        res = wizard.button_create_vendor_bill()
        invoice = self.env["account.move"].browse(res["res_id"])
        self.assertEqual(sum(invoice.invoice_line_ids.mapped("quantity")), qty)
        # Test create wa is used
        with self.assertRaises(ValidationError):
            wizard.button_create_vendor_bill()
        invoice = self.env["account.move"].browse(res["res_id"])
        self.assertEqual(sum(invoice.invoice_line_ids.mapped("quantity")), qty)

        # Create Return with required WA
        self.env["res.config.settings"].create(
            {"group_enforce_wa_on_in": True}
        ).execute()
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_return.id,
                "location_id": 4,
                "location_dest_id": 8,
            }
        )
        # Set bypass reutrn not required wa
        self.assertTrue(picking.require_wa)
        self.picking_type_return.bypass_wa = True
        picking._compute_require_wa()
        self.assertFalse(picking.require_wa)

    def test_05_create_multi_lines(self):
        qty = 5.0
        # Create Purchase Order
        purchase_order = self._create_multi_purchase_order(qty, multi=2)
        purchase_order.button_confirm()
        # Create Work Acceptance
        work_acceptance = work_acceptance = self._create_multi_work_acceptance(
            qty, purchase_order, multi=2
        )
        work_acceptance.button_accept()
        # Received Products
        picking = purchase_order.picking_ids[0]
        self.assertEqual(len(picking.move_ids_without_package), 2)
        with Form(picking) as p:
            p.wa_id = work_acceptance
        p.save()
        picking.button_validate()
        # Create Vendor Bill
        self.env["res.config.settings"].create(
            {"group_enable_wa_on_invoice": True}
        ).execute()
        res = purchase_order.with_context(create_bill=True).action_create_invoice()
        self.assertEqual(res.get("res_model"), "select.work.acceptance.wizard")
        wizard = self.env[res.get("res_model")].create({"wa_id": work_acceptance.id})
        res = wizard.with_context(
            active_id=purchase_order.id
        ).button_create_vendor_bill()
        invoice = self.env["account.move"].browse(res["res_id"])
        self.assertEqual(sum(invoice.invoice_line_ids.mapped("quantity")), qty * 2)

    def test_06_check_qty_accepted(self):
        qty_po = 20.0
        qty_wa = 12.0
        purchase_order = self._create_purchase_order(qty_po, self.product_product)
        purchase_order.button_confirm()
        work_acceptance = self._create_work_acceptance(qty_wa, po=purchase_order)
        work_acceptance.button_accept()
        self.assertEqual(purchase_order.order_line[0].qty_accepted, 12.0)
        self.assertEqual(purchase_order.order_line[0].qty_to_accept, 8.0)

    def test_07_hide_wa_button(self):
        qty_po = 20.0
        purchase_order = self._create_purchase_order(qty_po, self.product_product)
        purchase_order.button_confirm()
        work_acceptance = self._create_work_acceptance(qty=12, po=purchase_order)
        work_acceptance.button_accept()
        purchase_order._compute_wa_accepted()
        self.assertEqual(purchase_order.wa_accepted, False)
        work_acceptance = self._create_work_acceptance(qty=8, po=purchase_order)
        work_acceptance.button_accept()
        purchase_order._compute_wa_accepted()
        self.assertEqual(purchase_order.wa_accepted, True)
