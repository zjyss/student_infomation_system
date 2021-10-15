from django.contrib import admin
from Student.models import Student, Lesson, Teacher, Grades, News, Exam
# Register your models here.
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Teacher)
admin.site.register(Grades)
admin.site.register(News)
admin.site.register(Exam)