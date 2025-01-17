from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def testLogin(self):
        self.driver.get('http://127.0.0.1:8000/login/')  # Use dynamic test server URL

        # Log in to the application
        self.driver.find_element(By.ID, "id_username").send_keys("mithusen123")
        self.driver.find_element(By.ID, "id_password").send_keys("Apnl1234")
        self.driver.find_element(By.CLASS_NAME, 'loginButton').click()

        # Verify login success
        assert("ECS639 Web Programming - Group CW Template", self.driver.page_source)

    def tearDown(self):
        self.driver.quit()