from django.shortcuts import render
from django.utils import tree
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


# class CourseOnewithTaskView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CoursewithTasksTypeSerializer
#     permission_classes = [permissions.IsAdminUser]

class CourseOnewithTaskView(generics.RetrieveAPIView):
    lookup_field = 'name'
    queryset = Course.objects.all()
    serializer_class = CoursewithTasksSerializer
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


class QuestionView(generics.ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuiestionSerializer


class QuestionAddView(generics.ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuiestionSerializer
    permissions_classes = [permissions.IsAdminUser]


class UserOneView(generics.RetrieveAPIView):
    lookup_field = 'name'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCoursesAddView(generics.CreateAPIView):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer


class UserCourseAnswerAddView(generics.CreateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer


class UserCourseAnswerView(generics.ListAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer

    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


class UserCourseAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer


class CourseTasksAnsweredbyUserListView(generics.ListAPIView):
    serializer_class = CourseTasksSerializer
    
    def list(self, request, *args, **kwargs):
        # print(request.path.split('/')[2:4])
        r = request.path.split('/')
        user, course =  r[2:4]
        is_complete = False if r[5] == 'n' else True
        user = User.objects.filter(username = user)
        course = Course.objects.get(name = course)
        usercourse = UserCourses.objects.get(user = user[0].id, course = course.id)
        coursetasks = CourseTasks.objects.filter(course = course.id)
        usercoursestask = UserCoursesTasks.objects.filter(usercourses = usercourse.id, is_complete = is_complete)
        for i in usercoursestask:
            coursetasks = coursetasks.filter(task = i.task)
        instance = coursetasks
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class UserTasksAnswerAddView(generics.CreateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer


class UserTasksAnswerView(generics.ListAPIView):
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


class UserDailyAddView(generics.CreateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer


class UserDailyUpdateView(generics.UpdateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer