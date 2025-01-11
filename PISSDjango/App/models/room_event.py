from django.db import models
from .user import User
from datetime import date


class LectureType(models.Model):
    type = models.CharField(max_length=30, unique=True)
    """
    LECTURE = 'LECTURE'
    THEORETICAL_EXERCISE = 'THEORETICAL_EXERCISE'
    COMPUTER_PRACTICUM_EXERCISE = 'COMPUTER_PRACTICUM_EXERCISE'
    """
    objects = models.Manager()  # to stop PyCharm warnings


class RoomEvent(models.Model):
    host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # a meeting could be without a host (students group project's meeting)
        null=True,
        related_name="hosted_events"
    )
    topic = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name="events"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendees = models.ManyToManyField(
        User,
        related_name="attended_events",
        blank=True
    )
    objects = models.Manager()  # to stop PyCharm warnings

    def get_day_of_week(self):
        if not self.date:
            raise ValueError("Date field is not set.")
        assert isinstance(self.date, date)  # PyCharm is unhappy if there is no assert guarantee
        return self.date.strftime('%A')

    class Meta:  # Will order the events of a room based on date and then start time
        ordering = ['date', 'start_time']


class LessonEvent(RoomEvent):  # Will connect a single event to a subject and a lecture type
    lecture_type = models.ForeignKey(
        LectureType,
        on_delete=models.SET_NULL,
        related_name="lesson_events"
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='lesson_events'  # Based on this we call the object(Subject).<related_name>(lesson_events)
        # to get the models from DB
    )
    objects = models.Manager()  # to stop PyCharm warnings
