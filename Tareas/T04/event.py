import random
import math

'''
En este módulo se encuentran las clases que representan los eventos del
simulador.
'''


class SendGradesEvent:
    """
    Esta clase representa el proceso el evento de enviar las notas al
    coordinador. Su principal función es proporcionar un conjunto de
    evaluaciones al coordinador para que el actualice las notas.
    """
    homework_levels = {}
    quiz_levels = {}
    activity_levels = {}

    levels = {'HW': {}, 'AC': {}, 'Q': {}, 'EX': {}}

    def __init__(self, time, assessments, receive_grades):
        self.time = time
        self.priority = 3
        self.assessments = assessments
        self.receive_grades = receive_grades

    def simulate(self):
        """
        En este método el coordinador recibe una lista de objetos Assessment
        que representa una evaulación mediante la función receive_grades que le
        pertenece al coordinador.
        """
        week = math.ceil(self.time / 7)
        assessment_type = self.assessments[0]
        assessment_num = self.assessments[1]
        level = SendGradesEvent.levels[assessment_type][assessment_num]
        for assessment in self.assessments[2:]:
            assessment.grade = max((assessment.progress / level) * 7, 1)
            if assessment.grade > 7:
                assessment.grade = 7
        self.receive_grades(self.assessments, self.time)

        print_info = {
            'HW': 'la Tarea',
            'Q': 'el Control',
            'AC': 'la Actividad',
            'EX': 'el Examen'
        }[assessment_type]

        print('Se enviaron las notas de {} {} la semana {}.'
              .format(print_info, assessment_num, week))


class LectureEvent:
    """
    LectureEvent encapsula las distintas actividades que ocurren en la cátedra.
    Esta clase programa los eventos SendGradesEvent para los controles y las
    actividades. Esto se realiza con el metodo add_event que la clase recibe
    como argumento.
    """
    temp_quiz_count = 0
    num_quizzes = 0
    max_num_quizzes = 5
    quiz_dates = {}

    def __init__(self, time, students, add_event, receive_grades):
        self.time = time
        self.priority = 1
        self.students = students
        self.add_event = add_event
        self.receive_grades = receive_grades

    def simulate(self):
        """
        Primero decidimos si hay control o no. Si hay control sorpresa, las
        variables de clase se encargan de controlar que no existan dos
        controles consecutivos. Luego, se programa el evento de envío de notas
        del control. Después de eso, se realiza la cátedra y luego la
        actividad. Para esta última se programa igual el evento de envío de
        notas.
        """
        for student in self.students:
            student.update_topics_knowledge(self.time)
        week = math.ceil(self.time / 7)
        if LectureEvent.num_quizzes < LectureEvent.max_num_quizzes:
            new_quiz = random.randint(0, 1)
            if LectureEvent.temp_quiz_count == 3:
                LectureEvent.temp_quiz_count = 0
                new_quiz = 0
            if new_quiz:
                LectureEvent.num_quizzes += 1
                LectureEvent.quiz_dates[LectureEvent.num_quizzes] = self.time
                print('¡Control {}! la semana {}.'.
                      format(LectureEvent.num_quizzes, week))
                LectureEvent.temp_quiz_count += 1
                quiz_list = ['Q', LectureEvent.num_quizzes]
                for student in self.students:
                    quiz = student.do_quiz(week, LectureEvent.num_quizzes)
                    quiz_list.append(quiz)
                    # student.quiz_list.append(quiz)
                self.add_event(SendGradesEvent(self.time + 14, quiz_list,
                                               self.receive_grades))

        for student in self.students:
            student.take_lecture(week, self.time)
            student.num_questions = round(random.triangular(1, 10, 3))

        students = [s for s in self.students if s.num_questions > 0]
        max_num_questions = 600
        attended_students = []
        while students and max_num_questions > 0:
            student = random.choice(students)
            student.num_questions -= 1
            max_num_questions -= 1
            if student not in attended_students:
                attended_students.append(student)
            students = [s for s in self.students if s.num_questions > 0]

        num_attended_students = len(attended_students)
        num_of_students_with_answers = len(students)
        print('Se resolvieron dudas de {} estudiantes en la clase de la semana'
              ' {}. {} estudiantes quedaron con dudas'.format(
               num_attended_students, week, num_of_students_with_answers))

        activity_list = ['AC', week]
        for student in self.students:
            activity = student.do_activity(week)
            activity_list.append(activity)
            # student.activity_list.append(activity)

        self.add_event(SendGradesEvent(self.time + 14, activity_list,
                                       self.receive_grades))


