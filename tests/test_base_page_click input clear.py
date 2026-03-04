import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step
    def find(self, locator):
        return self.driver.find_element(*locator)

    @allure.step
    def click(self, locator):
        self.find(locator).click()

    @allure.step
    def click_js(self, locator):
        element = self.find(locator)
        self.driver.execute_script('arguments[0].click();', element)

    @allure.step
    def scroll_to_element(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step
    def send_keys(self, locator, text):
        self.find(locator).send_keys(text)

    @allure.step
    def send_enter(self, locator):
        self.find(locator).send_keys(Keys.ENTER)

    @allure.step
    def clear_input(self, locator):
        self.find(locator).clear()

    @allure.step
    def click_via_actions(self, locator):
        element = self.find(locator)
        ActionChains(self.driver).move_to_element(element).click().perform()

    @allure.step
    def get_text(self, locator):
        return self.find(locator).text


class SubscriptionPage(BasePage):
    URL = 'http://localhost:3000/automation-lab/subscription'

    GOALS_BTN = (By.CSS_SELECTOR, 'button.task-goals-btn')
    CLOSE_MODAL = (By.CSS_SELECTOR, 'button.modal-close-x')
    PERIOD_BTN = (By.CSS_SELECTOR, 'button.period-btn')
    PROMO_INPUT = (By.CSS_SELECTOR, '.promo-input-wrapper input')
    PROMO_APPLY_BTN = (By.CSS_SELECTOR, 'button.promo-apply-btn')
    PROMO_SUCCESS_MSG = (By.CSS_SELECTOR, '.promo-message.success')
    PROMO_HINT_BTN = (By.CSS_SELECTOR, 'button.promo-hint-btn')

    @allure.step('Открытие страницы подписки')
    def open(self):
        self.driver.get(self.URL)


@allure.feature('Подписка')
@allure.story('Проверка (клики, ввод, скролл)')
@allure.severity(allure.severity_level.CRITICAL)
def test_all_click_methods(driver):
    page = SubscriptionPage(driver)

    page.open()

    page.click(page.GOALS_BTN)
    time.sleep(2)
    page.click(page.CLOSE_MODAL)

    page.click_js(page.PERIOD_BTN)

    page.scroll_to_element(page.PROMO_INPUT)
    page.send_keys(page.PROMO_INPUT, 'ALWAYS')

    page.send_enter(page.PROMO_APPLY_BTN)

    with allure.step('сообщение об успешном применении промокода'):
        expected_text = 'Промокод применён: Скидка 15% для для всех тарифов'
        actual_text = page.get_text(page.PROMO_SUCCESS_MSG)
        assert actual_text == expected_text

    page.clear_input(page.PROMO_INPUT)
    page.click_via_actions(page.PROMO_HINT_BTN)
    time.sleep(2)
    page.click(page.CLOSE_MODAL)
