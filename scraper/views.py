from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from celery.execute import send_task


from scraper.forms import SearchTwitterFormForm
from scraper.models import TwitterUser, Twit
from .tasks import import_data


class TwitterSearchView(CreateView):
    form_class = SearchTwitterFormForm
    template_name = 'scraper/search_twitter.html'
    submit_text = 'Search'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class, 'submit_text': self.submit_text}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        url_list = request.POST['list_urls']
        for url in url_list.split(" "):
            TwitterUser.objects.get_or_create(
                url=url
            )
            user = TwitterUser.objects.get(url=url)
            send_task('import_data',
                      (user.id,),
                      queue='import_data')
            import_data.delay(user.id)

        return HttpResponseRedirect(reverse_lazy('user_list'))


class UsersListView(CreateView):
    template_name = 'scraper/twitter_users.html'
    submit_text = 'Users'
    heading = 'Users'

    def get(self, request, *args, **kwargs):
        users = TwitterUser.objects.all()
        context = {'users': users,
                   'submit_text': self.submit_text}
        return render(request, self.template_name, context)


class UserTwittsView(CreateView):
    template_name = 'scraper/twitters_list.html'
    submit_text = 'Users'
    heading = 'Users'

    def get(self, request, *args, **kwargs):
        user = TwitterUser.objects.get(pk=kwargs['user_id'])
        twits = Twit.objects.filter(user_name=user)
        context = {'twits': twits,
                   'submit_text': self.submit_text, 'user': user}
        return render(request, self.template_name, context)


class IndexView(View):
    template_name = 'scraper/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def delete_user_twitter(request, user_twitter_id):
    TwitterUser.objects.get(
        pk=user_twitter_id).delete()
    return HttpResponseRedirect(reverse_lazy('user_list'))


def update_user_twitter(request, user_twitter_id):
    user = TwitterUser.objects.get(
        pk=user_twitter_id)
    send_task('import_data',
              (user.id,),
              queue='import_data')
    import_data.delay(user.id)
    return HttpResponseRedirect(reverse_lazy('user_list'))
