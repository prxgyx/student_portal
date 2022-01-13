import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from requests.structures import CaseInsensitiveDict
from captcha import *
from selenium.webdriver.support.ui import Select
import sys
import re

file_to_write = open("exec2.log", "a")

def validate(date_text):
	try:
		datetime.strptime(date_text, '%d/%m/%Y')
		return True
	except ValueError:
		try:
			datetime.strptime(date_text, '%d/%m/%y')
			return True
		except:
			return False

def valid_date(date_str):
	if not validate(date_str):
		date_str = date_str.replace(" ", "")
		try:
			d = datetime.strptime(date_str, '%d%B%Y')
		except:
			d = datetime.strptime(date_str, '%d%b%Y')
		return d.strftime('%d/%m/%Y')
	else:
		return date_str

# Function Non plan admission > direct admission
def direct_admission(student_info):

	student_info = CaseInsensitiveDict(student_info)
	if "First" in student_info:
		student_name = student_info["First"]
	else:
		student_name = student_info["First Name"]

	print("Doing direct admission for {}".format(student_name))

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(1)"))

	time.sleep(1)

	# Click student
	browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()

	# Click Non plan admission
	# try except because sometimes student is not collapsed, so we expand it again, to make non plan admission element interactable
	try:
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[9]/td/a").click()
	except:
		browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()
		time.sleep(1)
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[9]/td/a").click()

	time.sleep(1)

	# Click direct admission
	try:
		browser.find_element_by_xpath("//*[@id='E07']/table/tbody/tr[2]/td").click()
	except:
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[9]/td/a").click()
		time.sleep(1)
		browser.find_element_by_xpath("//*[@id='E07']/table/tbody/tr[2]/td").click()

	time.sleep(2)

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	

	middle_name = student_info["Middle name"]

	last_name = student_info["Last name"]

	if "class" in student_info:
		grade = str(student_info["Class"])
	else:
		grade = str(student_info["grade"])
	section = student_info["Section"]

	grade_xpath_map = {"1": 4, "2": 5, "3": 6, "4": 7, "5": 8, "I": 4, "II": 5, "III": 6, "IV": 7, "V": 8}
	section_xpath_map = {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "F": 7, "G": 8, "H": 9}

	file_to_write.write(f"Executing for {student_name} {last_name} at {datetime.now()}\n")

	browser.find_element_by_xpath("//*[@id='txtFirstName']").send_keys(student_name)
	browser.find_element_by_xpath("//*[@id='txtMidName']").send_keys(middle_name)
	browser.find_element_by_xpath("//*[@id='txtLastName']").send_keys(last_name)

	# select grade
	grade_xpath = "//*[@id='ddlClass']/option[{}]".format(grade_xpath_map[grade])
	section_xpath = "//*[@id='ddlSection']/option[{}]".format(section_xpath_map[section])

	browser.find_element_by_xpath(grade_xpath).click()
	time.sleep(1)
	browser.find_element_by_xpath(section_xpath).click()

	if "DOB" in student_info:
		dob = student_info["DOB"]
	elif "Birth date" in student_info:
		dob = student_info["Birth date"]
	else:
		dob = student_info["Date of birth"]

	try:
		dob = valid_date(dob)
		browser.find_element_by_xpath("//*[@id='txtDOB']").send_keys(dob)

		#Male/Female
		browser.find_element_by_xpath("//*[@id='ddlGender']/option[2]").click()

		# Admission related process complete?
		browser.find_element_by_xpath("//*[@id='rblComplete_0']").click()

		# submit
		browser.find_element_by_xpath("//*[@id='btnSubmit']").click()

		time.sleep(2)

	except selenium.common.exceptions.StaleElementReferenceException as e:
		direct_admission(student_info)

	try:
		temp_id = browser.find_element_by_xpath("//*[@id='lblMsg']/font[2]").text + "\n"
		file_to_write.write(temp_id)
	except:
		data_already_exists = browser.find_element_by_xpath("//*[@id='tblMain']/tbody/tr[5]/td/center/font").text + "\n"
		file_to_write.write(data_already_exists)

	time.sleep(3)

