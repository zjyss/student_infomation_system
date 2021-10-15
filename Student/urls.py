from django.contrib import admin
from django.urls import path
from Student.views import index, register, Login_in_View, My_Lesson_View, My_Grades_view, my_info, User_Logout_View, Search_Test_View, grade1718, \
    grade1819, grade1920, school_news, news_detail, Lesson_Learn_View, get_exam, get_passwd, passwd, exam_check, index_a

app_name = '[Student]'





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_a),
    path('index/', index),
    path('register/', register),
    path('log_in/', Login_in_View.as_view(), name='log_in'),
    path('my_lesson/', My_Lesson_View.as_view()),
    path('my_grades/', My_Grades_view.as_view()),
    path('my_info/', my_info),
    path('logout/', User_Logout_View.as_view()),
    path('search_test/', Search_Test_View.as_view()),
    path('grade1718', grade1718),
    path('grade1819', grade1819),
    path('grade1920', grade1920),
    path('school_news/', school_news),
    path('news_detail/<int:new_ids>', news_detail),
    path('get_test/', Lesson_Learn_View.as_view()),
    path('get_exam/', get_exam),
    path('get_passwd', get_passwd),
    path('passwd', passwd),
    path('exam_check/',exam_check),
]
