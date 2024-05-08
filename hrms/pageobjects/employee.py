from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
import time, allure
from selenium.webdriver.support import expected_conditions as EC
from testcases.conftest import config_parse, take_screenshot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select



class Employee_page_obj(BasePage):
    MICROSOFT_LOGIN = (By.XPATH, "//a[text()='Continue with Microsoft']")
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    NEXT_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Next']")
    SIGN_IN_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Sign in']")
    STAY_SIGNED_IN_FIELD = (By.XPATH, "//input[@type='submit' and @value='Yes']")
    
    EMPLOYEE_CONFIGURATION_BUTTON = (By.XPATH, "//a[@id='Employee']")
    CLICK_EMPLOYEE_BUTTON = (By.XPATH, "//div[@id='Employee']")
    EMPLOYEE_LIST_BUTTON_CLICK = (By.XPATH, "//span[text()='Employee List']")
    ADD_BUTTON = (By.XPATH, "//*[text()=' Add']")
    FIRST_NAME = (By.XPATH, "//input[@name='first_name']")
    MIDDLE_NAME = (By.XPATH, "//input[@name='middle_name']")
    LAST_NAME = (By.XPATH, "//input[@name='last_name']")
    # SELECT_GENDER_DROPDOWN = (By.XPATH, "//label[text()='Gender']/following-sibling::select")
    SELECT_GENDER_DROPDOWN = (By.XPATH, "//label[text()='Gender']/following-sibling::button")
    SELECT_GENDER_OPTION = (By.XPATH, "//span[text()='Male']")
    SELECT_EMPLOYEE_TYPE_DROPDOWN = (By.XPATH, "//label[text()='Employee Type']/following-sibling::select")
    SELECT_DESIGNATION_DROPDOWN = (By.XPATH, "//label[text()='Designation']/following-sibling::select")
    SELECT_AZURE_ID_DROPDOWN = (By.XPATH, "//label[text()='Azure Id']/following-sibling::select")
    ENTER_EMPLOYEE_NUMBER = (By.XPATH, "//input[@name='employee_no']")
    ENTER_TOTAL_EXPERIENCE_ = (By.XPATH, "//input[@name='total_exp']")
    DATE_OF_JOIINING = (By.XPATH, "//div[@class='react-datepicker__input-container")
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

    def open_url_and_sign_in(self):
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


    def click_employee(self):
        try:
            element = self.find_element(*self.EMPLOYEE_CONFIGURATION_BUTTON)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            self.click_element(self.CLICK_EMPLOYEE_BUTTON)
            self.click_element(self.EMPLOYEE_LIST_BUTTON_CLICK)
        except Exception as e:
            print(f"Failed to click tenant button: {e}")


    def add_employee(self, first_name, middle_name, last_name, gender):
        with allure.step("Add Description"):
            self.click_element(self.ADD_BUTTON)
            self.fill_text(self.FIRST_NAME, first_name)
            self.fill_text(self.MIDDLE_NAME, middle_name)
            self.fill_text(self.LAST_NAME, last_name)
            self.click_element(self.SELECT_GENDER_DROPDOWN)
            self.click_element(self.SELECT_GENDER_OPTION)
            time.sleep(5)
            # gender = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, self.SELECT_GENDER_DROPDOWN[1]))
            # )
            # action = ActionChains(self.driver)
            # action.move_to_element(gender).perform()
            # gender.send_keys(gender)
            # gender.send_keys(Keys.ENTER)
            # time.sleep(1)
            
#             dropdown = self.find_element(By.XPATH, "//label[text()='Gender']/following-sibling::button[@role]")

# # Click the dropdown to open the options
#             dropdown.click()

#             # Create a Select object for the dropdown
#             select = Select(dropdown)

#             # Select an option from the dropdown by its value, text, or index
#             select.select_by_value("Male")
#             time.sleep(5)
            
            # value_to_select = "Male"
            # script = f"document.querySelector('select[aria-hidden=true]').value = '{value_to_select}';"
            # self.driver.execute_script(script)
            
            # dropdown = self.find_element(By.XPATH, "(//select[@aria-hidden='true'])[1]")

            # # Simulate keyboard actions to open the dropdown options
            # dropdown.click()  # Clicking to focus on the dropdown
            # dropdown.send_keys(Keys.ARROW_DOWN)  # Simulating arrow down key
            # dropdown.send_keys(Keys.ENTER)
            
            # self.click_element(self.SAVE_BUTTON)
            # time.sleep(2)
            # self.driver.refresh()
            # time.sleep(2)
            # assert desig_name == self.driver.find_element(*self.CONFIRM_DESIGNATION_CREATION).text, "Name of Designation Created not matched"
            # time.sleep(2)