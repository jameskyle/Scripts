#!/usr/bin/env python
import urllib2, smtplib, os, logging
import logging.handlers

from email.MIMEText import MIMEText

# you'll need to create this log directory
IPFILE       = "/var/log/ip_notify/current_ip"
FROM         = ("Home Admin", "your_from_email@domain.com")
SUBJECT      = "Your IP has changed"
TO           = ("Your Name", "your_to_email@domain.com")
SMTPSERVER   = "your.smtp.server.com"
IPSITE       = "http://www.whatismyip.com/automation/n09230945.asp"
LOG_FILENAME = "/var/log/ip_notify/ip.log"

def get_ip():
    page = urllib2.urlopen(IPSITE)
    return page.read()

def send_mail(ip):
    msg = MIMEText("Your new ip: %s " % ip)

    # Set the headers
    msg['Subject'] = SUBJECT
    msg['From']    = FROM[0]
    msg['To']      = TO[0]

    # Open smtp connection to roadrunner
    s = smtplib.SMTP()
    try:
        s.connect(SMTPSERVER)
        # send email: s.sendmail(:realfrom:, :realto:, :content:)
        s.sendmail(FROM[1], TO[1], msg.as_string())
    except:
        print("There was an smtp error")
    finally:
        s.close()

def ip_changed(current_ip):
    try:
        f = open(IPFILE, 'r')
        old_ip = f.read()
        f.close()
    except IOError:
        old_ip = None

    return(not old_ip == current_ip)

ip = get_ip()
logger = logging.getLogger('IPNotify')

logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                               when='D',
                                               interval=7,
                                               backupCount=5)
formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

if ip_changed(ip):
    logger.info("IP change detected. New ip: %s" % ip)
    f = open(IPFILE, 'w')
    f.write(ip)
    f.close()
    send_mail(ip)
    logger.info("Notification email sent to: %s<%s>" % (TO[0], TO[1]))
else:
    logger.info("No IP change detected <%s>" % ip)
