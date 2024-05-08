from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException
import time



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)
        
        
    def find_element(self, by, value, timeout=8, retries=2):
        attempts = 0
        while attempts < retries:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                if element:
                    element = self.scroll_to_element((by, value))
                    return element
            except (StaleElementReferenceException, TimeoutException):
                attempts += 1
                print(f"StaleElementReferenceException encountered. Retrying... Attempt {attempts}")
        return None
    
    def click_element(self, locator):
        try:
            el_to_scroll = self.scroll_to_element(locator)
            if el_to_scroll:
                el = self.find_element(*locator)
                el.click()
                return True
        except Exception as e:
            print(f"Failed to click: {e}")
            raise e
        raise Exception("Element not clickable")


    def fill_text(self, webelement, txt):
        try:
            el_to_scroll = self.scroll_to_element(webelement)
            if el_to_scroll:
                el = self.find_element(*webelement)
                el.clear()
                el.send_keys(txt)
        except StaleElementReferenceException:
            print("Element became stale. Retrying...")
            self.fill_text(webelement, txt)
        except Exception as e:
            print(f"Failed to fill text: {e}")
    

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_element(self, locator):
        try:
            element = self._wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });", element)
            return element
        except Exception as e:
            print(f"Failed to scroll to element: {e}")
            return None