from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    priority = models.SmallIntegerField()
    is_profile_disabled = models.BooleanField()
    #change password, reserveRoom, unreserve, attendClass/unattendClass, searchRooms, disableProfile, alert, timeTable
    #objects = models.Manager()  # to stop PyCharm warnings


class StudentSpeciality(models.Model):
    name = models.CharField(max_length=50, unique=True)
    """ - seed the DB
    APPLIED_MATHEMATICS = "Applied Mathematics"
    MATHEMATICS = "Mathematics"
    DATA_SCIENCE = "Data Science"
    STATISTICS = "Statistics"
    INFORMATICS = "Informatics"
    INFORMATION_SYSTEMS = "Information systems"
    COMPUTER_SCIENCE = "Computer science"
    SOFTWARE_ENGINEERING = "Software engineering" 
    """
    #objects = models.Manager()  # to stop PyCharm warnings


class Student(User):
    faculty_num = models.CharField(max_length=10)
    speciality = models.ForeignKey(
        StudentSpeciality,
        on_delete=models.RESTRICT,
        null=False,
        related_name="students"
    )
    is_in_charge_of_students_council_room = models.BooleanField(default=False)
    # function for taking up subject, taking off, finishing subject, rating subject/lesson,

    objects = models.Manager()  # to stop PyCharm warnings
