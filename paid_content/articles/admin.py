from django.contrib import admin

from .models import Profile, Article

class ProfileAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Article, ArticleAdmin)