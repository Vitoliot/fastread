from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone

# дописать валидаторы и индексы
class Task(models.Model):
    type_choices = (
        'текстовое задание',
        'задание с картинкой',
        'другое'
    )
    theme_choices = (
        'Избавление от проговаривания',
        'Схватывание и нахождение информации',
        'Работа с текстом',
        'Широта зрения',
        'Зрительная память',
        'Логическая память',
        'Внимание',
        'Регрессии',
    )
    name = models.CharField(max_length=45, unique=True)
    type = models.CharField(max_length=45, choices=type_choices)
    theme = models.CharField(max_length=45, choices=theme_choices)
    desription = models.CharField(max_length=100, blank=True)
    task_text = models.TextField(blank=True)
    use_in_testing = models.BooleanField()

    class Meta:
        indexes = (
            BrinIndex(fields=['name'])
        )
    def __str__(self):
        return self.name


class Question(models.Model):
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE, primary_key=True)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=45)
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
    date_of_creation = models.DateField(default=timezone.now)
    WPM_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    BOFI_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    VMem_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    LMem_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)
    At_par = models.IntegerField(choices=PARAMS_CHOICES, default=LOW)


class CourseTasks(models.Model):
    idcourse = models.ManyToManyField('Course', on_delete = models.DELETE)
    idtask = models.ManyToManyField('Task', on_delete = models.PROTECT)


class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True)
    icon = models.ImageField(blank=True)
    REQUIRED_FIELDS = [
        'email', 'first_name', 'last_name', 'icon'
    ]


u = get_user_model()

class UserParams(models.Model):
    iduser = models.ForeignKey(User, on_delete=models.PROTECT, primary_key=True)
    idparams = models.PositiveIntegerField()
    QER = models.PositiveIntegerField()
    WPM = models.PositiveIntegerField()
    text_proc = models.PositiveIntegerField()
    BOFI = models.PositiveIntegerField()
    VM = models.PositiveIntegerField()
    LM = models.PositiveIntegerField()
    Attention = models.PositiveIntegerField()
    measure_date = models.DateTimeField(default=timezone.now)


class TaskforAnser(models.Model):
    wasted_time = models.FloatField(blank=True)
    date = models.DateField(default=timezone.now)
    correctness = models.PositiveIntegerField(blank=True)


class Answer(models.Model):
    ans_number = models.PositiveIntegerField()
    answer = models.CharField(max_length=45)


class UserTasks(TaskforAnser):
    iduser = models.ManyToManyField(User, on_delete = models.PROTECT, primary_key=True)
    idtask = models.ManyToManyField(Task, on_delete = models.PROTECT, primary_key=True)


class TaskAnswer(Answer):
    idusertask = models.ForeignKey(UserTasks, on_delete=models.CASCADE, primary_key=True)


class UserCourses(models.Model):
    iduser = models.ManyToManyField(User, on_delete = models.Protect, primary_key=True)
    idcourse = models.ManyToManyField(Course, on_delete = models.Protect, primary_key=True)


class UserCoursesTasks(TaskforAnser):
    idusercourses = models.ForeignKey(UserCourses, on_delete=models.CASCADE, primary_key=True)
    is_complete = models.BooleanField(default=False)


class UserCoursesTasksAnswer(Answer):
    iductask = models.ForeignKey(UserCoursesTasks, on_delete=models.CASCADE, primary_key=True)