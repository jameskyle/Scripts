#!/opt/local/bin/python2.7
import feedparser
import time

from instapaperlib import Instapaper
from datetime import date

import logging
import logging.handlers

# Enter your username and password for instapaper.com
USERNAME = "InstaPaper Username"
PASSWORD = "InstaPaper Password"

# Add any feeds you wish to pull articles from
FEEDS = [
    'http://worldofweirdthings.com/feed/',
    'http://skepticblog.org/feed/',
    'http://www.skeptic.com/feed/',
    'http://feeds.feedburner.com/BadAstronomyBlog',
    'http://krugman.blogs.nytimes.com/feed/',
]

# Additional configuration. Normally no need to edit any of these
LOG_DEBUG_LEVEL   = logging.INFO
LOG_FILENAME      = "/var/log/daily_news.log"
LOG_ARCHIVE_COUNT = 5
LOG_INTERVAL      = 7 # in days
LOG_FORMAT        = "%(asctime)s - %(levelname)s: %(message)s"
LOG_DATE_FORMAT   = "%a, %d %b %Y %H:%M:%S"
LOGGER_NAME       = "DailyNewsLOgger"

logger            = logging.getLogger(LOGGER_NAME)
formatter         = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                                    when='D',
                                                    interval=LOG_INTERVAL,
                                                    backupCount=LOG_ARCHIVE_COUNT)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(LOG_DEBUG_LEVEL)

def main():
    for feed in FEEDS:
        d = feedparser.parse(feed)
        add_todays_entries(d.feed.title, d.entries)
        
def add_todays_entries(feed_title, entries):
    i = Instapaper(USERNAME, PASSWORD)
    
    for e in entries:
        pubdate = date.fromtimestamp(time.mktime(e.updated_parsed))
        if pubdate == date.today():
            title = u"{0} - {1}".format(e.title, feed_title)
            link = e.link
            ret = i.add_item(link, title, response_info=True)
            (statuscode, statusmessage, title, location) = ret
            logger.info("{0} :: {1}".format(title, statusmessage))
            
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(e)
