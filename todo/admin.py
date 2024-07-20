from django.contrib import admin
from .models import TaskFolder, Task

# Register your models here.
admin.site.register(TaskFolder)
admin.site.register(Task)
