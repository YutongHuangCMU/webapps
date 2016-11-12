from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
# for image uploading
from django.http import HttpResponse, Http404
from mimetypes import guess_type
# for sending email
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from grumblr.forms import *
from grumblr.models import *
#for using json
from django.core import serializers
import datetime


# Create your views here.

def signup(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'registration.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username1'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email_add'])
    new_user.save()
    new_profile = Profile(user=new_user,first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
    new_profile.save()

    new_user1 = authenticate(username=form.cleaned_data['username1'],
                            password=form.cleaned_data['password'])
    login(request, new_user1)

    token = default_token_generator.make_token(request.user)
    email_body = """
    This is an email sent from Grumblr. Please click the link below to verify your email address:
    http://%s%s
    """ % (request.get_host(),
           reverse('verify', args=(request.user.username, token)))
    send_mail(subject="Grumblr - Verify your email address",
              message=email_body,
              #from_email="yh1@andrew.cmu.edu",
              from_email="cmu.evelyn.huang@gmail.com",
              recipient_list=[request.user.email],
              fail_silently=False,
    )
    text = "One email has been sent to your email address. Please click the link in the email to verify your email address."
    context['text'] = text
    
    return render(request, 'registration.html', context)

def forgetpassword(request):
    context={}
    if request.method=='GET':
        context['form'] = ForgetForm()
        return render(request, 'forgetpassword.html', context)
    form = ForgetForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'forgetpassword.html', context)
    user = User.objects.get(username=form.cleaned_data['username'])
    profile = Profile.objects.get(user=user)
    token = default_token_generator.make_token(user)
    email_body = """
    This is an email sent from Grumblr. Please click the link below to verify your change of password:
    http://%s%s
    """ % (request.get_host(),
           reverse('reset', args=(user.username, token)))

    send_mail(subject="Verify the change of your password",
              message=email_body,
              #from_email="yh1@andrew.cmu.edu",
              from_email="cmu.evelyn.huang@gmail.com",
              recipient_list=[user.email],
              fail_silently=False,)
    text = "One email has been sent to your email address. Please click the link in the email to reset your password."
    context['text'] = text
    profile.token_password = token
    profile.save()
    return render(request,'forgetpassword.html',context)

def reset(request, name, token):
    context = {}
    context['token'] = token
    context['name'] = name
    user = User.objects.get(username__exact=name)
    if request.method == 'GET':
        profile = Profile.objects.get(user=user)
        if profile.token_password == token:
            context['form'] = PasswordForm()
            return render(request, 'resetpassword.html', context)
        else:
            raise Http404("The token doesn't match!")

    form = PasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'resetpassword.html', context)


    user.set_password(form.cleaned_data['password1'])
    user.save()
    new_user = authenticate(username=name,
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('global'))

@login_required
def view_homepage(request, name):
    context = {}
    con=[]  #whether the user is followed by the login user
    pro=[]
    users = User.objects.get(username=name)
    profile_of_loginuser = Profile.objects.get(user=request.user)
    if 'btn-follow' in request.POST:
        profile_of_loginuser.followings.add(users)
    if 'btn-unfollow' in request.POST:
        profile_of_loginuser.followings.remove(users)
    if not users == profile_of_loginuser.user:
        if users in profile_of_loginuser.followings.all():
            con.append("Unfollow")
            context['unfollow'] = con
        else:
            con.append("Follow")
            context['follow'] = con
    profile_to_view = get_object_or_404(Profile, user=users)
    pro.append(profile_to_view)
    posts = Post.objects.filter(user=users).order_by('-date_time')
    context['profile'] = pro
    context['posts'] = posts
    return render(request, 'homepage.html', context)


@login_required
def get_global(request):
    posts = []
    context = {}
    context['posts'] = posts
    form = PostForm()  # Creates form from the
    context['form'] = form         # existing entry.
    return render(request, 'global-stream.html', context)

def add_post_global(request):
    if not 'post' in request.POST or not request.POST['post']:
        raise Http404
    else:
        new_post = Post(text=request.POST['post'],user=request.user)
        new_post.save()

    return HttpResponse("")  # Empty response on success.


