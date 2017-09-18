from django.db import models

class JobTag(models.Model):
    name = models.CharField(max_length=200, unique=True)

class JobLocation(models.Model):
    name = models.CharField(max_length=2024)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Job(models.Model):
    name = models.CharField(max_length=2024)
    location = models.ForeignKey(JobLocation)
    link = models.URLField(unique=True)
    tags = models.ManyToManyField(JobTag)
    deleted = models.BooleanField(default=False)


