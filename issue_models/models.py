from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class user_table(models.Model):

    emailadd = models.EmailField(max_length=75 ,primary_key=True)
    password=models.CharField(max_length=30)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)




# class new_project(models.Model):
#
#     emailadd=models.ForeignKey(user_table)
#     projtitle=models.CharField(max_length=30 ,primary_key=True)
#     description=models.CharField(max_length=500)
#
#
#
# class projects_member(models.Model):
#     projtitle=models.ForeignKey(new_project)
#     emailadd=models.ForeignKey(user_table)



# #class stories(models.Model):
#     projtitle=models.ForeignKey(new_project)
#     emailadd=models.ForeignKey(user_table)
#     storytitle=models.CharField(max_length=50)
#     description=models.CharField(max_length=500)
#     assignee = models.ForeignKey(user_table)
#     estimate=models.IntegerField("in hours")
#     status_choice=(
#         ('strtd','started'),
#         ('finsh','finished'),
#         ('deliv','delivered')
#     )
#     status=models.CharField(max_length=5,choices=status_choice)
#     scheduled_choice=(
#         ('ys','yes'),
#         ('no','no')
#     )
#     scheduled=models.CharField(max_length=2,choices=scheduled_choice)
#     visibilty=models.BooleanField(default=True)
