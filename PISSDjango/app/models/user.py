from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    priority = models.SmallIntegerField()
    is_profile_disabled = models.BooleanField()

    def __str__(self):
        return self.username + self.password
    #change password, reserveRoom, unreserve, attendClass/unattendClass, searchRooms, disableProfile, alert, timeTable
    #objects = models.Manager()  # to stop PyCharm warnings



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    faculty_num = models.CharField(max_length=10)
    #faculty_num = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Student: {self.user.username} (Faculty No: {self.faculty_num})"
