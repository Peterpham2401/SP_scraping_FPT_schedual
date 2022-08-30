from selenium import  webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from Database_manager import Database
from Google_Calendar_APIs import Add_Event, get_list_event, Update_event
import serect

# username = serect.get_username()
# password = serect.get_password()


# driver = webdriver.Chrome()
# driver.get("https://fap.fpt.edu.vn/")


# #select campus
# select_campus = Select(driver.find_element(By.ID, "ctl00_mainContent_ddlCampus"))
# HCM_campus = select_campus.select_by_visible_text("FU-Hồ Chí Minh")

# #Sign_in button and switch page to enter
# sign_in = driver.find_element(By.XPATH, '//*[@id="loginform"]/center/div/div[2]/div/div/div/span')
# sign_in.click()

# pages = driver.window_handles
# base_page = pages[0]
# print(f'Switching window {driver.window_handles[1]} ')
# driver.switch_to.window(driver.window_handles[1])
# #Enter email to login
# email_in = driver.find_element(By.ID, "identifierId").send_keys(username)
# continue_click = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
# continue_click.click()

# driver.implicitly_wait(30)
# #Enter password
# password_in = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
# continue_click = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
# continue_click.click()



# driver.switch_to.window(base_page)

# #Enter to Attendency Report to collect data
# print('Click attendency_report')
# attendency_report = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li[1]/a')
# attendency_report.click()

# print('Colleting data starting ...')
# semester_frame = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/table/tbody')
# semesters = semester_frame.find_elements(By.TAG_NAME,'td')
# storage = Database(semesters[-1].text)
# print(f'Semester is {semesters[-1].text}')

# course_frame = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/table')
# courses = course_frame.find_elements(By.TAG_NAME, 'td')
# ID_courselist = list()
# for course in courses:
#     course_name = course.text.replace('(',',').replace(')',',').split(',')[0].strip()
#     course_id = course.text.replace('(',',').replace(')',',').split(',')[1].strip()
#     ID_courselist.append(course_id)
#     storage.addValue_Course(course_id,course_name)
#     print(f'Add {course_name}, {course_id} to databse Course')


# i = 2
# index_course = 0
# while i  <= len(courses)+1:
#     try:
#         # Get the schedual frame
#         schedual_frame = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table/tbody[2]')
#         schedual = schedual_frame.find_elements(By.TAG_NAME, 'td')

#         index_DOWDateMonth, index_Slot, index_Class= 1, 2, 5
#         while index_Class < len(schedual):
#             DOWDate_Month, Slot=  schedual[index_DOWDateMonth].text, schedual[index_Slot].text
#             Date = DOWDate_Month.split(' ')[1]
#             print(f'Date: {Date} - Slot: {Slot}')
#             storage.addValue_Calendar(Date,Slot, ID_courselist[index_course])
#             index_DOWDateMonth += 8
#             index_Slot += 8
#             index_Class += 8


#         next_course = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/table/tbody/tr[{i}]/td/a')
#         print(f'\n====\nNext course is : {next_course.text}')
#         next_course.click()
#         index_course +=1
#         i += 1
#     except:
#         break
# driver.quit()

storage = Database('Fall2022')
datas = storage.retrive_Calendar()
ls_event_id = get_list_event()
print(f'\n List event id in google calendar:\n{ls_event_id}')
if ls_event_id is None:
    for data in datas:
        try:
            name = data[0]
            date = data[1]
            time_start = data[2]
            time_end = data [3]
            ID_db_event = data[4]
            Add_Event(name, date, time_start, time_end, ID_db_event)
        except:
            continue
else:
    for data in datas:
        try:
            name = data[0]
            date = data[1]
            time_start = data[2]
            time_end = data [3]
            ID_db_event = data[4]
            ID_gg_event = data[5]
            print(f'\n {name} - {date} - {ID_db_event} - {ID_gg_event}')
            if ID_gg_event in ls_event_id:
                print(f'Calendar have event: {ID_db_event}')
                Update_event(date, time_start, time_end, ID_gg_event)
            else:
                Add_Event(storage, name, date, time_start, time_end, ID_db_event)
        except (Exception) as error:
            print(error)
            continue
