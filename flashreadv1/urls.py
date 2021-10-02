from django.urls import path, include
from .views import *

urlpatterns = [
    # path('course/<int:pk>/allinfo', OneCourseAllAll.as_view()),
    path('course/new', CourseCreateView.as_view()),
    ]