import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    enabled = models.BooleanField(default=True)  # Campo para habilitar o deshabilitar la pregunta
    enabled_date = models.DateTimeField(null=True, blank=True)  # Campo para registrar la fecha de deshabilitación
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
     return self.question_text
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    suspended = models.BooleanField(default=False)  # Campo para suspender la choice

    def __str__(self):
     return self.choice_text
    


    
class QuestionUser(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} votó en {self.question.question_text}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s Address"
