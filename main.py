import subject
import student

menu_commands = ('register', 'login', 'exit ')


def validate_student_input(try_name, try_last_name, try_password):
    raw_name = try_name + ' ' + try_last_name
    valid_name = None
    valid_last_name = None
    if subject.is_valid_person_name(raw_name):
        valid_name = try_name
        valid_last_name = try_last_name
    valid_password = None
    if student.is_valid_password(try_password):
        valid_password = try_password
    return valid_name, valid_last_name, valid_password

def execute_student_menu_commands(student_profile, command):
    while True:
        if command == 'back':
            break
            # my_profile.save_to_file
        elif command == 'create_subject':
            print('Please enter the following information, separated by commas and () if neccessary\n')
            raw_input = input(
                'name, group, lecturer, ECTS_credits, lecture_type, study_times, raw_place, can_be_signed_up_table')
            raw_input = raw_input.split(',')  # the dict and () may break this
            new_subj = subject.Subject(*raw_input)
            student_profile.create_subject(new_subj)
        elif command == 'destroy_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.destroy_subject(*raw_input)
        elif command == 'take_up_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.take_up_subject(*raw_input)
        elif command == 'take_off_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.take_off_subject(*raw_input)
        elif command == 'finish_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.finish_subject(*raw_input)
        elif command == 'rate_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer, score\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.rate_subject(*raw_input)
        elif command == 'comment_subject':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('name, lecturer, your_comment\n')
            raw_input = raw_input.split(',')  # the dict and () may break this
            student_profile.comment_subject(*raw_input)
        elif command == 'change_overlapping':
            print('Please enter the following information, separated by commas\n')
            raw_input = input('overlap_mode\n')
            raw_input = bool(raw_input)
            student_profile.change_overlapping(raw_input)
        else:
            raise subject.InvalidInput
        command = input('Enter next command please. Valid ones are create_subject, destroy_subject,'
                        'take_up_subject, take_off_subject, finish_subject, rate_subject, comment_subject,'
                        'change_overlapping or back')

def login(try_name, try_last_name, try_fn, try_password, input_file, output_file):
    input_file.readline()  # skip the first line
    has_entered = False
    for line in input_file:
        inp = line.split(',')
        if inp == [try_name, try_last_name, try_fn, try_password]:
            has_entered = True
            print('Login successful! ')
            my_profile = construct_student(try_name, try_last_name, try_fn, try_password)
            command = input('Enter next command please. Valid ones are create_subject, destroy_subject,'
                            'take_up_subject, take_off_subject, finish_subject, rate_subject, comment_subject,'
                            'change_overlapping or back')
            execute_student_menu_commands(my_profile, command)
    if not has_entered:
        print('No such user found. Please try to register or try correct credentials ')


# read from file
def construct_student(try_name, try_last_name, try_fn, try_password):
    file_name = ','.join([try_name, try_last_name, try_fn, try_password])
    with open(file_name + '.txt', 'r') as st_read_input_file:
        st_read_input_file.readline()  # skip the first introduction line
        user_info = st_read_input_file.readline()
        user_info = user_info.split(',')
        name, last_name, fn, password, semester, overlaps, specs = user_info
        """
         regular_subjects=None, choosable_subjects=None"""
        taken_regular_subjects = st_read_input_file.readline()
        if taken_regular_subjects == 'EMPTY':
            taken_regular_subjects = None
        else:
            taken_regular_subjects = taken_regular_subjects.split(',')

        free_table_is_valid = True
        freely_chosen_table = {}
        for i in range(9):
            raw_freely_chosen_subjects_table_row = st_read_input_file.readline()
            if raw_freely_chosen_subjects_table_row == 'EMPTY':
                freely_chosen_table = None
                free_table_is_valid = False
            else:
                if free_table_is_valid:
                    category, count = raw_freely_chosen_subjects_table_row.split(',')
                    freely_chosen_table[category] = count

        min_credits_needed = st_read_input_file.readline()
        if min_credits_needed == 'EMPTY':
            min_credits_needed = None
        else:
            min_credits_needed = int(min_credits_needed)

        taken_free_subjects = st_read_input_file.readline()
        if taken_free_subjects == 'EMPTY':
            taken_free_subjects = None
        else:
            taken_free_subjects = taken_free_subjects.split(',')

        current_regular_subject = st_read_input_file.readline()
        if current_regular_subject == 'EMPTY':
            current_regular_subject = None
        else:
            current_regular_subject = current_regular_subject.split(',')

        current_chooseable_subjects = st_read_input_file.readline()
        if current_chooseable_subjects == 'EMPTY':
            current_chooseable_subjects = None
        else:
            current_chooseable_subjects = current_chooseable_subjects.split(',')

        return student.Student(name, last_name, fn, password, overlaps, semester, specs, taken_regular_subjects,
                        freely_chosen_table, min_credits_needed, taken_free_subjects,
                        current_regular_subject, current_chooseable_subjects)


def register(try_name, try_last_name, try_fn, try_password, input_file, output_file):
    input_file.readline()  # skip the first line
    for line in input_file:
        inp = line.split(',')
        curr_st_name, curr_st_ln, curr_st_fn, curr_st_pass = inp
        if line == (try_name, try_last_name, try_fn, try_password):
            print('User has already been registered. Please try to login!')
            raise student.DoubletFacultyNum
        elif curr_st_fn == try_fn:
            print('Doublet faculty nums. Please try to enter valid untaken ones!')
            raise student.DoubletFacultyNum
    # no doublet person found, register the user
    st_info = ','.join([name, last_name, fn, password])
    output_file.write('\n')
    output_file.write(st_info)  # add it to the big pool of students

    # create a personal file of the person
    with open(st_info + '.txt', 'a') as st_file:
        st_file.write('Name, Last_name, Faculty_num, password, semsester, overlaps, speciality')
        st_file.write('\n')
        st_file.write(st_info + ',')
        st_info = input('Please enter your semester and also if you wish overlaps to '
                                          'appear also your speciality will be appreciated \n')
        st_file.write(st_info)
        print('All done, please login by reentering your credentials \n')


while True:
    command = input('Please enter one of the following commands to execute: <login>, <register>, <exit>')
    if command not in menu_commands:
        print('Please enter a valid command to execute!')
        continue
    if command == 'exit':
        break
    else:
        inp = input('Please fill the following forms:'
                                              'name, last_name, faculty_num, password')
        inp = inp.split(',')
        name, last_name, fn, password = inp
        name, last_name, password = validate_student_input(name, last_name, password)
        if name is None or last_name is None or password is None:
            continue  # given information is invalid, go onto next iteration

        with open('people_list.txt', 'r') as input_file:
            with open('people_list.txt', 'a') as output_file:
                if command == 'login':
                    login(name, last_name, fn, password, input_file, output_file)
                elif command == 'register':
                    register(name, last_name, fn, password, input_file, output_file)
                else:  # invalid command
                    raise subject.InvalidInput
