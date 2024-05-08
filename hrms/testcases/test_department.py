from pageobjects.department import Departmentpage
from conftest import driversetup, config_parse
import pytest

class Test_Department:

    @pytest.mark.execution_order(order=3)
    def test_department(self, driversetup):
        driver = driversetup
        department = Departmentpage(driver)
        department.open_department_url()
        department.click_department()
        # Add the department
        dep_name = config_parse('department_add', 'name')
        dep_description = config_parse('department_add', 'description')
        dep_head_name = config_parse('department_add', 'department_head')
        department.add_department(dep_name, dep_description, dep_head_name)
        #  Update the department
        updated_dept_name = config_parse('UPDATE_DEPARTMENT', 'updated_dept_name')
        updated_dept_descrip = config_parse('UPDATE_DEPARTMENT', 'updated_dept_description')
        updated_dept_head_name = config_parse('UPDATE_DEPARTMENT', 'updated_department_head_name')
        department.update_department(updated_dept_name, updated_dept_descrip, updated_dept_head_name)
        # Delete the department
        department.delete_department()
        # Negative Test case
        department.department_negative_testcase()