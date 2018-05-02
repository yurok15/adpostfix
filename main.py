from imaplib import IMAP4_SSL
import getpass
import smtplib
import random
from poplib import POP3_SSL


username = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
host = "mail154-1.exch154.serverdata.net"
password = "Gfhjkm951"
msg_id = random.randint(1000000, 10000000000)

def send_msg():
    print(msg_id)
    fromaddr = "yurok15@gmail.com"
    toaddrs = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
    msg = ("Subject: %s" % (msg_id))
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


def test_imap(username, host, password, msg_id):
    print("IMAP testing")

    connector = IMAP4_SSL(host)
    try:
        connector.login(username, password)
        print("OK - IMAPS connectivity (port 993)")
    except:
        print("FAILED - Couldn't connect to server")

    connector.select()
    msg = connector.search(None, 'Subject', '"testing222"')
    if msg[1] != [b'']:
        print("OK - Sent message was found")
    else:
        print("FAILED - Sent message was not delivered")

    connector.close()
    connector.logout()


def test_pop(username, host, password, msg_id):
    print("POP3 testing")

    connector = POP3_SSL(host)
    try:
        connector.user(username)
        connector.pass_(password)
        print("OK - POP3 connectivity (port 995)")
    except:
        print("FAILED - Couldn't connect to server")

    if len(connector.list()[1]) > 0:
        print("OK - INBOX not empty")
    else:
        print("--- - No messages in INBOX")

#test_imap(username, host, password, msg_id)
#test_pop(username, host, password, msg_id)


