import subject


# NB! Copying a collection by traversing creates a copy for the individual. Directly passing with =, gives the ptr
class SelectableSubjects:
    def __init__(self, required_selectable_subjects, freely_chosen_subjects_table, min_credits_needed,
                 person_finished_subjects=None):
        self.__required_selectable_subjects = required_selectable_subjects
        # Count a category as passed if its value is equal or less than 0
        self.__freely_chosen_subjects_categories = {}
        for key, value in freely_chosen_subjects_table.items():
            self.__freely_chosen_subjects_categories[key] = value
        self.__left_credits = min_credits_needed
        self.__person_finished_subjects = {}  # Dict of subjects<string>/tuple<category<str>,credits<doubles>> the person has finished
        if person_finished_subjects is not None:
            self.__person_finished_subjects = person_finished_subjects

    def __transfer_category_point(self, child_category, parent_category):
        while self.__freely_chosen_subjects_categories[child_category] < 0:
            self.__freely_chosen_subjects_categories[parent_category] -= 1
            self.__freely_chosen_subjects_categories[child_category] += 1

    def finish_subject(self, subj):
        subj_name = subj.get_subject_name()
        subj_group = subj.get_subject_group()
        """Clear a subject of its category. If it is already cleared, then clear its parent class(MATH/ COMP). 
                    If it also has been cleared, then subtract/clear the subject score from FREELY."""
        if subj_name in self.__person_finished_subjects:
            return  # The subject has already been cleared

        if subj_name in self.__required_selectable_subjects:
            subj_group = 'REQUIRED_CHOSEN'
            subj.set_subject_group(subj_group)
            self.__freely_chosen_subjects_categories[subj_group] -= 1
            self.__transfer_category_point('REQUIRED_CHOSEN', 'FREELY')

        elif subj_group in subject.SubjectGroup[2::]:
            if subj_group == 'OTHER':
                subj_group = 'FREELY'
            self.__freely_chosen_subjects_categories[subj_group] -= 1
            if subj_group in ('PURE_MATH', 'APM'):
                self.__transfer_category_point(subj_group, 'MATH')
                self.__transfer_category_point('MATH', 'FREELY')
            elif subj_group in ('CSF', 'CSC'):
                self.__transfer_category_point(subj_group, 'COMP')
                self.__transfer_category_point('COMP', 'FREELY')
            elif subj_group in ('CSP', 'REQUIRED_CHOSEN'):  # Just else would make an infinite loop of freely to freely
                self.__transfer_category_point(subj_group, 'FREELY')

        else:  # the subject group is not valid
            raise subject.InvalidSubjectGroup

        self.__left_credits -= subj.get_ECTS_credits()
        self.__person_finished_subjects[subj_name] = subj.get_ECTS_credits()

    def get_required_subject(self):
        return self.__required_selectable_subjects

    def get_freely_chosen_subjects_categories(self):
        return self.__freely_chosen_subjects_categories

    def get_remaining_credits_balance(self):
        return self.__left_credits

    def get_persons_finished_subjects(self):
        return self.__person_finished_subjects

    def every_category_is_cleared(self):
        for key, value in self.__freely_chosen_subjects_categories.items():
            if value > 0:
                return False
        return True

    def everything_is_cleared(self):  # If every discipline is cleared, together with summed credits passed
        return self.every_category_is_cleared() and self.__left_credits <= 0


DefaultRegularPlan_SI = (
    ('Algebra', 'Calculus 1', 'English', 'Discrete structures 1', 'Introduction to programming'),
    ('Geometry', 'Calculus 2', 'Computer english', 'Discrete structures 2', 'Object-oriented programming'),
    ('Computer architectures', 'Introduction to software engineering', 'Communication skills',
     'Data structures and algorithms'),
    ('Databases', 'Economics of software engineering', 'Software architectures and software development',
     'Computer networks', 'Operation systems', 'Differential equations and applications'),
    ('XML technologies for semantic web', 'Social aspects of IT', 'Statistics and empirical methods',
     'Quality assurance'),
    ('Web technologies', 'Requirements engineering', 'Design of human machine interface',
     'Distributed software architectures'),
    ('Data Mining', 'Design and integration of software systems', 'Projects management')
)

DefaultRegularPlan_IS = (
    ('Algebra', 'Calculus 1', 'Discrete structures', 'Introduction to programming'),
    ('Geometry', 'Calculus 2', 'Functional programming', 'Object-oriented programming',
     'Information systems basics 1'),
    ('Computer architectures', 'English 1', 'Information systems basics 2', 'Data structures',
     'Information systems - theory and practice'),
    ('Databases', 'English 2', 'Applied object-oriented programming 1', 'Computer networks',
     'Statistics and empirical methods'),
    ('XML technologies', 'Databases management systems', 'Systems based on knowledge', 'Specialized english',
     'Communication skills and teamwork'),
    ('Web technologies', 'Analysis and design of information systems', 'Distributed IT architectures'),
    ('E-Business systems', 'Projects management', 'Information security fundamentals')
)

DefaultRegularPlan_KN = (
    ('Algebra 1', 'Calculus 1', 'Discrete structures', 'Introduction to programming'),
    ('Geometry', 'Calculus 2', 'English', 'Languages, automatas, computability', 'Object-oriented programming'),
    ('Computer architectures', 'Computer english', 'Functional programming', 'Data structures and programming',
     'Computer graphics basics'),
    ('Operations Research', 'Algebra 2', 'Design and analysis of algorithms', 'Computer networks',
     'Operation systems'),
    ('Logical programming', 'Network programming', 'System programming', 'Social aspects of IT',
     'Numerical Analysis'),
    ('Databases', 'Probabilities and statistics', 'Parallel processing systems ', 'Software technologies'),
    ('Web technologies', 'Artificial Intelligence', 'Software architectures')
)


