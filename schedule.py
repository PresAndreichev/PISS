import subject


class ViewedSubject(subject.Subject):
    """The class may be overkill, but I think it would give class Schedule managable and nice interface for the GUI"""

    def __init__(self, name, group, lecturer, ECTS_credits, lecture_type, study_times, raw_place,
                 can_be_signed_up_by_table, background_color, font_color, priority=None, ratings=None, reviews=None):
        super().__init__(name, group, lecturer, ECTS_credits, lecture_type, study_times, raw_place,
                         can_be_signed_up_by_table, ratings, reviews)
        self.__background_color = None
        self.set_background_color(background_color)
        self.__font_color = None
        self.set_font_color(font_color)
        self.__priority = None
        self.set_priority(priority)

    def get_background_color(self):
        return self.__background_color

    def get_font_color(self):
        return self.__font_color

    def get_priority(self):
        return self.__priority

    def set_background_color(self, color):
        color = color.lower()
        self.__background_color = color

    def set_font_color(self, color):
        color = color.lower()
        self.__font_color = color

    def set_priority(self, priority):
        if priority is None or priority < 0:
            self.__priority = 0
        else:
            self.__priority = priority

    def increment_priority(self):  # This may be a perfect situation to implement __methods__
        self.__priority += 1

    def decrement_priority(self):
        if self.__priority > 0:
            self.__priority -= 1

    def __lt__(self, other_subj):
        return self.__priority < other_subj.get_priority()

    # Equility breaks the logic of subject removal from schedule. No __eq__ for know

    def __le__(self, other_subj):
        return self.__priority <= other_subj.get_priority()


class Schedule:

    def __init__(self, overlaps_can_appear, regular_subjects=None, choosable_subjects=None):
        # dict of key<day>: value<dict>. The second dict consists of key<hour>: value<[subject]>
        self.__weekly_table = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                               'Saturday': {}, 'Sunday': {}}
        """the weekly_table has to be regenerated every time in order to guarantee the correctness of 
        the programme given subjects"""
        self.__overlaps_can_appear = None
        self.change_overlapping(overlaps_can_appear)
        self.__current_compulsory_subjects = []
        if regular_subjects is not None:
            for subj in regular_subjects:
                self.add_subject(subj)
        self.__current_choosable_subjects = []
        if choosable_subjects is not None:
            for subj in choosable_subjects:
                self.add_subject(subj)
        """overlaps should be dealt with from the programme by putting the highest 
        priority subject of given hour in the front of the list"""

    def get_weekly_table(self):
        return self.__weekly_table

    def change_overlapping(self, mode):
        if mode in ('yes', 'Yes', 'YES', 'true', 'True', 'TRUE'):
            self.__overlaps_can_appear = True
        else:
            self.__overlaps_can_appear = False

    def get_subjects_of_given_time(self, day, hour):
        try:
            subjects_of_this_hour = self.__weekly_table[day][hour]
        except KeyError:  # no subjects in this time period
            return []
        return subjects_of_this_hour  # will return a list of subjects or empty list

    def can_add_choosable_subj(self):
        return len(self.__current_choosable_subjects) < 5

    def add_subject(self, subj):
        if subj.get_subject_group() == 'COMPULSORY':
            try:
                self.__current_compulsory_subjects.index(subj)
            except ValueError:  # the value has not yet been added
                self.__current_compulsory_subjects.append(subj)
                self.__manipulate_subject_times(subj, 'add')
        else:
            if self.can_add_choosable_subj():
                try:
                    self.__current_choosable_subjects.index(subj)
                except ValueError:  # the value has not yet been added
                    self.__current_choosable_subjects.append(subj)
                    self.__manipulate_subject_times(subj, 'add')

    def __manipulate_subject_times(self, subj, mode):
        study_times = subj.get_study_times()
        for key, value in study_times.items():
            start_hour, end_hour = value
            while start_hour < end_hour:
                if mode == 'remove':
                    try:
                        self.__weekly_table[key][start_hour].remove(subj)  # no more cells have been added after this
                    except ValueError:
                        return
                else:  # we add subject
                    if self.__overlaps_can_appear:
                        if not self.get_subjects_of_given_time(key, start_hour):
                            self.__weekly_table[key][start_hour] = []
                        self.__weekly_table[key][start_hour].append(subj)
                    else:
                        if not self.get_subjects_of_given_time(key, start_hour):  # the list is empty
                            self.__weekly_table[key][start_hour] = []
                            self.__weekly_table[key][start_hour].append(subj)
                        else:  # there is already a subject there and no overlaps are allowed
                            self.__manipulate_subject_times(subj, 'remove')  # remove all the currently placed cells
                            return
                start_hour += 1

    def remove_subject(self, subj):
        if subj.get_subject_group() == 'COMPULSORY':
            return
        try:
            self.__current_choosable_subjects.remove(subj)
        except ValueError:
            return
        self.__manipulate_subject_times(subj, 'remove')

    def finish_subject(self, subj):
        # tick the study_plan
        if subj.get_subject_group() != 'COMPULSORY':
            self.remove_subject(subj)
        else:
            try:
                self.__current_compulsory_subjects.remove(subj)
            except ValueError:
                return
            self.__manipulate_subject_times(subj, 'remove')

    def generate_final_study_table(self):
        study_schedule = []
        for i in range(7):
            study_schedule.append([])  # creates a matrix of 7 rows(days)
            for j in range(17):  # offset from 7 to 24, 7 -> 0, 24 is not in the interval, so it will go [0, 16)
                study_schedule[i].append('EMPTY')  # for every hour in this day, add 'EMPTY' default val
        day_to_num = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thurdsay': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

        for day, daily_plan in self.__weekly_table.items():
            if not daily_plan:
                continue
            for hour, subjects in daily_plan.items():
                self.get_subjects_of_given_time(day, hour).sort(reverse=True)  # sort them in descending order. highest
                if self.get_subjects_of_given_time(day, hour):  # priority subject should be taken
                    curr_subj = self.get_subjects_of_given_time(day, hour)[0]
                    study_schedule[day_to_num[day]][hour - 7] = curr_subj
        return study_schedule

    # TODO read/write from files, export programme with Pillow
