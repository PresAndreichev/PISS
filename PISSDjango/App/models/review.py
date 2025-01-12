from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .user import User


class Review:
    reviewer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="reviews"
                                 )
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating should be between 1 and 5!"
    )
    as_anonymous = models.BooleanField(default=True)
    comment = models.TextField(null=True,
                               blank=True
                               )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # to stop PyCharm warnings


    class Meta:
        abstract = True


# Since Review is abstract, we should map it to 2 separate but correlated entities - RoomEventReview and SubjectReview

class RoomEventReview(Review):
    room_event = models.ForeignKey('RoomEvent',
                                   on_delete=models.CASCADE,
                                   related_name="reviews"
                                   )
    objects = models.Manager()  # to stop PyCharm warnings


class SubjectReview(Review):
    subject = models.ForeignKey('Subject',
                                on_delete=models.CASCADE,
                                related_name="reviews"
                                )
    # objects = models.Manager()  # to stop PyCharm warnings
