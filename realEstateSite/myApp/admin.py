from django.contrib import admin

# Register your models here.
from .models import Customer, Professional, Answer, JobDetail, JobApproval, Question, AnswerJob

admin.site.register(Customer)
admin.site.register(Professional)
admin.site.register(Answer)
admin.site.register(JobDetail)
admin.site.register(JobApproval)
admin.site.register(Question)
admin.site.register(AnswerJob)