def is_valid_semester(semester, plan):
    return len(plan) >= semester > 0


class StudyPlan:
    def __init__(self, speciality, semester, taken_regular_subjects=None, freely_chosen_subjects_table=None,
                 min_credits_needed=None, taken_free_subjects=None):
        self.__speciality = speciality
        if speciality == 'Software Engineering':
            self.__planned_regular_all = DefaultRegularPlan_SI
            if freely_chosen_subjects_table is None:
                self.__planned_additional = SelectableSubjects(('Operations Research', 'Numerical Analysis'),
                                                               {'CSF': 1, 'CSC': 1,
                                                                'COMP': 4, 'CSP': 2, 'PURE_MATH': 1, 'APM': 0,
                                                                'MATH': 2,
                                                                'REQUIRED_CHOSEN': 1, 'FREELY': 1}, 62)
            else:
                self.__planned_additional = SelectableSubjects(('Operations Research', 'Numerical Analysis'),
                                                               freely_chosen_subjects_table, min_credits_needed,
                                                               taken_free_subjects)

        elif speciality == 'Information Systems':
            self.__planned_regular_all = DefaultRegularPlan_IS
            if freely_chosen_subjects_table is None:
                self.__planned_additional = SelectableSubjects(('Differential equations', 'Operations Research',
                                                                'Numerical Analysis', 'Algebra 2'),
                                                               {'CSF': 2, 'CSC': 2, 'COMP': 2, 'CSP': 3, 'PURE_MATH': 0,
                                                                'APM': 0,
                                                                'MATH': 3, 'REQUIRED_CHOSEN': 1, 'FREELY': 1}, 68)
            else:
                self.__planned_additional = SelectableSubjects(('Differential equations', 'Operations Research',
                                                                'Numerical Analysis', 'Algebra 2'),
                                                               freely_chosen_subjects_table, min_credits_needed,
                                                               taken_free_subjects)
        elif speciality == 'Computer science':
            self.__planned_regular_all = DefaultRegularPlan_KN
            if freely_chosen_subjects_table is None:
                self.__planned_additional = SelectableSubjects(('Programming languages semantics',
                                                                'Computability and complexity', 'Set theory'),
                                                               {'CSF': 3, 'CSC': 3, 'COMP': 0, 'CSP': 2, 'PURE_MATH': 0,
                                                                'APM': 0, 'MATH': 2, 'REQUIRED_CHOSEN': 1, 'FREELY': 0},
                                                               55.5)
            else:
                self.__planned_additional = SelectableSubjects(('Programming languages semantics',
                                                                'Computability and complexity', 'Set theory'),
                                                               freely_chosen_subjects_table, min_credits_needed,
                                                               taken_free_subjects)
        else:
            raise subject.InvalidSpeciality

        self.__semester = semester
        self.__taken_regular_subjects = []
        if taken_regular_subjects is not None:
            self.__taken_regular_subjects = taken_regular_subjects
        self.__regular_subjects_left = []  # List of compulsory subjects left to be taken
        if not is_valid_semester(self.__semester, self.__planned_regular_all):
            raise subject.InvalidSpeciality

        for curr_semester in range(semester):
            curr_semester_subjects = self.__planned_regular_all[curr_semester]
            for curr_subject in curr_semester_subjects:
                self.__regular_subjects_left.append(curr_subject)
        self.__util_remove_duplicate_subjects(self.__taken_regular_subjects)
        for finished_subj in self.__taken_regular_subjects:
            self.__util_finish_subject(finished_subj)

    def get_speciality(self):
        return self.__speciality

    def get_semester(self):
        return self.__semester

    def get_additional(self):
        return self.__planned_additional

    def advance_semester(self):
        self.__semester += 1
        if self.__semester <= len(self.__planned_regular_all):
            for curr_subject in self.__planned_regular_all[self.__semester - 1]:
                self.__regular_subjects_left.append(curr_subject)

    def taken_subjects(self):
        return self.__taken_regular_subjects

    def left_subjects(self):
        return self.__regular_subjects_left

    def __util_remove_duplicate_subjects(self, collection):
        for element in collection:
            while collection.count(element) > 1:
                collection.remove(element)

    def __util_finish_subject(self,
                              subj):  # We keep in files the str type of file, we keep the dict categories and credits
        if type(subj) is str:
            try:
                self.__regular_subjects_left.index(subj)
            except ValueError:  # the subject is freely chosen
                pass
            else:
                self.__regular_subjects_left.remove(subj)

        else:  # the type of subj is subject
            if subj.get_subject_group() == 'COMPULSORY':
                self.__taken_regular_subjects.append(subj.get_subject_name())
                self.__regular_subjects_left.remove(subj.get_subject_name())
            else:
                self.__planned_additional.finish_subject(subj)

    def finish_subject(self, subj):
        try:
            if type(subj) is str:
                self.__taken_regular_subjects.index(subj)
            else:  # it is subject
                self.__taken_regular_subjects.index(subj.get_subject_name())
        except ValueError or TypeError:  # the subject is yet to be taken
            self.__util_finish_subject(subj)

    def can_graduate(self):
        return self.__semester >= 7 and self.__regular_subjects_left == [] and \
               self.__planned_additional.everything_is_cleared()
# TODO add read/write from files


# TODO Class Schedule
