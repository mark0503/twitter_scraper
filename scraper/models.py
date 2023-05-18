from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class TwitterUser(models.Model):
    USER_STATUS = [
        ('New', 'New'),
        ('Ready to Scrape', 'Ready to Scrape'),
        ('Failed to Scrape', 'Failed to Scrape'),
        ('Complete', 'Complete'),
    ]
    url = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    followers = models.IntegerField(null=True)
    following = models.IntegerField(null=True)
    description = models.CharField(max_length=200)
    status_user = models.CharField(
        choices=USER_STATUS, max_length=26, help_text='The status of scrape_user', default='New')
    date_update = models.DateTimeField(gettext_lazy('date update'), default=timezone.now)

    class Meta:
        app_label = 'scraper'
        db_table = 'twitter_user'

    def __str__(self):
        return f'{self.user_name} {self.description}'


class Twit(models.Model):
    user_name = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
