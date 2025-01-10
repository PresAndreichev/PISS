import unittest
import review
import subject
import study_plan
import schedule


class RatingTests(unittest.TestCase):
    """Test how well rating handles different lists"""

    def test_basic_rating(self):
        """Every rating is fine, calc it"""
        example_grades = [5, 7, 8]
        my_rating = rating.Rating(example_grades)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), len(example_grades))
        self.assertEqual(my_rating.get_average_rating(), sum(example_grades) / len(example_grades))

    def test_empty_list(self):
        """Test empty list"""
        example_grades = []
        my_rating = rating.Rating(example_grades)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), 0)
        self.assertEqual(my_rating.get_average_rating(), 1)

    def test_invalid_scores_only(self):
        """The input grades has only invalid scores"""
        example_grades = [-5, -1, 11, 23]
        my_rating = rating.Rating(example_grades)
        self.assertListEqual(my_rating.get_scores(), [])
        self.assertEqual(my_rating.get_count(), 0)
        self.assertEqual(my_rating.get_average_rating(), 1)

    def test_mixed_scores(self):
        """The only valid scores are 5 and 10, so make a rating out of them"""
        example_grades = [-5, -1, 0, 5, 10, 11, 23]
        my_rating = rating.Rating(example_grades)
        self.assertListEqual(my_rating.get_scores(), [5, 10])
        self.assertEqual(my_rating.get_count(), 2)
        self.assertEqual(my_rating.get_average_rating(), 7.5)

    """Test the operation of adding a new score to the active set"""

    def test_invalid_score_adding(self):
        """Test rating by adding invalid score into it"""
        example_grades = [5, 7, 8]
        inv_score = -5
        my_rating = rating.Rating(example_grades)
        my_rating.add_score(inv_score)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), len(example_grades))
        self.assertEqual(my_rating.get_average_rating(), sum(example_grades) / len(example_grades))

    def test_valid_score_to_add(self):
        """We have valid scores, so valid rating. Add a new valid score, recalculations must be made"""
        example_grades = [5, 7, 8]
        valid_score = 4
        my_rating = rating.Rating(example_grades)
        my_rating.add_score(valid_score)
        example_grades.append(valid_score)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), len(example_grades))
        self.assertEqual(my_rating.get_average_rating(), sum(example_grades) / len(example_grades))

    def test_correct_rounding_downwards(self):
        """We have valid scores, so valid rating. Add a new valid score, recalculations must be made. since the score is
        64.06, when rounded it should go down to 64"""
        # Notice the system usually works with int scores only, for testing we will use doubles also
        example_grades = [3, 3, 4, 4, 5, 5, 6, 4, 4, 5, 5, 6,
                          6]  # average_rating of 4.62, should give 60.06 when multiplied
        valid_score = 4
        my_rating = rating.Rating(example_grades)
        my_rating.add_score(valid_score)  # 64.06 should be rounded to 64
        example_grades.append(valid_score)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), len(example_grades))
        self.assertEqual(my_rating.get_average_rating() * len(example_grades), 64)

    def test_correct_rounding_upwards(self):
        """We have valid scores, so valid rating. Add a new valid score, recalculations must be made. since the score is
        65.796, when rounded it should go up to 66"""
        example_grades = [3, 3, 4, 4, 5, 5, 6, 4, 4, 5, 5, 6, 6,
                          1.8]  # average_rating of 4.414, should give 61.796 when multiplied
        valid_score = 4
        my_rating = rating.Rating(example_grades)
        my_rating.add_score(valid_score)  # 65.796 should be rounded to 66
        example_grades.append(valid_score)
        self.assertListEqual(my_rating.get_scores(), example_grades)
        self.assertEqual(my_rating.get_count(), len(example_grades))
        self.assertEqual(my_rating.get_average_rating() * len(example_grades), 66)


