from django.db import models

# Create your models here.

class graph(models.Model):

    # schema:
    label = models.CharField(max_length=128)
    duration = models.CharField(max_length=128)

    def publish(self):
        self.save()

    def __str__(self):
        return self.label
