import selenium,requests,time
from datetime import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import smtplib 

def email(location):
    try: 
        #Create your SMTP session 
        smtp = smtplib.SMTP('smtp.gmail.com', 587) 
        #Use TLS to add security 
        smtp.starttls() 
        #User Authentication 
        smtp.login("YOUR EMAIL ADDRESS","YOUR EMAIL PASSWORD")
        #Defining The Message 
        message = location
        #Sending the Email
        smtp.sendmail("YOUR EMAIL ADDRESS", "TARGET EMAIL ADDRESS",message) 
        #Terminating the session 
        smtp.quit() 
        print ("Email sent successfully!") 
    except Exception as ex: 
        print("Something went wrong....",ex) 

with open('locations.txt','r') as f:
    locations = f.read().splitlines()
    
def log(msg):
    now = datetime.now()
    timenow = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = timenow+' '+msg+'\n'
    with open("log.txt",'a') as f:
        f.write(msg)

def look_through_schedule():
    for _ in range(len(locations)):
        if _ > 0:
            time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/div/div[2]/div[2]/div[2]/a[1]')))
        driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/div[2]/div[2]/a[1]').click()
        time.sleep(.4)
        dropdown = driver.find_element_by_id('divECs').click()
        selected_school=driver.find_element_by_link_text(locations[_]).click()
        print(locations[_])
        driver.find_element_by_xpath('//*[@id="btnRefinesearch"]').click()
        try:
            time.sleep(7)
            alert = driver.find_element_by_id("OpenSlotdata").text
            print(alert)
        except:
            alert='???'
            print("Possible Appointment Available")
        if alert=="No appointment is available for your search.":
            log(alert)
        else:
            email(locations[_])
            log(f"APPOINTMENT FOUND!!!!! {locations[_]}")
    driver.quit()
def main():
    #on homepage after login
    driver.maximize_window()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/a")))
    driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/a").click() #clicks onto calendar page
    time.sleep(5)
    look_through_schedule()
def login():
    driver.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(usr)
    driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
    main()

while True:
    usr = "YOUR USERNAME"
    passwd = "YOUR PASSWORD"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.topdriversignals.com/Student/StudentLogin.aspx")
    login()
    time.sleep(3600)