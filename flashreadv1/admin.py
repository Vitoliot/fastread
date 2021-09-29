from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserParams)
admin.site.register(UserCourses)
admin.site.register(UserCoursesTasks)
admin.site.register(UserCoursesTasksAnswer)
admin.site.register(UserTasks)
admin.site.register(Task)
admin.site.register(TaskAnswer)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(CourseTasks)

