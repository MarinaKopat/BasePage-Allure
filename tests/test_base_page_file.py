import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step
    def open(self, url):
        self.driver.get(url)

    @allure.step
    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step
    def upload_file(self, locator, file_path):
        abs_path = os.path.abspath(file_path)
        self.driver.find_element(*locator).send_keys(abs_path)

    @allure.step
    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    @allure.step
    def is_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()


URL = 'https://demoqa.com/upload-download'
DOWNLOAD_BTN = (By.ID, 'downloadButton')
UPLOAD_INPUT = (By.ID, 'uploadFile')
RESULT_PATH = (By.ID, 'uploadedFilePath')


@allure.feature('Upload and Download')
@allure.story('Скачивание файла')
def test_download(driver):
    page = BasePage(driver)
    page.open(URL)
    page.click_element(DOWNLOAD_BTN)


@allure.feature('Upload and Download')
@allure.story('Загрузка файла')
def test_upload(driver):
    page = BasePage(driver)
    page.open(URL)

    file_path = 'file/sampleFile.jpeg'
    page.upload_file(UPLOAD_INPUT, file_path)

    with allure.step('Проверка загрузки'):
        assert page.is_element_visible(RESULT_PATH)
        assert 'sampleFile.jpeg' in page.get_text(RESULT_PATH)
