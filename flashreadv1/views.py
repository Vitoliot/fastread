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
    lookup_field = 'name'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCoursesAddView(generics.CreateAPIView):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
        user, course, task = r_path[2:5]
        user, course = User.objects.filter(username=user), course = Course.objects.filter(name=course) 
        usercourse = UserCourses.objects.get(user = user[0].id, course = course.id)
        self.get_queryset().filter(usercourses = usercourse, task = task)
        return super().list(request, *args, **kwargs)


class UserCourseAnswerUpdateView(generics.UpdateAPIView):
    queryset = UserCoursesTasksAnswer.objects.all()
    serializer_class = UserCoursesTasksAnswerSerializer
    lookup_fields = ['task', 'ans_number']
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        r_path = request.path.split('/')
        user, course = r_path[2:4]
        user, course = User.objects.filter(username=user), course = Course.objects.filter(name=course) 
        usercourse = UserCourses.objects.get(user = user[0].id, course = course.id)
        self.get_queryset().filter(usercourses = usercourse)
        return super().update(request, *args, **kwargs)


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
    permission_classes = [permissions.IsAuthenticated]


class UserTasksAnswerView(generics.ListAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, task =  r[2:4]
        user = User.objects.filter(username = user)
        usertask = UserTasks.objects.get(user = user[0].id, task = task)
        self.get_queryset().filter(usertask = usertask.id)
        return super().list(request, *args, **kwargs)


class UserTasksAnswerUpdateView(generics.UpdateAPIView):
    queryset = TaskAnswer.objects.all()
    serializer_class = TaskAnswerSerializer
    lookup_field = 'ans_number'
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        r = request.path.split('/')
        user, task =  r[2:4]
        user = User.objects.filter(username = user)
        usertask = UserTasks.objects.get(user = user.id, task = task)
        self.get_queryset().filter(usertask = usertask.id)
        return super().update(request, *args, **kwargs)


class UserParamsView(generics.ListAPIView):
    serializer_class = UserParamsSerializer
    queryset = UserParams.objects.order_by('measure_date')
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.filter(username = user)
        self.get_queryset().filter(usertask = user[0].id)
        return super().list(request, *args, **kwargs)
    # def get_queryset(self):
    #     user = self.request.query_params.get('user', None)
    #     if user:
    #         return UserParams.objects.order_by('measure_date').filter(user=user)
    #     return UserParams.objects.order_by('measure_date')


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
        user = User.objects.filter(username = user)
        self.get_queryset().filter(usertask = user[0].id)
        return super().update(request, *args, **kwargs)


class UserDailyView(generics.ListAPIView):
    serializer_class = UserDailySerializer
    queryset = UserDaily.objects.order_by('date')
    permission_classes = [permissions.IsAuthenticated]
    # def get_queryset(self):
    #     user = self.request.query_params.get('user', None)
    #     if user:
    #         return UserDaily.objects.order_by('measure_date').filter(user=user)
    #     return UserDaily.objects.order_by('measure_date')
    def list(self, request, *args, **kwargs):
        r = request.path.split('/')
        user =  r[2]
        user = User.objects.filter(username = user)
        self.get_queryset().filter(usertask = user[0].id)
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
        self.get_queryset().filter(usertask = user[0].id)
        return super().update(request, *args, **kwargs)