from django.db import models


class Floor(models.Model):
    number = models.SmallIntegerField(unique=True)
    # note that we only have to declare the relationship many to one with room once!
    # Manipulate rooms based on user!!
    objects = models.Manager()  # to stop PyCharm warnings