@login_required
def get_posts_global(request, time="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    posts = Post.get_changes(time).order_by('-date_time')
    context = {"max_time":max_time, "posts":posts}
    return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_posts_following(request, time="1970-01-01T00:00+00:00"):
    posts = []
    follows = []
    profile = Profile.objects.get(user=request.user)
    users = profile.followings.all()
    max_time = Post.get_max_time_user(users[0])

    for user in users:
        follows.append(user)
        max_time_1 = Post.get_max_time_user(user)
        if max_time_1 > max_time:
            max_time = max_time_1

    following_posts = Post.objects.all().order_by('-date_time')
    for post in following_posts:
        if post.user in follows:
            posts.append(post)
    context = {"max_time":max_time, "posts":posts}
    return render(request, 'posts.json', context, content_type='application/json')

@login_required
def get_posts_homepage(request, name, time="1970-01-01T00:00+00:00"):
    user1 = User.objects.get(username=name)
    max_time = Post.get_max_time_user(user1)
    posts = Post.get_changes_user(user1,time).order_by('-date_time')
    context = {"max_time":max_time, "posts":posts}
    return render(request, 'posts.json', context, content_type='application/json')


@login_required
def get_comments_global_post(request,post_id, time="1970-01-01T00:00+00:00"):
    post1 = Post.objects.get(id=post_id)
    max_time = Comment.objects.filter(post=post1).aggregate(Max('date_time'))['date_time__max'] or datetime.datetime(1970,1,1)
    comments = Comment.get_changes(time).filter(post=post1).order_by('date_time')
    context = {"post_id":post_id, "max_time":max_time, "comments":comments}
    return render(request, 'comments.json', context, content_type='application/json')


@login_required
def comment_global(request, post_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        post_com = Post.objects.get(id=post_id)
        new_com = Comment(text=request.POST['comment'],user=request.user, post=post_com)
        new_com.save()
    return HttpResponse("")  # Empty response on success.



@login_required
def post_following(request):
    errors = []
    posts = []
    follows = []
    context = {}
    context['error'] = errors
    context['posts'] = posts
    context['follows'] = follows

    if request.method == 'GET':
        form = PostForm()  # Creates form from the
        context['form'] = form         # existing entry.
    elif 'post' in request.POST:
        form = PostForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'password.html', context)
        new_post = Post(text=request.POST['post'], user=request.user)
        new_post.save()
    profile = Profile.objects.get(user=request.user)
    for user in profile.followings.all():
        follows.append(user)
    # posts = Post.objects.filter(user in follows).roder_by('-date_time')
    following_posts = Post.objects.all().order_by('-date_time')
    for post in following_posts:
        if post.user in follows:
            posts.append(post)
    return render(request, 'following-stream.html', context)

@login_required
@transaction.atomic
def view_profile(request, name):
    profile_to_view = get_object_or_404(Profile, user=request.user)
    context = {}

    if request.method == 'GET':
        form1 = ProfileForm(instance=profile_to_view)  # Creates form from the
        context = {'form1':form1,'id':name}          # existing entry.
        return render(request, 'profile.html', context)

    # if method is POST, get form data to update the model
    form1 = ProfileForm(request.POST, request.FILES, instance=profile_to_view)
    # #the email part
    if 'btn-password' in request.POST:
        token = default_token_generator.make_token(request.user)
        email_body = """
        This is an email sent from Grumblr. Please click the link below to verify your change of your password:
        http://%s%s
        """ % (request.get_host(),
               reverse('confirm', args=(request.user.username, token)))

        send_mail(subject="Verify the change of your password",
                  message=email_body,
                  from_email="yh1@andrew.cmu.edu",
                  recipient_list=[request.user.email])

    context['email']=request.user.email

    if not form1.is_valid():
        context = {'form1':form1, 'id':name}
        return render(request, 'profile.html', context)

    form1.save()
    return redirect(reverse('global'))

@login_required
def get_photo(request, name):
    profile = get_object_or_404(Profile, user=User.objects.get(username=name))
    if not profile.photo:
        raise Http404
    content_type1 = guess_type(profile.photo.name)
    #content_type = guess_type("photo1.png")
    return HttpResponse(profile.photo, content_type=content_type1)

def verify_email(request, name, token):
    return redirect(reverse('global'))

# def confirm_password(request, name, token):
#     return redirect(reverse('change_password', kwargs={'name':name}))
@login_required
def change_password(request, name):
    context = {}
    if request.method == 'GET':
        context['form'] = PasswordForm()
        return render(request, 'password.html', context)

    form = PasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'password.html', context)

    user = User.objects.get(username__exact=name)
    user.set_password(form.cleaned_data['password1'])
    user.save()
    new_user = authenticate(username=name,
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('global'))
