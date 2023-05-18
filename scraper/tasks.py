# -*- coding: utf-8 -*-
import sys
import logging
import traceback
from datetime import datetime, timedelta
from os import path, environ
import django
from .celery import app
from .core.twitter_import import TwitterImportParser


sys.path.append(path.dirname(path.abspath(__file__)))
environ.setdefault("DJANGO_SETTINGS_MODULE", "twitter_import.settings")
django.setup()

from .models import TwitterUser, Twit

"""Queue types:
    `supplier` - to place orders and other operations on supplier's suppliers.
"""

SUPPLIER_TASK_LOCK_EXPIRE = 60 * 10


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        300.0,
        update_data(),
    )


@app.task
def update_data():
    nowdate = datetime.today()

    startdate = nowdate - timedelta(days=1)
    invdate = startdate - timedelta(days=1)
    user_twitter = TwitterUser.objects.filter(date_update__range=[invdate, startdate])

    user_twitter.update(status_user='Ready to Scrape')
    res = ''
    for usr in user_twitter:
        try:
            scraper = TwitterImportParser()
            scraper.import_info(usr.id)
        except:
            logging.error('Error in attempting to import %s: %s', usr.id, traceback.format_exc())
            # Set status to FTP
            status = 'Failed to Scrape'
            TwitterUser.objects.filter(pk=usr.id).update(status_user=status)
        res += 'Status for import {} is {}. '.format(usr.id, user_twitter.first().status_user)
    return res


@app.task
def import_data(user_id):
    """
    :param user_id: user id
    """
    user_twitter = TwitterUser.objects.filter(id=user_id)
    try:
        user_twitter.update(status_user='N')
        scraper = TwitterImportParser()
        scraper.import_info(user_id)
    except:
        logging.error('Error in attempting to import %s: %s', user_id, traceback.format_exc())
        # Set status to FTP
        status = 'Failed to Scrape'
        user_twitter.update(status_user=status)
    return 'Status for import {} is {}'.format(user_id, user_twitter.first().status_user)
