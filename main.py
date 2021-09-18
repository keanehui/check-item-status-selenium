EMAIL_ADDRESS: str = "" # STEP 1
EMAIL_PASSWORD: str = "" # STEP 2
# Access to the link below and switch it on # STEP 3
# https://www.google.com/settings/security/lesssecureapps
# STEP 4 Click Run to check if email is working
# STEP 5 Change email_test to "False" and click Run to start
test_email: bool = False

EMAIL_MESSAGE: str = "Click to buy: \n https://www.mclarenstore.com/gb/en/mclaren-f1-gulf-9fifty-cap/701218456-blue.html"
CHECK_FREQUENCY_SECS: int = 15
CHECK_DURATION_HOURS: int = 10

########## DO NOT MODIFY THE CODE AFTER THIS LINE ##########

import time
import datetime
import smtplib
from email.message import EmailMessage
from selenium.webdriver import Chrome

def send_email(to_addr:str=EMAIL_ADDRESS):
    email_obj = EmailMessage()
    email_obj.set_content(EMAIL_MESSAGE)
    email_obj['Subject'] = 'Available NOW - McLaren Gulf Cap'
    email_obj['From'] = EMAIL_ADDRESS
    email_obj['To'] = to_addr

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end="\t")
    try:
        server.send_message(email_obj)
        server.quit()
        print("EMAIL SENT TO " + to_addr)
    except:
        print("ERROR: Failed to send email.")
    
if test_email:
    send_email()
    exit()

print("Starting... ")
print("Log: ")
log_id: int = 0
gulf_cap_url: str = "https://www.mclarenstore.com/gb/en/mclaren-f1-gulf-9fifty-cap/701218456-blue.html"
region_cancel_selector: str = "#locale-change-modal > div > div > div > div.action-buttons > button.btn.btn-outline-dark"
comming_soon_text_selector: str = "#maincontent > div > div.container.px-0.px-md-3.mb-6.mb-lg-7 > div:nth-child(2) > div.col-12.col-md-4.px-3.px-md-0 > div.product-top-wrap > div.product-promotions > div"

checking_end_time = datetime.datetime.now() + datetime.timedelta(hours=CHECK_DURATION_HOURS)
while (datetime.datetime.now() < checking_end_time):
    driver = Chrome()
    driver.get(gulf_cap_url)
    driver.find_element_by_css_selector(region_cancel_selector).click()
    elem = None
    
    log_id += 1
    print(str(log_id), end="\t")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end="\t")
    try:
        elem = driver.find_element_by_css_selector(comming_soon_text_selector)
        indicator: str = elem.get_attribute('innerHTML')
        if "COMING SOON" in indicator:
            print("COMING SOON")
        else:
            print("ERROR: Element found, text mismatch. ")
    except:
        print("AVAILABLE NOW")
        send_email()
        send_email("kawonghui@gmail.com")

    driver.quit()
    time.sleep(CHECK_FREQUENCY_SECS)
