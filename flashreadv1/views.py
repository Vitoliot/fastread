from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
# from rest_framework.views import APIView
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
# Questions - s -
# Course - s -
# CourseTasks - s -


# class OneCourseAllAll(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CoursewithTasksSerializer


class CourseOnewithTaskView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursewithTasksTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskOneView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserOneView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCoursesAddView(generics.CreateAPIView):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer


class UserCourseAnswerAddView(generics.CreateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer


class UserCourseAnswerView(generics.RetrieveAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer


class UserCourseAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer


class CourseTasksAnsweredbyUserListView(generics.ListAPIView):
    serializers = CoursewithTasksSerializer

    def get_queryset(self):
        return super().get_queryset()


class UserTasksAnswerAddView(generics.CreateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer


class UserTasksAnswerView(generics.RetrieveAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer


class UserTasksAnswerUpdateView(generics.UpdateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer


class UserParamsView(generics.ListAPIView):
    serializer_class = UserParamsSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        if user:
            return UserParams.objects.order_by('measure_date').filter(user=user)
        return UserParams.objects.order_by('measure_date')


class UserParamsAddView(generics.CreateAPIView):
    queryset = UserParams.objects.all()
    serializer_class = UserParamsSerializer


class UserParamsUpdateView(generics.UpdateAPIView):
    queryset = UserParams.objects.all()
    serializer_class = UserParamsSerializer


class UserDailyView(generics.ListAPIView):
    serializer_class = UserDailySerializer

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        if user:
            return UserDaily.objects.order_by('measure_date').filter(user=user)
        return UserDaily.objects.order_by('measure_date')


class UserDailyCreateView(generics.CreateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer


class UserDailyUpdateView(generics.UpdateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer