from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


with open("credentials.txt","r") as f:
    contents = f.read().split("\n")
    username , password = contents

def wait_to_load(): 
    WebDriverWait(driver, 15).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
        )   
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.pesuacademy.com/Academy/s/studentProfilePESU#"
driver.get(url)
wait = WebDriverWait(driver, 15)
#wait till all contents loads

wait_to_load()

username_field = driver.find_element(By.ID, "j_scriptusername")
username_field.send_keys(username) 

pwd_field = driver.find_element(By.NAME, "j_password")
pwd_field.send_keys(password)

sign_in_btn = driver.find_element(By.ID, "postloginform#/Academy/j_spring_security_check")
sign_in_btn.click()


wait_to_load()

my_courses = driver.find_element(By.XPATH, "//a[span[@class='menu-name' and text()='My Courses']]")
my_courses.click()

time.sleep(5)

wait_to_load()

course_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'rowWiseCourseContent_')]")))

print(f"Found {len(course_rows)} courses.")

# Iterate through each course
for index in range(len(course_rows)):
    try:
        course_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'rowWiseCourseContent_')]")))
        course = course_rows[index]
        course_id = course.get_attribute("id")
        
        print(f"Opening course: {course_id}")

        wait.until(EC.element_to_be_clickable(course)).click()

        time.sleep(1)
        my_courses_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'back_link') and contains(@onclick, 'handleShowMore')]")))
        my_courses_link.click()

        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'rowWiseCourseContent_')]")))
        
        
        continue
       

    except Exception as e:
        print(f"Error opening course {course_id}: {e}")

print("Finished opening all courses.")
time.sleep(500)