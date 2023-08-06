from odoo import models, fields


class OpenCellServiceCodes(models.Model):
    _name = 'opencell.service_codes'
    product_template = fields.Many2one(
        'product.template', 'Product', required=True
    )
    code = fields.Char('Opencell Code', required=True)
    _sql_constraints = [(
        'product_template_unique', 'unique(product_template)',
        'Product template must be unique'
    )]
