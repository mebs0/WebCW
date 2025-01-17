from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

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
        # update name
        enter_name = self.driver.find_element(By.ID, "enter_name")
        enter_name.clear()
        enter_name.send_keys("maciej")
        #self.driver.find_element(By.ID, "enter_name").send_keys("maciej")

        # update nusername
        enter_username = self.driver.find_element(By.ID, "enter_username")
        enter_username.clear()
        enter_username.send_keys("BigMac")
        #self.driver.find_element(By.ID, "enter_username").send_keys("BigMac")
        
        # update email
        enter_email = self.driver.find_element(By.ID, "enter_email")
        enter_email.clear()
        enter_email.send_keys("bigmac@gmail.com")
        #self.driver.find_element(By.ID, "enter_email").send_keys("bigmac@gmail.com")
        
        # update dob
        enter_dob = self.driver.find_element(By.ID, "enter_dob")
        enter_dob.clear()
        enter_dob.send_keys("2004-01-01")
        #self.driver.find_element(By.ID, "enter_dob").send_keys("2004-01-01")
        
        # update password
        enter_old_pass = self.driver.find_element(By.ID, "enter_old_pass")
        enter_old_pass.clear()
        enter_old_pass.send_keys("Apnl1234")
        #self.driver.find_element(By.ID, "enter_old_pass").send_keys("Apnl1234")
        self.driver.find_element(By.ID, "enter_new_pass").send_keys("Aqwer123")

        # click update button
        self.driver.find_element(By.ID, 'update_button').click()

        time.sleep(10)
        # Verify success
        assert('{"message": "User updated successfully"}', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()