class ActivityReunionEvent:
    """
    La clase ActivityReunionEvent, tal como sugiere su nombre, representa
    la reunion de ayudantes en la que deciden la dificultad de la actividad.
    Las dificultades se almacenan en la clase SendGradesEvent para poder
    revisar las evaluaciones antes de enviarlas al coordinador.
    """
    def __init__(self, time, get_difficulty):
        self.time = time
        self.get_difficulty = get_difficulty
        self.priority = 1

    def simulate(self):
        """
        Definimos las difucultades
        """
        week = math.ceil(self.time / 7)
        difficulty = self.get_difficulty(week)
        level = 7 + (random.randint(1, 5) / difficulty)
        SendGradesEvent.levels['AC'][week] = level
        SendGradesEvent.levels['Q'][LectureEvent.num_quizzes + 1] = level
        print('Se reunieron los ayudantes para definir la dificultad de la '
              'actividad {} la semana {}'.format(week, week))


class SubmitHomeworkEvent:
    """
    La clase representa la subida de la tarea por parte de los alumnos. Se
    reprograma el evento en caso de que se acepte la extensión del plazo. De
    otra forma, se programa el envío de las notas por parte de los ayudantes.
    """
    deadline_extended = False
    homework_num = 1

    def __init__(self, time, add_event, students, receive_grades):
        self.time = time
        self.priority = 2
        self.add_event = add_event
        self.homework_num = SubmitHomeworkEvent.homework_num
        self.students = students
        self.receive_grades = receive_grades
        SubmitHomeworkEvent.homework_num += 1

    def simulate(self):
        """

        """
        num_extension_requests = 0
        homework_list = ['HW', self.homework_num]
        for student in self.students:
            homework = student.do_homework(self.homework_num, self.time)
            homework_list.append(homework)
            if not SubmitHomeworkEvent.deadline_extended:
                num_extension_requests += (homework.progress <= 50)

        ratio = num_extension_requests / len(self.students)

        if ratio >= 0.8 and not SubmitHomeworkEvent.deadline_extended and \
                random.random() <= 0.2:
            print('El plazo de la Tarea {} se extendió'
                  .format(self.homework_num))
            SubmitHomeworkEvent.deadline_extended = True
            # El evento de repograma a si mismo.
            self.time += 2
            self.add_event(self)
        else:
            """
            Tambien se encarga de programar el evento de enviar las notas al
            coordinador
            """
            self.add_event(SendGradesEvent(self.time + 14, homework_list,
                                           self.receive_grades))
            print('{} alumnos entregaron la Tarea {}'.format(
                len(self.students), self.homework_num))


class HomeworkReunionEvent:
    """
    Esta clase representa la reunión de tareos.
    """
    homework_num = 1

    def __init__(self, time, get_difficulty):
        self.time = time
        self.priority = 1
        self.get_difficulty = get_difficulty
        self.homework_num = HomeworkReunionEvent.homework_num
        HomeworkReunionEvent.homework_num += 1

    def simulate(self):
        """
        Se define la dificultad de la tarea en la variable de la clase
        SendGradesEvent.
        """
        week = math.ceil(self.time / 7)
        topic_a, topic_b = self.homework_num * 2, self.homework_num * 2 - 1

        difficulty = \
            (self.get_difficulty(topic_a) + self.get_difficulty(topic_b)) / 2
        level = 7 + (random.randint(1, 5) / difficulty)

        SendGradesEvent.levels['HW'][self.homework_num] = level
        print('Se subió la Tarea {} la semana {}.'.
              format(self.homework_num, week))


