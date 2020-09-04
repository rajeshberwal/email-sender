# Importing smtp library
import smtplib

# json library
import json

# importing pandas to read csv file
import pandas as pd

# importing Python's email utility package
import email.utils

# importing MIME text format library
from email.mime.text import MIMEText

# reading data from json file
with open("creditential.json", "r") as read_file:
    data = json.load(read_file)

# Sender's email address and Name
username = data['sender_email']
sender_name = 'Your Name'

# password for your account
password = data['password']

# reading csv file using pandas
columns_name = ['name', 'email']
data = pd.read_csv('email-list.csv', names=columns_name)

# reciver's mail address and name
recipient_emails = data.email.tolist()[1:]
recipient_names = data.name.tolist()[1:]

# reading message from html file
html_file = open('./template.html', 'r')

# email body
email_body = html_file.read()


# function to send emails
def brodcast_email():
    print('Brodcasting email...')

    for recipient_name, recipient_email in zip(recipient_names, recipient_emails):
    # encoding text with MIMEtext for mail format and adding html functionality
        message = MIMEText(email_body, 'html')
        message.add_header('Content-Type', 'text/html')

        # populating message with email data
        message['To'] = email.utils.formataddr((recipient_name, recipient_email))  
        message['From'] = email.utils.formataddr((sender_name, username))
        message['Subject'] = 'Testing SMTP with Python'

        # creating SMTP server
        # all the servers are stored in smtp-server.json
        with open("smtp-server.json", "r") as file:
            smtp_server = json.load(file)
        
        # using gmail's smtp server and setting smtp server
        server = smtplib.SMTP(smtp_server['gmail'], 587)

        # Turning on tls security for smtp
        server.starttls()
        
        # Login to sender's mail
        server.login(username, password)

        #sending email
        server.sendmail(username, recipient_email, message.as_string())

        # cleanup
        server.quit()

        # confirmation that email has sent to client
        print(f'Email sent to {recipient_name} {recipient_email}')

    print('Email Brodcasted.')


# sending emails
brodcast_email()