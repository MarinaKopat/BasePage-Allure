import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://demoqa.com/frames'


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step
    def switch_to_frame(self, frame_locator):
        frame_element = self.driver.find_element(*frame_locator)
        self.driver.switch_to.frame(frame_element)

    @allure.step
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()


@allure.feature('Работа с фреймами')
@allure.story('Проверка текста внутри фрейма')
@pytest.mark.frame
def test_frame(driver):
    page = BasePage(driver)

    with allure.step(f'Открытие страницы {URL}'):
        driver.get(URL)

    page.switch_to_frame((By.ID, 'frame1'))

    with allure.step('Проверка текста заголовка'):
        text_element = driver.find_element(By.CSS_SELECTOR, '#sampleHeading')
        actual_text = text_element.text
        allure.attach(actual_text, name='Текст в фрейме', attachment_type=allure.attachment_type.TEXT)
        assert actual_text == 'This is a sample page'

    page.switch_to_default_content()