class AssistantshipEvent:
    """
    La ayudantía. Este evento se encarga de modificar el manejo de contenidos
    si es que corresponde.
    """
    def __init__(self, time, teaching_assistants, students):
        self.time = time
        self.priority = 2
        self.teaching_assistants = teaching_assistants
        self.students = students

    def simulate(self):
        """
        Escoge los ayudantes por cada sección y define los bonus
        correspondientes.
        """
        week = math.ceil(self.time / 7)
        topic = week - 1
        tips_change = 1
        assistants = random.sample(self.teaching_assistants, 2)
        if topic in assistants[0].topics:
            tips_change *= 1.1
        if topic in assistants[1].topics:
            tips_change *= 1.1

        for student in self.students:
            student.topic_knowledge[topic] *= tips_change
        if tips_change > 1:
            change = (tips_change - 1) * 100
            print('Los alumnos asistieron a la ayudantía {} en la semana {}'
                  ' y aumentaron su manejo de contenidos en un {}%'.format(
                   topic, week, round(change, 3)))
        else:
            print('Los alumnos asistieron a la ayudantía {} en la semana {}'.
                  format(topic, week))


class DropCourseEvent:
    """
    Representa el retiro del curso.
    """
    def __init__(self, time, students):
        self.time = time
        self.priority = 3
        self.students = students

    def simulate(self):
        """
        Llamamos el método evaluate_withdrawal que nos dice si el alumno
        decidio botar el ramo. Si es así, lo eliminamos de la lista de
        estudiantes.
        """
        num_of_withdrawals = 0
        for student in self.students:
            decision = student.evaluate_withdrawal()
            if decision is True:
                num_of_withdrawals += 1
                self.students.remove(student)

        print('{} alumnos botaron el curso la semana {}'.
              format(num_of_withdrawals, math.ceil(self.time / 7)))


class PartyEvent:
    """
    Esta clase representa la fiesta.
    """
    def __init__(self, time, students):
        self.time = time
        self.priority = 1
        self.students = students

    def simulate(self):
        """
        Se eligen 50 estudiantes y se procede a modificar el nivel de
        programación y a quitar 2 horas de trabajo.
        """
        students = self.students
        if len(self.students) > 50:
            students = random.sample(self.students, 50)

        for student in students:
            students.programming_level *= 0.85
            if student.work_hours < 2:
                student.work_hours = 0
            else:
                student.work_hours -= 2


class SoccerGameEvent:
    pass


class WaterShutdownEvent:
    pass


class UpdateStudentsEvent:
    """
    Esta clase se usa para actualizar el estado de el estudiante. Este evento
    se programa para cada domingo.
    """
    def __init__(self, time, students):
        self.priority = 10
        self.time = time
        self.students = students

    def simulate(self):
        """
        Llama el método update de Student
        """
        for student in self.students:
            student.update()


class PublishGradesEvent:
    """
    Representa la publicación de las notas por parte del coordinador. Se
    reprograma el evento si se decide atrasar la entrega.
    """
    def __init__(self, time, students, publish_grades, info, add_event,
                 receive_grades, get_difficulty):
        self.time = time
        self.priority = 10
        self.students = students
        self.publish_grades = publish_grades
        self.assessment_type = info[0]
        self.assessment_num = info[1]
        self.add_event = add_event
        self.receive_grades = receive_grades
        self.get_difficulty = get_difficulty

    def simulate(self):
        """
        Llamamos el método publish_grades del coordinador y le entregamos como
        argumento el tipo de evaluación y el número. Luego, se procede a
        actualizar el promedio y la confianza de cada estudiante.
        """
        week = math.ceil(self.time / 7)
        self.publish_grades(self.time, self.assessment_type,
                            self.assessment_num)

        info_str = {
            'HW': 'la Tarea',
            'Q': 'el Control',
            'AC': 'la Actividad',
            'EX': 'el Examen'
        }[self.assessment_type]

        print('Dr. Mavrakis publicó las notas de {} {} la semana {}'
              .format(info_str, self.assessment_num, week))

        for student in self.students:
            student.recalculate_confidence()
            student.recalculate_gpa()
            student.gpa_history[self.time] = student.gpa
        if self.assessment_type == 'AC' and self.assessment_num == 4:
            num_of_withdrawals = 0
            for student in self.students:
                x = student.evaluate_withdrawal()
                if x:
                    num_of_withdrawals += 1
                    self.students.remove(student)
            print('**** {} alumnos botaron el ramo. ****'
                  .format(num_of_withdrawals))

        if self.assessment_type == 'HW' and self.assessment_num == 6:
            self.add_event(ExamEvent(self.time + 5, self.students,
                                     self.add_event, self.receive_grades,
                                     self.get_difficulty))


