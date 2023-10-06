#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import sys
import os.path
import datetime
import smtplib
import argparse

from email import encoders
from email.utils import formatdate
from email.utils import make_msgid
from email.message import EmailMessage

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dns.resolver

EICAR = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
SPAM  = 'XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X'

def create_spam(from_addr, to_addr, subject, body):

    msg = EmailMessage()
    msg["Message-Id"] = make_msgid()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate(localtime=True)

    msg.set_content(body)
    return msg

def create_virus(from_addr, to_addr):

    msg = MIMEMultipart()
    msg["Message-Id"] = make_msgid()
    msg["Subject"] = "Eicar TEST"
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate(localtime=True)

    body = MIMEText("test body")
    msg.attach(body)

    attachment = MIMEBase('text', 'comma-separated-values')
    attachment.set_payload(EICAR)
    encoders.encode_base64(attachment)
    msg.attach(attachment)
    attachment.add_header("Content-Disposition","attachment", filename='eicar.com')
    return msg

def get_exchange(domain):
    records  = dns.resolver.resolve(domain, 'MX')
    return str(records.response.answer[0][0].exchange).strip('.')

def send(from_addr, to_domain, to_addr, password, msg):
    smtp = smtplib.SMTP(get_exchange(to_domain), 587)
    smtp.ehlo()
    smtp.login(to_addr, password)
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.quit()

def send25(from_addr, to_domain, to_addr, msg):
    smtp = smtplib.SMTP(get_exchange(to_domain), 25)
    smtp.ehlo()
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.quit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--from',  '-f', type=str, dest='from_addr',required=True)
    parser.add_argument('--to',    '-t', type=str, dest='to_addr',required=True)
    parser.add_argument('--password', '-p', type=str, dest='password',required=True)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    subparsers.add_parser('virus')
    subparsers.add_parser('spam')
    subparsers.add_parser('test')

    args = parser.parse_args(sys.argv[1:])
    to_domain = args.to_addr.split('@')[1]

    if args.command == 'virus':
        send(args.from_addr, to_domain, args.to_addr, args.password,
             create_virus(args.from_addr,args.to_addr))

    elif args.command == 'spam':
        send(args.from_addr, to_domain, args.to_addr, args.password,
             create_spam(args.from_addr,args.to_addr,"Thank You",SPAM))
    else:
        send(args.from_addr, to_domain, args.to_addr, args.password,
             create_spam(args.from_addr,args.to_addr,"Test Mail","this is the test mail"))
