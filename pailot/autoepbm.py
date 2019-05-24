from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from random import randint
from time import sleep

TIMEOUT = 60 # in seconds

driver = webdriver.Firefox()
driver.get('https://simak.ipb.ac.id/Account/Login')
username = raw_input('username : ')
password = getpass(prompt='password : ')
userField = driver.find_element_by_name("UserName")
passField = user = driver.find_element_by_name("Password")
userField.send_keys(username)
passField.send_keys(password)
passField.send_keys(Keys.ENTER)

WebDriverWait(driver, TIMEOUT).until(
	EC.presence_of_element_located((By.XPATH, "//img[@class='animation-pulseSlow']"))
)
driver.get('https://simak.ipb.ac.id/EPBMOnline/EPBM')
while True:
	try:	
		WebDriverWait(driver, TIMEOUT).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='panel panel-danger']"))
		)
	except:
		driver.quit()
		exit(0)
	driver.find_element_by_xpath("//div[@class='panel panel-danger']").click()
	
	WebDriverWait(driver, TIMEOUT).until(
		EC.presence_of_element_located((By.XPATH, "//input[@type='radio']"))
		)
	threes = driver.find_elements_by_xpath("//input[@type='radio' and @value='3']")
	fours = driver.find_elements_by_xpath("//input[@type='radio' and @value='4']")
	
	for i in range(len(threes)):
		r = randint(1,2)
		if r == 1:
			threes[i].click()
		else:
			fours[i].click()
	
	driver.find_element_by_xpath("//input[@type='checkbox']").click()
	driver.find_element_by_xpath("//input[@class='btn btn-lg btn-primary']").click()


