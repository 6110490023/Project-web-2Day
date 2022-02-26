from django.db import models

# Create your models here.
class Teacher(models.Model):
     User_id = models.CharField(max_length = 64)
     username = models.CharField(max_length = 64)
     firstname = models.CharField(max_length = 64)
     lastname = models.CharField(max_length = 64)
     sex = models.CharField(max_length = 64)
     age = models.PositiveIntegerField()
     subject = models.CharField(max_length = 64)

class Student(models.Model):
     User_id = models.CharField(max_length = 64)
     username = models.CharField(max_length = 64)
     firstname = models.CharField(max_length = 64)
     lastname = models.CharField(max_length = 64)
     sex = models.CharField(max_length = 64)
     age = models.PositiveIntegerField()
     class_number = models.PositiveIntegerField()
     room = models.PositiveIntegerField()


class Couse(models.Model):
     Cousename = models.CharField(max_length = 64)
     teacher = models.CharField(max_length = 64)