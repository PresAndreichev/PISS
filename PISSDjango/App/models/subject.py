from django.db import models
from .user import User


class SubjectGroup(models.TextChoices):
    name = models.CharField(max_length=50, unique=True)
    """ - seed the db later
    MATH = 'MATH'
    APPLIED_MATH = 'APM'
    CSF = 'COMP_SCIENCE_FUNDAMENTALS'
    CSC = 'COMP_SCIENCE_CORE'
    CSP = 'COMP_SCIENCE_PRACTICUM'
    COMPULSORY = 'COMPULSORY'
    REQUIRED_CHOSEN = 'REQUIRED_CHOSEN'
    OTHER = 'OTHER'
    """


class Subject(models.Model):
    name = models.CharField(max_length=255)
    subject_group = models.ForeignKey(
        SubjectGroup,
        on_delete=models.RESTRICT,
        related_name="subjects"
    )
    lecturers = models.ManyToManyField(
        User,
        related_name="subjects"
    )
    ects_credits = models.FloatField()
    weekly_lectures_duration = models.PositiveSmallIntegerField()
    weekly_exercises_duration = models.PositiveSmallIntegerField()
    weekly_computer_exercises_duration = models.PositiveSmallIntegerField()