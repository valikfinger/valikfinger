# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import unittest


class AddressBookTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost/addressbook/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_add_contact(self):
        driver = self.driver
        self.login("admin", "secret")
        self.add_new_contact("Taldykin", "Valeriy", "vval1", "Omsk, tarariratampampam", "valeravalik@list.ru", "7",
                             "April", "2003")
        driver.find_element(By.LINK_TEXT, "home page").click()

    def login(self, username, password):
        driver = self.driver
        driver.get(self.base_url)
        self.fill_input(By.NAME, "user", username)
        self.fill_input(By.NAME, "pass", password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

    def add_new_contact(self, firstname, middlename, nickname, address, email, bday, bmonth, byear):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "add new").click()

        self.fill_input(By.NAME, "firstname", firstname)
        self.fill_input(By.NAME, "middlename", middlename)
        self.fill_input(By.NAME, "nickname", nickname)
        self.fill_input(By.NAME, "address", address)
        self.fill_input(By.NAME, "email", email)

        Select(driver.find_element(By.NAME, "bday")).select_by_visible_text(bday)
        Select(driver.find_element(By.NAME, "bmonth")).select_by_visible_text(bmonth)

        self.fill_input(By.NAME, "byear", byear)

        driver.find_element(By.XPATH, "//div[@id='content']/form/input[20]").click()

    def fill_input(self, by, value, text):
        element = self.driver.find_element(by, value)
        element.click()
        element.clear()
        element.send_keys(text)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
            return True
        except NoSuchElementException:
            return False

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
