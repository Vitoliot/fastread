from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
# Create your views here.
# User - s -
# UserParams - s
# UserCourses - s
# UserCoursesTasks - s
# UserCoursesTasksAnswer - s
# UserTasks - s -
# Task - s -
# TaskAnswer
# Question - s -
# Course - s -
# CourseTasks - s -

class OneCourseAllAll(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursewithTasksSerializer

# class OneCourseAllAll(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer