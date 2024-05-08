# from pageobjects.employee import Employee_page_obj
# from conftest import driversetup, config_parse
# import pytest, time

# class Test_Employee:

#     @pytest.mark.execution_order(order=1)
#     def test_employee(self, driversetup):
#         driver = driversetup
#         employee = Employee_page_obj(driver)
#         employee.open_url_and_sign_in()
#         employee.click_employee()
#         # Add Employee
#         first_name = config_parse('EMPLOYEE', 'first_name')
#         middle_name = config_parse('EMPLOYEE', 'middle_name')
#         last_name = config_parse('EMPLOYEE', 'last_name')
#         gender = config_parse('EMPLOYEE', 'gender')
#         employee.add_employee(first_name, middle_name, last_name, gender)
#         time.sleep(5)
#         #  Update the department
#         updated_dept_name = config_parse('UPDATE_DEPARTMENT', 'updated_dept_name')
#         updated_dept_descrip = config_parse('UPDATE_DEPARTMENT', 'updated_dept_description')
#         updated_dept_head_name = config_parse('UPDATE_DEPARTMENT', 'updated_department_head_name')
#         department.update_department(updated_dept_name, updated_dept_descrip, updated_dept_head_name)
#         # Delete the department
#         department.delete_department()
#         # Negative Test case
#         department.department_negative_testcase()