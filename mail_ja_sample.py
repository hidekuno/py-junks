#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.utils import make_msgid
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header

import sys
import argparse

SUBJECT_TEXT = "テストメール"
BODY_TEXT = """
これはテストメールです。

添付ファイルにて資料を送付します。

以上ご確認の程願います。
"""

SENDER = 'xxxx@xxxx.xxx'
PASSWORD = 'xxxxxxxxxxxxxxxxxxxxx'
SMTP_SERVER = 'mail.xxxxxx.xxx'
FROM_ADDRESS = 'xxxx@xxx.xxxxxx.xxx'
TO_ADDRESS = 'xxxxxxx@xxxx.xxx'

def create_message(test_file, charset="ISO-2022-JP"):
    msg = MIMEMultipart()
    msg["Message-Id"] = make_msgid()
    msg['Subject'] = Header(SUBJECT_TEXT, charset)
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(BODY_TEXT, 'plain', charset))

    with open(test_file, 'rb') as pdf:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {test_file}")
        msg.attach(part)

    return msg

def send_mail(msg):
    smtp = smtplib.SMTP(SMTP_SERVER, 587)
    smtp.starttls()
    smtp.login(SENDER, PASSWORD)
    smtp.send_message(msg)
    smtp.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, dest="test_file", required=True)
    args = parser.parse_args(sys.argv[1:])

    send_mail(create_message(args.test_file))
