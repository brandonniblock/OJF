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
import sys

class OJF:
    def __init__(self):
        self.subject = "Weekly Job Report"
        self.body = "This is an email with the desired report attached"
        self.sender_email = "thenibsman@gmail.com"
        self.receiver_email = "bniblock@zagmail.gonzaga.edu"
        self.file = "report.pdf" # in the same directory as script
        f = open("email.ps", "r")
        password = f.read()
        self.password = password
    def sendEmail(self):
        email = MIMEMultipart()
        email["From"] = self.sender_email
        email["To"] = self.receiver_email 
        email["Subject"] = self.subject
        attach_file = open(self.file, "rb") # open the file
        report = MIMEBase("application", "octate-stream")
        report.set_payload((attach_file).read())
        encoders.encode_base64(report)
        #add report header with the file name
        report.add_header("Content-Decomposition", "attachment", filename = self.file)
        email.attach(report)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP_SSL('smtp.googlemail.com', 465) #use gmail with port
        session.ehlo()
        try:
            session.login(self.sender_email, self.password)
        except SMTPAuthenticationError:
            print('SMTPAuthenticationError')
        
        text = email.as_string()
        session.sendmail(self.sender_email, self.receiver_email, text)
        session.quit()
        print('Mail Sent')
    def createFile(self):
        pdf = FPDF() 
        
        # Add a page 
        pdf.add_page() 
        
        # set style and size of font  
        # that you want in the pdf 
        pdf.set_font("Arial", size = 12) 
        
        pdf.cell(200, 10, txt = "GeeksforGeeks",  
                    ln = 1, align = 'C') 
            
        # save the pdf with name .pdf 
        pdf.output("report.pdf") 