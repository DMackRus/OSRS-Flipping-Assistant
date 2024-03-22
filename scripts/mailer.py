import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


class Mailer:
    def __init__(self):

        # Load secrets.json - create this file and add your email credentials
        secrets = json.load(open('json/secrets.json'))

        self.smtp_server    = secrets["smtp_server"]
        self.smtp_port      = secrets["smtp_port"]                
        self.sender_email   = secrets["sender_email"]
        self.receiver_email = secrets["receiver_email"]
        self.password       = secrets["sender_password"]

    def send_email(self, subject, msg):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = subject

        # Add body to email
        body = msg
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()  # Secure the connection
        server.login(self.sender_email, self.password)

        # Send the email
        server.send_message(message)

        # Quit the server
        server.quit()


    