class ExamEvent:
    """
    Es el examen final del curso.
    """
    def __init__(self, time, students, add_event, receive_grades,
                 get_difficulty):
        self.time = time
        self.students = students
        self.priority = 1
        self.topics = None
        self.add_event = add_event
        self.receive_grades = receive_grades
        self.get_difficulty = get_difficulty

    def choose_topics(self):
        """
        Este método se encarga de elegir los contenidos correspondientes para
        armar las preguntas. Se calclan los promedios de las tareas, controles
        y actividades. En el caso de los controles, se consideran todos los
        contenidos anteriores a la fecha de rendición de este. Finalmente,
        elegimos los mejores dos contenidos y los peores 6.
        """
        hw_mean = []
        for i in range(1, 7):
            mean = sum([s.assessments['HW'][i].grade for s in self.students])
            mean /= len(self.students)
            hw_mean.append(mean)
            hw_mean.append(mean)

        ac_mean = []
        for i in range(1, 13):
            mean = sum([s.assessments['AC'][i].grade for s in self.students])
            mean /= len(self.students)
            ac_mean.append(mean)

        q_mean = []
        index = 1
        for i in range(1, 13):
            index = math.ceil(i / LectureEvent.quiz_dates[index])
            if index <= LectureEvent.num_quizzes:
                mean = sum(
                    [s.assessments['Q'][index].grade for s in self.students])
                mean /= len(self.students)
                q_mean.append(mean)
                index += i >= LectureEvent.quiz_dates[index]
            else:
                q_mean.append(0)

        mean_topics = {}
        for i in range(1, 13):
            a, b, c = hw_mean[i - 1], ac_mean[i - 1], q_mean[i - 1]
            mean_topics[i] = (a + b + c) / len([x for x in [a, b, c] if x > 0])

        topics = []
        for i in range(2):
            topic = max(mean_topics, key=mean_topics.get)
            topics.append(topic)
            del mean_topics[topic]

        for i in range(6):
            topic = min(mean_topics, key=mean_topics.get)
            topics.append(topic)
            del mean_topics[topic]

        level = 0
        for topic in topics:
            level += self.get_difficulty(topic)
        level /= 8
        SendGradesEvent.levels['EX'][0] = level

        self.topics = topics

    def simulate(self):
        """
        Se llama choose_topics para definir los contenidos de las preguntas.
        Luego, le indicamos a cada estudiante que realice el examen y
        programamos el evento de envío de notas.
        """
        week = math.ceil(self.time / 7)
        self.choose_topics()
        exam_list = ['EX', 0]
        for student in self.students:
            exam = student.take_exam(self.topics)
            exam_list.append(exam)

        self.add_event(SendGradesEvent(self.time + 14, exam_list,
                                       self.receive_grades))
        print('Alumnos rinden examen final del curso la semana', week)


class OfficeReunionEvent:
    """
    OfficeReunionEvent es la clase que representa la reunion de los alumnos con
    los profesores.
    """
    def __init__(self, time, students, professors):
        self.time = time
        self.students = students
        self.professors = professors
        self.priority = 1

    def simulate(self):
        """
        Se encarga de definir grupos de alumnos de acuerdo al profesor que
        cada alumno eligió. Después de eso, llamamos el método attend_students
        que recibe el grupo de alumnos y realiza los cambios corresponfientes.
        """
        week = math.ceil(self.time / 7)
        groups = {}
        for professor in self.professors:
            groups[professor.name] = []

        for student in self.students:
            if student.visit_professor():
                professor = random.choice(self.professors)
                groups[professor.name].append(student)

        for professor in self.professors:
            professor.attend_students(groups[professor.name], week)
