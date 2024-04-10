from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_customer(self, username, full_name, password=None):
        user = self.model(username=username, full_name=full_name, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_professional(self, username, full_name, number_of_jobs, years_of_experience, password=None):
        user = self.model(username=username, full_name=full_name, number_of_jobs=number_of_jobs,
                          years_of_experience=years_of_experience)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Specialization(Enum):
    CONTRACTOR = 'contractor'
    ARCHITECT = 'architect'
    SUPERVISOR = 'supervisor'
    DESIGNER = 'interior designer'


class Customer(AbstractBaseUser):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['username']


class Professional(AbstractBaseUser):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    specialization = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Specialization])
    number_of_jobs = models.IntegerField()
    years_of_experience = models.IntegerField()
    is_available = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['username', 'specialization', 'number_of_jobs', 'years_of_experience']


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    specialization = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Specialization])
    num_question_special = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    answer_value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    objects = models.Manager()


class JobDetail(models.Model):
    job_name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()


class AnswerJob(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)
    jobDetail = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    answer_value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    objects = models.Manager()


class JobApproval(models.Model):
    job_detail = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    professional = models.ForeignKey('Professional', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    objects = models.Manager()
