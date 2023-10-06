#!/usr/bin/python3
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import poplib

def pop_list(server, user, password):
    cli = poplib.POP3(server)
    cli.user(user)
    cli.pass_(password)

    print(len(cli.list()[1]))

    for i in range(len(cli.list()[1])):
        no = i + 1
        print(cli.top(no, 0)[1])
    cli.quit()
