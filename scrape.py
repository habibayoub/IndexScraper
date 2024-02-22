from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import requests
import getpass

def init():
    
    driver = webdriver.Chrome()
    URL = "https://web.coop.uottawa.ca/IndEX/Authentication/Login?ReturnUrl=%2fIndEX%2f"

    driver.get(URL)
    login(driver)
    
    
def login(driver):
    
    username = input("Please Enter Your Username: ")
    username_field = driver.find_element("id", "Username")
    username_field.send_keys(username)

    password = getpass.getpass("Please Enter Your Password: ")
    password_field = driver.find_element("id", "Password")
    password_field.send_keys(password)

    dropdown_element = driver.find_element("id", "ddlUserType")
    select = Select(dropdown_element)

    select.select_by_visible_text("Student")

    login_button = driver.find_element("xpath", "//input[@type='submit']")
    login_button.click()
    time.sleep(3)
    
    parse(driver)
    
    
def parse(driver):
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    results = soup.find(id='Jobs')
    job_elements = results.find_all("div", class_="card")
    programs = []
    for job_element in job_elements:
        programs.append(job_element.find_all("span"))
    
    keywords = {"csi", "seg", "ceg"}
    jobs = []
    for job_element in job_elements:
        courses = job_element.find("span").text.lower().strip().split(",")
        if any(keyword in courses for keyword in keywords):
            job_links = job_element.find_all("a")
            for link in job_links:
                title = link.contents[0].strip()
                job_info = {
                    "title": title,
                    "url": link["href"]
                }
                jobs.append(job_info)
        else:continue
        
    for job in jobs:
        print("Title:", job["title"])
        print("URL:", job["url"])
        print()

    with open("jobs.txt", "w") as file:
        for job in jobs:
            file.write(f"Title: {job['title']}\n")
            file.write(f"URL: {job['url']}\n")
            file.write("\n")

    time.sleep(2)

    driver.quit()
    
    
def main():
    init()

if __name__ == '__main__':
    main()