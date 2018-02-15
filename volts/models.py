from django.db import models

# Create your models here.

class graph(models.Model):

    # schema:
    label = models.CharField(max_length=128)
    duration = models.CharField(max_length=128)

    upper = models.FloatField(default=20.0)
    lower = models.FloatField(default=0.0)

    axis_label = models.CharField(default='Volts', max_length=128)
    value_field = models.CharField(default='voltage', max_length=128)

    def publish(self):
        self.save()

    def __str__(self):
        return self.label
