from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup


class InstaBot:
    def __init__(self,username,password):
        self.username  = username
        self.password = password
        chrome_options= webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.bot = webdriver.Chrome()



    def login_into_insta(self):
        bot = self.bot
        bot.fullscreen_window()
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        email = bot.find_element_by_name("username")
        password = bot.find_element_by_name("password")
        email.send_keys(self.username)
        password.send_keys(self.password)
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        time.sleep(2)
        # 'not now' button clicking for no desktop notification
        bot.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() # when not headless 
        #into user account to find follower
        bot.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a').click()
        time.sleep(2)
        
#        first_story = bot.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[2]/div[2]/div/div/div/div[1]/button').click()
        #Find follower
        follower = bot.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a/span').text
        return follower
     
        
if __name__ == '__main__':    
    omg = InstaBot('Your intsagram username','Your instagram password')
    follower = omg.login_into_insta()
    #set up the SMTP server
    msg = MIMEMultipart()       # create a message
    # setup the parameters of the message
    email_html = open('email_body.html')
    message = email_html.read()
    msg['From']='Your from email address goes here.'
    msg['To']='Your to email address goes here.'
    msg['Subject']="Insta followers"
    message = 'Hi This is insta bot!!!'+'\n'+ 'Your Followers found on insta:-' + ' ' + follower
    #add in the message body
    msg.attach(MIMEText(message, 'html'))
    if int(follower) >300:
        try:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            #Set up gmail login to send mail
            s.login('Your gamil login email ', 'Your gamil password')
            print("Sending mail...................")
            s.quit()
        except Exception as e:
            print(f'Oh no !!! something bad happened.\n{e}')
        finally:
            print("Closing the server...............")
    # send the message via the server set up earlier.
    del msg