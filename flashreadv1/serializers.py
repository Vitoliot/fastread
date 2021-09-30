from django.db.models import fields
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from .models import *

# User
# UserParams
# UserCourses
# UserCoursesTasks
# UserCoursesTasksAnswer
# UserTasks
# Task - v
# TaskAnswer
# Question - v
# Course - v
# CourseTasks - v


# class FullTaskSerializer(serializers):
#     pass

class DynaminSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynaminSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TaskSerializer(DynaminSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'

# class TaskSerializerForMany(serializers.ModelSerializer):
    
#     class Meta:
#         model = Task
#         fields = ['id', 'name']

class QuiestionSerializer(serializers.ModelSerializer):
    task = TaskSerializer(fields = ('id', 'name'))
    class Meta:
        model = Question
        fields = '__all__'

class CourseSerializer(DynaminSerializer):
    
    WPM_par = serializers.CharField(source='get_WPM_par_display', read_only=True)
    BOFI_par = serializers.CharField(source='get_BOFI_par_display', read_only=True)
    VMem_par = serializers.CharField(source='get_VMem_par_display', read_only=True)
    LMem_par = serializers.CharField(source='get_LMem_par_display', read_only=True)
    At_par = serializers.CharField(source='get_At_par_display', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

# class CourseSerializerForMany(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['id', 'name', 'task']


class CoursewithTasksSerializer(serializers.ModelSerializer):
    task = TaskSerializer(fields = ('id', 'name', 'description'), many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'task']


class CourseTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseTasks
        fields = '__all__'

# class User

# class CourseSerializerForMany2(serializers.ModelSerializer):
#     Course_set = TaskSerializer(many=True)
#     class Meta:
#         model = Course
#         fields = ['id', 'name', 'Course_set']


# class CourseTasksSerializer(serializers.ModelSerializer):
#     course = CourseSerializerForMany()
#     task = TaskSerializerForMany()

# class TaskSerializer2(serializers.ModelSerializer):
#     CCCCCCCC = CourseSerializerForMany(many=True)

#     class Meta:
#         model = Task
#         fields = '__all__'