class TestSubjectExceptions(unittest.TestCase):
    """Test for life of exceptions and the wanted inheritances(InvalidInput comes from Exception, all other should
    inherit InvalidInput"""

    def test_correct_input_parent(self):
        exception = subject.InvalidInput()
        self.assertIsInstance(exception, Exception)

    def test_correct_inheritance_of_input_to_subject_name(self):
        subj_name = subject.InvalidSubjectName()
        self.assertIsInstance(subj_name, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_person_name(self):
        person_name = subject.InvalidPersonName()
        self.assertIsInstance(person_name, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_subject_group(self):
        subject_group = subject.InvalidSubjectGroup()
        self.assertIsInstance(subject_group, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_credits(self):
        ECTScredits = subject.InvalidECTSCredits()
        self.assertIsInstance(ECTScredits, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_lecture(self):
        lecture = subject.InvalidLectureType()
        self.assertIsInstance(lecture, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_weekday(self):
        weekday = subject.InvalidWeekday()
        self.assertIsInstance(weekday, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_workhour(self):
        workhour = subject.InvalidWorkHour()
        self.assertIsInstance(workhour, subject.InvalidInput)

    def test_correct_inheritance_of_input_to_rating(self):
        rating = subject.InvalidRating()
        self.assertIsInstance(rating, subject.InvalidInput)


class TestSubject(unittest.TestCase):
    """Test initializer and setters"""

    """TEST_Subject_NAME"""
    """Valid name should consist of a given set of chars, together with first letter being capital"""

    def test_subject_name_small_letters_only(self):
        self.assertRaises(subject.InvalidSubjectName, subject.Subject, 'algebra', 'COMPULSORY', 'Konstantin Tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_subject_name_forbiden_chars(self):
        self.assertRaises(subject.InvalidSubjectName, subject.Subject, 'Algebra$', 'COMPULSORY', 'Konstantin Tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    """TEST_Subject_Group"""

    def test_invalid_group(self):
        self.assertRaises(subject.InvalidSubjectGroup, subject.Subject, 'Algebra', 'random123', 'Konstantin Tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    """TEST_Lecturer_NAME"""
    """Valid name should be of 2 names, each starting with caps and containing other small letters only"""

    def test_invalid_person_small_letters(self):
        self.assertRaises(subject.InvalidPersonName, subject.Subject, 'Algebra', 'COMPULSORY', 'konstantin Tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_person_one_name(self):
        self.assertRaises(subject.InvalidPersonName, subject.Subject, 'Algebra', 'COMPULSORY', 'KonstantinTabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_person_only_one_capital(self):
        self.assertRaises(subject.InvalidPersonName, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_person_random_chars(self):
        self.assertRaises(subject.InvalidPersonName, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin1337Tabakov',
                          6.5, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    """TEST CREDITS. They should be between 1 and 10"""

    def test_negative_credits(self):
        self.assertRaises(subject.InvalidECTSCredits, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov',
                          -3, 'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_lecture_type(self):
        self.assertRaises(subject.InvalidLectureType, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov',
                          6.5, 'poredna tupotiq', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 10,
                          'Mnogo e pich, toq Tabakov be :)')

    """Test days. Each day should be a valid English day"""

    def test_invalid_day(self):
        self.assertRaises(subject.InvalidWeekday, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Ponedelnik': (16, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_multiple_days(self):
        self.assertRaises(subject.InvalidWeekday, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (16, 19), 'Vtornik': (16, 19)}, 'FHF-210', {'ALL': 1}, 10,
                          'Mnogo e pich, toq Tabakov be :)')

    """Check if it follows the rules of the hours"""

    def test_too_early_start_hour(self):
        self.assertRaises(subject.InvalidWorkHour, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (6, 9)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_too_late_start_hour(self):
        self.assertRaises(subject.InvalidWorkHour, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (23, 24)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_too_early_end_hour(self):
        self.assertRaises(subject.InvalidWorkHour, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (7, 7)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_too_late_end_hour(self):
        self.assertRaises(subject.InvalidWorkHour, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (22, 1)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    def test_invalid_diff_between_start_and_end_hour(self):
        self.assertRaises(subject.InvalidWorkHour, subject.Subject, 'Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                          'L', {'Monday': (12, 19)}, 'FHF-210', {'ALL': 1}, 10, 'Mnogo e pich, toq Tabakov be :)')

    """Continuation of the rating tests from the start lines"""

    def test_rating_too_small(self):
        my_subject = subject.Subject('Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                                     'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 0,
                                     'Mnogo e pich, toq Tabakov be :)')
        self.assertEqual(my_subject.get_subject_rating().get_average_rating(),
                         1)  # by default if invalid it will be set to 1

    def test_rating_too_great(self):
        my_subject = subject.Subject('Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5,
                                     'L', {'Monday': (16, 19)}, 'FHF-210', {'ALL': 1}, 11,
                                     'Mnogo e pich, toq Tabakov be :)')
        self.assertEqual(my_subject.get_subject_rating().get_average_rating(),
                         1)  # by default if invalid it will be set to 1

    """Tests for behaviour on who can sign up the subject"""

    def test_add_speciality_course_of_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'SI': 1}, 1, 'DIS + politika = klasika')
        comp_science = 'KN'
        course = 1
        calculus.change_speciality_course_of_signing_up_table(comp_science, course)
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 1, 'KN': 1})

    def test_add_invalid_speciality_to_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'SI': 1}, 1, 'DIS + politika = klasika')
        applied_maths = 'APM'
        course = 1
        try:
            calculus.change_speciality_course_of_signing_up_table(applied_maths, course)
        except subject.InvalidSpeciality:
            self.assertEqual(1, 1)

    def test_change_speciality_course_of_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'SI': 1}, 1, 'DIS + politika = klasika')
        soft_eng = 'SI'
        course = 3
        calculus.change_speciality_course_of_signing_up_table(soft_eng, course)
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 3})

    def test_remove_speciality_course_of_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 3}, 1, 'DIS + politika = klasika')
        soft_eng = 'SI'
        calculus.remove_speciality_from_signing_up_table(soft_eng)
        self.assertDictEqual(calculus.get_signing_up_table(), {'IS': 3, 'KN': 3})

    def test_remove_invalid_speciality_course_of_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 3}, 1, 'DIS + politika = klasika')
        math = 'MATH'
        try:
            calculus.remove_speciality_from_signing_up_table(math)
        except subject.InvalidSpeciality:
            self.assertEqual(1, 1)

    def test_remove_missing_speciality_course_of_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'KN': 1}, 1, 'DIS + politika = klasika')
        soft_eng = 'SI'
        try:
            calculus.remove_speciality_from_signing_up_table(soft_eng)
        except KeyError:
            self.assertEqual(1, 1)

    def test_parse_valid_signing_up_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'KN': 1}, 1, 'DIS + politika = klasika')
        calculus.set_signing_up_table({'SI': 3, 'IS': 3, 'KN': 3})
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 3, 'IS': 3, 'KN': 3})

    def test_parse_all_subjects_from_key_all(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'KN': 4}, 1, 'DIS + politika = klasika')
        calculus.set_signing_up_table({'IS': 3, 'SI': 1, 'ALL': 2})  # 'All' will overwrite all the others
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 2, 'IS': 2, 'KN': 2})

    def test_set_all_subjects_and_change_individual_table(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'KN': 4}, 1, 'DIS + politika = klasika')
        calculus.set_signing_up_table({'ALL': 2, 'SI': 3})  # 'All' will overwrite the others, then SI will be set to 3
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 3, 'IS': 2, 'KN': 2})

    def test_invalid_parse_with_one_broken_speciality(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'KN': 4}, 1, 'DIS + politika = klasika')
        try:
            calculus.set_signing_up_table({'ALL': 2, 'APM': 2})  # APM is not allowed, so it will throw exception
        except subject.InvalidSpeciality:
            self.assertEqual(1, 1)

    """Test ok subject"""

    def test_ok_subject(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 1}, 1, 'DIS + politika = klasika')
        self.assertEqual(calculus.get_subject_name(), 'DIS')
        self.assertEqual(calculus.get_subject_group(), 'COMPULSORY')
        self.assertEqual(calculus.get_lecturer(), 'Vladimir Babev')
        self.assertEqual(calculus.get_ECTS_credits(), 8)
        self.assertEqual(calculus.get_lecture_type(), 'L')
        self.assertDictEqual(calculus.get_study_times(), {'Wednesday': (10, 14)})
        self.assertEqual(calculus.get_faculty(), 'FMI')
        self.assertEqual(calculus.get_room(), '325')
        self.assertDictEqual(calculus.get_signing_up_table(), {'SI': 1, 'IS': 1, 'KN': 1})
        self.assertEqual(calculus.get_subject_rating().get_average_rating(), 1)
        self.assertListEqual(calculus.get_reviews(), ['DIS + politika = klasika'])

    """Test more setters or advanced functions"""

    def test_change_invalid_faculty(self):  # There is probably a better way to do it
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 1}, 1, 'DIS + politika = klasika')
        try:
            calculus.set_faculty('Rektorat')
        except subject.InvalidPlace:
            self.assertEqual(1, 1)

    def test_change_invalid_room(self):  # There is probably a better way to do it
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 1}, 1, 'DIS + politika = klasika')
        try:
            calculus.set_room('a21')
        except subject.InvalidPlace:
            self.assertEqual(1, 1)

    def test_add_review(self):
        original_review = ['DIS + politika = klasika']
        dis_review = original_review
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 1}, 1, dis_review)
        my_review = '18-ti proizvodni ne mojem da namirame!'
        calculus.add_review(my_review)
        my_list = [original_review, my_review]
        self.assertListEqual(calculus.get_reviews(), my_list)

    def test_add_study_time(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)}, 'FMI-325',
                                   {'ALL': 1}, 1, '18-ti proizvodni ne mojem da namirame!')
        calculus.add_new_study_time('Monday', 16, 19)
        self.assertDictEqual(calculus.get_study_times(), {'Wednesday': (10, 14), 'Monday': (16, 19)})

    def test_remove_study_time(self):
        calculus = subject.Subject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14),
                                                                                   'Monday': (16, 19)}, 'FMI-325',
                                   {'ALL': 1}, 1, '18-ti proizvodni ne mojem da namirame!')
        calculus.remove_study_time_by_day('Wednesday')
        self.assertDictEqual(calculus.get_study_times(), {'Monday': (16, 19)})


