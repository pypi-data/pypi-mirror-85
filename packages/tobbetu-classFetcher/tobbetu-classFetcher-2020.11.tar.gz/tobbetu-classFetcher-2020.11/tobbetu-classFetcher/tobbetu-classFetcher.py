from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def classFetcher(lessonName, lessonClass):
    #Using web driver to access web and opening the website
    driver = webdriver.Chrome(executable_path="c:\programming\sources\chromedriver.exe")
    driver.get('http://kayit.etu.edu.tr/rapor/web/index.php/Program2020guz')

    #Find the class input box and send in the class of your choosing
    input_box = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div/form/div/span/span[1]/span/ul/li/input')
    input_box.send_keys(lessonName)
    input_box.send_keys(Keys.ENTER)

    #Find the submit box
    submit_box = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div/form/button')
    #Submit
    submit_box.click()

    #Get the zoom link for the class and open it
    class_links = driver.find_elements_by_class_name(lessonClass)
    try:
        class_link = class_links[0].find_element_by_css_selector('a').get_attribute('href')
        driver.get(class_link)
    except:
        class_link = class_links[2].find_element_by_css_selector('a').get_attribute('href')
        driver.get(class_link)
  

    #Wait for Zoom to open and close the browser
    sleep(2)
    driver.quit()