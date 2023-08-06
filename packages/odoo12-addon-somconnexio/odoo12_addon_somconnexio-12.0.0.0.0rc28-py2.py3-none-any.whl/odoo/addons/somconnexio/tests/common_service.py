from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)
        AuthApiKey = cls.env["auth.api.key"]
        admin = cls.env.ref("base.user_admin")
        cls.api_key_test = AuthApiKey.create(
            {"name": "test-key", "key": "api-key", "user_id": admin.id}
        )
