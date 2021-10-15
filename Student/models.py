from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Student(models.Model):
    student_id = models.AutoField(primary_key=True, verbose_name='学生序号')
    student_study_id = models.IntegerField(verbose_name='学号')
    student_name = models.CharField(max_length=20, verbose_name='学生姓名')
    student_sex = models.CharField(max_length=3, default='男', verbose_name='性别')
    student_id_card = models.BigIntegerField(verbose_name='身份证')
    student_go_school_year = models.IntegerField(verbose_name='入学年份')
    student_major = models.CharField(max_length=20, verbose_name='专业')
    student_id_home = models.CharField(max_length=20, verbose_name='户籍')
    student_study_style = models.CharField(max_length=20, verbose_name='就读状态')
    student_passwd = models.CharField(max_length=6, verbose_name='登陆密码', default=None)
    student_tel = models.BigIntegerField(default=50, verbose_name='手机号码')
    student_email = models.CharField(max_length=20, default=None, verbose_name='邮箱')
    student_addr = models.CharField(max_length=100, default=None, verbose_name='通讯地址')
    student_short = models.CharField(max_length=500, default=None, verbose_name='个人简介')

    def __str__(self):
        return self.student_name

    class Meta:
        verbose_name_plural = '学生信息'


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True, verbose_name='课程号')
    lesson_name = models.CharField(max_length=20, verbose_name='课程名')
    lesson_local = models.CharField(max_length=30, default=None)
    lesson_time = models.CharField(max_length=30, default=None)
    lesson_score = models.IntegerField(default=0, verbose_name='课程学分')
    lesson_data = models.CharField(max_length=20, default=None, verbose_name='年份')
    lesson_num = models.IntegerField(default=121, verbose_name='剩余可选人数')
    is_default = models.BooleanField(default=False, verbose_name='是否必修')
    student = models.ManyToManyField(Student, default=None)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name_plural = '课程表单'


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, verbose_name='老师编号')
    teacher_name = models.CharField(max_length=20, verbose_name='老师姓名')
    # student = models.ForeignKey(Student, default=None,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher_name

    class Meta:
        verbose_name_plural = '老师信息'


class Grades(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student_name = models.ForeignKey(Student, default=None, on_delete=models.CASCADE, verbose_name='学生姓名')
    lesson_name = models.ForeignKey(Lesson, default=None, on_delete=models.CASCADE, verbose_name='课程名称')
    grade = models.IntegerField(verbose_name='成绩')

    def __str__(self):
        return str(self.grade) + '--------' + str(self.lesson_name)

    class Meta:
        verbose_name_plural = '成绩信息'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=50, verbose_name='新闻标题')
    news_brief = models.CharField(max_length=200, default=333, verbose_name='新闻简略')
    news_body = models.TextField(max_length=5000, verbose_name='新闻内容')

    def __str__(self):
        return self.news_title

    class Meta:
        verbose_name_plural = '新闻信息'


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=50, verbose_name='考试名称')
    exam_time = models.CharField(max_length=100, verbose_name='考试时间')
    student = models.ManyToManyField(Student, default=None)

    def __str__(self):
        return self.exam_name

    class Meta:
        verbose_name_plural = '全国考试列表'
