#to create pdf report
from io import BytesIO
import re
from fpdf import FPDF
#to automate email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import sys
#used to automate finding each website
#and determining if there are any jobs open
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pathlib
import os

def replaceBackslash(string):
    return str(string.as_posix())

def getCurrentPath():
    dir_path = pathlib.PureWindowsPath(os.path.dirname(os.path.realpath(__file__)))
    return dir_path

class OJF:
    def __init__(self):
        self.subject = "Daily Job Report"
        self.body = "This is an email with the desired report attached"
        self.sender_email = "thenibsman@gmail.com"
        self.receiver_email = "bniblock@zagmail.gonzaga.edu"
        self.file = "report.txt" # in the same directory as script
        self.companyFile = 'companyList.txt'
        f = open("email.ps", "r")
        password = f.read()
        self.password = password
    def sendEmail(self):
        email = EmailMessage()
        email["From"] = self.sender_email
        email["To"] = self.receiver_email 
        email["Subject"] = self.subject
        attach_file = open(self.file, "r+") # open the file
        email.set_content(attach_file.read())
        attach_file.close()
        #Create SMTP session for sending the mail
        session = smtplib.SMTP_SSL('smtp.googlemail.com', 465) #use gmail with port
        session.ehlo()
        try:
            session.login(self.sender_email, self.password)
        except SMTPAuthenticationError:
            print('SMTPAuthenticationError')
        text = email.as_string()
        #session.send_message(email)
        session.quit()
        print('Mail Sent')
    def createFile(self):
        f = open(self.file, 'r')
        f.read()
        f.close()
        f = open(self.file, 'w+')
        f.write('hello world\n')
        f.write('nice to meet you')
        f.close()
    def getListOfCompanies(self):
        f = open(self.companyFile, 'r')
        file_contents = f.readlines()
        company_list = []
        for x in file_contents:
            company_list.append(x.rstrip())
        f.close()        
        return company_list
    def findIfJobsAreOpen(self, company_list):
        options = Options()
        options.headless = False
        options.add_argument('log-level=3')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        CHROMEDRIVER_PATH = str(replaceBackslash(getCurrentPath()))+'/Driver/chromedriver'
        driver = webdriver.Chrome(CHROMEDRIVER_PATH ,options=options)
        driver.get("https://www.google.com/")
        for company in company_list:
            search = driver.find_element_by_name('q')
            search.send_keys(company)
            search.send_keys(Keys.ENTER)
            driver.execute_script("window.history.go(-1)")
            #r = requests.get("<add your URL here>")
            #soup = BeautifulSoup(r.content)