from imaplib import IMAP4_SSL
import getpass
import smtplib
import random
from poplib import POP3_SSL
import time
import dns.resolver
####
#To-do list
# 1. Remove message
# 2. arg parser
# 3. configuration
# 4. Send message from 3-d party provider
####

username = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
host = "mail154-1.exch154.serverdata.net"
password = ""
msg_id = random.randint(1000000, 10000000000)

def get_mx(host):
    answer = dns.resolver.query(host.split('@')[1], 'MX')
    return answer[0].exchange.to_text()

def send_msg():
    print("\n     SMTP testing")
    fromaddr = "yurok15@gmail.com"
    toaddrs = "yzhigulskiy@OPS-EXCH154-W.hostpilot.com"
    msg = ("Subject: %s" % (msg_id))
    try:
        server = smtplib.SMTP(get_mx(toaddrs))
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        print("OK - Messages with msg_id %s was sent " % msg_id)
    except:
        print("FAILED - Unable to sent a message")


def test_imap(username, host, password, msg_id):
    print("\n     IMAP testing")
    time.sleep(10)
    connector = IMAP4_SSL(host)
    try:
        connector.login(username, password)
        print("OK - IMAPS connectivity (port 993)")
    except:
        print("FAILED - Couldn't connect to server")
    connector.select()
    msg = connector.search(None, 'Subject', str(msg_id))
    if msg[1] != [b'']:
        print("OK - Message with id %s was found" % msg_id)
    else:
        print("FAILED - Sent message was not delivered")
    connector.close()
    connector.logout()


def test_pop(username, host, password, msg_id):
    print("\n     POP3 testing")
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

send_msg()
test_imap(username, host, password, msg_id)
test_pop(username, host, password, msg_id)