# Function Existing students > new entry
def new_entry(student_info):

	student_info = CaseInsensitiveDict(student_info)

	religion = student_info["Religion"].lower()

	if "Admission Date" in student_info:
		admission_date = valid_date(student_info["Admission Date"])
	else:
		admission_date = valid_date(student_info["Date of Admission"])

	admission_num = student_info["Admission number"]
	address = student_info["Address"]

	if "Father name" in student_info:
		father_name = student_info["Father name"]
	else:
		father_name = student_info["Father's name"]

	if "mother name" in student_info:
		mother_name = student_info["mother name"]
	else:
		mother_name = student_info["mother's name"]

	if "Category" in student_info:
		social_category = student_info["Category"].lower()
	else:
		social_category = student_info["Social Category"].lower()

	if "phone number" in student_info:
		mob_num = student_info["phone number"]
	else:
		mob_num = student_info["Mob No"]

	if "First" in student_info:
		student_name = student_info["First"]
	else:
		student_name = student_info["First Name"]

	middle_name = student_info["Middle name"]

	last_name = student_info["Last name"]

	name = student_name + " " + middle_name + " " + last_name

	name = name.strip()

	name = re.sub(' +', ' ', name)

	browser.switch_to.default_content()

	# Switch to left panel
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(1)"))

	# Student
	browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()

	# Existing students
	try:
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[1]/td/a").click()
	except:
		browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()
		time.sleep(1)
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[1]/td/a").click()

	# New entry
	try:
		browser.find_element_by_xpath("//*[@id='E01']/table/tbody/tr[8]/td/a").click()
	except:
		browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[1]/td/a").click()
		time.sleep(1)
		browser.find_element_by_xpath("//*[@id='E01']/table/tbody/tr[8]/td/a").click()

	browser.switch_to.default_content()
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	# Direct admission
	browser.find_element_by_xpath("//*[@id='ddlType']/option[3]").click()

	time.sleep(1)

	if "class" in student_info:
		grade = str(student_info["Class"])
	else:
		grade = str(student_info["grade"])


	grade_xpath_map = {"1": 4, "2": 5, "3": 6, "4": 7, "5": 8, "I": 4, "II": 5, "III": 6, "IV": 7, "V": 8}

	# select grade
	grade_xpath = "//*[@id='ddlClass']/option[{}]".format(grade_xpath_map[grade])

	browser.find_element_by_xpath(grade_xpath).click()
	time.sleep(1)

	# click next
	browser.find_element_by_xpath("//*[@id='btnNext']").click()

	# select student name
	# Assumption - Just 1 name in the list
	selector = Select(browser.find_element_by_xpath("//*[@id='ddlStudent']"))

	# print(name)

	options = selector.options
	name_found_flag = False
	for index in range(0, len(options)-1):
		option_text = options[index].text
		# print(option_text)
		if name.lower() in option_text.lower():
			options[index].click()
			name_found_flag = True

	if not name_found_flag:
		name_idx = len(options)
		hidden_name_option = browser.find_element_by_xpath("//*[@id='ddlStudent']/option[{}]".format(name_idx))
		if name.lower() in hidden_name_option.text.lower():
			hidden_name_option.click()

	# browser.find_element_by_xpath("//*[@id='ddlStudent']/option[1]").click()
	time.sleep(2)

	# click next
	browser.find_element_by_xpath("//*[@id='btnStudentNameNext']").click()

	browser.switch_to.default_content()
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	## Student ID Creation

	# Selec birth state delhi
	browser.find_element_by_xpath("//*[@id='ddlBirthPlace']/option[7]").click()

	# Religion
	if religion == "hindu":
		browser.find_element_by_xpath("//*[@id='ddlReligion']/option[2]").click()
	elif religion == "muslim":
		browser.find_element_by_xpath("//*[@id='ddlReligion']/option[3]").click()
	else:
		raise Exception("invalid religion")

	if social_category == "general" or social_category == "gen":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[2]").click()
	elif social_category == "sc" or social_category == "s/c":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[3]").click()
	elif social_category == "st" or social_category == "s/t":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[4]").click()
	elif social_category == "obc":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[5]").click()
	else:
		raise Exception("invalid social category - {}".format(social_category))

	browser.find_element_by_xpath("//*[@id='txtAdmissionDate']").send_keys(admission_date)

	browser.find_element_by_xpath("//*[@id='txtAdmissionNo']").send_keys(admission_num)

	browser.find_element_by_xpath("//*[@id='txtCorAddress']").send_keys(address)

	browser.find_element_by_xpath("//*[@id='txtPhoneNo']").send_keys(mob_num)

	# Select state Delhi
	browser.find_element_by_xpath("//*[@id='ddlCorState']/option[7]").click()
	# Select city Delhi
	browser.find_element_by_xpath("//*[@id='ddlCorCity']/option[18]").click()

	# select birth certificate
	browser.find_element_by_xpath("//*[@id='rbBirthCertificate_0']").click()

	browser.find_element_by_xpath("//*[@id='rbtnDisability_1']").click()

	time.sleep(1)

	# Create family ID
	browser.find_element_by_xpath("//*[@id='Label1']/a").click()

	# Switch to search family member window
	browser.switch_to.window(browser.window_handles[1])

	# Select family income 10k-15k
	browser.find_element_by_xpath("//*[@id='ddlIncome']/option[5]").click()
	browser.find_element_by_xpath("//*[@id='txtFatherName']").send_keys(father_name)
	# Select father occupation N/A
	browser.find_element_by_xpath("//*[@id='ddlFatherOccupation']/option[6]").click()
	browser.find_element_by_xpath("//*[@id='txtMotherName']").send_keys(mother_name)

	# Click submit for family ID
	browser.find_element_by_xpath("//*[@id='btnSubmit']").click()

	browser.switch_to.window(browser.window_handles[0])

	time.sleep(2)

	browser.switch_to.default_content()

	# Switch to left panel
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	browser.find_element(By.ID,"btnSumbit").click()

	student_id = browser.find_element_by_xpath("//*[@id='lblMessage']/font").text + "\n"

	file_to_write.write(student_id)

	if("Temporary" in student_id):
		print(student_id)
		sys.exit()

