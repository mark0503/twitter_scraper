from django import forms


class SearchTwitterFormForm(forms.Form):
    list_urls = forms.CharField(help_text='List url for search')
