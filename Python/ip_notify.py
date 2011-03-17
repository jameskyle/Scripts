#!/opt/local/bin/python
import os
import subprocess
import smtplib
import logging
import logging.handlers
from email.MIMEText import MIMEText
"""
In order to use this script you'll need to enable snmp on your router and set
the appropriate variables below.
"""
# you'll need to create this log directory
FROM             = ("Home Admin", "YOUR_FROM_ADDRESS")
SUBJECT          = "Your IP has changed"
TO               = ("YOUR_NAME", "YOUR_TO_ADDRESS")
# (address, port), you can use any smtp, of course. but provide the port
SMTP_SERVER      = ("smtp.gmail.com", 587) 
SMTP_USER        = "SMTP_LOGIN_USERNAME"
SMTP_PASS        = "SMTP_USER_PASS"

SNMP_PASSWORD    = "SNMP_PASS"
ROUTER_IP        = "192.168.1.1"

LOG_FILENAME     = "/var/log/ip_notify/ip_notify.log"
IPFILE           = "/var/log/ip_notify/current_ip"
LOGGER_NAME      = "IPNotify"
LOGGER_LEVEL     = logging.INFO
LOG_FORMAT       = "[%(asctime)s - %(levelname)s] %(message)s"
LOG_DATE_FORMAT  = "%a, %d %b %Y %H:%M:%S"
LOG_ARCHIVE_COUNT = 5
LOG_INTERVAL      = 7 # in days

EXCLUDE_LIST     = ['127', '192', '169', '10'] # private ips

# There should be no need to edit anything below this line

def main():
    logger = get_log()
    
    try:
        ip = get_ip()
        logger.info("Fetched ip {0}".format(ip))
        
        changed = cache_ip(ip)
        
        if not changed:
            logger.info("No change in IP")
        else:
            logger.info("IP Changed")
            send_mail(ip)
            logger.info("Notification email sent to {0}".format(TO[1]))
            
    except Exception as e:
        logger.critical(e)        
            
def send_mail(ip):
    msg = MIMEText("Your new ip: {0}".format(ip))

    # Set the headers
    msg['Subject'] = SUBJECT
    msg['From']    = FROM[0]
    msg['To']      = TO[0]

    # Open smtp connection to roadrunner
    s = smtplib.SMTP(*SMTP_SERVER)
    
    try:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(SMTP_USER, SMTP_PASS)
        # send email: s.sendmail(:realfrom:, :realto:, :content:)
        s.sendmail(FROM[1], TO[1], msg.as_string())
        
    except Exception as e:
        print("There was an smtp error: {0}".format(e))
    finally:
        s.close()

def filter_ips(ip):
    for exc in EXCLUDE_LIST:
        if exc in ip:
            return False
    return True

def get_ip():
    cmd = ["snmpwalk", "-v", "2c", "-c", SNMP_PASSWORD, ROUTER_IP,
           "ipAdEntIfIndex"]
    PIPE = subprocess.PIPE
    try:
        p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
        ret = p.communicate()[0].strip()
        lines = ret.split("\n")
        
        wans = filter(filter_ips, lines)
        ip = wans[0].split("=")[0].split("IP-MIB::ipAdEntIfIndex.")[1].strip()
    except:
        raise Exception("Failed to retrive IP from router!")
    
    return ip

def get_log():
    log_dir = os.path.dirname(LOG_FILENAME)
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(LOGGER_NAME)
    
    logger.setLevel(LOGGER_LEVEL)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                                        when='D',
                                                        interval=LOG_INTERVAL,
                                                        backupCount=LOG_ARCHIVE_COUNT)
    
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def cache_ip(ip):
    changed = False
    content = ""
    
    with open(IPFILE,'r') as f:
        content = f.read().strip()
    if ip != content:
        changed = True
        with open(IPFILE, 'w') as f:
            f.write(ip)
            
    return changed

if __name__=='__main__':
    main()
