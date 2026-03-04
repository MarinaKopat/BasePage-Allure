import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step
    def get_alert(self):
        return self.wait.until(EC.alert_is_present())

    @allure.step
    def alert_accept(self):
        self.get_alert().accept()

    @allure.step
    def alert_dismiss(self):
        self.get_alert().dismiss()

    @allure.step
    def alert_get_text(self):
        return self.get_alert().text

    @allure.step
    def alert_send_keys(self, text):
        alert = self.get_alert()
        alert.send_keys(text)


URL = 'https://demo.automationtesting.in/Alerts.html'


@allure.title('Проверка простого алерта')
def test_alert_simple(driver):
    page = BasePage(driver)

    with allure.step(f'Открытие страницы {URL}'):
        driver.get(URL)

    with allure.step('Вызов алерта'):
        driver.find_element(By.CSS_SELECTOR, "[onclick='alertbox()']").click()

    assert page.alert_get_text() == "I am an alert box!"
    page.alert_accept()


@allure.title('Проверка отмены алерта (OK & Cancel)')
def test_alert_cancel(driver):
    page = BasePage(driver)
    driver.get(URL)

    with allure.step("Переход в раздел 'Alert with OK & Cancel'"):
        driver.find_element(By.LINK_TEXT, 'Alert with OK & Cancel').click()
        driver.find_element(By.CSS_SELECTOR, "[onclick='confirmbox()']").click()

    assert page.alert_get_text() == 'Press a Button !'
    page.alert_dismiss()

    with allure.step('Проверка сообщения'):
        result_text = driver.find_element(By.ID, 'demo').text
        assert result_text == "You Pressed Cancel"


@allure.title('Проверка ввода текста в алерт')
def test_alert_input_text(driver):
    page = BasePage(driver)
    driver.get(URL)

    with allure.step("Переход в раздел 'Alert with Textbox'"):
        driver.find_element(By.LINK_TEXT, 'Alert with Textbox').click()
        driver.find_element(By.CSS_SELECTOR, '[onclick="promptbox()"]').click()

    name = 'Marina'
    assert page.alert_get_text() == 'Please enter your name'

    page.alert_send_keys(name)
    page.alert_accept()

    with allure.step(f"Проверка наличия имени '{name}' в результате"):
        result_element = driver.find_element(By.ID, 'demo1')
        assert name in result_element.text
