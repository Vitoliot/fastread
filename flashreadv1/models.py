from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import BrinIndex
from django.utils.timezone import now
from django.core.validators import validate_unicode_slug

class Task(models.Model):
    type_choices = (
        (1, 'текстовое задание'),
        (2, 'задание с картинкой'),
        (3, 'другое')
    )
    theme_choices = (
        (1, 'Избавление от проговаривания'),
        (2, 'Схватывание и нахождение информации'),
        (3, 'Работа с текстом'),
        (4, 'Широта зрения'),
        (5, 'Зрительная память'),
        (6, 'Логическая память'),
        (7, 'Внимание'),
        (8, 'Регрессии'),
    )
    name = models.CharField(max_length=45, unique=True)
    type = models.PositiveIntegerField(choices=type_choices, )
    theme = models.PositiveIntegerField(choices=theme_choices)
    description = models.CharField(max_length=100, blank=True)
    task_text = models.TextField(blank=True)
    use_in_testing = models.BooleanField()

    class Meta:
        indexes = [
            BrinIndex(fields=['name']),
        ]
    def __str__(self):
        return self.name


class Question(models.Model):
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE, primary_key=True, unique=False)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=45, validators=[validate_unicode_slug])
    p_answer1 = models.CharField(max_length=45, blank=True)
    p_answer2 = models.CharField(max_length=45, blank=True)
    p_answer3 = models.CharField(max_length=45, blank=True)
    def __str__(self) -> str:
        return super().__str__()


class Course(models.Model):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    PARAMS_CHOICES = (
    (LOW, 'Low'),
    (NORMAL, 'Normal'),
    (HIGH, 'High'),
    )

    name = models.CharField(max_length=45, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_creation = models.DateField(default=now)
    WPM_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    BOFI_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    VMem_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    LMem_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    At_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    task = models.ManyToManyField(Task, through='CourseTasks', through_fields=('idcourse', 'idtask'), related_name='TaskCourse')

    def __str__(self) -> str:
        return super().__str__()

class CourseTasks(models.Model):
    idcourse = models.ForeignKey(Course, on_delete=models.CASCADE)
    idtask = models.ForeignKey(Task, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self) -> str:
        return super().__str__()

class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, default=18)
    icon = models.ImageField(blank=True, upload_to='flashread/static/images')
    REQUIRED_FIELDS = [
        'email', 'icon'
    ]
    courses = models.ManyToManyField(Course, through='UserCourses', through_fields=['iduser', 'idcourse'])
    tasks = models.ManyToManyField(Task, through='UserTasks', through_fields=['iduser', 'idtask'])

    def __str__(self) -> str:
        return super().__str__()

u = get_user_model()

class UserParams(models.Model):
    iduser = models.ForeignKey(User, on_delete=models.PROTECT, primary_key=True, unique=False)
    idparams = models.PositiveIntegerField()
    QER = models.PositiveIntegerField()
    WPM = models.PositiveIntegerField()
    text_proc = models.PositiveIntegerField()
    BOFI = models.PositiveIntegerField()
    VM = models.PositiveIntegerField()
    LM = models.PositiveIntegerField()
    Attention = models.PositiveIntegerField()
    measure_date = models.DateTimeField(default=now)
    
    def __str__(self) -> str:
        return super().__str__()


class TaskforAnswer(models.Model):
    wasted_time = models.FloatField(blank=True)
    date = models.DateField(default=now)
    correctness = models.PositiveIntegerField(blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()


class Answer(models.Model):
    ans_number = models.PositiveIntegerField()
    answer = models.CharField(max_length=45, validators=[validate_unicode_slug]) 
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()


class UserTasks(TaskforAnswer):
    iduser = models.ForeignKey(User, on_delete=models.CASCADE)
    idtask = models.ForeignKey(Task, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return super().__str__()


class TaskAnswer(Answer):
    idusertask = models.ForeignKey(UserTasks, on_delete=models.CASCADE, primary_key=True, unique=False)

    def __str__(self) -> str:
        return super().__str__()


class UserCourses(models.Model):
    iduser = models.ForeignKey(User, on_delete=models.CASCADE)
    idcourse = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return super().__str__()


class UserCoursesTasks(TaskforAnswer):
    idusercourses = models.ForeignKey(UserCourses, on_delete=models.CASCADE, primary_key=True, unique=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return super().__str__()


class UserCoursesTasksAnswer(Answer):
    iductask = models.ForeignKey(UserCoursesTasks, on_delete=models.CASCADE, primary_key=True, unique=False)
    
    def __str__(self) -> str:
        return super().__str__()