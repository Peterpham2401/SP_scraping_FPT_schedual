from selenium import  webdriver
from selenium.webdriver.support.select import Select
from Database_manager import Database
from Google_Calendar_APIs import Add_Event
import serect

username = serect.get_username()
password = serect.get_password()


driver = webdriver.Chrome()
driver.get("https://fap.fpt.edu.vn/")


#select campus
select_campus = Select(driver.find_element_by_id("ctl00_mainContent_ddlCampus"))
HCM_campus = select_campus.select_by_visible_text("FU-Hồ Chí Minh")

#Sign_in button and switch page to enter
sign_in = driver.find_element_by_xpath('//*[@id="loginform"]/center/div/div[2]/div/div/div/span')
sign_in.click()

pages = driver.window_handles
base_page = pages[0]
driver.switch_to_window(driver.window_handles[1])
#Enter email to login
email_in = driver.find_element_by_id("identifierId").send_keys(username)
continue_click = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span')
continue_click.click()

driver.implicitly_wait(5)
#Enter password
password_in = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
continue_click = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/span')
continue_click.click()



driver.switch_to_window(base_page)

#Enter to Attendency Report to collect data
attendency_report = driver.find_element_by_xpath('//*[@id="ctl00_mainContent_divMain"]/div[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/ul/li[1]/a')
attendency_report.click()


semester = driver.find_element_by_xpath('/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr[14]/td/b')
storage = Database(semester.text)

course_frame = driver.find_element_by_xpath('/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/table')
courses = course_frame.find_elements_by_tag_name('td')
ID_courselist = list()
for course in courses:
    course_name = course.text.replace('(',',').replace(')',',').split(',')[0].strip()
    course_id = course.text.replace('(',',').replace(')',',').split(',')[1].strip()
    ID_courselist.append(course_id)
    storage.addValue_Course(course_id,course_name)


i = 2
index_course = 0
while i  <= len(courses)+1:
    try:
        schedual_frame = driver.find_element_by_xpath('/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table/tbody[2]')
        schedual = schedual_frame.find_elements_by_tag_name('td')

        index_DOWDateMonth, index_Slot, index_Class= 1, 2, 5
        while index_Class < len(schedual):
            DOWDate_Month, Slot=  schedual[index_DOWDateMonth].text, schedual[index_Slot].text
            Date = DOWDate_Month.split(' ')[1]
            storage.addValue_Calendar(Date,Slot, ID_courselist[index_course])
            index_DOWDateMonth += 8
            index_Slot += 8
            index_Class += 8


        next_course = driver.find_element_by_xpath(f'/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/table/tbody/tr[{i}]/td/a')
        next_course.click()
        index_course +=1
        i += 1
    except:
        break
driver.quit()


datas = storage.retrive_Calendar()

'''
for data in datas:
    try:
        name = data[0]
        date = data[1]
        time_start = data[2]
        time_end = data [3]
        Add_Event(name,date,time_start,time_end)
    except:
        continue
'''