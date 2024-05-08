from pageobjects.designation import Designation_page_obj
from conftest import driversetup, config_parse
import pytest

class Test_Designation:

    @pytest.mark.execution_order(order=2)
    def test_department(self, driversetup):
        driver = driversetup
        designation = Designation_page_obj(driver)
        designation.open_designation_url()
        designation.click_designation()
        desig_name = config_parse('add_designation', 'designation_name')
        desig_description = config_parse('add_designation', 'designation_description')
        designation.add_designation(desig_name, desig_description)
        updated_desig_name = config_parse('update_designation', 'update_designation_name')
        updated_desig_descrip = config_parse('update_designation', 'update_designation_description')
        designation.update_designation(updated_desig_name, updated_desig_descrip)
        designation.delete_designation()
        # Negative Test case
        designation.designation_negative_testcase()