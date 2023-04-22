import smtplib
import mimetypes
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


def send_mail(email, subject, text_body=None, html_body=None):
    addr_from = os.getenv('FROM')
    password = os.getenv('PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = email
    msg['Subject'] = subject
    if text_body:
        msg.attach(MIMEText(text_body, "plain"))
    if html_body:
        msg.attach(MIMEText(html_body, "html"))
    
    server = smtplib.SMTP_SSL(os.getenv('HOST'), os.getenv('PORT'))
    server.login(addr_from, password)
    
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    load_dotenv()
    send_mail(1, 1, 1)