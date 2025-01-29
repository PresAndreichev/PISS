from django.contrib import admin
from .models import User, Floor, RoomEventReview, SubjectReview, Room, LectureType, RoomEvent, LessonEvent, SubjectGroup, Subject, Student
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'priority', 'is_profile_disabled')

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')
"""
@admin.register(RoomEventReview)
class RoomEventReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'as_anonymous', 'rating', 'comment','created_at', 'room_event')

@admin.register(SubjectReview)
class SubjectReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'as_anonymous', 'rating', 'comment','created_at', 'subject')
"""
@admin.register(Room) 
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'floor', 'seats', 'characteristics')

@admin.register(LectureType)
class LectureTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')

@admin.register(RoomEvent)
class RoomEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'topic', 'room', 'date', 'start_time', 'end_time' )

@admin.register(LessonEvent)
class LessonEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'topic', 'room', 'date', 'start_time', 'end_time','lecture_type', 'subject')

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject_group','ects_credits','weekly_lectures_duration','weekly_exercises_duration','weekly_computer_exercises_duration')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('faculty_num',)


