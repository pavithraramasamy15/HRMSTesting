from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time, allure
from selenium.webdriver.support import expected_conditions as EC
from testcases.conftest import config_parse, take_screenshot
import traceback, pytest
from selenium.webdriver.common.action_chains import ActionChains


class Leavepage(BasePage):
    MICROSOFT_LOGIN = (By.XPATH, "//a[text()='Continue with Microsoft']")
    EMAIL_FIELD = (By.XPATH,"//input[@id='i0116']")
    NEXT_BUTTON=(By.XPATH,"//input[@id='idSIButton9']")
    PASSWORD_FIELD = (By.XPATH,"//input[@id='i0118']")
    SIGN_IN_BUTTON = (By.XPATH, "//input[@id='idSIButton9']")
    STAY_SIGNED_IN_FIELD = (By.XPATH,"//input[@id='idSIButton9']")
    LEAVE_CONFIGURATION_BUTTON = (By.XPATH,"//a[@id='Leave']")
    CLICK_LEAVE_BUTTON = (By.XPATH,"//div[@id='Leave']")
    LEAVE_POLICY_BUTTON_CLICK=(By.XPATH,"//span[text()='Leave Policy']")
    ADD_BUTTON = (By.XPATH,"//button[text()=' Add']")
    POLICY_NAME=(By.XPATH,"//p[text()='Policy Name']/following::input[@name='policy_name']")
    POLICY_CODE=(By.XPATH,"//p[text()='Policy Code']/following::input[@name='policy_code']")
    
    
    
    
    
    
    
    
    
    

    
    
    