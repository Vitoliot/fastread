from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import BrinIndex
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.utils.timezone import now
from django.core.validators import validate_unicode_slug
from .validators import procent_validator

# добавить класс TaskType и связать с ним Task связью один ко многим и дописать сериализаторы

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
    task_text = models.TextField(blank=True)

    class Meta:
        indexes = [
            BrinIndex(fields=['tasktypeid']),
        ]
    def __str__(self) -> str:
        return super().__str__()


class Questions(models.Model):
    qid = models.PositiveIntegerField(primary_key=True, default=1)
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)
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
    task = models.ManyToManyField(Task, through='CourseTasks', through_fields=('course', 'task'),
                                  related_name='TaskCourse')

    def __str__(self) -> str:
        return super().__str__()


class CourseTasks(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)
    task = models.ForeignKey(Task, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self) -> str:
        return super().__str__()


class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, default=18)
    icon = models.ImageField(blank=True, upload_to='flashread/static/images')
    taskinday = models.PositiveIntegerField(choices=((5, 'LOW'), (7, 'NORMAL'), (9, 'HIGH')), default=5)

    # REQUIRED_FIELDS = [
    #     'email', 'icon'
    # ]

    courses = models.ManyToManyField(Course, through='UserCourses', through_fields=['user', 'course'])
    tasks = models.ManyToManyField(Task, through='UserTasks', through_fields=['user', 'task'])

    def __str__(self) -> str:
        return super().__str__()


# u = get_user_model()


class UserDaily(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, primary_key=True, unique=False)
    task_amount = models.PositiveIntegerField()
    # correctness_of_answers = models.PositiveIntegerField(blank=True, validators=[procent_validator])
    date = models.DateField(default=now)


class UserParams(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, primary_key=True, unique=False)
    idparams = models.PositiveIntegerField()
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
    # @staticmethod
    # def post_save(sender, **kwargs):
    #     instance = kwargs.get('instance')
    #     created = kwargs.get('created')
    #     if instance.previous_state != instance.state or created:
    #         pass

# @receiver(post_save, sender = UserParams)
# def add_course_to_user(sender, instance, **kwargs):
#     usid = instance.user
    # WPM_list = [0, 300, 500]
    # BOFI_list = []
    # VMem_list = []
    # LMem_list = []
    # At_list = []
    # WPM_par = WPM_par
    # BOFI_par = BOFI_par
    # VMem_par = VMem_par
    # LMem_par = LMem_par
    # At_par = At_par
    # courses = Course.objects.filter(
    #     WPM_par = WPM_par,
    #     BOFI_par = BOFI_par,
    #     VMem_par = VMem_par, 
    #     LMem_par = LMem_par, 
    #     At_par = At_par)

class TaskforAnswer(models.Model):
    wasted_time = models.FloatField(blank=True)
    date = models.DateField(default=now)
    correctness = models.PositiveIntegerField(blank=True, validators=[procent_validator])

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()


class Answer(models.Model):
    ans_number = models.PositiveIntegerField()
    answer = models.CharField(max_length=45, validators=[validate_unicode_slug])
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
    usertask = models.ForeignKey(UserTasks, on_delete=models.CASCADE, primary_key=True, unique=False)
    task_number = models.PositiveIntegerField()
    def __str__(self) -> str:
        return super().__str__()

@receiver(pre_save, sender = TaskAnswer)
def check_correctness_usertasks(sender, instance, **kwargs):
    usertask = UserTasks.objects.get(id=instance.usertask)
    task = usertask.task
    questions = Questions.objects.filter(taskid = task)
    for question in questions:
        if question.number == instance.ans_number:
            if question.answer == instance.answer:
                instance.update(is_correct = True)
    usertask.update(is_complete = True)
    usertask.update(correctness = usertask.correctness + (1/len(questions))*100)
    usertask.save()
    # instance.save()


class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, default=0)

    def __str__(self) -> str:
        return super().__str__()


class UserCoursesTasks(TaskforAnswer):
    usercourses = models.ForeignKey(UserCourses, on_delete=models.CASCADE, primary_key=True, unique=False)
    task = models.ForeignKey(Task, on_delete=models.PROTECT,default=1)
    is_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return super().__str__()


class UserCoursesTasksAnswer(Answer):
    uctask = models.ForeignKey(UserCoursesTasks, on_delete=models.CASCADE, primary_key=True, unique=False)

    def __str__(self) -> str:
        return super().__str__()

@receiver(pre_save, sender = UserCoursesTasksAnswer)
def check_correctness_usercoursestasks(sender, instance, **kwargs):
    uctask = UserCoursesTasks.objects.get(id=instance.uctask)
    task = uctask.task
    questions = Questions.objects.filter(taskid = task)
    for question in questions:
        if question.number == instance.ans_number:
            if question.answer == instance.answer:
                instance.update(is_correct = True)
    uctask.update(is_complete = True)
    uctask.update(correctness = uctask.correctness + (1/len(questions))*100)
    uctask.save()
    # instance.save()