import schedule
import study_plan
import subject
import os

class InvalidPassword(subject.InvalidInput):
    pass


class InvalidFacultyNum(subject.InvalidInput):
    pass


class DoubletFacultyNum(subject.InvalidInput):
    pass


def is_valid_password(password):
    if len(password) < 8:
        return False
    small_chars_count = 0
    big_chars_count = 0
    digits_count = 0
    for char in password:
        if char.islower():
            small_chars_count += 1
        elif char.isupper():
            big_chars_count += 1
        elif char.isdigit():
            digits_count += 1
    return digits_count >= 1 and small_chars_count >= 1 and big_chars_count >= 1

class Student:
    __OLD_FN_LEN = 5
    __NEW_FN_LEN = 10  # For example 7MI0600129. Note: The 5th digit contains info for the speciality of the student

    def __init__(self, name, last_name, faculty_num, password, overlaps_can_appear, semester, speciality,
                 taken_regular_subjects=None, freely_chosen_subjects_table=None, min_credits_needed=None,
                 taken_free_subjects=None, regular_subjects=None, choosable_subjects=None):
        raw_name = name + ' ' + last_name
        self.name = None
        if subject.is_valid_person_name(raw_name):
            self.name = name
            self.last_name = last_name
        else:
            raise subject.InvalidPersonName
        self.password = None
        if is_valid_password(password):
            self.password = password
        else:
            raise InvalidPassword
        self.semester = semester
        self.speciality = speciality
        # NB parse reading from files here and maybe read these subjects more properly
        self.study_plan = study_plan.StudyPlan(self.speciality, self.semester, taken_regular_subjects,
                    freely_chosen_subjects_table, min_credits_needed, taken_free_subjects)
        self.weekly_schedule = schedule.Schedule(overlaps_can_appear, regular_subjects, choosable_subjects)

    def create_subject(self, subj):
        subj_name = subj.get_subject_name
        subj_lecturer = subj.get_lecturer
        duplicate_found = False
        with open('all_subjects.txt', 'r') as input_file:
            for line in input_file:
                curr_name, curr_lecturer = line.split(',')
                if [subj_name, subj_lecturer] == [curr_name, curr_lecturer]:
                    duplicate_found = True
                    print('Duplicate subject. You cannot add this one, sorry\n!')
                    break
            if not duplicate_found:
                print('Creating successfully new subject!\n')
                with open('all_subjects.txt', 'a') as output_file:
                    output_file.write(subj_name + ',' + subj_lecturer)
                subj.save_info_to_file()

    def destroy_subject(self, subj_name, lecturer):
        searching_for = subj_name + ',' + lecturer
        with open("all_subjects.txt", "r") as f:
            lines = f.readlines()
        with open("all_subjects.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != searching_for:
                    f.write(line)
        os.remove(searching_for + ".txt")

    def take_up_subject(self, subj_name, lecturer):
        searching_for = subj_name + ',' + lecturer
        info = subject.get_info_from_file(searching_for)
        my_subj = subject.Subject(*info)
        self.weekly_schedule.add_subject(my_subj)

    def take_off_subject(self, subj_name, lecturer):
        searching_for = subj_name + ',' + lecturer
        info = subject.get_info_from_file(searching_for)
        my_subj = subject.Subject(*info)
        self.weekly_schedule.remove_subject(my_subj)

    def finish_subject(self, subj_name, lecturer):
        searching_for = subj_name + ',' + lecturer
        info = subject.get_info_from_file(searching_for)
        my_subj = subject.Subject(*info)
        self.weekly_schedule.finish_subject(my_subj)
        self.study_plan.finish_subject(my_subj)

    def rate_subject(self, subj_name, lecturer, score):
        if subj_name not in self.study_plan.taken_subjects():
            return
        searching_for = subj_name + ',' + lecturer
        info = subject.get_info_from_file(searching_for)
        my_subj = subject.Subject(*info)
        score = int(score)
        my_subj.get_subject_rating().add_score(score)
        my_subj.save_info_to_file()

    def comment_subject(self, subj_name, lecturer, comment):
        if subj_name not in self.study_plan.taken_subjects():
            return
        searching_for = subj_name + ',' + lecturer
        info = subject.get_info_from_file(searching_for)
        my_subj = subject.Subject(*info)
        my_subj.add_review(comment)
        my_subj.save_info_to_file()

    def change_overlapping(self, overlap_mode):
        self.weekly_schedule.change_overlapping(overlap_mode)

    # TODO write to file

