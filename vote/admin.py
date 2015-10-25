from django.contrib import admin

from vote.models import Student, Category, Video, Vote

# Register your models here.
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Vote)