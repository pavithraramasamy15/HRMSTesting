from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time, allure
from selenium.webdriver.support import expected_conditions as EC
from testcases.conftest import config_parse, take_screenshot
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class Departmentpage(BasePage):
    MICROSOFT_LOGIN = (By.XPATH, "//a[text()='Continue with Microsoft']")
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    NEXT_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Next']")
    SIGN_IN_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Sign in']")
    STAY_SIGNED_IN_FIELD = (By.XPATH, "//input[@type='submit' and @value='Yes']")
    
    HOVER_CONFIGURATION_BUTTON = (By.XPATH, "//a[@id='Configuration']")
    CLICK_CONFIGURATION_BUTTON = (By.XPATH, "//div[@id='Configuration']")
    DEPARTMENT_BUTTON_CLICK = (By.XPATH, "//span[text()='Department']")
    ADD_BUTTON = (By.XPATH, "//*[text()=' Add']")
    ENTER_DEPARTMENT_NAME_BUTTON = (By.XPATH, "//input[@name='department_name']")
    SELECT_DEPARTMENT_HEAD_NAME_DROPDOWN = (By.XPATH, "//button[@role='combobox']")
    SELECT_DROPDOWN_VALUE = (By.XPATH, "//select[@aria-hidden='true']")
    ENTER_DESCRIPTION_BUTTON = (By.XPATH, "//textarea[@name='department_desc']")
    SELECT_HEAD_BUTTON = (By.XPATH, "//input[@placeholder='Enter Head Name']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")
    
    CONFIRM_DEPARTMENT_CREATION = (By.XPATH, f"//h3[text()='{config_parse('department_add', 'name')}']")
    EDIT_DEPARTMENT_NAME_VERIFICATION = (By.XPATH, f"//h3[text()='{config_parse('UPDATE_DEPARTMENT', 'updated_dept_name')}']")
    
    CLICK_VIEW_MORE = (By.XPATH, f"//div[@id='{config_parse('department_add', 'name')}']/descendant::button[text()='View more']")
    CLICK_VIEW_MORE_ICON = (By.XPATH, "//div[@class='cursor-pointer w-10 h-10 p-1 rounded-full flex items-center justify-center bg-secondary']")
    
    CLICK_DELETE_BUTTON = (By.XPATH, f"//div[@id='{config_parse('UPDATE_DEPARTMENT', 'updated_dept_name')}']/descendant::div[@id='delete']")
    CLICK_YES_TO_CONFIRM_DELETE = (By.XPATH, "//button[text()='Yes']")
    
    # Negative case verify element
    DEPARTMENT_NAME_REQUIRED_ELEMENT_VERIFICATION = (By.XPATH, "//label[text()='Name']/following-sibling::p[text()='Required']")
    DESCRIPTION_REQUIRED_ELEMENT_VERIFICATION = (By.XPATH, "//label[text()='Description']/following-sibling::p[text()='Required']")
    DEPARTMENT_HEAD_REQUIRED_ELEMENT_VERIFICATION = (By.XPATH, "//label[text()='Department Head']/following-sibling::p[text()='Required']")
    
    def __init__(self, driver):
        super().__init__(driver)

    def open_department_url(self):
        try:
            url = config_parse("hrms_url", "base_url")
            self.driver.get(url)
            self.click_element(self.MICROSOFT_LOGIN)
            email = config_parse("sign_in_cred", "email")
            self.fill_text(self.EMAIL_FIELD, email)
            self.click_element(self.NEXT_BUTTON)
            password = config_parse("sign_in_cred", "password")
            self.fill_text(self.PASSWORD_FIELD, password)
            self.click_element(self.SIGN_IN_BUTTON)
            self.click_element(self.STAY_SIGNED_IN_FIELD)
            time.sleep(2)
        except Exception as e:
            print(f"Failed to open URL: {e}")
    
    def click_department(self):
        try:
            element = self.find_element(*self.HOVER_CONFIGURATION_BUTTON)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(1)
            self.click_element(self.CLICK_CONFIGURATION_BUTTON)
            time.sleep(1)
            self.click_element(self.DEPARTMENT_BUTTON_CLICK)
            time.sleep(1)
        except Exception as e:
            print(f"Failed to click tenant button: {e}")
    

    def add_department(self, dept_name, dept_description, dept_head):
        with allure.step("Add Tenant"):
            self.click_element(self.ADD_BUTTON)
            self.fill_text(self.ENTER_DEPARTMENT_NAME_BUTTON, dept_name)
            self.fill_text(self.ENTER_DESCRIPTION_BUTTON, dept_description)

            hidden_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.SELECT_DROPDOWN_VALUE[1])))
            actions = ActionChains(self.driver)
            actions.move_to_element(hidden_element).perform()
            hidden_element.send_keys(dept_head)
            hidden_element.send_keys(Keys.ENTER)
            time.sleep(1)
            
            self.click_element(self.SAVE_BUTTON)
            time.sleep(1)
            self.driver.refresh()
            time.sleep(2)
            assert dept_name == self.driver.find_element(*self.CONFIRM_DEPARTMENT_CREATION).text, "Name of Department not matched"
    

    def update_department(self, updated_dept_name, updated_dept_description, updated_dept_head_name):
        with allure.step("Update Department"):
            self.click_element(self.CLICK_VIEW_MORE)
            self.click_element(self.CLICK_VIEW_MORE_ICON)
            dept_name_input = self.driver.find_element(*self.ENTER_DEPARTMENT_NAME_BUTTON)
            dept_name_input.clear()
            self.fill_text(self.ENTER_DEPARTMENT_NAME_BUTTON, updated_dept_name)
            dept_description = self.driver.find_element(*self.ENTER_DESCRIPTION_BUTTON)
            dept_description.clear()
            self.fill_text(self.ENTER_DESCRIPTION_BUTTON, updated_dept_description)
            hidden_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.SELECT_DROPDOWN_VALUE[1])))
            actions = ActionChains(self.driver)
            actions.move_to_element(hidden_element).perform()
            hidden_element.send_keys(updated_dept_head_name)
            hidden_element.send_keys(Keys.ENTER)
            time.sleep(1)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(1)
            self.driver.refresh()
            time.sleep(2)
            assert updated_dept_name == self.driver.find_element(*self.EDIT_DEPARTMENT_NAME_VERIFICATION).text, "Failed to Update department Name"


    def delete_department(self):
        with allure.step("Delete Department"):
            self.click_element(self.CLICK_DELETE_BUTTON)
            self.click_element(self.CLICK_YES_TO_CONFIRM_DELETE)
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CLICK_YES_TO_CONFIRM_DELETE))    

    def department_negative_testcase(self):
        with allure.step("Negative test case"):
            time.sleep(2)
            self.click_element(self.ADD_BUTTON)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(3)

            errors_found = []

            try:
                if self.driver.find_element(*self.DEPARTMENT_NAME_REQUIRED_ELEMENT_VERIFICATION):
                    take_screenshot(self.driver, "Department_name_required_verification_screenshot")
                    errors_found.append("Department_name_required field error confirmation")
            except NoSuchElementException:
                pass

            try:
                if self.driver.find_element(*self.DESCRIPTION_REQUIRED_ELEMENT_VERIFICATION):
                    take_screenshot(self.driver, "Department_Description_required_verification_screenshot")
                    errors_found.append("Department_Description_required field error confirmation")
            except NoSuchElementException:
                pass

            try:
                if self.driver.find_element(*self.DEPARTMENT_HEAD_REQUIRED_ELEMENT_VERIFICATION):
                    take_screenshot(self.driver, "Department_Head_name_required_verification_screenshot")
                    errors_found.append("Department_Head_name_required field error confirmation")
            except NoSuchElementException:
                pass

            print("Negative test case passed for Department Module:")
            for index, error_message in enumerate(errors_found, 1):
                print(f"{index}. {error_message}")
                