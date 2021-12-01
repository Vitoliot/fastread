from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import BrinIndex
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.utils.timezone import now
from django.core.validators import RegexValidator, _lazy_re_compile
from .validators import procent_validator
from django.core.exceptions import ObjectDoesNotExist

# validate_answers = RegexValidator(
#     _lazy_re_compile(r"/[^\.\,\-\_\'\"\@\?\!\:\$ a-zA-Z0-9А-Яа-я()]/u"),
#     ('Enter a valid value'),
#     'invalid')
class TaskType(models.Model):
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
    use_in_testing = models.BooleanField()


    def __str__(self):
        return self.name

class Task(models.Model):
    tasktypeid = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    task_text_name = models.CharField(max_length=300, blank=True)
    task_text = models.TextField(blank=True)
    task_text_icon = models.ImageField(blank=True, upload_to='task_icons/')

    class Meta:
        indexes = [
            BrinIndex(fields=['tasktypeid']),
        ]
    def __str__(self) -> str:
        return super().__str__()


class Questions(models.Model):
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=45, 
    # validators=[validate_answers,]
    )
    p_answer1 = models.CharField(max_length=45, blank=True)
    p_answer2 = models.CharField(max_length=45, blank=True)
    p_answer3 = models.CharField(max_length=45, blank=True)

    def __str__(self) -> str:
        return super().__str__()


class Course(models.Model):
    LOW = 1
    NORMAL = 2
    HIGH = 3
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
    task = models.ManyToManyField(Task, through='CourseTasks', through_fields=('course', 'task'),
                                  related_name='TaskCourse')

    def __str__(self) -> str:
        return super().__str__()


class CourseTasks(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()


class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, default=18)
    icon = models.ImageField(blank=True, upload_to='user_icons/')
    taskinday = models.PositiveIntegerField(choices=((5, 'LOW'), (7, 'NORMAL'), (9, 'HIGH')), default=5)

    courses = models.ManyToManyField(Course, through='UserCourses', through_fields=['user', 'course'])
    tasks = models.ManyToManyField(Task, through='UserTasks', through_fields=['user', 'task'])

    def __str__(self) -> str:
        return super().__str__()


class UserDaily(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    task_amount = models.PositiveIntegerField()
    date = models.DateField(default=now)

class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, default=0)
    is_complete = models.BooleanField(auto_created=True, default=False)

    def __str__(self) -> str:
        return super().__str__()


class UserParams(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    QER = models.PositiveIntegerField()
    WPM = models.PositiveIntegerField()
    text_proc = models.PositiveIntegerField(validators=[procent_validator])
    BOFI = models.PositiveIntegerField()
    VM = models.PositiveIntegerField()
    LM = models.PositiveIntegerField()
    Attention = models.PositiveIntegerField()
    measure_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return super().__str__()

def add_course(instance, **kwargs):
    WPM_list = [0, 100, 300, 500]
    BOFI_list = [0, 4, 7, 9]
    VMem_list = [0, 30, 50, 80]
    LMem_list = [0, 30, 50, 80]
    At_list = [0, ((15-5)*600)/15, ((15-3)*400)/15, ((15-1)*200)/15]
    WPM_par = BOFI_par = VMem_par = LMem_par = At_par = 0
    for level in range(1, 4): 
        WPM_par = level if WPM_list[level-1] < instance.WPM <= WPM_list[level] else WPM_par
        BOFI_par = level if BOFI_list[level-1] < instance.BOFI <= BOFI_list[level] else BOFI_par
        VMem_par = level if VMem_list[level-1] < instance.VM <= VMem_list[level] else VMem_par
        LMem_par = level if LMem_list[level-1] < instance.LM <= LMem_list[level] else LMem_par
        At_par = level if At_par < instance.Attention <= At_list[level] else At_par
        print(level, WPM_par, BOFI_par, VMem_par, LMem_par, At_par)
    # модернизировать
    courses = Course.objects.filter(
        WPM_par = WPM_par,
        BOFI_par = BOFI_par,
        VMem_par = VMem_par, 
        LMem_par = LMem_par, 
        At_par = At_par)
    if len(courses) > 1:
        # подобрать параметр разделения, либо предоставить юзеру выбор из курсов
        UserCourses(course = courses[0], user = instance.user).save()
    elif len(courses) == 1:
        UserCourses(course = courses[0], user = instance.user).save()
    else:
        print("Под ваши параметры не нашлось доступных курсов")


@receiver(post_save, sender = UserParams)
def add_course_to_user(sender, instance, **kwargs):
    print('add_course_to_user_is_work')
    try:
        courses = UserCourses.objects.get(user=instance.user, is_complete = False)
        if len(courses):
            print('Finish another course')
    except ObjectDoesNotExist:
        add_course(instance)


class TaskforAnswer(models.Model):
    wasted_time = models.FloatField(blank=True)
    date = models.DateField(default=now)
    correctness = models.PositiveIntegerField(default=0, blank=True, validators=[procent_validator])
    is_complete = models.BooleanField(auto_created=True, default=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()


class Answer(models.Model):
    ans_number = models.PositiveIntegerField()
    answer = models.CharField(max_length=45, 
    # validators=[validate_answers]
    )
    date = models.DateField(default=now)
    is_correct = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()


class UserTasks(TaskforAnswer):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, default=0)

    def __str__(self) -> str:
        return super().__str__()


class TaskAnswer(Answer):
    usertask = models.ForeignKey(UserTasks, on_delete=models.CASCADE)
    task_number = models.PositiveIntegerField()
    def __str__(self) -> str:
        return super().__str__()

@receiver(pre_save, sender = TaskAnswer)
def check_correctness_usertasks(sender, instance, **kwargs):
    print('check_correctness_usertasks is_work')
    print(instance)
    usertask = UserTasks.objects.get(id=instance.usertask.id)
    task = usertask.task
    questions = Questions.objects.filter(taskid = task)
    for question in questions:
        if question.number == instance.ans_number:
            if question.answer == instance.answer:
                instance.is_correct = True
    usertask.is_complete = True
    usertask.correctness = (1/len(questions))*100
    usertask.save()


class UserCoursesTasks(TaskforAnswer):
    usercourses = models.ForeignKey(UserCourses, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.PROTECT,default=1)

    def __str__(self) -> str:
        return super().__str__()


class UserCoursesTasksAnswer(Answer):
    uctask = models.ForeignKey(UserCoursesTasks, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()

@receiver(pre_save, sender = UserCoursesTasksAnswer)
def check_correctness_usercoursestasks(sender, instance, **kwargs):
    print('check_correctness_usercoursestasks is_work')
    uctask = UserCoursesTasks.objects.get(id=instance.uctask.id)
    task = uctask.task
    questions = Questions.objects.filter(taskid = task)
    for question in questions:
        if question.number == instance.ans_number:
            if question.answer == instance.answer:
                instance.is_correct = True
    uctask.is_complete = True
    uctask.correctness = (1/len(questions))*100
    uctask.save()