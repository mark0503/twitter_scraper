import datetime

import requests
from django.utils import timezone

from twitter_import import settings
from ..models import TwitterUser, Twit
from dotenv import load_dotenv
import os
import logging

load_dotenv()
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")


class TwitterImportParser:

    def __init__(self):
        self._session = requests.Session()
        self._session.headers = {
            "Authorization": f"Bearer {API_BEARER_TOKEN}",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }

    def import_info(self, user_id):
        user = TwitterUser.objects.filter(id=user_id)
        user.update(status_user='Ready to Scrape',
                    user_name=user.first().url.split('/')[-1])
        user_data = self.get_user_info(user.first().user_name)
        item_id = user_data['id']
        get_followers = self.get_user_followers(user_data)
        get_following = self.get_user_following(user_data)
        get_user_bio = self.get_user_bio(user_data)
        user.update(
            followers=get_followers,
            following=get_following,
            description=get_user_bio,
            date_update=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        twits = self.get_last_ten_twits(item_id)
        for twit in twits:
            Twit.objects.get_or_create(
                user_name=user.first(),
                text=twit['text'][:250]
            )
        user.update(status_user='Complete')

    def get_user_info(self, user_name):
        url = f"https://api.twitter.com/2/users/by/username/{user_name}"
        resp = self._session.get(url, params={'user.fields': 'public_metrics,description'}).json()

        return resp['data']

    def get_user_followers(self, user_data):
        return user_data['public_metrics'].get('followers_count', 0)

    def get_user_following(self, user_data):
        return user_data['public_metrics'].get('following_count', 0)

    def get_user_bio(self, user_data):
        return user_data['description']

    def get_last_ten_twits(self, user_item_id):
        url = f"https://api.twitter.com/2/users/{user_item_id}/tweets"
        resp = self._session.get(url=url, params={
                'max_results': 10

            }).json()
        return resp['data']
