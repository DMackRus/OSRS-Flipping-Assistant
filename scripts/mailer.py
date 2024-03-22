import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailer:
    def __init__(self):

        self.mailer_available = False

        # Check if the secrets file is present
        file = 'json/secrets.json'
        if(os.path.isfile(file)):
            secrets = json.load(open('json/secrets.json'))

            self.smtp_server    = secrets["smtp_server"]
            self.smtp_port      = secrets["smtp_port"]                
            self.sender_email   = secrets["sender_email"]
            self.receiver_email = secrets["receiver_email"]
            self.password       = secrets["sender_password"]

            #TODO: check all values loaded correctly?

            self.mailer_available = True

    def compose_msg(self):
        # Here is where it gets fun, we need to write some code to take the current trends
        # see what items have crossed their alerts and compose a meaningful message to send to the user.

        # Perhaps we could use chat gpt for this?

        pass

    def send_email(self, subject, msg):

        if not self.mailer_available:
            print("Mailer not available, please check the secrets.json file")
            return

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


    