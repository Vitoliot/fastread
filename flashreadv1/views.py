from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .models import *
from .serializers import *
from flashread.permissions import IsOwnerProfileOrReadOnly


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
    lookup_field = 'taskid'


class QuestionAddView(generics.CreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuiestionSerializer
    permissions_classes = [permissions.IsAdminUser]


class QuestionUpdateView(generics.UpdateAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuiestionSerializer
    permissions_classes = [permissions.IsAdminUser]


class QuestionDeleteView(generics.DestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuiestionSerializer
    permissions_classes = [permissions.IsAdminUser]


class UserOneView(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCoursesAddView(generics.CreateAPIView):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCourseAnswerAddView(generics.CreateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCourseAnswerView(generics.ListAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        r_path = request.path.split('/')
        user, course, task = r_path[3:6]
        user = User.objects.get(username=user)
        course = Course.objects.get(name=course) 
        usercourse = UserCourses.objects.get(user = user, course = course)
        usercoursetasks = UserCoursesTasks.objects.get(usercourses = usercourse,  task = task)
        self.get_queryset().filter(uctask = usercoursetasks)
        return super().list(request, *args, **kwargs)


class UserCourseAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer
    lookup_field = 'ans_number'
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        r_path = request.path.split('/')
        user, course, task  = r_path[4:7]
        user = User.objects.get(username=user)
        course = Course.objects.get(name=course) 
        usercourse = UserCourses.objects.get(user = user, course = course)
        usercoursetasks = UserCoursesTasks.objects.get(usercourses = usercourse,  task = task)
        self.get_queryset().filter(uctask = usercoursetasks)
        return super().update(request, *args, **kwargs)


class CourseTasksAnsweredbyUserListView(generics.ListAPIView):
    serializer_class = UserCoursesTaskSerializer
    queryset = UserCoursesTasks.objects.filter(is_complete = True)
    
    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, course = r[2:4]
        user = User.objects.get(username = user)
        course = Course.objects.get(name = course)
        usercourse = UserCourses.objects.get(user = user, course = course)
        self.get_queryset().filter(usercourses = usercourse)
        return super().list(request, *args, **kwargs)

class CourseTasksNotAnsweredbyUserListView(generics.ListAPIView):
    serializer_class = CourseTasksSerializer
    queryset = CourseTasks.objects.all()

    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, course = r[2:4]
        user = User.objects.get(username = user)
        course = Course.objects.get(name = course)
        usercourse = UserCourses.objects.get(user = user, course = course)
        tasks = UserCoursesTasks.objects.filter(usercourses = usercourse)
        for task in tasks:
            self.get_queryset().filter(task = task.task)
        return super().list(request, *args, **kwargs)


class UserTasksAnswerAddView(generics.CreateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTasksAnswerView(generics.ListAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, task =  r[3:5]
        print(user)
        user = User.objects.get(username = user)
        usertask = UserTasks.objects.get(user = user, task = task)
        self.get_queryset().filter(usertask = usertask.id)
        return super().list(request, *args, **kwargs)


class UserTasksAnswerUpdateView(generics.UpdateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer
    lookup_field = 'ans_number'
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, task =  r[4:6]
        user = User.objects.get(username = user)
        usertask = UserTasks.objects.get(user = user, task = task)
        self.get_queryset().filter(usertask = usertask.id)
        return super().update(request, *args, **kwargs)


class UserParamsView(generics.ListAPIView):
    serializer_class = UserParamsSerializer
    queryset = UserParams.objects.order_by('measure_date')
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.get(username = user)
        self.get_queryset().filter(user = user)
        return super().list(request, *args, **kwargs)


class UserParamsAddView(generics.CreateAPIView):
    queryset = UserParams.objects.all()
    serializer_class = UserParamsSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserParamsUpdateView(generics.UpdateAPIView):
    queryset = UserParams.objects.all()
    serializer_class = UserParamsSerializer
    lookup_field = 'measure_date'
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.get(username = user)
        self.get_queryset().filter(user = user)
        return super().update(request, *args, **kwargs)


class UserDailyView(generics.ListAPIView):
    serializer_class = UserDailySerializer
    queryset = UserDaily.objects.order_by('date')
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.get(username = user)
        self.get_queryset().filter(user = user)
        return super().list(request, *args, **kwargs)


class UserDailyAddView(generics.CreateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDailyUpdateView(generics.UpdateAPIView):
    queryset = UserDaily.objects.all()
    serializer_class = UserDailySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'date'

    def update(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.filter(username = user)
        self.get_queryset().filter(user = user)
        return super().update(request, *args, **kwargs)