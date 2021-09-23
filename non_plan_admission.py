import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import dateutil.parser
from webdriver_manager.chrome import ChromeDriverManager
from requests.structures import CaseInsensitiveDict

def valid_date(date_str):
	d = datetime.strptime(date_str, '%d %B %Y')
	return d.strftime('%d/%m/%Y')

# Non plan admission > direct admission
def direct_admission(student_info):

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(1)"))

	browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()

	browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[9]/td/a").click()

	browser.find_element_by_xpath("//*[@id='E07']/table/tbody/tr[2]/td").click()

	time.sleep(2)

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	student_info = CaseInsensitiveDict(student_info)
	if "First" in student_info:
		student_name = student_info["First"]
	else:
		student_name = student_info["First Name"]
	
	last_name = student_info["Last name"]

	grade = str(student_info["Class"])
	section = student_info["Section"]

	grade_xpath_map = {"1": 4, "2": 5, "3": 6, "4": 7, "5": 8, "I": 4, "II": 5, "III": 6, "IV": 7, "V": 8}
	section_xpath_map = {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "F": 7, "G": 8, "H": 9}

	browser.switch_to.default_content()

	print(f"Executing for {student_name} {last_name} at {datetime.now()}")

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	browser.find_element_by_xpath("//*[@id='txtFirstName']").send_keys(student_name)

	browser.find_element_by_xpath("//*[@id='txtLastName']").send_keys(last_name)

	# select grade
	grade_xpath = "//*[@id='ddlClass']/option[{}]".format(grade_xpath_map[grade])
	section_xpath = "//*[@id='ddlSection']/option[{}]".format(section_xpath_map[section])

	print(section_xpath)
	browser.find_element_by_xpath(grade_xpath).click()
	time.sleep(1)
	browser.find_element_by_xpath(section_xpath).click()

	dob = valid_date(student_info["DOB"])
	browser.find_element_by_xpath("//*[@id='txtDOB']").send_keys(dob)

	#Male/Female
	browser.find_element_by_xpath("//*[@id='ddlGender']/option[2]").click()

# Existing students > new entry
def new_entry(student_info):

	student_info = CaseInsensitiveDict(student_info)

	religion = student_info["Religion"].lower()
	admission_date = valid_date(student_info["Admission Date"])
	admission_num = student_info["Admission number"]
	address = student_info["Address"]
	father_name = student_info["Father name"]
	mother_name = student_info["Mother name"]
	social_category = student_info["Category"].lower()
	mob_num = student_info["Mob No"]
	mob_num = "9718304063"


	browser.switch_to.default_content()

	# Switch to left panel
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(1)"))

	# Student
	browser.find_element_by_xpath("//*[@id='MainIndex']/table/tbody/tr[1]/td/a").click()

	# Existing students
	browser.find_element_by_xpath("//*[@id='E']/table/tbody/tr[1]/td/a").click()

	# New entry
	browser.find_element_by_xpath("//*[@id='E01']/table/tbody/tr[8]/td/a").click()

	browser.switch_to.default_content()
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	# Direct admission
	browser.find_element_by_xpath("//*[@id='ddlType']/option[3]").click()

	time.sleep(1)

	grade = str(student_info["Class"])
	grade_xpath_map = {"1": 4, "2": 5, "3": 6, "4": 7, "5": 8, "I": 4, "II": 5, "III": 6, "IV": 7, "V": 8}

	# select grade
	grade_xpath = "//*[@id='ddlClass']/option[{}]".format(grade_xpath_map[grade])

	browser.find_element_by_xpath(grade_xpath).click()
	time.sleep(1)

	# click next
	browser.find_element_by_xpath("//*[@id='btnNext']").click()

	# select student name
	# Assumption - Just 1 name in the list
	browser.find_element_by_xpath("//*[@id='ddlStudent']/option[2]").click()
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
	elif social_category == "sc":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[3]").click()
	elif social_category == "st":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[4]").click()
	elif social_category == "obc":
		browser.find_element_by_xpath("//*[@id='ddlCategory']/option[5]").click()
	else:
		raise Exception("invalid social category")

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

	# Click submit
	browser.find_element_by_xpath("//*[@id='btnSubmit']").click()

	browser.switch_to.window(browser.window_handles[0])

	time.sleep(2)

	browser.switch_to.default_content()

	# Switch to left panel
	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	browser.find_element_by_xpath("//*[@id='btnSubmit']").click()


website_link = "http://edustud.nic.in/mis/MisAdmin/frmMisLoginStudent.aspx"

f = open('student_info_for_npa.json')
student_json_list = json.load(f)

browser = webdriver.Chrome()

browser.get(website_link)

browser.find_element_by_xpath("//*[@id='txtLoginid']").send_keys("")

browser.find_element_by_xpath("//*[@id='txtpassword']").send_keys("")

browser.find_element_by_xpath("//*[@id='ddllogintype']/option[2]").click()

browser.find_element_by_xpath("//*[@id='txtimg']").send_keys("")

student_id = browser.find_element_by_xpath("//*[@id='lblMessage']/font").text

for i in range(0,20):
	print(i)
	time.sleep(1)

for student_info in student_json_list:
	# direct_admission(student_info)
	new_entry(student_info)

