from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.CharField(max_length=2)
    completed = models.BooleanField(default=0)
    day = models.CharField(max_length=9)

    def __str__(self):
        return self.title
