from ..common_service import BaseEMCRestCaseAdmin
import odoo


class InvoiceServiceRestCase(BaseEMCRestCaseAdmin):

    def test_route_right_notify_new_invoice(self):
        url = "/api/invoice/notify_new"
        data = {
            "invoice_number": "1234"
        }
        response = self.http_post(url, data=data)

        self.assertEquals(response.status_code, 200)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_wrong_notify_new_invoice_missing_invoice_number(self):
        url = "/api/invoice/notify_new"
        data = {
        }
        response = self.http_post(url, data=data)

        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_wrong_notify_new_invoice_bad_format(self):
        url = "/api/invoice/notify_new"
        data = {
            "invoice_number": 1234
        }
        response = self.http_post(url, data=data)

        self.assertEquals(response.status_code, 400)
