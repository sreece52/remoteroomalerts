import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Email:

    # change setting here
    port = 587 # stmp port
    emailServer = "smtp.gmail.com" # gmail servers
    sender = "Pi" #Sender and receiver for email
    receiver = "" #add email here
    loginEmail = '' # senders email address
    password = '' # senders email address password
   
    # Message creation
    # This message format must be used because message headers must be included
    # A subject header can also be used after the To header
    def sendEmail(self, image_path):
        print("connection to %s through port %d" % (Email.emailServer, Email.port))
        server = smtplib.SMTP(Email.emailServer, Email.port) # email object
        
        # Puts the SMTP connection in TLS (Transport Layer Security Mode
        # All SMTP commands that follow will be encrypted
        server.starttls()

        # Parameters: login using your Gmail address and password
        server.login(Email.loginEmail,Email.password)

        # building the email
        img_data = open(image_path, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Security Alert'
        msg['From'] = Email.sender
        msg['To'] = Email.receiver
        text = MIMEText('Motion has been detected!')
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(image_path))
        msg.attach(image)
        print("sending email...")
        server.sendmail(Email.sender, Email.receiver, msg.as_string())
        
        print("Email Alert Sent to %s" % Email.receiver)
        print("connection to %s closed" % Email.emailServer)
        server.quit() #close connection
    
