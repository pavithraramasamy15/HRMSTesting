from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time, allure
from selenium.webdriver.support import expected_conditions as EC
from testcases.conftest import config_parse, take_screenshot
import traceback, pytest
from selenium.webdriver.common.action_chains import ActionChains



class Tenentpage(BasePage):
    MICROSOFT_LOGIN = (By.XPATH, "//a[text()='Continue with Microsoft']")
    TENANT_URL = config_parse('tenant_create_details', 'TENANT_URL')
    HOVER_CONFIGURATION_BUTTON = (By.XPATH, "//a[@id='Configuration']")
    CLICK_CONFIGURATION_BUTTON = (By.XPATH, "//div[@id='Configuration']")
    TENANT_CLICK = (By.XPATH, "//span[text()='Tenant']")
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    NEXT_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Next']")
    SIGN_IN_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Sign in']")
    STAY_SIGNED_IN_FIELD = (By.XPATH, "//input[@type='submit' and @value='Yes']")
    ADD_BUTTON = (By.XPATH, "//*[text()=' Add']")
    ENTER_NAME = (By.XPATH, "//input[@placeholder='Enter Name']")
    ENTER_ADDRESS = (By.XPATH, "//textarea[@placeholder='Enter Address']")
    ENTER_CONTACT_NUMBER = (By.XPATH, "//input[@placeholder='Enter Contact Number']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")
    CONFIRM_TENANT_CREATION = (By.XPATH, f"//h3[text()='{config_parse('tenant_create_details', 'name')}']")
    CONFIRM_TENANT_CREATION_2 = (By.XPATH, f"//h3[text()='{config_parse('updated_tenant_details', 'name')}']")
    # Edit Section
    CLICK_VIEW_MORE = (By.XPATH, f"//div[@id='{config_parse('tenant_create_details', 'name')}']/descendant::button[text()='View more']")
    CLICK_EDIT_ICON_BUTTON = (By.XPATH, "//div[@class='cursor-pointer w-10 h-10 p-1 rounded-full flex items-center justify-center bg-secondary']")
    # Delete Section
    CLICK_DELETE_BUTTON = (By.XPATH, f"//div[@id='{config_parse('tenant_create_details', 'name')}1']/descendant::div[@id='delete']")
    CLICK_YES_TO_CONFIRM_DELETE = (By.XPATH, "//button[text()='Yes']")
    
    
    def __init__(self, driver):
        super().__init__(driver)
    
    
    def open_tenant_url(self):
        try:
            self.driver.get(self.TENANT_URL)
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
    
    def click_tenant(self):
        try:
            element = self.find_element(*self.HOVER_CONFIGURATION_BUTTON)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(1)
            self.click_element(self.CLICK_CONFIGURATION_BUTTON)
            time.sleep(1)
            self.click_element(self.TENANT_CLICK)
            time.sleep(1)
        except Exception as e:
            print(f"Failed to click tenant button: {e}")


    def add_tenant(self, name, address, contact_number):
        with allure.step("Add Tenant"):
            self.click_element(self.ADD_BUTTON)
            self.fill_text(self.ENTER_NAME, name)
            self.fill_text(self.ENTER_ADDRESS, address)
            self.fill_text(self.ENTER_CONTACT_NUMBER, contact_number)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(2)
            self.driver.refresh()
            time.sleep(2)
            assert name == self.driver.find_element(*self.CONFIRM_TENANT_CREATION).text, "Created Tenant Name doesnt match, Failed to add tenant"

    def edit_tenant(self, name, address, contact_number):
        with allure.step("Edit Tenant"):
            self.click_element(self.CLICK_VIEW_MORE)
            self.click_element(self.CLICK_EDIT_ICON_BUTTON)
            name_input = self.driver.find_element(*self.ENTER_NAME)
            name_input.clear()
            self.fill_text(self.ENTER_NAME, name)
            address_input = self.driver.find_element(*self.ENTER_ADDRESS)
            address_input.clear()
            self.fill_text(self.ENTER_ADDRESS, address)
            contact_input = self.driver.find_element(*self.ENTER_CONTACT_NUMBER)
            contact_input.clear()
            self.fill_text(self.ENTER_CONTACT_NUMBER, contact_number)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(3)
            assert name == self.driver.find_element(*self.CONFIRM_TENANT_CREATION_2).text, "Failed to edit tenant"

    def delete_tenant(self):
        with allure.step("Delete Tenant"):
            self.click_element(self.CLICK_DELETE_BUTTON)
            self.click_element(self.CLICK_YES_TO_CONFIRM_DELETE)
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CLICK_YES_TO_CONFIRM_DELETE))    

    def failed_add_tenant(self, name, address, contact_number):
        with allure.step("Add Tenant"):
            self.click_element(self.ADD_BUTTON)
            # self.fill_text(self.ENTER_NAME, name)
            # self.fill_text(self.ENTER_ADDRESS, address)
            # self.fill_text(self.ENTER_CONTACT_NUMBER, contact_number)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(3)

            errors_found = []
            failed_name_field_verify = (By.XPATH, "//p[text()='Name should not be empty']")
            failed_address_field_verify = (By.XPATH, "//p[text()='Address should not be empty']")
            failed_mobile_number_field_verify = (By.XPATH, "//p[text()='Contact number should be at least 10 characters' or text()='Contact number must only contain numerics, +, and -' or text()='Contact number should not exceed 15 characters']")

            try:
                if self.driver.find_element(*failed_name_field_verify):
                    take_screenshot(self.driver, "name_field_error")
                    errors_found.append("Name field error message and screenshot")
            except NoSuchElementException:
                pass

            try:
                if self.driver.find_element(*failed_address_field_verify):
                    take_screenshot(self.driver, "address_field_error")
                    errors_found.append("Address field error message and screenshot")
            except NoSuchElementException:
                pass

            try:
                if self.driver.find_element(*failed_mobile_number_field_verify):
                    take_screenshot(self.driver, "mobile_number_field_error")
                    errors_found.append("Mobile number field error message and screenshot")
            except NoSuchElementException:
                pass

            if errors_found:
                traceback_str = traceback.format_exc()
                errors_str = '\n'.join(errors_found).replace('\n', '\\n')
                message = f"Test failed due to the following errors:\n{errors_str}\n\nTraceback:\n{traceback_str}"
                print(message)

