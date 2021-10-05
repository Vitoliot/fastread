from django.urls import path, include
from .views import *

urlpatterns = [
    # path('course/<int:pk>/allinfo', OneCourseAllAll.as_view()),
    path('course/all', CourseListView.as_view()),
    path('course/<int:pk>', CourseOnewithTaskView.as_view()),
    path('task/all', TaskListView.as_view()),
    path('task/<int:pk>', TaskOneView.as_view()),
    ]