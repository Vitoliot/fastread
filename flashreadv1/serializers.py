from django.db.models import query
from rest_framework import serializers
from .models import *
from djoser.serializers import UserCreateSerializer

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


class DynamycSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamycSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TaskSerializer(DynamycSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'


class QuiestionSerializer(serializers.ModelSerializer):
    task = TaskSerializer(fields = ('id', 'name'))
    class Meta:
        model = Question
        fields = '__all__'

class CourseSerializer(DynamycSerializer):
    
    WPM_par = serializers.CharField(source='get_WPM_par_display', read_only=True)
    BOFI_par = serializers.CharField(source='get_BOFI_par_display', read_only=True)
    VMem_par = serializers.CharField(source='get_VMem_par_display', read_only=True)
    LMem_par = serializers.CharField(source='get_LMem_par_display', read_only=True)
    At_par = serializers.CharField(source='get_At_par_display', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'


class CoursewithTasksSerializer(CourseSerializer):
    task = TaskSerializer(fields = ('id', 'name', 'description'), many=True)


class UserSerializer(DynamycSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserwithTasksSerializer(UserSerializer):
    tasks = TaskSerializer(fields = ('id', 'name', 'description'), many=True)


class UserwithCoursesSerializer(UserSerializer):
    courses = CourseSerializer(fields = ('id', 'name', 'created_by'), many=True)


class UserDailySerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many = True, queryset = User.objects.all())
    user = UserSerializer(fields = ('username', 'taskinday'))

    class Meta:
        model = UserDaily
        fields = '__all__'

class UserParamsSerializer(DynamycSerializer):
    user = UserSerializer(fields = ('username', 'age'))
    
    class Meta:
        model = UserParams
        fields = '__all__'


class UserCoursesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCourses
        fields = '__all__'


class UserTasksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserTasks
        fields = '__all__'


class TaskAnswerSerializer(serializers.ModelSerializer):
    usertask = UserTasksSerializer()

    class Meta:
        model = TaskAnswer
        fields = '__all__'


class UserCoursesTaskSerializer(serializers.ModelSerializer):
    usercourses = UserCoursesSerializer()

    class Meta:
        model = UserCoursesTasks
        fields = '__all__'


class UserCoursesTasksAnswerSerializer(serializers.ModelSerializer):
    uctask = UserCoursesTaskSerializer()

    class Meta:
        model = UserCoursesTasksAnswer
        fields = '__all__'


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('username', 'firstname', 'lastname', 'email', 'age', 'icon', 'taskinday')
    