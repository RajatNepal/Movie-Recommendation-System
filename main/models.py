from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.

class Rating(models.Model):
    username =  models.CharField(max_length=15, unique = True)
    #pass_hash = models.CharField(max_length=100)
    email = models.CharField(max_length=150)

    #  I belive "models.BooleanField()" is the equivalent of TINYINT in Django
    #booleanfield is a boolean, 0 or 1, we want it to have -1 option as well (so we will store as IntegerField)
    Movie_1 = models.IntegerField()
    Movie_2 = models.IntegerField()
    Movie_3 = models.IntegerField()
    Movie_4 = models.IntegerField()
    Movie_5 = models.IntegerField()
    Movie_6 = models.IntegerField()
    Movie_7 = models.IntegerField()
    Movie_8 = models.IntegerField()
    Movie_9 = models.IntegerField()
    Movie_10 = models.IntegerField()

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=255)
    link = models.TextField()
    description = models.TextField()

class Comment(models.Model):
    body = models.CharField(max_length = 400, default = '')
    movie_id = models.ForeignKey(Movie, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
