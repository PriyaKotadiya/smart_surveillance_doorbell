import os
import glob
from picamera import PiCamera
import RPi.GPIO as GPIO
import smtplib
import email
from time import sleep
from pathlib import Path
import imghdr
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#SMTP_SERVER = 'smtp.gmail.com' #EMAIL SERVER(DON'T CHANGE)
#SMTP_PORT = 587
GMAIL_USERNAME = 'fifuurself1680@gmail.com'
GMAIL_PASSWORD = 'zkjulapozlqxflpm'
subject = "VISITOR"

# sender = 'fifuurself@gmail.com'
# password = 'Fifu@1680'
recipient = 'piyukotadiya2001@gmail.com'
DIR = './Visitors/'
prefix = 'image'
content = "U have a visitor"
filename  = os.path.join(DIR, prefix + '%03d.jpg')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
     
class Emailer:
    def __init__(self,recipient, subject, content):
        self.recipient=recipient
        self.subject=subject
        self.content=content
        
    def sendmail(self):

        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient, "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        
        newMessage = EmailMessage()    #creating an object of EmailMessage class
        newMessage['Subject'] = "Visitor" #Defining email subject
        newMessage['From'] = GMAIL_USERNAME  #Defining sender email
        newMessage['To'] = recipient  #Defining reciever email
        newMessage.set_content('Open the door You have a visitor') #Defining email body
        #content = EmailMessage()
        
        
        
        with open("/home/pi/Desktop/Visitors/image%03d.jpg", "rb") as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
            
        newMessage.add_attachment(image_data, maintype = 'image', subtype = image_type, filename= image_name)
        
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
            smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD) #Login to SMTP server
            smtp.send_message(newMessage)   


sender = Emailer(recipient, subject, content)  
        
def capture_img():
    print ('captuting')
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
 
    
    filename  = os.path.join(DIR, prefix + '%03d.jpg')
    camera = PiCamera()
    camera.capture(filename)
    camera.stop_preview()
    camera.close() 
    print("done")
    
    sender.sendmail()
    print("ok")
    
while True:
    int = GPIO.input(11)
    if int == 0:
        print('waiting')
    
    elif int == 1:
        capture_img()