def data_validate(student_json_list):

	sample_student = CaseInsensitiveDict(student_json_list[0])

	key_list = ["First", "First Name", "Middle name", "Last name", "Class", "grade", "Section", "DOB", "Birth date", "Date of birth", "Religion", "Admission Date", "Date of Admission", "Admission number", "Address", "Father name", "Mother name", "Category", "Mob No"]

	key_error = []

	for key_name in key_list:
		if key_name not in sample_student:
			key_error.append(key_name)

	print("Keys missing in data - " + str(key_error))

	for student_info in student_json_list:

		student_info = CaseInsensitiveDict(student_info)
		if "DOB" in student_info:
			dob = student_info["DOB"]
		elif "Birth date" in student_info:
			dob = student_info["Birth date"]
		else:
			dob = student_info["Date of birth"]

		dob = valid_date(dob)

		# print(student_info)

		if "Admission Date" in student_info:
			admission_date = valid_date(student_info["Admission Date"])
		else:
			admission_date = valid_date(student_info["Date of Admission"])

def enter_login(browser):
	print("Entering username, password and captcha")

	old_url = browser.current_url

	browser.find_element_by_xpath("//*[@id='txtLoginid']").send_keys("1959115")

	browser.find_element_by_xpath("//*[@id='txtpassword']").send_keys("99009900")

	browser.find_element_by_xpath("//*[@id='ddllogintype']/option[2]").click()

	with open('IMG.png', 'wb') as file:
	    file.write(browser.find_element_by_xpath('//*[@id="table3"]/tbody/tr[5]/td[2]/img').screenshot_as_png)

	write_text_from_image()
	captcha = read_text_from_image()

	browser.find_element_by_xpath("//*[@id='txtimg']").send_keys(captcha)
	file_to_write.write(captcha)

	time.sleep(3)

	browser.find_element_by_xpath("//*[@id='btnSubmit']").click()

	time.sleep(3)

	new_url = browser.current_url

	## Retry in case captcha is incorrect
	if new_url == old_url:
		enter_login(browser)


# def main():

if __name__ == '__main__':
	website_link = "http://edustud.nic.in/mis/MisAdmin/frmMisLoginStudent.aspx"

	f = open('student_info_for_npa.json')
	student_json_list = json.load(f)

	data_validate(student_json_list)

	chrome_options = Options()
	# chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	# options.headless = True

	browser = webdriver.Chrome(options=chrome_options)

	browser.get(website_link)

	enter_login(browser)

	student_info = student_json_list[0]

	# for i in range(0,20):
	# 	print(i)
	# 	time.sleep(1)


	for student_info in student_json_list:
		direct_admission(student_info)
		new_entry(student_info)
