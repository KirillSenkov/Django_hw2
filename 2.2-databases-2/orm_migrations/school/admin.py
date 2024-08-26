from django.contrib import admin
from .models import Teacher, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    filter_horizontal = ('teachers',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)