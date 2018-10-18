from django.db import models


class User(models.Model):
    username = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1)


class County(models.Model):
    name = models.TextField()
    state = models.CharField(max_length=2)
    population = models.IntegerField()


class Picture(models.Model):
    file_url = models.TextField()
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class Review(models.Model):
    description = models.TextField()
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.DateTimeField()


class Crime(models.Model):
    county_id = models.ForeignKey(County, on_delete=models.CASCADE)
    count = models.FloatField()
    type = models.TextField()