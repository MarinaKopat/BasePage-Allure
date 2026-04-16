import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://demoqa.com/browser-windows'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step
    def switch_to_window(self, index):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    @allure.step
    def close_current_window(self):
        self.driver.close()


class BrowserWindowsPage(BasePage):
    TAB_BUTTON = (By.ID, "tabButton")
    SAMPLE_HEADING = (By.ID, "sampleHeading")

    @allure.step
    def open(self, url):
        self.driver.get(url)

    @allure.step
    def click_tab_button(self):
        self.find_element(self.TAB_BUTTON).click()

    @allure.step
    def get_heading_text(self):
        return self.find_element(self.SAMPLE_HEADING).text


@allure.feature("Browser Windows")
@allure.story("Работа с вкладками")
@pytest.mark.window
def test_tab(driver):
    page = BrowserWindowsPage(driver)

    page.open(URL)
    page.click_tab_button()

    page.switch_to_window(1)

    with allure.step("Проверка текста на новой вкладке"):
        assert page.get_heading_text() == "This is a sample page"

    page.close_current_window()
    page.switch_to_window(0)

    with allure.step("Проверка возврата на исходный URL"):
        assert driver.current_url == URL
