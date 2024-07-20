from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.
class TaskFolder(models.Model):
    name = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_categories', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'taskcategories'
        ordering = ('-created_at',)
    
class Task(models.Model):
    folder = models.ForeignKey(TaskFolder, on_delete=models.CASCADE, related_name='tasks', null=True)

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False, blank=True)
    completion_date = models.DateField(null=True, blank=True)  
    completion_time = models.TimeField(null=True, blank=True)  
    description = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publ_or_priv = models.BooleanField(default=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self) -> str:
        return str(self.title) + ' - ' + str(self.owner) + ' - ' + str(self.created_at)

    class Meta:
        verbose_name_plural = 'tasks'
        ordering = ('-created_at',)