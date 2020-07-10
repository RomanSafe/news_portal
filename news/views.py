from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404
from .forms import NewPostForm, SearchForm
from datetime import datetime
from random import randint
import json


def deserialize():
    with open(settings.NEWS_JSON_PATH) as json_file:
        return json.load(json_file)


def serialize(object):
    with open(settings.NEWS_JSON_PATH, 'w') as json_file:
        json.dump(object, json_file)
        return None


def create_datetime_object(date_time, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_time, format)


class FuturePage(View):
    def get(self, request, *args, **kwargs):
        new_post_form = NewPostForm()
        return render(request, 'news/addnews.html', context={'new_post_form': new_post_form})

    def post(self, request, *args, **kwargs):
        new_post_form = NewPostForm(request.POST)
        if new_post_form.is_valid():
            new = {}
            new["created"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            new["text"] = new_post_form.cleaned_data["text"]
            new["title"] = new_post_form.cleaned_data["title"]
            # new["text"] = request.POST["text"]
            # new["title"] = request.POST["title"]
            all_news = deserialize()
            link_list = []
            for item in all_news:
                link_list.append(item["link"])
            link = randint(4, 1000)
            while link in link_list:
                link = randint(4, 1000)
            new["link"] = link
            all_news.append(new)
            serialize(all_news)
            return redirect('/news/')


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


def sort_news_list(searched_word=''):
    news = {}
    news_list = []
    news_from_json = deserialize()
    for item in news_from_json:
        if searched_word.casefold() in item["title"].casefold():
            news_list.append(item)
    news_list.sort(key=lambda dictionary: dictionary["created"], reverse=True)
    for post in news_list:
        datetime_object = create_datetime_object(post["created"])
        date_ = datetime_object.strftime("%Y-%m-%d")
        if date_ not in news:
            news[date_] = [post]
        else:
            news[date_].append(post)
    return news


class MainPage(View):

    def get(self, request, *args, **kwargs):
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            news = sort_news_list(searched_word=search_form.cleaned_data['q'])
        else:
            news = sort_news_list()
        return render(request, 'news/mainpage.html', context={
            'searchform': search_form,
            'news': news})


class PostPage(View):

    def show_requested_news(self, post_number):
        for post in deserialize():
            if post["link"] == post_number:
                return post
        raise Http404

    def get(self, request, *args, **kwargs):
        post = self.show_requested_news(self.kwargs["post_number"])
        datetime_object = create_datetime_object(post["created"])

        return render(request, 'news/index.html', context={
            'news_object': post,
            'date_time': datetime_object.strftime("%Y-%m-%d %H:%M:%S")})
