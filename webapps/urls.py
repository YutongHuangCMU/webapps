"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import grumblr.views
from grumblr.forms import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',auth_views.login, {'template_name':'login.html', 'authentication_form': LoginForm}, name='auth_views.login'),
    url(r'^registration',grumblr.views.signup, name = 'registration'),
    url(r'^homepage/(?P<name>[^/]+)$',grumblr.views.view_homepage, name = 'homepage'),
    #the url for global stream page
    url(r'^global/?$',grumblr.views.get_global, name='global'),
    url(r'^add-post-global/?$',grumblr.views.add_post_global),
    # url(r'^post-global/?$',grumblr.views.post_global, name='post-global'),
    # url(r'^post-global/(?P<time>.+)$',grumblr.views.post_global, name='post-global'),
    url(r'^get-posts-global/$',grumblr.views.get_posts_global),
    url(r'^get-posts-global/(?P<time>.+)$',grumblr.views.get_posts_global),

    url(r'^get-posts-following/$',grumblr.views.get_posts_following),
    url(r'^get-posts-following/(?P<time>.+)$',grumblr.views.get_posts_following),

    url(r'^homepage/get-posts-homepage/(?P<name>[^/]+)$',grumblr.views.get_posts_homepage),
    url(r'^homepage/get-posts-homepage/(?P<name>[^/]+)/(?P<time>.+)$',grumblr.views.get_posts_homepage),
    # url(r'^get-comments-global/?$',grumblr.views.get_comments_global),
    # url(r'^get-comments-global/(?P<time>.+)$',grumblr.views.get_comments_global),
    #get comments for specific post
    url(r'^get-comments-global-post/(?P<post_id>\d+)$',grumblr.views.get_comments_global_post),
    url(r'^get-comments-global-post/(?P<post_id>\d+)/(?P<time>.+)$',grumblr.views.get_comments_global_post),
    url(r'^homepage/get-comments-global-post/(?P<post_id>\d+)$',grumblr.views.get_comments_global_post),
    url(r'^homepage/get-comments-global-post/(?P<post_id>\d+)/(?P<time>.+)$',grumblr.views.get_comments_global_post),
    #the url for following page
    url(r'^following',grumblr.views.post_following, name='following'),
    url(r'^logout$',auth_views.logout_then_login, name ='logout'),
    url(r'^profile/(?P<name>[^/]+)$',grumblr.views.view_profile, name = 'profile'),
    url(r'^photo/(?P<name>[^/]+)$',grumblr.views.get_photo, name = 'photo'),
    url(r'^homepage/photo/(?P<name>[^/]+)$',grumblr.views.get_photo, name = 'photo'),
    url(r'^verify/(?P<name>[^/]+)/(?P<token>[^/]+)$',grumblr.views.verify_email, name = 'verify'),#registration
    url(r'^reset/(?P<name>[^/]+)/(?P<token>[^/]+)$',grumblr.views.reset, name = 'reset'),#before login
    url(r'^change_password/(?P<name>[^/]+)$',grumblr.views.change_password, name = 'change_password'),#after login
    url(r'^forgetpassword',grumblr.views.forgetpassword, name = 'forget'),
    #for add comment
    url(r'^comment-global/(?P<post_id>\d+)$',grumblr.views.comment_global, name='comment-global'),
    url(r'^homepage/comment-global/(?P<post_id>\d+)$',grumblr.views.comment_global, name='comment-global'),
]
