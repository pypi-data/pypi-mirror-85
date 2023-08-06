from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    oc_number = fields.Char()

    @api.multi
    def compute_taxes(self):
        for invoice in self:
            oc_invoice = any([
                line.oc_amount_taxes
                for line in invoice.invoice_line_ids
            ])
            if not oc_invoice:
                super().compute_taxes()
                continue
            taxes_amount = sum(invoice.invoice_line_ids.mapped('oc_amount_taxes'))
            base = sum(invoice.invoice_line_ids.mapped('oc_amount_untaxed'))
            tax = self.env['account.tax'].search([
                ('name', '=', 'IVA 21% (Servicios)')
            ])
            vals = {
                'invoice_id': invoice.id,
                'name': tax.name,
                'tax_id': tax.id,
                'amount': taxes_amount,
                'base': base,
                'manual': False,
                'account_id': tax.account_id.id
            }
            self.env['account.invoice.tax'].create(vals)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    oc_amount_untaxed = fields.Float()
    oc_amount_taxes = fields.Float()
    price_unit = fields.Float(required=False)
    quantity = fields.Float(required=False)

    def _compute_price(self):
        super()._compute_price()
        if not self.oc_amount_untaxed and not self.oc_amount_taxes:
            return
        elif not self.oc_amount_untaxed or not self.oc_amount_taxes:
            raise ValidationError(
                'oc_amount_taxes and oc_amount_untaxed must be provided together'
            )
        self.price_subtotal = self.oc_amount_untaxed
        self.price_total = self.oc_amount_taxes + self.oc_amount_untaxed
