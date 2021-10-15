from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from Student.redis_catch import _del
from .serializers import StudentSerializer, TeacherSerializer, LessonSerializer, GradeSerializer
from Student.models import Student, Teacher, Lesson, Grades, News, Exam
from .token_hash import hash_decode, hash_encode


def index_a(request):
    return render(request, 'index.html', {})


# 登陆
def index(request):
    student_school_id = request.POST.get('student_school_id')
    student_passwd = request.POST.get('student_passwd')
    if student_school_id is None or student_passwd is None:
        return JsonResponse({'code': '400', })
    try:
        search_student = Student.objects.get(student_study_id=student_school_id)
    except Exception:
        return JsonResponse({'code': '400', })
    if search_student.student_passwd != student_passwd:
        return JsonResponse({'code': '400', })
    else:
        # response = redirect('/log_in')
        # response.set_cookie('user_id', student_school_id, max_age=60 * 60 * 24)
        token = hash_encode(student_school_id)
        return JsonResponse({'code': '200', 'id': token})


# 找回密码x
def get_passwd(request):
    student_name = request.POST.get('student_name')
    student_study_id = request.POST.get('student_study_id')
    student_id_card = request.POST.get('student_id_card')
    if student_name is None or student_id_card is None or student_study_id is None:
        return render(request, 'get_passwd.html', {})
    student = Student.objects.get(student_name=student_name)
    student_passwd = student.student_passwd
    if student.student_study_id == int(student_study_id) and student.student_id_card == int(student_id_card):
        response = redirect('/passwd')
        response.set_cookie('student_study_id', student_study_id, max_age=5)
        return render(request, 'passwd.html', {'student_passwd': student_passwd})
    err = '存在错误项，请检查！'
    return render(request, 'get_passwd.html', {'err': err})


def passwd(request):
    return render(request, 'passwd.html', {})


