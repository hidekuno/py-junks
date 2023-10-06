#!/usr/bin/python3
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import imaplib

def imap_quota(server, user, password):
    cli = imaplib.IMAP4(server)
    cli.login(user, password)

    quota = cli.getquotaroot("INBOX")
    rate = str(quota[1][1][0]).replace('(','').replace(')','').replace("'",'').split(' ')

    #print(rate)
    print(int(int(rate[2])/int(rate[3])*100))
    cli.logout()
