"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from news.views import PostPage, ComingSoon, MainPage, FuturePage
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.decorators.cache import never_cache, patch_cache_control, cache_control


urlpatterns = [
    path('news/create/', FuturePage.as_view()),
    path('news/<int:post_number>/', PostPage.as_view()),
    path('news/', MainPage.as_view()),
    path('', ComingSoon.as_view())
]
# urlpatterns += static(settings.STATIC_URL)
# urlpatterns = [re_path('news/(?P<link_number>[^/]*)/?', NewsPage.as_view())]
