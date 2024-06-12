from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone


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
    average_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    objects = UserManager()

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['username', 'specialization', 'number_of_jobs', 'years_of_experience']

    def update_average_rating(self, new_rating):
        total_ratings = self.number_of_jobs
        current_total_rating = self.average_rating * total_ratings
        new_total_rating = current_total_rating + new_rating
        new_average_rating = new_total_rating / (
                total_ratings + 1)  # Incrementing total_ratings by 1 for the new rating
        self.average_rating = new_average_rating
        self.number_of_jobs += 1
        self.save()


    def money_for_pro(self, budget, listOfSp):
        for pro in listOfSp:
            if self.specialization == pro:
                index = listOfSp.index(pro)
                if index == 0:
                    return budget * Decimal('0.5')
                elif index == 1:
                    return budget * Decimal('0.3')
                elif index == 2:
                    return budget * Decimal('0.1')
                elif index == 3:
                    return budget * Decimal('0.1')
        return Decimal('0')


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
    detail_of_project = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    project_ended = models.BooleanField(default=False)
    objects = models.Manager()

    def check_project_status(self):
        if self.end_time and timezone.now() > self.end_time:
            self.project_ended = True
        else:
            self.project_ended = False
        self.save()

    def determine_professional_priority(self, total_score):
        if total_score > 75:
            return ['CONTRACTOR', 'ARCHITECT', 'SUPERVISOR', 'DESIGNER']
        elif 50 < total_score <= 75:
            return ['ARCHITECT', 'CONTRACTOR', 'SUPERVISOR', 'DESIGNER']
        elif 30 < total_score <= 50:
            return ['SUPERVISOR', 'ARCHITECT', 'CONTRACTOR', 'DESIGNER']
        else:
            return ['DESIGNER', 'SUPERVISOR', 'ARCHITECT', 'CONTRACTOR']


class AnswerJob(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)
    jobDetail = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    answer_value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    objects = models.Manager()


class JobApproval(models.Model):
    job_detail = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    professional = models.ForeignKey('Professional', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    contract_approved = models.BooleanField(default=False)

    objects = models.Manager()
