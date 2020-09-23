from django.contrib import admin
from .models import Years,Dept,Student,Sem,User,Profile,Subjects,Faculty,Notes,Questions,Answers
from django.contrib.auth.admin import UserAdmin

# admin.site.register(User,UserAdmin)
admin.site.register(Years)
admin.site.register(Dept)
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Sem)
admin.site.register(Subjects)
admin.site.register(Faculty)
admin.site.register(Notes)
admin.site.register(Questions)
admin.site.register(Answers)

