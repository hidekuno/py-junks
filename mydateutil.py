#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import datetime
import pytz
from email import utils
import imaplib

def unixtime2date(u):
    # 1696561039
    dt = datetime.datetime.fromtimestamp(u)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def gmt2date(gmt):
    # '06/Oct/2023:08:46:40 +0900'
    timezone = pytz.timezone('Asia/Tokyo')
    gmt_date = datetime.datetime.strptime(gmt, '%d/%b/%Y:%H:%M:%S %z')
    return gmt_date.astimezone(timezone).strftime('%Y-%m-%d %H:%M:%S')

def aws2date(aws):
    # '2023-10-03T18:30:11.487+09:00'
    parsed_date = datetime.datetime.strptime(aws, '%Y-%m-%dT%H:%M:%S.%f%z')
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')

def mail2date(r):
    # RFC2822
    # ex) Sun, 17 Oct 2010 22:31:50 +0900 (JST)
    return datetime.datetime(*utils.parsedate(r)[:7]).strftime('%Y-%m-%d %H:%M:%S')

def internal_date2date(imap_date):
    # 27-Oct-2023 13:04:49 +0900
    st = imaplib.Internaldate2tuple(f'INTERNALDATE "{imap_date}"'.encode())
    return datetime.datetime(*st[:6]).strftime('%Y-%m-%d %H:%M:%S')
