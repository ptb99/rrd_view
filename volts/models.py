from django.db import models

# Create your models here.

class graph(models.Model):

    # schema:
    label = models.CharField(max_length=128)
    duration = models.CharField(max_length=128)

    upper = models.FloatField(default=20.0)
    lower = models.FloatField(default=0.0)

    axis_label = models.CharField(default='Volts', max_length=128)
    value_field = models.CharField(default='volts', max_length=128)

    def publish(self):
        self.save()

    def __str__(self):
        return self.label


class recipe_step(models.Model):

    # schema
    target = models.FloatField(default=75.0)
    duration = models.FloatField(default=0)

    def __str__(self):
        return "{0:.1f}:{1:.0f}".format(self.target, self.duration)


class labels(models.Model):

    # schema
    title = models.CharField(default='Voltage Graphs', max_length=128)
    banner = models.CharField(default='Raspberry Pi Voltage Grapher',
                              max_length=128)
    control = models.CharField(default='Temperature Recipe', max_length=128)
    color = models.CharField(default='#FCA205', max_length=16)

    def __str__(self):
        return str(self.pk)
