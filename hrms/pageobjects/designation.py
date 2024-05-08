from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time, allure
from selenium.webdriver.support import expected_conditions as EC
from testcases.conftest import config_parse, take_screenshot
import traceback
from selenium.webdriver.common.action_chains import ActionChains


class Designation_page_obj(BasePage):
    MICROSOFT_LOGIN = (By.XPATH, "//a[text()='Continue with Microsoft']")
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    NEXT_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Next']")
    SIGN_IN_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Sign in']")
    STAY_SIGNED_IN_FIELD = (By.XPATH, "//input[@type='submit' and @value='Yes']")
    
    HOVER_CONFIGURATION_BUTTON = (By.XPATH, "//a[@id='Configuration']")
    CLICK_CONFIGURATION_BUTTON = (By.XPATH, "//div[@id='Configuration']")
    DESIGNATION_BUTTON_CLICK = (By.XPATH, "//span[text()='Designation']")
    ADD_BUTTON = (By.XPATH, "//*[text()=' Add']")
    ENTER_DESIGNATION_NAME_BUTTON = (By.XPATH, "//input[@name='designation_name']")
    ENTER_DESCRIPTION_BUTTON = (By.XPATH, "//textarea[@name='designation_desc']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")
    
    CONFIRM_DESIGNATION_CREATION = (By.XPATH, f"//h3[text()='{config_parse('add_designation', 'designation_name')}']")
    UPDATE_DESIGNATION_NAME_VERIFICATION = (By.XPATH, f"//h3[text()='{config_parse('update_designation', 'update_designation_name')}']")
    
    CLICK_VIEW_MORE = (By.XPATH, f"//div[@id='{config_parse('update_designation', 'update_designation_name')}']/descendant::button[text()='View more']")
    CLICK_VIEW_MORE_ICON = (By.XPATH, "//div[@class='cursor-pointer w-10 h-10 p-1 rounded-full flex items-center justify-center bg-secondary']")
    
    CLICK_DELETE_BUTTON = (By.XPATH, f"//div[@id='{config_parse('update_designation', 'update_designation_name')}']/descendant::div[@id='delete']")
    CLICK_YES_TO_CONFIRM_DELETE = (By.XPATH, "//button[text()='Yes']")
    
    # Negative case verify element
    DESIGNATION_NAME_REQUIRED_ELEMENT_VERIFICATION = (By.XPATH, "//label[text()='Name']/following-sibling::p[text()='Required']")
    DESIGNATION_DESCRIPTION_REQUIRED_ELEMENT_VERIFICATION = (By.XPATH, "//label[text()='Description']/following-sibling::p[text()='Required']")
    
    def __init__(self, driver):
        super().__init__(driver)

    def open_designation_url(self):
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


    def click_designation(self):
        try:
            element = self.find_element(*self.HOVER_CONFIGURATION_BUTTON)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(1)
            self.click_element(self.CLICK_CONFIGURATION_BUTTON)
            time.sleep(1)
            self.click_element(self.DESIGNATION_BUTTON_CLICK)
            time.sleep(1)
        except Exception as e:
            print(f"Failed to click tenant button: {e}")


    def add_designation(self, desig_name, desig_description):
        with allure.step("Add Description"):
            self.click_element(self.ADD_BUTTON)
            self.fill_text(self.ENTER_DESIGNATION_NAME_BUTTON, desig_name)
            self.fill_text(self.ENTER_DESCRIPTION_BUTTON, desig_description)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(2)
            self.driver.refresh()
            time.sleep(2)
            assert desig_name == self.driver.find_element(*self.CONFIRM_DESIGNATION_CREATION).text, "Name of Designation Created not matched"
            time.sleep(2)
            
            
    def update_designation(self, update_desig_name, desig_description):
        with allure.step("Update Designation"):
            self.click_element(self.CLICK_VIEW_MORE)
            self.click_element(self.CLICK_VIEW_MORE_ICON)
            designation_name_input = self.driver.find_element(*self.ENTER_DESIGNATION_NAME_BUTTON)
            designation_name_input.clear()
            self.fill_text(self.ENTER_DESIGNATION_NAME_BUTTON, update_desig_name)
            desig_description = self.driver.find_element(*self.ENTER_DESCRIPTION_BUTTON)
            desig_description.clear()
            self.fill_text(self.ENTER_DESCRIPTION_BUTTON, desig_description)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(1)
            self.driver.refresh()
            time.sleep(2)
            assert update_desig_name == self.driver.find_element(*self.UPDATE_DESIGNATION_NAME_VERIFICATION).text, "Failed to Update Designation Name"


    def delete_designation(self):
        with allure.step("Delete Designation"):
            self.click_element(self.CLICK_DELETE_BUTTON)
            self.click_element(self.CLICK_YES_TO_CONFIRM_DELETE)
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.CLICK_YES_TO_CONFIRM_DELETE))    

    def designation_negative_testcase(self):
        with allure.step("Negative test case for Designation Module"):
            time.sleep(2)
            self.click_element(self.ADD_BUTTON)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(3)

            errors_found = []

            try:
                if self.driver.find_element(*self.DESIGNATION_NAME_REQUIRED_ELEMENT_VERIFICATION):
                    take_screenshot(self.driver, "Designation_name_required_verification_screenshot")
                    errors_found.append("Designation Name field error")
            except NoSuchElementException:
                pass

            try:
                if self.driver.find_element(*self.DESIGNATION_DESCRIPTION_REQUIRED_ELEMENT_VERIFICATION):
                    take_screenshot(self.driver, "Designation_Description_required_verification_screenshot")
                    errors_found.append("Designation Description field error")
            except NoSuchElementException:
                pass

            if errors_found:
                traceback_str = traceback.format_exc()
                errors_str = '\n'.join(errors_found).replace('\n', '\\n')
                message = f"Test failed due to the following errors:\n{errors_str}\n\nTraceback:\n{traceback_str}"
                print(message)