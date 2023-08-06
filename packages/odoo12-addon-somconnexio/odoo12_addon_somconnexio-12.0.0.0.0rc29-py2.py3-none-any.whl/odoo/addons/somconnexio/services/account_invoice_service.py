import logging
from odoo.addons.component.core import Component
from . import schemas

_logger = logging.getLogger(__name__)


class AccountInvoiceService(Component):
    _inherit = "account.invoice.service"

    def notify_new(self, **params):
        return {}

    def _validator_notify_new(self):
        return schemas.S_ACCOUNT_INVOICE_NOTIFY_NEW

    def _validator_return_notify_new(self):
        return schemas.S_ACCOUNT_INVOICE_RETURN_NOTIFY_NEW
