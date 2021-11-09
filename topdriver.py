import selenium,time,colorama,os
from datetime import datetime
from colorama import Fore, Back, init
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import smtplib 
import traceback,sys

recipients=['recipient email here@gmail.com','recipient2@gmail.com']
alreadybooked=['DEC 29','DEC 13','other dates you already have booked']
critical_errors=0

init(autoreset=True)
os.system("cls")
os.system("color 48")
def email(location):
    try: 
        message=f"""
Appointment Found :
{location} --- https://www.topdriversignals.com/Student/StudentLogin.aspx
        """
        smtp = smtplib.SMTP('smtp.gmail.com', 587) 
        smtp.starttls() 
        smtp.login("senderemailaddress@gmail.com","passwordtoemail")
        for recipient in recipients:
            smtp.sendmail("senderemailaddress@gmail.com", recipient,message) 
        smtp.quit() 
        print ("Email sent successfully!") 
    except Exception as ex: 
        print(Fore.BLACK+"Something went wrong....",ex)

with open('locations.txt','r') as f:
    locations = f.read().splitlines()
    
def log(msg):
    now = datetime.now()
    timenow = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = timenow+' '+str(msg)+'\n'
    with open("log.txt",'a') as f:
        f.write(msg)

def look_through_schedule():
    global driver
    try:
        for _ in range(len(locations)):
            if _ > 0:
                time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/div/div[2]/div[2]/div[2]/a[1]')))
            driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/div[2]/div[2]/a[1]').click()
            time.sleep(.4)
            dropdown = driver.find_element_by_id('divECs').click()
            selected_school=driver.find_element_by_link_text(locations[_]).click()
            print(Back.RED+f"Checking : {locations[_]}")
            driver.find_element_by_xpath('//*[@id="refineSearch"]/div[2]/div/div[2]/form/div/div[4]/div/ins').click()
            time.sleep(.2)
            #driver.find_element_by_xpath('//*[@id="btncloseRefineSearch"]').click()
            driver.find_element_by_xpath('//*[@id="btnRefinesearch"]').click()
            try:
                time.sleep(7)
                alert = driver.find_element_by_id("OpenSlotdata").text
                now = datetime.now()
                timenow = now.strftime("%d/%m/%Y %H:%M:%S")
                os.system("color 48")
                #print(Back.RED+Fore.WHITE+timenow+' '+alert)
            except Exception as e:
                print(e)
                alert='???'
                print("Possible Appointment Available")
            if str(alert)=="No appointment is available for your search.":
                log(alert)
            else:
                if str(alert.split(', ')[1].split(',')[0]) not in alreadybooked:
                    print("Appointment Available",alert)
                    email(locations[_])
                    log(f"Appointment Available {locations[_]}")
        driver.quit()
    except Exception as e:
        os.system("color 48")
        print(e)
        log(e)
        look_through_schedule()
def main():
    global driver
    #on homepage after login
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dragable_portlets"]/div[3]/div[2]/div/div[2]/div[2]/div[1]/a')))
        print(Back.RED+Fore.GREEN+f'Logged In : {usr}')
        driver.find_element_by_xpath('//*[@id="dragable_portlets"]/div[3]/div[2]/div/div[2]/div[2]/div[1]/a').click() #clicks onto calendar page
        time.sleep(10)
        look_through_schedule()
    except Exception as e:
        exception_message = str(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print(exception_type,exception_traceback.tb_lineno)


        print(e)
        log("error waiting for schedule appointment button")
        critical_errors=+1
        if critical_errors>=3:
            driver.quit()
            initialize()
        driver.refresh()
        time.sleep(10)
        main()

def login():
    global driver
    driver.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(usr)
    driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
    main()
def initialize():
    global driver
    while True:
        os.system("color 48")
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.topdriversignals.com/Student/StudentLogin.aspx")
        driver.minimize_window()
        login()
        time.sleep(1800)

usr = "topdriver username"
passwd = "topdriver password"
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-extensions")

initialize()
