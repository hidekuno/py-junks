#!/usr/bin/env python
#
# this is toy tool
#
# hidekuno@gmail.com
#
import pexpect

child = pexpect.spawn('sudo certbot certonly --manual -d hogehoge.com --dry-run --manual-public-ip-logging-ok --test-cert')
child.expect("Create a file containing just this data:")
print(child.readline(2))
print(child.readline(2))

line = child.readline(1024)
print(line.decode().rstrip())

child.expect("And make it available on your web server at this URL:")
print(child.readline(2))
print(child.readline(2))

line = child.readline(1024)
print(line.decode().rstrip())

child.expect("Press Enter to Continue")
child.sendline("\n")
print(child.readline(1024))

child.close()
