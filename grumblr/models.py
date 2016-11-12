from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.html import escape
# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now=True)
    max_comment_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.text)
    def __str__(self):
        return self.__unicode__()
    #the get-posts should be same as the get_changes
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(date_time__gt=time).distinct()

    @staticmethod
    def get_changes_user(user,time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(date_time__gt=time,user=user).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('date_time'))['date_time__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_user(user1):
        posts = Post.objects.filter(user=user1)
        return posts.aggregate(Max('date_time'))['date_time__max'] or "1970-01-01T00:00+00:00"

    @property
    def html(self):

        return "<div class='panel panel-info' id='post-%s'> \
            <div class='panel-heading'> \
              <h3 class='panel-title'> \
                <img class='img-circle' src='photo/%s' alt='failure' width='30' height='30'> \
                <a href = 'homepage/%s'>%s</a> \
              </h3> \
            </div> \
            <div class='panel-body'> \
              <label>%s</label> \
              <p>%s</p> \
            </div> \
            <ol id='com-list-%s'></ol> \
                <input type='text-com' id='text-com-%s' placeholder='add comment here...'> \
                <button class='btn-com' id='btn-com'>Comment</button> \
          </div> \
      </div>" % (escape(self.id), escape(self.user.username), escape(self.user.username), escape(self.user.username), escape(self.date_time), escape(self.text), escape(self.id), escape(self.id))

class Comment(models.Model):
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)
    def __unicode__(self):
        return "%s" % (self.text)
    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_max_time():
        return Comment.objects.all().aggregate(Max('date_time'))['date_time__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_post(post1):
        comments = Comment.objects.filter(post=post1)
        return comments.aggregate(Max('date_time'))['date_time__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_postid(self):
        return self.post.id


    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Comment.objects.filter(date_time__gt=time).distinct()

    @property
    def html(self):
        return "<div class='label-com-title'><img class='img-circle' src='photo/%s' alt='failure' width='30' height='30'> \
                <a href = 'homepage/%s'>%s      </a><label>%s</label></div><div class='label-com-text'><p>%s</p></div>" % (escape(self.user.username), escape(self.user.username), escape(self.user.username), escape(self.date_time), escape(self.text))



#return "<div class='col-sm-6' id='post-%s'> \
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="users")
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    age = models.IntegerField(default=0,blank=True)
    short_bio = models.TextField(max_length=420, blank=True)
    photo = models.ImageField(upload_to='profile-photo')
    token_password = models.CharField(max_length=200, blank=True)
    followings = models.ManyToManyField(User,related_name="followings", blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.first_name, self.last_name)
    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_profile(user):
        return Profile.objects.filter(user=user)

class following(models.Model):
    profile = models.ForeignKey(Profile)
    followings = models.ManyToManyField(User)
