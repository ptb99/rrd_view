from django.contrib import admin
from .models import graph,recipe_step,labels

# Register your models here.

admin.site.register(graph)
admin.site.register(recipe_step)
admin.site.register(labels)
