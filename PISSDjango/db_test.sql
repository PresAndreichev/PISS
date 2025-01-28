INSERT OR IGNORE INTO App_lecturetype (type)
VALUES
('Lecture'),
('Seminar'),
('Practicum'),
('GuestLecture');
	
INSERT INTO App_floor (number)
VALUES
(0),
(1),
(2),
(3),
(4),
(5);

INSERT INTO App_room (floor_id, characteristics, number, seats)
VALUES
(1, 146, 2, 50),
(2, 148, 101, 120),
(3, 211, 222, 25),
(4, 211, 321, 25),
(5, 146, 404, 30),
(6, 146, 500, 50),
(4, 146, 325, 100),
(1, 146, 1, 70);

INSERT or Ignore INTO App_subjectgroup (name)
VALUES
('MATH'),
('APPLIED_MATH'),
('CSF'),
('CSC'),
('CSP'),
('OTHERS');

INSERT INTO App_subject (subject_group_id, ects_credits, name, weekly_computer_exercises_duration, weekly_exercises_duration, weekly_lectures_duration)
VALUES
(1, 7, 'Теория на множествата', 0, 2, 2),
(1, 5, 'Линейна алгебра', 0, 2, 3),
(2, 5, 'Размити множества и приложения', 1, 0, 3),
(3, 6.5, 'Функционално програмиране', 0, 2, 3),
(4, 6, 'Основи на компютърните мрежи', 4, 0, 1),
(4, 6, 'Изкуствен интелект', 0, 2, 3),
(5, 2.5, 'Увод в програмирането - практикум', 2, 0, 0),
(6, 2.5, 'Философия на математиката', 0, 0, 2);

INSERT or IGNORE into App_user (email, is_profile_disabled, password, priority, username)
VALUES
('boris_georgiev1998@gmail.com', 0, 'starwarsisC00L', 2, 'bobygeorg'),
('gergana_ivanova@gmail.com', 1, 'GeriIvanova22', 1, 'geryivanova'),
('drago_konstantinov@abv.bg', 0, 'strongestpasswordEVER2000', 2, 'dragokonst'),
('rosi_kostova@abv.bg', 0, 'rosiKostovalovesBelot22', 1, 'rosibosi'),
('dani_kostov@gmail.bg', 0, 'Loser12345', 1, 'dankata'),
('silvia_wolf@gmail.bg', 0, 'JinxWasHere19', 1, 'wolvesgirl'),
('ivanivanov@gmail.bg', 0, 'IvanIvanov1973', 2, 'ivanivanov'),
('dimitarPetrov@gmail.bg', 0, 'dimiPetrov123', 2, 'dimitarpetr'),
('veselina_pavlova@gmail.com', 0, 'VeselaPav9875', 2, 'veselinap'),
('yana_evgenieva@gmail.com', 0, 'YanaEvgenieva4', 2, 'yanaevgeni'),
('vasil_vasilev@gmail.com', 0, 'VaskoVasilev2121', 2, 'vasilvasil'),
('stanimir_gospodinov@gmail.com', 0, 'StaniGospodinov1', 2, 'stanimir'),
('anita_peneva@gmail.com', 0, 'AnitaPeneva90', 2, 'anitapeneva');

INSERT or IGNORE INTO App_student (user_id, faculty_num)
VALUES
(4, '1MI0600044'),
(5, '9MI0700010'),
(6, '4MI0600104'),	
(2, '2MI0800231');

INSERT INTO App_roomevent (host_id, room_id, date, start_time, end_time, topic)
VALUES
(1, 1, '2025-01-27', '10:00:00', '12:00:00', 'Въведение в Алгоритмите'),
(3, 2, '2025-01-28', '14:00:00', '16:00:00', 'Основи на Линейната Алгебра'),
(7, 3, '2025-01-29', '11:00:00', '15:00:00', 'Машинно Обучение с учител'),
(8, 4, '2025-01-30', '08:00:00', '10:00:00', 'Невронни мрежи за напреднали'),
(9, 5, '2025-01-31', '12:00:00', '15:00:00', 'Ламбда функции в Haskell'),
(10, 6, '2025-02-03', '09:00:00', '12:00:00', 'Възникване на Математиката'), 
(11, 7, '2025-02-04', '13:00:00', '16:00:00', 'Сечение на Множества'),
(12, 8, '2025-02-05', '15:00:00', '17:00:00', 'Същност на Размитите Множества'),
(13, 2, '2025-02-06', '10:00:00', '12:00:00', 'TCP/IP'),
(13, 1, '2025-02-07', '08:00:00', '11:00:00', 'Матрици и Детерминанти'),
(3, 5, '2025-02-10', '09:00:00', '10:00:00', 'Кортежи'),
(7, 3, '2025-02-11', '11:00:00', '13:00:00', 'Условни оператори в C++'),
(10, 7, '2025-02-12', '14:00:00', '16:00:00', 'Дървета на решенията'),
(1, 2,'2025-02-13', '12:00:00', '14:00:00', 'Обединение на множества'),
(12, 8, '2025-02-14', '10:00:00', '12:00:00', 'Смисълът на математиката');

INSERT or IGNORE INTO App_lessonevent (roomevent_ptr_id, lecture_type_id, subject_id)
VALUES
(1, 1, 5),
(2, 4, 2),
(5, 1, 4),
(6, 1, 8),
(7, 1, 1),
(8, 2, 3),
(9, 3, 5),
(10, 1, 2),
(11, 3, 4),
(12, 3, 7),
(13, 2, 6),
(14, 2, 1),
(15, 4, 8),
(3, 3, 6);
