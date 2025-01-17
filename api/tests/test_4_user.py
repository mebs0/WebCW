from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestProfile(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def testProfile(self):
        # Register user
        self.driver.get('http://127.0.0.1:8000/register/')
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.driver.find_element(By.ID, "id_username").send_keys("mithusen123")
        self.driver.find_element(By.ID, "id_email").send_keys("mithu@sen.com")
        self.driver.find_element(By.ID, "id_name").send_keys("mithusen")
        self.driver.find_element(By.ID, "id_date_of_birth").send_keys("2000-01-01")
        self.driver.find_element(By.ID, "id_password1").send_keys("Apnl1234")
        self.driver.find_element(By.ID, "id_password2").send_keys("Apnl1234")
        self.driver.find_element(By.CLASS_NAME, 'registerButton').click()

        # Log in to the application
        self.driver.get('http://127.0.0.1:8000/login/')
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.driver.find_element(By.ID, "id_username").send_keys("mithusen123")
        self.driver.find_element(By.ID, "id_password").send_keys("Apnl1234")
        self.driver.find_element(By.CLASS_NAME, 'loginButton').click()
        self.wait.until(EC.presence_of_element_located((By.ID, "enter_name")))

        # Update profile
        self.driver.find_element(By.ID, "enter_name").send_keys("maciej")
        self.driver.find_element(By.ID, "enter_username").send_keys("BigMac")
        self.driver.find_element(By.ID, "enter_email").send_keys("bigmac@gmail.com")
        self.driver.find_element(By.ID, "enter_dob").send_keys("2004-01-01")
        self.driver.find_element(By.ID, "enter_old_pass").send_keys("Apnl1234")
        self.driver.find_element(By.ID, "enter_new_pass").send_keys("Aqwer123")
        self.driver.find_element(By.ID, 'update_button').click()

        # Filter by age
        self.driver.find_element(By.ID, 'otherUsers').click()
        self.driver.find_element(By.ID, 'minAge').click()
        self.driver.find_element(By.ID, 'maxAge').click()
        self.driver.find_element(By.ID, 'filterButton').click()
        WebDriverWait(10)

        # Verify success
        ##assert('{"message": "User updated successfully"}', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()