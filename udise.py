import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import datetime
import dateutil.parser
from requests.structures import CaseInsensitiveDict

doe_website_link = "http://www.edudel.nic.in/mis/dise/frmLoginDise.aspx"

def valid_date(date_str):
	slash_split = date_str.split("/")
	try:
		if len(slash_split) !=2:
			if len(slash_split[2]) == 2:
				fmt_date = datetime.datetime.strptime(date_str, '%d/%m/%y')
			elif len(slash_split[2]) == 4:
				fmt_date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
			else:
				raise Exception("invalid date - {}".format(date_str))
		else:
			raise Exception("invalid date - {}".format(date_str))
	except:
		fmt_date = dateutil.parser.parse(date_str)
	fmt_date = fmt_date.strftime('%d/%m/%Y')
	return fmt_date

def click_udise_to_class_section(student_info, edit=None):
	student_info = CaseInsensitiveDict(student_info)
	if "Grade" in student_info:
		grade = str(student_info["Grade"])
	else:
		grade = str(student_info["Grade/Class"])

	grade_xpath_map = {"1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "I": 2, "II": 3, "III": 4, "IV": 5, "V": 6}

	section = student_info["Section"]
	section_xpath_map = {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "F": 7, "G": 8, "H": 9}

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset:nth-child(2) > frameset:nth-child(2) > frame:nth-child(1)"))

	# Click UDISE
	browser.find_element_by_xpath("//*[@id='Table1']/tbody/tr[1]/td/a").click()

	time.sleep(2)

	browser.switch_to.default_content()

	# pageSource = browser.page_source
	# fileToWrite = open("page_source.html", "w")
	# fileToWrite.write(pageSource)
	# fileToWrite.close()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset:nth-child(2) > frameset:nth-child(2) > frame:nth-child(2)"))

	# Click Update, search, entry
	browser.find_element_by_xpath("//*[@id='tblReport']/tbody/tr[4]/td[5]/a[1]/font/b").click()

	time.sleep(2)

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset > frameset > frame:nth-child(2)"))

	# Click New entry
	if edit:
		new_entry_xpath = "//*[@id='RadioButtonList1_1']"
		grade_xpath = "/html/body/form/table/tbody/tr[1]/td[2]/select/option[{}]".format(grade_xpath_map[grade])
		section_xpath = "/html/body/form/table/tbody/tr[2]/td[2]/select/option[{}]".format(section_xpath_map[section] + 1)
		next_xpath = "//*[@id='Button1']"
	else:
		new_entry_xpath = "//*[@id='RadioButtonList1_0']"
		grade_xpath = "/html/body/form/table/tbody/tr[2]/td[2]/select/option[{}]".format(grade_xpath_map[grade])
		section_xpath = "/html/body/form/table/tbody/tr[3]/td[2]/select/option[{}]".format(section_xpath_map[section])
		next_xpath = "//*[@id='btnNext']"

	browser.find_element_by_xpath(new_entry_xpath).click()
	time.sleep(2)

	browser.switch_to.default_content()

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset:nth-child(2) > frameset:nth-child(2) > frame:nth-child(2)"))

	#Select grade
	browser.find_element_by_xpath(grade_xpath).click()

	# time.sleep(1)

	#Select section
	browser.find_element_by_xpath(section_xpath).click()

	# Click next
	browser.find_element_by_xpath(next_xpath).click()

def fill_student_form(student_info, retry, retry_num):
	student_info = CaseInsensitiveDict(student_info)
	if "First" in student_info:
		student_name = student_info["First"]
	else:
		student_name = student_info["First Name"]

	if retry:
		student_name = "Retry" + student_name
	
	middle_name = student_info["Middle Name"]
	last_name = student_info["Last name"]
	father_name = student_info["Father's Name"]
	mother_name = student_info["Mother's Name"]
	dob = valid_date(student_info["Date of birth"])
	social_category = student_info["Social Category"].lower()
	religion = student_info["Religion"].lower()
	address = student_info["Address"]
	admission_date = valid_date(student_info["Date of Admission"])
	admission_num = student_info["Admission Number"]
	
	if "Medium" in student_info:
		inst_medium = student_info["Medium"]
	else:
		inst_medium = student_info["Medium of instruction"]

	inst_medium = inst_medium.lower()
	if "Grade" in student_info:
		grade = str(student_info["Grade"])
	else:
		grade = str(student_info["Grade/Class"])
	section = student_info["Section"]

	browser.switch_to.default_content()

	print(f"Executing for {student_name} {middle_name} {last_name} at {datetime.datetime.now()}")

	browser.switch_to.frame(browser.find_element_by_css_selector("html > frameset:nth-child(2) > frameset:nth-child(2) > frame:nth-child(2)"))

	browser.find_element_by_xpath("//*[@id='txtStudentNameF']").send_keys(student_name)

	browser.find_element_by_xpath("//*[@id='txtStudentNameM']").send_keys(middle_name)

	browser.find_element_by_xpath("//*[@id='txtStudentNameL']").send_keys(last_name)

	browser.find_element_by_xpath("//*[@id='txtFatherName']").send_keys(father_name)

	browser.find_element_by_xpath("//*[@id='txtMotherName']").send_keys(mother_name)

	browser.find_element_by_xpath("//*[@id='txtDOB']").send_keys(dob)

	#Male/Female
	browser.find_element_by_xpath("//*[@id='rbtnSex_0']").click()

	if social_category == "general" or social_category == "gen":
		browser.find_element_by_xpath("//*[@id='rbtnCaste_0']").click()
	elif social_category == "sc":
		browser.find_element_by_xpath("//*[@id='rbtnCaste_1']").click()
	elif social_category == "st":
		browser.find_element_by_xpath("//*[@id='rbtnCaste_2']").click()
	elif social_category == "obc":
		browser.find_element_by_xpath("//*[@id='rbtnCaste_3']").click()
	else:
		raise Exception("invalid social category")

	if religion == "hindu":
		browser.find_element_by_xpath("//*[@id='ddlReligion']/option[2]").click()
	elif religion == "muslim":
		browser.find_element_by_xpath("//*[@id='ddlReligion']/option[3]").click()
	else:
		raise Exception("invalid religion")

	# Language
	browser.find_element_by_xpath("//*[@id='ddlMotherTongue']/option[5]").click()

	browser.find_element_by_xpath("//*[@id='txtLocality']").send_keys(address)

	browser.find_element_by_xpath("//*[@id='txtadmissionDate']").send_keys(admission_date)

	browser.find_element_by_xpath("//*[@id='txtadmissionNo']").send_keys(admission_num)

	time.sleep(2)

	browser.find_element_by_xpath("//*[@id='rbtnBpl_1']").click()

	browser.find_element_by_xpath("//*[@id='rbtnDisadvantagedGroup_1']").click()

	browser.find_element_by_xpath("//*[@id='rbtnfreeEducation_0']").click()

	browser.find_element_by_xpath("//*[@id='ddlClassStudyPrevious']/option[16]").click()

	browser.find_element_by_xpath("//*[@id='ddlstudyingClass1']/option[2]").click()

	# browser.find_element_by_xpath("").click()

	browser.find_element_by_xpath("//*[@id='txtchildAttended']").send_keys("0")

	if inst_medium == "english":
		browser.find_element_by_xpath("//*[@id='ddlMediumofInstruction']/option[20]").click()
	# Default is Hindi
	else:
		browser.find_element_by_xpath("//*[@id='ddlMediumofInstruction']/option[5]").click()

	browser.find_element_by_xpath("//*[@id='ddlTypeofDisability']/option[2]").click()

	browser.find_element_by_xpath("//*[@id='ddlFacilitiesCWSN1']/option[2]").click()

	browser.find_element_by_xpath("//*[@id='rbtnNoofuniformset_0']").click()

	browser.find_element_by_xpath("//*[@id='RbtnfreeTextbook_1']").click()

	browser.find_element_by_xpath("//*[@id='RbtnFreeTransportfacility_0']").click()

	browser.find_element_by_xpath("//*[@id='rbtnfreebicycle_0']").click()

	browser.find_element_by_xpath("//*[@id='RbtnFreeEscortfacility_2']").click()

	browser.find_element_by_xpath("//*[@id='RbtnMDM_1']").click()

	browser.find_element_by_xpath("//*[@id='ddlFreeHostelfacility']/option[2]").click()

	browser.find_element_by_xpath("//*[@id='RbtnChildattendedSpecialTraining_0']").click()

	browser.find_element_by_xpath("//*[@id='RbtnIronFolicacid_0']").click()

	browser.find_element_by_xpath("//*[@id='RbtnDewormingtablets_0']").click()

	browser.find_element_by_xpath("//*[@id='RbtnVitaminsupplement_0']").click()

	browser.find_element_by_xpath("//*[@id='Rbtnhomeless_1']").click()

	browser.find_element_by_xpath("//*[@id='RbtnAppearedlastexamination_1']").click()

	browser.find_element_by_xpath("//*[@id='RbtnPassedlastexamination_3']").click()

	browser.find_element_by_xpath("//*[@id='txtMarksobtained']").send_keys("0")

	browser.find_element_by_xpath("//*[@id='btnPreview']").click()

	time.sleep(2)

	try:
		browser.find_element_by_xpath("//*[@id='btnSubmit']").click()
	except Exception as e:
		error_text = student_name + " " + middle_name + " " + last_name + " " + grade + section + "\n"
		fileToWrite = open("failed.txt", "a")
		if retry_num >= 0:
			error_text = "Failed - " + error_text
			fileToWrite.write(error_text)
		else:
			retry_num = retry_num + 1
			error_text = "Retry - " + error_text
			fileToWrite.write(error_text)
			click_udise_to_class_section(student_info)
			fill_student_form(student_info, True, retry_num)

def get_edit_student_table(student_info):

	print("Fetching student table")
	click_udise_to_class_section(student_info, True)

	pageSource = browser.page_source
	fileToWrite = open("page_source.html", "w")
	fileToWrite.write(pageSource)
	fileToWrite.close()

	table = browser.find_elements_by_css_selector("#GridView3 > tbody > tr")

	return table

def validate_student_data(student_json_list):
	for student_info in student_json_list:
		student_info = CaseInsensitiveDict(student_info)
		if "First" in student_info:
			student_name = student_info["First"]
		else:
			student_name = student_info["First Name"]

		middle_name = student_info["Middle Name"]
		last_name = student_info["Last name"]
		father_name = student_info["Father's Name"]
		mother_name = student_info["Mother's Name"]
		dob = valid_date(student_info["Date of birth"])
		social_category = student_info["Social Category"].lower()
		religion = student_info["Religion"].lower()
		address = student_info["Address"]
		admission_date = valid_date(student_info["Date of Admission"])
		admission_num = student_info["Admission Number"]
		
		if "Medium" in student_info:
			inst_medium = student_info["Medium"]
		else:
			inst_medium = student_info["Medium of instruction"]

		inst_medium = inst_medium.lower()
		if "Grade" in student_info:
			grade = str(student_info["Grade"])
		else:
			grade = str(student_info["Grade/Class"])
		section = student_info["Section"]

def edit_instruction_medium(student_info):
	table = get_edit_student_table(student_info)

	# student_name_index = 3

	inst_medium_index = 27
	update_index = 1
	hindi_medium_option = 5

	for row_idx, row in enumerate(table[1:]):
		time.sleep(1)
		row_xpath = f"/html/body/form/table/tbody/tr[4]/td/div/table/tbody/tr[{row_idx+2}]"

		# Click edit button
		browser.find_element_by_xpath(f"{row_xpath}/td[1]/a").click()
		inst_medium_xpath = f"{row_xpath}/td[{inst_medium_index}]/select/option[{hindi_medium_option}]"
		browser.find_element_by_xpath(inst_medium_xpath).click()

		#Click update
		browser.find_element_by_xpath(f"{row_xpath}/td[{update_index}]/a[1]").click()
		time.sleep(2)

def edit_retry(student_info):
	table = get_edit_student_table(student_info)
	print("Fetched student table")

	if "First" in student_info:
		student_name = student_info["First"]
	else:
		student_name = student_info["First Name"]

	# Retry_student_name
	backspaces_num = len(student_name) + 6

	name_index = 4

	# //*[@id="GridView3_ctl02_Label42"]

	for row_idx, row in enumerate(table[1:]):
		time.sleep(1)
		row_xpath = f"/html/body/form/table/tbody/tr[4]/td/div/table/tbody/tr[{row_idx+2}]"

		print(f"Finding cols of row - {row_idx}")
		row_values = row.find_elements_by_tag_name('td')

		if row_values[3].text == "Retry" + student_name:

			# /html/body/form/table/tbody/tr[4]/td/div/table/tbody/tr[19]/td[1]/a
			# Click edit button
			browser.find_element_by_xpath(f"{row_xpath}/td[1]/a").click()

			# Because of leading zero for single digits
			if row_idx < 8:
				row_str = f"0{row_idx + 2}"
			else:
				row_str = row_idx + 2


			name_xpath = f"//*[@id='GridView3_ctl{row_str}_txtfname']"
			browser.find_element_by_xpath(name_xpath).send_keys(Keys.BACK_SPACE*backspaces_num)
			browser.find_element_by_xpath(name_xpath).send_keys(student_name)

			time.sleep(1)

			#Click update
			browser.find_element_by_xpath(f"{row_xpath}/td[1]/a[1]").click()
			time.sleep(2)
			return

f = open('student_info.json')
student_json_list = json.load(f)

validate_student_data(student_json_list)

fireFoxOptions = webdriver.FirefoxOptions()

browser = webdriver.Firefox(options=fireFoxOptions)

browser.get(doe_website_link)

time.sleep(3)

browser.find_element_by_xpath("//*[@id='txtUserID']").send_keys("")

browser.find_element_by_xpath("//*[@id='txtpassword']").send_keys("")

browser.find_element_by_xpath("//*[@id='txtimg']").send_keys("")

for i in range(0,6):
	# print(i)
	time.sleep(1)

for student_info in student_json_list:
	# edit_instruction_medium(student_info)
	# 
	click_udise_to_class_section(student_info)
	fill_student_form(student_info, False, 0)
	# edit_retry(student_info)


