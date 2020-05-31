import os
import time
import requests
from PIL import Image
import pytesseract
from selenium import webdriver

#BEGIN CHANGE HERE

chromedriver = "./chromedriver"

users = [	
	['user1','pass1'],
	['user2','pass2'],
	['user3','pass3'],
	['user4','pass4']
]

#END CHANGE HERE

url_login = "http://svktx.vnuhcm.edu.vn"
url_report = "http://svktx.vnuhcm.edu.vn/Default/DiseaseCovidReport"

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

def get_captcha(driver):
	captcha_tmp = "captcha_tmp.png"
	driver.save_screenshot(captcha_tmp)
	image_captcha = Image.open(captcha_tmp)
	left = 466
	right = left + 92
	top = 406
	bottom = top + 39
	image_captcha = image_captcha.crop((left, top, right, bottom))
	image_captcha.save(captcha_tmp)
	captcha = pytesseract.image_to_string(Image.open(captcha_tmp), config='digits')
	os.remove(captcha_tmp)
	return captcha

def Login(username, password):
	driver = webdriver.Chrome(chromedriver)
	driver.get(url_login)
	captcha = get_captcha(driver)
	if (len(captcha) == 5):
		driver.find_element_by_id('StudentCode').send_keys(username)
		driver.find_element_by_id('PIN').send_keys(password)
		driver.find_element_by_id('Captcha').send_keys(captcha)
		driver.find_element_by_css_selector('[class="btn btn-primary"]').click()
		driver.get(url_report)
		params = driver.find_elements_by_css_selector("input[type='radio'][value='False']")
		for param in params:
			param.click()
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		driver.find_element_by_id('isCheck').click()
		driver.find_element_by_css_selector('[class="btn btn-success"]').click()
		time.sleep(2)
	else:
		Login(username, password)
	driver.close()

for user in users:	
	Login(user[0], user[1])
	print("- Report success for", user[0], " !!!")
