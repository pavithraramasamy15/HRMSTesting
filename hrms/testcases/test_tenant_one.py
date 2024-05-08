from pageobjects.tenant import Tenentpage
from conftest import driversetup, config_parse
import pytest

class Test_Tenant:

    @pytest.mark.execution_order(order=1)
    def test_tenant(self, driversetup):
        driver = driversetup
        tenant = Tenentpage(driver)
        tenant.open_tenant_url()
        tenant.click_tenant()
        
        name = config_parse('tenant_create_details', 'name')
        location = config_parse('tenant_create_details', 'location')
        phone = config_parse('tenant_create_details', 'phone')
        
        tenant.add_tenant(name, location, phone)
        
        updated_name = config_parse('updated_tenant_details', 'name')
        updated_location = config_parse('updated_tenant_details', 'location')
        updated_phone = config_parse('updated_tenant_details', 'phone')
        
        tenant.edit_tenant(updated_name, updated_location, updated_phone)
        
        
        tenant.delete_tenant()
        
        failed_name = config_parse('failed_tenant_details', 'name')
        failed_location = config_parse('failed_tenant_details', 'location')
        failed_Phone = config_parse('failed_tenant_details', 'phone')
        tenant.failed_add_tenant(failed_name, failed_location, failed_Phone)