class TestSelectableSubjects(unittest.TestCase):
    """Tests for the class of table for choosable subjects"""

    """The subject_table is correct and so it should be parsed successfully"""

    def test_correct_selectable_subject(self):
        example_tuple = 'Operations Research', 'Numerical Analysis'
        example_dict = {'CSF': 1, 'CSC': 1, 'COMP': 4, 'CSP': 2, 'PURE_MATH': 1, 'APM': 0,
                        'MATH': 2, 'REQUIRED_CHOSEN': 1, 'FREELY': 1}
        my_plan = study_plan.SelectableSubjects(example_tuple, example_dict, 62)
        self.assertTupleEqual(my_plan.get_required_subject(), example_tuple)
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertEqual(my_plan.get_remaining_credits_balance(), 62)

    """Test to prove, that same subject clearing earns no extra benefits"""

    def test_clearance_of_same_subject(self):
        example_tuple = 'Operations Research', 'Numerical Analysis'
        example_dict = {'CSF': 1, 'CSC': 1, 'COMP': 4, 'CSP': 2, 'PURE_MATH': 1, 'APM': 0,
                        'MATH': 2, 'REQUIRED_CHOSEN': 1, 'FREELY': 1}
        my_plan = study_plan.SelectableSubjects(example_tuple, example_dict, 62, {'Operations Research': 5})
        operations_research = subject.Subject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                              {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2})
        my_plan.finish_subject(operations_research)  # The subject has already been done, don't change anything
        self.assertEqual(my_plan.get_remaining_credits_balance(), 62)
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {'Operations Research': 5})

    """Test to prove that finishing subject works correctly and the changes are directly accepted"""

    def test_correct_subject_finish(self):
        example_tuple = 'Operations Research', 'Numerical Analysis'
        example_dict = {'CSF': 1, 'CSC': 1, 'COMP': 4, 'CSP': 2, 'PURE_MATH': 1, 'APM': 0,
                        'MATH': 2, 'REQUIRED_CHOSEN': 1, 'FREELY': 1}
        my_plan = study_plan.SelectableSubjects(example_tuple, example_dict, 62)
        operations_research = subject.Subject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                              {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2})
        my_plan.finish_subject(operations_research)
        self.assertEqual(my_plan.get_remaining_credits_balance(), 62 - operations_research.get_ECTS_credits())
        example_dict['REQUIRED_CHOSEN'] -= 1
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {'Operations Research': 5})

    """Test to prove the correctness of transfer credits func, which works in the background and makes sure that each
    category given wanted values will give sufficient table. In the example it is throughoutly explained how the 
    rounding works."""

    def test_transfer_of_credits(self):
        example_tuple = 'Operations Research', 'Numerical Analysis'
        example_dict = {'CSF': 1, 'CSC': 1, 'COMP': 1, 'CSP': 2, 'PURE_MATH': 1, 'APM': 0,
                        'MATH': 2, 'REQUIRED_CHOSEN': 1, 'FREELY': 1}
        my_plan = study_plan.SelectableSubjects(example_tuple, example_dict, 62)
        dsa_2 = subject.Subject('Data structures and programming 2', 'CSC', 'Atanas Semerdzhiev', 8, 'L',
                                {'Monday': (12, 14)}, 'FMI-200', {'ALL': 3})
        my_plan.finish_subject(dsa_2)
        example_dict[dsa_2.get_subject_group()] -= 1  # category csc drops to zero
        self.assertEqual(my_plan.get_remaining_credits_balance(), 62 - dsa_2.get_ECTS_credits())  # 54 credits
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {dsa_2.get_subject_name(): 8})

        daa_1 = subject.Subject('Design and Analysis of Algorithms 1', 'CSC', 'Minko Markov', 7, 'L',
                                {'Tuesday': (14, 16)}, 'FHF-210', {'KN': 3})
        my_plan.finish_subject(daa_1)
        example_dict['COMP'] -= 1  # although csc is decreased, it is already cleared, so clear comp category
        self.assertEqual(my_plan.get_remaining_credits_balance(), 54 - daa_1.get_ECTS_credits())  # 47 credits
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {dsa_2.get_subject_name(): 8,
                                                                       daa_1.get_subject_name(): 7})

        intro_to_python = subject.Subject('Introduction to Python programming', 'CSF', 'Victor Bechev', 5, 'L',
                                          {'Wednesday': (16, 20)}, 'FHF-210', {'SI': 2})
        my_plan.finish_subject(intro_to_python)
        example_dict[intro_to_python.get_subject_group()] -= 1  # clear CSF category
        self.assertEqual(my_plan.get_remaining_credits_balance(), 47 - intro_to_python.get_ECTS_credits())  # 42 credits
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {dsa_2.get_subject_name(): 8,
                                                                       daa_1.get_subject_name(): 7,
                                                                       intro_to_python.get_subject_name(): 5})

        current_java_technologies = subject.Subject('Current Java Technologies', 'CSF', 'Stoyan Velev', 8, 'L',
                                                    {'Wednesday': (16, 20)}, 'FMI-325', {'SI': 2})
        my_plan.finish_subject(current_java_technologies)
        example_dict['FREELY'] -= 1  # the comp category is already cleared, go onto the freely category
        self.assertEqual(my_plan.get_remaining_credits_balance(),
                         42 - current_java_technologies.get_ECTS_credits())  # 34 credits
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertDictEqual(my_plan.get_persons_finished_subjects(), {dsa_2.get_subject_name(): 8,
                                                                       daa_1.get_subject_name(): 7,
                                                                       intro_to_python.get_subject_name(): 5,
                                                                       current_java_technologies.get_subject_name(): 8})
        self.assertFalse(my_plan.everything_is_cleared())  # we still have to take up maths and comp practicums

    """Test to continue on the finish subject dilemma, this time by allowing the user to know when he may successfully
    graduate."""

    def test_possible_clearance_of_table(self):
        example_tuple = 'Operations Research', 'Numerical Analysis'
        example_dict = {'CSF': 0, 'CSC': 0, 'COMP': 1, 'CSP': 0, 'PURE_MATH': 0, 'APM': 0,
                        'MATH': 0, 'REQUIRED_CHOSEN': 0, 'FREELY': 1}
        my_plan = study_plan.SelectableSubjects(example_tuple, example_dict, 13)
        daa_1 = subject.Subject('Design and Analysis of Algorithms 1', 'CSC', 'Minko Markov', 7, 'L',
                                {'Tuesday': (14, 16)}, 'FHF-210', {'KN': 3})
        my_plan.finish_subject(daa_1)
        example_dict['COMP'] -= 1  # FREELY stands together with 6 credits
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertFalse(my_plan.every_category_is_cleared())
        self.assertFalse(my_plan.get_remaining_credits_balance() < 0)
        self.assertFalse(my_plan.everything_is_cleared())

        intro_to_python = subject.Subject('Introduction to Python programming', 'CSF', 'Victor Bechev', 5, 'L',
                                          {'Wednesday': (16, 20)}, 'FHF-210', {'SI': 2})
        my_plan.finish_subject(intro_to_python)
        example_dict['FREELY'] -= 1  # no categories left but still 1 credit
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertTrue(my_plan.every_category_is_cleared())
        self.assertFalse(my_plan.get_remaining_credits_balance() < 0)
        self.assertFalse(my_plan.everything_is_cleared())

        nuclear_physics = subject.Subject('Nuclear Physics', 'APM', 'Albert Einstein', 10, 'L',
                                          {'Wednesday': (16, 20)}, 'FZF-32', {'SI': 4})
        my_plan.finish_subject(nuclear_physics)
        example_dict['FREELY'] -= 1  # everything is cleared
        self.assertDictEqual(my_plan.get_freely_chosen_subjects_categories(), example_dict)
        self.assertTrue(my_plan.every_category_is_cleared())
        self.assertTrue(my_plan.get_remaining_credits_balance() < 0)
        self.assertTrue(my_plan.everything_is_cleared())


