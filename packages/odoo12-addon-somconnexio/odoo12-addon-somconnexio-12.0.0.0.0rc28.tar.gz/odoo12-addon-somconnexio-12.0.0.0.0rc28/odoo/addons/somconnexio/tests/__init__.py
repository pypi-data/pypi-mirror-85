from . import test_subscription_request
from . import test_coop_agreement
from . import test_contract
from . import test_service_supplier
from . import test_product_category_technology_supplier
from . import test_crm_lead_line
from . import test_mobile_isp_info
from . import test_broadband_isp_info
from . import test_res_partner
from . import test_contract_contract_service
from . import test_previous_provider_service
from . import test_production_lot
from . import test_stock_move_line
from . import test_account_invoice_service
from . import test_description
from . import test_address
from . import test_customer
from . import test_subscription
from . import test_opencell_configuration_wrapper
from . import test_opencell_service_codes

from .services import test_crm_lead_service
from .services import test_subscription_request_service

from .opencell_models import test_crm_account_hierarchy

from .opencell_services import test_crm_account_hierarchy_service
from .opencell_services import test_subscription_service
from .opencell_services import test_contract_service

from .otrs_factories import test_customer_data_from_res_partner
from .otrs_factories import test_adsl_data_from_crm_lead_line
from .otrs_factories import test_fiber_data_from_crm_lead_line
from .otrs_factories import test_mobile_data_from_crm_lead_line

from .wizards import test_crm_leads_validate_wizard
from .wizards import test_contract_iban_change_wizard
from .wizards import test_contract_holder_change
from .wizards import test_contract_email_change_wizard
