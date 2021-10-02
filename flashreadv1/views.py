from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from .models import *
from .serializers import *
from flashread.permissions import IsOwnerProfileOrReadOnly
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


# class OneCourseAllAll(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CoursewithTasksSerializer


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursewithTasksSerializer
    permission_classes = [permissions.IsAdminUser]