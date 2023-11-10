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
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def date2unixtime(s):
    # "2023-10-03 18:30:11"
    t = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    return t.timestamp()


def gmt2date(gmt):
    # '06/Oct/2023:08:46:40 +0900'
    timezone = pytz.timezone("Asia/Tokyo")
    gmt_date = datetime.datetime.strptime(gmt, "%d/%b/%Y:%H:%M:%S %z")
    return gmt_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")


def date2gmt(s):
    # "2023-10-03 18:30:11"
    timezone = pytz.timezone("Asia/Tokyo")
    t = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    return t.astimezone(timezone).strftime("%d/%b/%Y:%H:%M:%S %z")


def aws2date(aws):
    # '2023-10-03T18:30:11.487+09:00'
    parsed_date = datetime.datetime.strptime(aws, "%Y-%m-%dT%H:%M:%S.%f%z")
    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")


def date2aws(s):
    # "2023-10-03 18:30:11"
    timezone = pytz.timezone("Asia/Tokyo")
    t = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    return t.astimezone(timezone).strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def mail2date(r):
    # RFC2822
    # ex) Sun, 17 Oct 2010 22:31:50 +0900 (JST)
    return utils.parsedate_to_datetime(r).strftime("%Y-%m-%d %H:%M:%S")


def date2mail(s):
    # "2023-10-03 18:30:11"
    t = datetime.datetime.strptime(f"{s} +0900", "%Y-%m-%d %H:%M:%S %z")
    return utils.format_datetime(t)


def internal_date2date(imap_date):
    # 27-Oct-2023 13:04:49 +0900
    st = imaplib.Internaldate2tuple(f'INTERNALDATE "{imap_date}"'.encode())
    return datetime.datetime(*st[:6]).strftime("%Y-%m-%d %H:%M:%S")


def date2internal_date(s):
    # "2023-10-03 18:30:11"
    t = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    return imaplib.Time2Internaldate(t.timestamp())
