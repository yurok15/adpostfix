from imaplib import IMAP4_SSL
import getpass
import smtplib
import random


username = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
host = "mail154-1.exch154.serverdata.net"
password = "Gfhjkm951"
msg_id = random.randint(1000000, 10000000000)

print("IMAP testing")

connector = IMAP4_SSL(host)
try:
    connector.login(username, password)
    print("OK - IMAPS connectivity (port 993)")
except:
    print("FAILED - Couldn't connect to server - BAD")

connector.select()
msg = connector.search(None, 'Subject', '"testing222"')
if msg[1] != [b'']:
    print("OK - Sent message was found")
else:
    print("FAILED - Sent message was not delivered")

#connector.close()
connector.logout()

print(msg_id)
fromaddr = "yurok15@gmail.com"
toaddrs  = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
msg = ("Subject: %s" %(msg_id) )
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    msg = msg + line

print("Message length is", len(msg))

server = smtplib.SMTP('west.smtp.mx.exch154.serverdata.net')
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()