class TestStudyPlan(unittest.TestCase):
    """Tests to confirm the correctness of study_plan"""

    """Test plans by initialisation"""

    def test_brand_new_plan(self):
        my_specs = 'Software Engineering'
        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester)
        self.assertEqual(my_plan.get_speciality(), my_specs)
        self.assertEqual(my_plan.get_semester(), semester)
        self.assertListEqual(my_plan.taken_subjects(), [])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                       'Introduction to programming'])

    def test_valid_study_plan(self):
        my_specs = 'Software Engineering'
        semester = 2
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Calculus 1'])
        self.assertEqual(my_plan.get_speciality(), my_specs)
        self.assertEqual(my_plan.get_semester(), semester)
        self.assertListEqual(my_plan.taken_subjects(), ['Calculus 1'])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'English', 'Discrete structures 1',
                                                       'Introduction to programming', 'Geometry', 'Calculus 2',
                                                       'Computer english', 'Discrete structures 2',
                                                       'Object-oriented programming'])

    def test_duplicate_finished_subjects(self):
        my_specs = 'Software Engineering'
        semester = 2
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Calculus 1', 'Calculus 1'])
        self.assertEqual(my_plan.get_speciality(), my_specs)
        self.assertEqual(my_plan.get_semester(), semester)
        self.assertListEqual(my_plan.taken_subjects(), ['Calculus 1'])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'English', 'Discrete structures 1',
                                                       'Introduction to programming', 'Geometry', 'Calculus 2',
                                                       'Computer english', 'Discrete structures 2',
                                                       'Object-oriented programming'])

    """Test invalid specialties or semesters"""

    def test_invalid_speciality(self):
        my_specs = 'Informatics'
        semester = 2
        self.assertRaises(subject.InvalidSpeciality, study_plan.StudyPlan, my_specs, semester)

    def test_invalid_semester(self):
        my_specs = 'Software Engineering'
        semester = 8
        self.assertRaises(subject.InvalidSpeciality, study_plan.StudyPlan, my_specs, semester)

    """Advance semester check ups"""

    def test_advance_semester_basic(self):
        my_specs = 'Software Engineering'
        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester)
        self.assertEqual(my_plan.get_semester(), semester)
        self.assertListEqual(my_plan.taken_subjects(), [])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                       'Introduction to programming'])
        my_plan.advance_semester()
        self.assertEqual(my_plan.get_semester(), semester + 1)
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                       'Introduction to programming', 'Geometry', 'Calculus 2',
                                                       'Computer english', 'Discrete structures 2',
                                                       'Object-oriented programming'])

    def test_advance_semester_final(self):
        my_specs = 'Software Engineering'
        all_subjects = ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1', 'Introduction to programming',
                        'Geometry', 'Calculus 2', 'Computer english', 'Discrete structures 2',
                        'Object-oriented programming', 'Computer architectures', 'Introduction to software engineering',
                        'Communication skills', 'Data structures and algorithms', 'Databases',
                        'Economics of software engineering', 'Software architectures and software development',
                        'Computer networks', 'Operation systems', 'Differential equations and applications',
                        'XML technologies for semantic web', 'Social aspects of IT', 'Statistics and empirical methods',
                        'Quality assurance', 'Web technologies', 'Requirements engineering',
                        'Design of human machine interface', 'Distributed software architectures', 'Data Mining',
                        'Design and integration of software systems', 'Projects management']
        semester = 7
        my_plan = study_plan.StudyPlan(my_specs, semester)
        self.assertEqual(my_plan.get_semester(), semester)
        self.assertListEqual(my_plan.taken_subjects(), [])
        self.assertListEqual(my_plan.left_subjects(), all_subjects)
        my_plan.advance_semester()
        self.assertEqual(my_plan.get_semester(), semester + 1)
        self.assertListEqual(my_plan.left_subjects(), all_subjects)

    """tests with subject objects"""
    """FINISH_SUBJECT tests"""

    def test_check_already_finished_regular_subject(self):
        my_specs = 'Software Engineering'
        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Calculus 1'])
        calculus = subject.Subject('Calculus 1', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                   'FMI-325', {'SI': 1}, 1, 'DIS + politika = klasika')
        self.assertListEqual(my_plan.taken_subjects(), ['Calculus 1'])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'English', 'Discrete structures 1',
                                                       'Introduction to programming'])
        my_plan.finish_subject(calculus)
        self.assertListEqual(my_plan.taken_subjects(), ['Calculus 1'])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'English', 'Discrete structures 1',
                                                       'Introduction to programming'])

    def test_check_already_finished_chooseable_subject(self):
        my_specs = 'Software Engineering'

        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester, [], {'CSF': 1, 'CSC': 1, 'COMP': 4, 'CSP': 2, 'PURE_MATH': 1,
                                                                'APM': 0, 'MATH': 2, 'REQUIRED_CHOSEN': 0, 'FREELY': 1},
                                       57, {'Operations Research': 5})
        self.assertDictEqual(my_plan.get_additional().get_persons_finished_subjects(), {'Operations Research': 5})
        operations_research = subject.Subject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                              {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2})
        my_plan.finish_subject(operations_research)
        self.assertDictEqual(my_plan.get_additional().get_persons_finished_subjects(), {'Operations Research': 5})
        self.assertListEqual(my_plan.taken_subjects(), [])

    def test_check_valid_finishing_regular_subject(self):
        my_specs = 'Software Engineering'
        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester)
        calculus = subject.Subject('Calculus 1', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                   'FMI-325', {'SI': 1}, 1, 'DIS + politika = klasika')
        self.assertListEqual(my_plan.taken_subjects(), [])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                       'Introduction to programming'])
        my_plan.finish_subject(calculus)
        self.assertListEqual(my_plan.taken_subjects(), ['Calculus 1'])
        self.assertListEqual(my_plan.left_subjects(), ['Algebra', 'English', 'Discrete structures 1',

                                                       'Introduction to programming'])

    def test_check_valid_finishing_choosable_subject(self):
        my_specs = 'Software Engineering'
        semester = 1
        my_plan = study_plan.StudyPlan(my_specs, semester)
        self.assertDictEqual(my_plan.get_additional().get_persons_finished_subjects(), {})
        operations_research = subject.Subject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                              {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2})
        my_plan.finish_subject(operations_research)
        self.assertDictEqual(my_plan.get_additional().get_persons_finished_subjects(), {'Operations Research': 5})
        self.assertListEqual(my_plan.taken_subjects(), [])

    """CAN_GRADUATE Checkups"""

    def test_valid_graduation(self):
        my_specs = 'Software Engineering'
        semester = 7
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                            'Introduction to programming',
                                                            'Geometry', 'Calculus 2', 'Computer english',
                                                            'Discrete structures 2', 'Object-oriented programming',
                                                            'Computer architectures',
                                                            'Introduction to software engineering',
                                                            'Communication skills',
                                                            'Data structures and algorithms', 'Databases',
                                                            'Economics of software engineering',
                                                            'Software architectures and software development',
                                                            'Computer networks', 'Operation systems',
                                                            'Differential equations and applications',
                                                            'XML technologies for semantic web', 'Social aspects of IT',
                                                            'Statistics and empirical methods', 'Quality assurance',
                                                            'Web technologies', 'Requirements engineering',
                                                            'Design of human machine interface',
                                                            'Distributed software architectures', 'Data Mining',
                                                            'Design and integration of software systems',
                                                            'Projects management'],
                                       {'CSF': 0, 'CSC': 0, 'COMP': 0, 'CSP': 0,
                                        'PURE_MATH': 0, 'APM': 0, 'MATH': 0, 'REQUIRED_CHOSEN': 0, 'FREELY': 0}, 0)
        self.assertTrue(my_plan.can_graduate())

    def test_invalid_graduation_compulsory_subject(self):
        my_specs = 'Software Engineering'
        semester = 7
        #  'Introduction to programming' is missing
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                            'Geometry', 'Calculus 2', 'Computer english',
                                                            'Discrete structures 2',
                                                            'Object-oriented programming', 'Computer architectures',
                                                            'Introduction to software engineering',
                                                            'Communication skills', 'Data structures and algorithms',
                                                            'Databases',
                                                            'Economics of software engineering',
                                                            'Software architectures and software development',
                                                            'Computer networks', 'Operation systems',
                                                            'Differential equations and applications',
                                                            'XML technologies for semantic web', 'Social aspects of IT',
                                                            'Statistics and empirical methods',
                                                            'Quality assurance', 'Web technologies',
                                                            'Requirements engineering',
                                                            'Design of human machine interface',
                                                            'Distributed software architectures', 'Data Mining',
                                                            'Design and integration of software systems',
                                                            'Projects management'], {'CSF': 0, 'CSC': 0,
                                                                                     'COMP': 0, 'CSP': 0,
                                                                                     'PURE_MATH': 0, 'APM': 0,
                                                                                     'MATH': 0,
                                                                                     'REQUIRED_CHOSEN': 0, 'FREELY': 0},
                                       0)
        self.assertFalse(my_plan.can_graduate())

    def test_invalid_graduation_chooseable_subjects(self):
        my_specs = 'Software Engineering'
        semester = 7
        #  'One more extra math subject of chooseable is needed'
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                            'Introduction to programming',
                                                            'Geometry', 'Calculus 2', 'Computer english',
                                                            'Discrete structures 2', 'Object-oriented programming',
                                                            'Computer architectures',
                                                            'Introduction to software engineering',
                                                            'Communication skills',
                                                            'Data structures and algorithms', 'Databases',
                                                            'Economics of software engineering',
                                                            'Software architectures and software development',
                                                            'Computer networks', 'Operation systems',
                                                            'Differential equations and applications',
                                                            'XML technologies for semantic web', 'Social aspects of IT',
                                                            'Statistics and empirical methods', 'Quality assurance',
                                                            'Web technologies', 'Requirements engineering',
                                                            'Design of human machine interface',
                                                            'Distributed software architectures', 'Data Mining',
                                                            'Design and integration of software systems',
                                                            'Projects management'], {'CSF': 0, 'CSC': 0,
                                                                                     'COMP': 0, 'CSP': 0,
                                                                                     'PURE_MATH': 0, 'APM': 0,
                                                                                     'MATH': 1,
                                                                                     'REQUIRED_CHOSEN': 0, 'FREELY': 0},
                                       0)
        self.assertFalse(my_plan.can_graduate())

    def test_invalid_graduation_missing_credits(self):
        my_specs = 'Software Engineering'
        semester = 7
        #  we need 1 more credit from extra disciplines
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                            'Introduction to programming',
                                                            'Geometry', 'Calculus 2', 'Computer english',
                                                            'Discrete structures 2', 'Object-oriented programming',
                                                            'Computer architectures',
                                                            'Introduction to software engineering',
                                                            'Communication skills',
                                                            'Data structures and algorithms', 'Databases',
                                                            'Economics of software engineering',
                                                            'Software architectures and software development',
                                                            'Computer networks', 'Operation systems',
                                                            'Differential equations and applications',
                                                            'XML technologies for semantic web', 'Social aspects of IT',
                                                            'Statistics and empirical methods', 'Quality assurance',
                                                            'Web technologies', 'Requirements engineering',
                                                            'Design of human machine interface',
                                                            'Distributed software architectures', 'Data Mining',
                                                            'Design and integration of software systems',
                                                            'Projects management'], {'CSF': 0, 'CSC': 0,
                                                                                     'COMP': 0, 'CSP': 0,
                                                                                     'PURE_MATH': 0, 'APM': 0,
                                                                                     'MATH': 0,
                                                                                     'REQUIRED_CHOSEN': 0, 'FREELY': 0},
                                       1)
        self.assertFalse(my_plan.can_graduate())

    def test_invalid_graduation_semester_too_low(self):
        my_specs = 'Software Engineering'
        semester = 6
        #  The semester is too low
        my_plan = study_plan.StudyPlan(my_specs, semester, ['Algebra', 'Calculus 1', 'English', 'Discrete structures 1',
                                                            'Introduction to programming',
                                                            'Geometry', 'Calculus 2', 'Computer english',
                                                            'Discrete structures 2', 'Object-oriented programming',
                                                            'Computer architectures',
                                                            'Introduction to software engineering',
                                                            'Communication skills',
                                                            'Data structures and algorithms', 'Databases',
                                                            'Economics of software engineering',
                                                            'Software architectures and software development',
                                                            'Computer networks', 'Operation systems',
                                                            'Differential equations and applications',
                                                            'XML technologies for semantic web', 'Social aspects of IT',
                                                            'Statistics and empirical methods', 'Quality assurance',
                                                            'Web technologies', 'Requirements engineering',
                                                            'Design of human machine interface',
                                                            'Distributed software architectures', 'Data Mining',
                                                            'Design and integration of software systems',
                                                            'Projects management'], {'CSF': 0, 'CSC': 0,
                                                                                     'COMP': 0, 'CSP': 0,
                                                                                     'PURE_MATH': 0, 'APM': 0,
                                                                                     'MATH': 0,
                                                                                     'REQUIRED_CHOSEN': 0, 'FREELY': 0},
                                       0)
        self.assertFalse(my_plan.can_graduate())


