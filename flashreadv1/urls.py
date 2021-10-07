from django.urls import path, include
from .views import *

urlpatterns = [
    path('course/all', CourseListView.as_view()),
    path('course/<str:name>', CourseOnewithTaskView.as_view()),

    path('task/all', TaskListView.as_view()),
    path('task/<int:pk>', TaskOneView.as_view()),

    path('<slug:username>', UserOneView.as_view()),
    path('usercourses/add', UserCoursesAddView.as_view()),
    # not test
    path('usercoursesanswers/add', UserCourseAnswerAddView.as_view()),
    path('usercoursesanswers/<slug:username>/<str:name>/<int:task>', UserCourseAnswerView.as_view()),
    path('usercoursesanswers/update/<slug:username>/<str:name>/<int:task>/<int:ans_number>', UserCourseAnswerUpdateView.as_view()),

    path('<slug:username>/<str:name>/answered', CourseTasksAnsweredbyUserListView.as_view()),
    path('<slug:username>/<str:name>/notanswered', CourseTasksAnsweredbyUserListView.as_view()),
    # not test
    path('usertaskanswers/add', UserTasksAnswerAddView.as_view()),
    path('usertaskanswers/<slug:username>/<int:task>', UserTasksAnswerView.as_view()),
    path('usertaskanswers/update/<slug:username>/<int:id>/<int:ans_number>', UserTasksAnswerUpdateView.as_view()),
    # not test
    path('<slug:username>/params', UserParamsView.as_view()),
    path('params/add', UserParamsAddView.as_view()),
    path('<slug:username>/params/update/<slug:measure_date>', UserParamsUpdateView.as_view()),
    # not test
    path('<slug:username>/daily', UserDailyView.as_view()),
    path('daily/add', UserDailyAddView.as_view()),
    path('<slug:username>/daily/update/<slug:date>', UserDailyUpdateView.as_view()),
    # not test 
    path('<int:taskid>/questions', QuestionView.as_view()),
    path('questions/add', QuestionAddView.as_view()),
    path('questions/delete/<int:pk>', QuestionDeleteView.as_view()),
    path('questions/update/<int:pk>', QuestionUpdateView.as_view()),
    # + stats 
    ]