# 修改密码页面
def register(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        user = Student.objects.get(student_study_id=user_id)
        student_passwd = request.POST.get('student_passwd')
        if user.student_passwd != student_passwd and request.method == 'POST':
            err = '原密码错误!'
            return render(request, 'register.html', {'err': err})
        student_passwd1 = request.POST.get('student_passwd1')
        student_passwd2 = request.POST.get('student_passwd2')
        if student_passwd1 != student_passwd2 and request.method == 'POST':
            err1 = '密码输入不一致!'
            return render(request, 'register.html', {'err1': err1})
        if student_passwd1 is None:
            user.student_passwd = user.student_passwd
        else:
            user.student_passwd = student_passwd1
        user.save()
        if request.method == 'POST':
            return redirect('/index')
        return render(request, 'register.html', {})
    else:
        return redirect('/index')


# 学生中心首页
# def log_in(request):
#     if request.method == 'GET':
#         return render(request, 'base.html', {})
#     else:
#         user_id = request.POST.get('id')
#         student1 = Student.objects.filter(student_study_id=user_id).first()
#         # return JsonResponse({'code': '200', 'student': {
#         #     'student_name': student1.student_name,
#         #     'student_sex': student1.student_sex,
#         #     'student_study_id': student1.student_study_id,
#         #     'student_id_card': student1.student_id_card,
#         #     'student_go_school_year': student1.student_go_school_year,
#         #     'student_major': student1.student_major,
#         #     'student_id_home': student1.student_id_home,
#         #     'student_study_style': student1.student_study_style
#         # }})

class Login_in_View(APIView):
    def get(self, request, format=None):
        return render(request, 'base.html', {})

    @csrf_exempt
    def post(self, request):
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            student1 = Student.objects.filter(student_study_id=user_id).first()
            serializer = StudentSerializer(student1)
            return Response(serializer.data)
        else:
            return Response({'code': '400'})


# 课程表
class My_Lesson_View(APIView):
    def get(self, request):
        return render(request, 'my_lesson.html', {})

    def post(self, request):
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            lesson = Lesson.objects.filter(student__student_study_id=user_id)
            student1 = Student.objects.filter(student_study_id=user_id).first()
            list_teacher = []
            for i in lesson:
                teacher = Teacher.objects.filter(lesson__lesson_name=i.lesson_name)
                for i in teacher:
                    list_teacher.append(i.teacher_name)
            s_stu = StudentSerializer(student1)
            s_lesson = LessonSerializer(lesson, many=True)
            return Response([s_stu.data, s_lesson.data, list_teacher])
        else:
            return redirect('/index_a/')


# 我的成绩
class My_Grades_view(APIView):
    def get(self, request):
        return render(request, 'my_grades.html', {})

    def post(self, request):
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            lesson = Lesson.objects.filter(student__student_study_id=user_id)
            student1 = Student.objects.filter(student_study_id=user_id).first()
            grade = Grades.objects.filter(student_name__student_study_id=user_id)
            l_le = LessonSerializer(lesson, many=True)
            s_stu = StudentSerializer(student1)
            g_gr = GradeSerializer(grade, many=True)
            # sum = 0
            # sum1 = 0
            # k = 0
            # m = 0
            # for i in grade:
            #     sum += i.lesson_name.lesson_score
            #     if i.grade < 60:
            #         k += 1
            #     if i.grade >= 60:
            #         sum1 += i.lesson_name.lesson_score
            #         m += 1
            # return render(request, 'my_grades.html', {'student': student1, 'grade': grade, 'sum': sum, 'k': k,
            #                                           'sum1': sum1, 'm': m})
            return Response([s_stu.data, l_le.data, g_gr.data])
        else:
            return redirect('/index_a/')


# 基本信息
def my_info(request):
    if request.method == 'GET':
        return render(request, 'my_info.html', {})
    else:
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            student_tel = request.POST.get('tel')
            student_email = request.POST.get('email')
            student_addr = request.POST.get('addr')
            student_short = request.POST.get('short')
            student1 = Student.objects.filter(student_study_id=user_id).first()
            user = Student.objects.get(student_study_id=user_id)
            if student_tel is None:
                user.student_tel = user.student_tel
            else:
                user.student_tel = student_tel
            if student_email is None:
                user.student_email = user.student_email
            else:
                user.student_email = student_email
            if student_addr is None:
                user.student_addr = user.student_addr
            else:
                user.student_addr = student_addr
            if student_short is None:
                user.student_short = user.student_short
            else:
                user.student_short = student_short
            user.save()
            return JsonResponse({'code': '200', 'info': {
                'student_name': student1.student_name,
                'student_passwd': student1.student_passwd,
                'student_tel': student1.student_tel,
                'student_email': student1.student_email,
                'student_addr': student1.student_addr,
                'student_short': student1.student_short,
                'student_study_id': student1.student_study_id,
            }})
        else:
            return JsonResponse({'code': '400'})


# 退出登陆
class User_Logout_View(APIView):

    def post(self, request):
        user_id = request.POST.get('id')
        if user_id:
            # 先解密获取token中的用户id
            key_id = hash_decode(user_id)
            # 删除redis缓存中的用户token
            print(key_id)
            if _del(key_id):
                return Response({'code': '200'})
            return Response({'code': '500'})
        else:
            return redirect('/index_a/')


# 查看考试
# def search_test(request):
#     user_id = request.COOKIES.get('user_id')
#     if user_id:
#         lesson = Lesson.objects.filter(student__student_study_id=user_id)
#         student1 = Student.objects.filter(student_study_id=user_id)
#         return render(request, 'search_test.html', {'lesson': lesson, 'student': student1})
#     else:
#         return redirect('/index')


class Search_Test_View(APIView):
    def get(self, request):
        return render(request, 'search_test.html', {})

    def post(self, request):
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            lesson = Lesson.objects.filter(student__student_study_id=user_id)
            student1 = Student.objects.filter(student_study_id=user_id).first()
            s_stu = StudentSerializer(student1)
            s_les = LessonSerializer(lesson, many=True)
            return Response([s_stu.data, s_les.data])
        else:
            return redirect('/index_a/')


def grade1718(request):
    return render(request, 'grade-1718.html', {})


def grade1819(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        grade = Grades.objects.filter(student_name__student_study_id=user_id)
        sum = 0
        sum1 = 0
        k = 0
        m = 0
        for i in grade:
            if i.lesson_name.lesson_data == '18-19':
                sum += i.lesson_name.lesson_score
                if i.grade < 60:
                    k += 1
                if i.grade >= 60:
                    sum1 += i.lesson_name.lesson_score
                    m += 1
        return render(request, 'grade-18-19.html',
                      {'student': student1, 'grade': grade, 'sum': sum, 'sum1': sum1, 'm': m, 'k': k})
    else:
        return redirect('/index')


def grade1920(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        student1 = Student.objects.filter(student_study_id=user_id)
        grade = Grades.objects.filter(student_name__student_study_id=user_id)
        sum = 0
        sum1 = 0
        k = 0
        m = 0
        for i in grade:
            if i.lesson_name.lesson_data == '19-20':
                sum += i.lesson_name.lesson_score
                if i.grade < 60:
                    k += 1
                if i.grade >= 60:
                    sum1 += i.lesson_name.lesson_score
                    m += 1
        return render(request, 'grade-19-20.html',
                      {'student': student1, 'grade': grade, 'sum': sum, 'sum1': sum1, 'm': m, 'k': k})
    else:
        return redirect('/index')


# 学校新闻页面
def school_news(request):
    if request.method == 'GET':
        today = datetime.date.today()
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        data = week_day_dict[datetime.datetime.now().weekday()]
        return render(request, 'school_news.html', {'today': today, 'data': data})
    else:
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            student1 = Student.objects.filter(student_study_id=user_id).first()
            page = request.GET.get('page')
            if page:
                page = int(page)
            else:
                page = 1
            news = News.objects.all()
            paginator = Paginator(news, 5)
            page_num = paginator.num_pages
            page_news_list = paginator.page(page)
            if page_news_list.has_next():
                next_page = page + 1
            else:
                next_page = page
            if page_news_list.has_previous():
                previous_page = page - 1
            else:
                previous_page = page
            return JsonResponse({'code': '200', 'newslist': {
                'student_school_id': student1.student_study_id,
                'student_name': student1.student_name
            }})

        else:
            return redirect('index_a/')


# 新闻详情页面
def news_detail(request, new_ids):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        news = News.objects.all()
        student1 = Student.objects.filter(student_study_id=user_id)
        for index, new in enumerate(news):
            if new.news_id == new_ids:
                title = new.news_title
                acontents = new.news_body.split('\n')
                break
        return render(request, 'news_detail.html', {'student': student1, 'acontents': acontents, 'title': title,
                                                    })
    else:
        return redirect('/index')


# 选修课程选择
class Lesson_Learn_View(APIView):
    def get(self, request):
        return render(request, 'get_test.html', {})

    def post(self, request):
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            lesson_name = request.POST.get('lesson_name')
            student1 = Student.objects.filter(student_study_id=user_id).first()
            lesson_all = Lesson.objects.all()
            if lesson_name:
                lesson = Lesson.objects.filter(student__student_study_id=user_id)
                flag = 0
                for i in lesson:
                    if not i.is_default:
                        flag += 1
                if flag >= 4:
                    err = '每个学生一学期之多选择四门选修课！'
                    return Response(err)
                for i in lesson:
                    if i.lesson_name == lesson_name:
                        if flag >= 4:
                            err = '每个学生一学期之多选择四门选修课！'
                        else:
                            err = '该门课程已经选过了！请重新选择！'
                        return Response(err)
                get_num = Lesson.objects.get(lesson_name=lesson_name)
                if get_num.lesson_num <= 0:
                    err = '课程人数已满！'
                    return Response(err)
                get_num.lesson_num -= 1
                get_num.save()
                Lesson.objects.get(lesson_name=lesson_name).student.add(student1)
                mes = '选课成功！'
                return Response(mes)
            s_stu = StudentSerializer(student1)
            l_lesson = LessonSerializer(lesson_all, many=True)
            return Response([s_stu.data, l_lesson.data])
        else:
            return redirect('/index_a/')


# 全国考试选择
def get_exam(request):
    if request.method == 'GET':
        return render(request, 'get_exam.html', {})
    else:
        token = request.POST.get('id')
        user_id = hash_decode(token)
        if user_id:
            exam_d = {}
            exam_get_d = {}
            student1 = Student.objects.filter(student_study_id=user_id).first()
            exam = Exam.objects.all()
            for i in exam:
                a = {
                    'exam_id': i.exam_id,
                    'exam_name': i.exam_name,
                    'exam_time': i.exam_time
                }
                exam_d[i.exam_name] = a
            exam_get = Exam.objects.filter(student__student_study_id=user_id)
            for i in exam_get:
                a = {
                    'exam_id': i.exam_id,
                    'exam_name': i.exam_name,
                    'exam_time': i.exam_time
                }
                exam_get_d[i.exam_name] = a
            a = request.POST.get('exam_name')
            if a:
                Exam.objects.get(exam_name=a).student.add(student1)
            return JsonResponse({'code': '200', 'examlist': exam_d, 'exam_get_list': exam_get_d,
                                 'student': {
                                     'student_study_id': student1.student_study_id,
                                     'student_name': student1.student_name
                                 }})
        else:
            return redirect('/index_a/')


def exam_check(request):
    user_id = request.POST.get('id')
    if user_id:
        student = Student.objects.filter(student_study_id=user_id).first()
        a = request.POST.get('exam_name')
        if a:
            Exam.objects.get(exam_name=a).student.remove(student)
            return JsonResponse({'code': '200'})
        return JsonResponse({'code': '400'})
    return JsonResponse({'code': '401'})