class TestViewedSubject(unittest.TestCase):
    """Tests for the Viewedsubject class. As it is trivial they will be short and self-explanatory."""

    def test_basic_viewed_subject(self):
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE', 'BLACK', 3)
        self.assertEqual(operations_research.get_background_color(), 'white')
        self.assertEqual(operations_research.get_font_color(), 'black')
        self.assertEqual(operations_research.get_priority(), 3)

    def test_increment_priority(self):
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE', 'BLACK', 3)
        self.assertEqual(operations_research.get_priority(), 3)
        operations_research.increment_priority()
        self.assertEqual(operations_research.get_priority(), 4)

    def test_decrement_priority_basic(self):
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE', 'BLACK', 3)
        self.assertEqual(operations_research.get_priority(), 3)
        operations_research.decrement_priority()
        self.assertEqual(operations_research.get_priority(), 2)

    def test_decrement_priority_extremal(self):
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE', 'BLACK', 0)
        self.assertEqual(operations_research.get_priority(), 0)
        operations_research.decrement_priority()
        self.assertEqual(operations_research.get_priority(), 0)

    def test_compare_subject_priorities(self):
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE', 'BLACK', 0)
        intro_to_python = schedule.ViewedSubject('Introduction to Python programming', 'CSF', 'Victor Bechev', 5, 'L',
                                                 {'Wednesday': (16, 20)}, 'FHF-210', {'SI': 2}, 'WHITE', 'BLACK', 10)
        algebra = schedule.ViewedSubject('Algebra', 'COMPULSORY', 'Konstantin Tabakov', 6.5, 'L', {'Monday': (16, 19)},
                                         'FHF-210', {'ALL': 1}, 'WHITE', 'BLACK', 10, 11,
                                         'Mnogo e pich, toq Tabakov be :)')
        self.assertLess(operations_research, intro_to_python)
        self.assertLessEqual(intro_to_python, algebra)
        self.assertGreaterEqual(intro_to_python, algebra)
        self.assertGreater(algebra, operations_research)


