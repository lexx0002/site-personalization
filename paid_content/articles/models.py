from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    name = models.CharField('имя', max_length=50)
    is_paid_user = models.BooleanField(default=False)
    
    def toggle_subscription(self):
        if self.is_paid_user:
            self.is_paid_user = False
        else:
            self.is_paid_user = True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.name)


class Article(models.Model):
    title = models.CharField('заголовок', max_length=100)
    text = models.TextField('текст статьи')
    img = models.FileField(upload_to='media/%Y/%m/%d/')
    is_paid_content = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return str(self.title)

