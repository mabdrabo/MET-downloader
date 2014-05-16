#!/usr/bin/python
#Author: Mahmoud Abdrabo
#Date: 2013 Sat Sep 28, 4:05:14

################################# EDIT ####################################
UNIVERSITY_PATH = "/Users/mahmoud/Documents/University" # full path to university folder
SEMESTER_NUMBER = "Semester 10"  # semester number
COURSES_ID = [462, 474, 479, 492, 493, 494] # found in the url of the course page
USE_LOGIN = True    # to login to MET and download password-protected files
STUDENT_EMAIL = "mahmoud.abdrabo@student.guc.edu.eg"    # guc email address
STUDENT_PASSWORD = "password"    # met password (you can leave it empty, and enter it in CLI)

############## NO EDIT (UNLESS YOU KNOW WHAT YOU ARE DOING) ##############
from selenium import webdriver
import getpass
import time
import os

MET_COURSE_URL = "http://met.guc.edu.eg/Courses/Material.aspx?crsEdId="    # MET Course Material URL
MET_HOME_URL = "http://met.guc.edu.eg/" # MET Home URL

files_count = 0

def wait_till_download():
   print "Downloading.",
   if len(new_part_files) > 0:
        time.sleep(1)
        print ".",
        [wait_till_download() for part_file in new_part_files if part_file in os.listdir(".")]
   print "DONE"


def move_files():
    if len(files_dict) > 0:
        print "Moving files to correct locations"
        [os.rename(f, k + f) for k, v in files_dict.iteritems() for f in v]


fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("network.http.max-connections-per-server", 25)
file_types = "text/plain, application/vnd.ms-excel, application/vnd.sealed.ppt, application/vnd.sealed.doc," \
            "text/csv, text/comma-separated-values, application/octet-stream"
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", file_types)
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
crawler = webdriver.Firefox(firefox_profile=fp)

if USE_LOGIN:
    if not STUDENT_PASSWORD:
        print "Enter password for " + STUDENT_EMAIL
        STUDENT_PASSWORD = getpass.getpass()
    crawler.get(MET_HOME_URL) # Load home page
    email_field = crawler.find_element_by_id("LoginUserControl1_usernameTextBox")
    email_field.click()
    email_field.clear()
    email_field.send_keys(STUDENT_EMAIL)
    password_field = crawler.find_element_by_id("LoginUserControl1_passwordTextBox")
    password_field.click()
    password_field.clear()
    password_field.send_keys(STUDENT_PASSWORD)
    login_button = crawler.find_element_by_id("LoginUserControl1_loginButton")
    login_button.click()
    time.sleep(1)

files_dict = {}
for course_id in COURSES_ID:
    print MET_COURSE_URL + str(course_id)
    crawler.get(MET_COURSE_URL + str(course_id)) # Load page

    file_type_link = crawler.find_element_by_link_text("File Type")
    file_type_link.click()
    time.sleep(1)

    title = crawler.find_elements_by_class_name("coursesPageTitle")
    COURSE_NAME = title[0].text + " " + title[1].text

    badges = crawler.find_elements_by_class_name("badgeHeader")
    for x in xrange(0, len(badges)):
        FILE_CATEGORY = badges[x].text
        try:
            present_files = os.listdir(UNIVERSITY_PATH + "/" + SEMESTER_NUMBER + "/" + COURSE_NAME + "/" + FILE_CATEGORY)
        except OSError:
            os.makedirs(UNIVERSITY_PATH + "/" + SEMESTER_NUMBER + "/" + COURSE_NAME + "/" + FILE_CATEGORY)
            present_files = os.listdir(UNIVERSITY_PATH + "/" + SEMESTER_NUMBER + "/" + COURSE_NAME + "/" + FILE_CATEGORY)

        new_files = []
        new_part_files = []
        link_elements = crawler.find_elements_by_xpath("(//ul[@class='materialList'])[" + str(x+1) + "]//a")
        for link_element in link_elements:
            if len(link_element.text) > 0:
                file_name_start_index = link_element.get_attribute("href").find("file=")
                file_name = (link_element.get_attribute("href")[file_name_start_index + 5:]).replace('%20', ' ')
                if not file_name in present_files:
                    new_files.append(file_name)
                    new_part_files.append(file_name + ".part")
                    link_element.click()
        if len(new_files) > 0:
            files_dict[UNIVERSITY_PATH + "/" + SEMESTER_NUMBER + "/" + COURSE_NAME + "/" + FILE_CATEGORY + "/"] = new_files
            wait_till_download()

move_files()
time.sleep(1)
print "downloaded %d file(s)"  %(sum([len(v) for v in files_dict.itervalues()]),)
for k, v in files_dict.iteritems():
    print "\t (%d) %s" %(len(v), k)
    
crawler.quit()
