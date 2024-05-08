from selenium import webdriver
import pytest, configparser, os, allure, time
from datetime import datetime



def config_parse(section, key):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get(section, key)


BROWSER_DRIVERS = {
    "chrome": webdriver.Chrome,
    "edge": webdriver.Edge,
    "firefox": webdriver.Firefox
}

@pytest.fixture(scope="module")
def driversetup(request):
    browser = request.config.getoption("--browser")
    
    if browser not in BROWSER_DRIVERS:
        raise ValueError(f"Unsupported browser: {browser}")

    driver = BROWSER_DRIVERS[browser]()

    driver.implicitly_wait(5)
    driver.maximize_window()

    yield driver
    driver.quit()
    

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get('driversetup')
        if driver:
            time.sleep(1)
            take_screenshot(driver)

def take_screenshot(driver, screenshot_name='screenshot_on_failure'):
    current_time = datetime.now().strftime("%Y--%m--%d_%H-%M-%S")
    full_screenshot_name = f'{screenshot_name}_{current_time}.png'
    directory = os.path.join(os.getcwd(), 'screenshots')
    if not os.path.exists(directory):
        os.makedirs(directory)
    screenshot_path = os.path.join(directory, full_screenshot_name)
    allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
                attachment_type=allure.attachment_type.PNG)
    driver.save_screenshot(screenshot_path)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "execution_order(order): Order of test execution"
    )

def pytest_collection_modifyitems(config, items):
    items.sort(key=lambda item: item.get_closest_marker("execution_order").kwargs.get("order", 0))

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")




