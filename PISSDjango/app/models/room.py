from django.db import models


class Room(models.Model):
    number = models.IntegerField()  # could be string
    characteristics = models.PositiveSmallIntegerField()
    seats = models.PositiveIntegerField()
    floor = models.ForeignKey('Floor',
                              on_delete=models.CASCADE,
                              related_name="rooms"
                              )
    objects = models.Manager()  # to stop PyCharm warnings

    def __bit_is_as_expected(self, binary_bit_to_check):
        CONVERTED_TO_INT_BINARY = int(binary_bit_to_check, 2)
        return self.characteristics & CONVERTED_TO_INT_BINARY == CONVERTED_TO_INT_BINARY

    def is_computer_room(self):
        IS_PC_ROOM_BIT = '0b1'
        return self.__bit_is_as_expected(IS_PC_ROOM_BIT)

    def has_white_board(self):
        HAS_WHITE_BOARD_BIT = '0b10'
        return self.__bit_is_as_expected(HAS_WHITE_BOARD_BIT)

    def has_black_board(self):
        HAS_BLACK_BOARD_BIT = '0b100'
        return self.__bit_is_as_expected(HAS_BLACK_BOARD_BIT)

    def has_interactive_board(self):
        HAS_INTERACTIVE_BOARD_BIT = '0b1000'
        return self.__bit_is_as_expected(HAS_INTERACTIVE_BOARD_BIT)

    def has_media(self):
        HAS_MEDIA_BIT = '0b10000'
        return self.__bit_is_as_expected(HAS_MEDIA_BIT)

    def is_class_running(self):
        IS_CLASS_RUNNING_BIT = '0b100000'
        return self.__bit_is_as_expected(IS_CLASS_RUNNING_BIT)

    def is_locked(self):
        IS_LOCKED_BIT = '0b1000000'
        return self.__bit_is_as_expected(IS_LOCKED_BIT)

    def does_function(self):
        DOES_FUNCTION_BIT = '0b10000000'
        return self.__bit_is_as_expected(DOES_FUNCTION_BIT)

    # isReservedTime da se napravi zaedno s generateTimeTable