class TestSchedule(unittest.TestCase):

    def test_basic_schedule(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        self.assertDictEqual(my_plan.get_weekly_table(), {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                                          'Friday': {}, 'Saturday': {}, 'Sunday': {}})

    def test_basic_time_business(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        my_plan.add_subject(calculus)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 10), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 9), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])  # subjects starts here
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 14), [])  # subject end here
        self.assertListEqual(my_plan.get_subjects_of_given_time('Thursday', 13), [])

    def test_basic_compulory_add(self):  # subject.add in initializer uses this function
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])

    def test_basic_compulsory_removal(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan.remove_subject(calculus)  # you cannot remove a compulsory subject, you can only finish it
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])

    def test_basic_compulsory_finish(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan.finish_subject(calculus)  # you cannot remove a compulsory subject, you can only finish it
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [])

    def test_basic_choosable_add(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Tuesday': (15, 17)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 3)
        my_plan.add_subject(operations_research)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 15), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 16), [operations_research])

    def test_basic_choosable_removal(self):
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Tuesday': (15, 17)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 3)
        my_plan.add_subject(operations_research)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 15), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 16), [operations_research])
        my_plan.remove_subject(operations_research)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 15), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 16), [])

    def test_compulsory_with_chooseable_without_overlaps(self):
        """Compulsory then chooseable with no overlaps"""
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Wednesday': (12, 14)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 3)
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan.add_subject(operations_research)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])

    def test_compulsory_with_chooseable_with_overlaps(self):
        """Compulsory with chooseable with overlaps"""
        overlaps = 'True'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Wednesday': (12, 14)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 3)
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan.add_subject(operations_research)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus, operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus, operations_research])

    def test_max_chooseable_already_in(self):
        def test_compulsory_with_chooseable_with_overlaps(self):
            """Test placing more chooseables then allowed(5 is max allowed at a time)"""
            overlaps = 'True'
            my_plan = schedule.Schedule(overlaps)
            operations_research_one = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                             {'Monday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                             'BLACK', 3)
            operations_research_two = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                             {'Tuesday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                             'BLACK', 3)
            operations_research_three = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                               {'Wednesday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                               'BLACK', 3)
            operations_research_four = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                              {'Thursday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                              'BLACK', 3)
            operations_research_five = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                              {'Friday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                              'BLACK', 3)
            operations_research_too_much = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                              {'Saturday': (12, 14)}, 'FMI-200', {'ALL': 2}, 'WHITE',
                                                              'BLACK', 3)
            my_plan.add_subject(operations_research_one)  # time interval is [start, end)
            my_plan.add_subject(operations_research_two)
            my_plan.add_subject(operations_research_three)
            my_plan.add_subject(operations_research_four)
            my_plan.add_subject(operations_research_five)
            my_plan.add_subject(operations_research_too_much)  # if its valid addition, it will add interval in Saturday
            self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [operations_research_one])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [operations_research_one])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 12), [operations_research_two])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Tuesday', 13), [operations_research_two])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [operations_research_three])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [operations_research_three])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Thursday', 12), [operations_research_four])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Thursday', 13), [operations_research_four])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Friday', 12), [operations_research_five])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Friday', 13), [operations_research_five])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [])
            self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [])

    def test_generate_programme_without_overlaps(self):
        """No overlaps are allowed. The subject which gets in the programme first(usually a compulsory one) will
        be prioritised over higher priority subjects."""
        overlaps = 'False'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Wednesday': (12, 14)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 5)
        my_plan.add_subject(calculus)  # time interval is [start, end)
        my_plan.add_subject(operations_research)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan_printable = my_plan.generate_final_study_table()
        comparor = []
        for i in range(7):
            comparor.append([])  # creates a matrix of 7 rows(days)
            for j in range(17):  # offset from 7 to 24
                comparor[i].append('EMPTY')
        for i in range(3, 7): # set dis table
            comparor[2][i] = calculus
        self.assertListEqual(my_plan_printable, comparor)

    def test_generate_programme_with_overlaps(self):
        """Overlaps are allowed. The subject which has the highest priority will be put in front of older subject. This
        usually means that chooseable may be chosen over compulsory (and put up earlier) subjects."""
        overlaps = 'True'
        my_plan = schedule.Schedule(overlaps)
        calculus = schedule.ViewedSubject('DIS', 'COMPULSORY', 'Vladimir Babev', 8, 'L', {'Wednesday': (10, 14)},
                                          'FMI-325',
                                          {'KN': 1}, 'WHITE', 'BLACK', 3, 1, 'DIS + politika = klasika')
        operations_research = schedule.ViewedSubject('Operations Research', 'APM', 'Nadq Zlateva', 5, 'L',
                                                     {'Monday': (12, 14), 'Wednesday': (12, 14)}, 'FMI-200', {'ALL': 2},
                                                     'WHITE', 'BLACK', 6)
        my_plan.add_subject(calculus)  # time interval is [start, end)
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus])
        my_plan.add_subject(operations_research)
        # final study table
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 12), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Monday', 13), [operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 10), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 11), [calculus])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 12), [calculus, operations_research])
        self.assertListEqual(my_plan.get_subjects_of_given_time('Wednesday', 13), [calculus, operations_research])
        # the printable should consist of 2 ors in monday, 2 disses from 10 to 12 in wednesday and ors after it
        my_plan_printable = my_plan.generate_final_study_table()
        comparor = []
        for i in range(7):
            comparor.append([])  # creates a matrix of 7 rows(days)
            for j in range(17):  # offset from 7 to 24
                comparor[i].append('EMPTY')
        comparor[0][5] = operations_research
        comparor[0][6] = operations_research
        comparor[2][3] = calculus
        comparor[2][4] = calculus
        comparor[2][5] = operations_research
        comparor[2][6] = operations_research
        self.assertListEqual(my_plan_printable, comparor)


if __name__ == '__main__':
    unittest.main()
