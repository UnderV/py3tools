#!/usr/bin/python3
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mailer(server_addr, server_port, user, passw, from_mail, to_mail_list, subject, text_html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = ";".join(to_mail_list)

    message = MIMEText(text_html, 'html')
    msg.attach(message)

    try:
        server = smtplib.SMTP(server_addr, server_port) #To use port 465 encryption is required
        server.ehlo()
        server.starttls()
        server.login(user, passw)
        server.sendmail(from_mail, to_mail_list, msg.as_string())
        server.close()
        return 0
    except:
        return 1
