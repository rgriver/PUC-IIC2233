import random
import math
from assessment import Assessment


class Student:
    """
    Es la clase que representa a un alumno. Contiene muchas variables que
    almacenan notas, confianza, nivel de programacion.....
    """
    id = 0

    def __init__(self, name, section, get_units, get_hours,
                 get_confidence, get_difficulty, get_grade):
        self.name = name
        self.id = Student.id
        self.get_difficulty = get_difficulty
        self.personality = random.choice(['Efficient',
                                          'Artistic',
                                          'Theoretical'])
        self.get_hours = get_hours
        self.get_grade = get_grade
        self.init_confidence = get_confidence()
        self.confidence = self.init_confidence
        self.units = get_units()
        self.work_hours = get_hours(self.units)
        self.programming_level = random.randint(2, 10)
        self.topic_knowledge = {}
        self.section = section
        self.prob_of_paying_attention = random.random()
        self.prob_of_visiting = random.random()
        self.gpa = None
        self.active = True
        self.num_questions = 0
        self.homework_grades = {}
        self.quiz_grades = {}
        self.activity_grades = {}
        self.exam_grade = None
        self.hours_history = [self.work_hours]
        self.homework_list = []
        self.quiz_list = []
        self.activity_list = []
        self.exam = None
        self.assessments = {'HW': {}, 'AC': {}, 'Q': {}, 'EX': {}}
        self.hw_history = []
        self.ac_history = []
        self.q_history = []
        self.dates = {'HW': [], 'Q': [], 'AC': [], 'EX': []}
        self.topic_hours_history = {}
        self.programming_level_history = []
        self.gpa_history = {}
        Student.id += 1

    def do_homework(self, homework_num, time):
        """
        Hacer la tarea. Calcla las horas actuales de trabajo, los progresos
        y la nota esperada. Retorna una evaluacion.
        :param homework_num:
        :param time:
        :return: tarea
        """
        topic_a, topic_b = homework_num * 2, homework_num * 2 - 1
        temp_days = 14
        days = time % 7
        if days == 0:
            days = 7
        index = -1
        homework_hours = days * self.hours_history[index] * 0.7 / 7
        temp_days -= days
        while temp_days > 0:
            index -= 1
            days = min(7, temp_days)
            homework_hours += days * self.hours_history[index] * 0.7 / 7
            temp_days -= days

        topic_knowledge = (self.topic_knowledge[topic_a] +
                           self.topic_knowledge[topic_b]) / 2

        pep8_progress = 0.5 * homework_hours + 0.5 * self.programming_level

        topics_progress = 0.7 * topic_knowledge
        topics_progress += 0.1 * self.programming_level
        topics_progress += 0.2 * homework_hours

        functionality_progress = 0.5 * topic_knowledge
        functionality_progress += 0.1 * self.programming_level
        functionality_progress += 0.4 * homework_hours

        progress = 0.4 * functionality_progress + 0.4 * topics_progress + \
            0.2 * pep8_progress

        expected_grade_a = self.get_grade(topic_a, round(homework_hours))
        expected_grade_b = self.get_grade(topic_a, round(homework_hours))

        expected_grade = (expected_grade_a + expected_grade_b) / 2

        homework = Assessment(homework_num, self.id, progress, expected_grade)

        return homework

    def do_activity(self, topic):
        """
        Actividad en clase. Similar a la tarea. Calcula los progresos y las
        horas de trabajo, la nota esperada, etc.
        :param topic:
        :return:
        """
        topic_hours = self.hours_history[-1] * 0.3 / 7
        self.topic_hours_history[topic] = topic_hours

        pep8_progress = 0.7 * self.topic_knowledge[topic] + \
            0.2 * self.programming_level + \
            0.1 * self.confidence

        functionality_progress = 0.3 * self.topic_knowledge[topic] + \
            0.6 * self.programming_level + \
            0.1 * self.confidence

        topics_progress = 0.7 * self.topic_knowledge[topic] + \
            0.2 * self.programming_level + \
            0.1 * self.confidence

        progress = 0.4 * functionality_progress + 0.4 * topics_progress + \
            0.2 * pep8_progress

        expected_grade = self.get_grade(topic, round(topic_hours))

        activity = Assessment(topic, self.id, progress, expected_grade)

        return activity

    def do_quiz(self, topic, num):
        """
        El control sorpresa. Lo mismo que en las tareas y los controles
        :param topic: contenido: int
        :param num: numero de evaluacion
        :return:
        """
        topic_hours = 4 * self.hours_history[-1] * 0.3 / 7

        topics_progress = 0.7 * self.topic_knowledge[topic] + \
            0.05 * self.programming_level + \
            0.25 * self.confidence

        functionality_progress = 0.3 * self.topic_knowledge[topic] + \
            0.2 * self.programming_level + 0.5 * self.confidence

        progress = 0.3 * functionality_progress + 0.7 * topics_progress

        expected_grade = self.get_grade(topic, round(topic_hours))

        quiz = Assessment(num, self.id, progress, expected_grade)

        return quiz

    def take_exam(self, topics):
        """
        Realiza el examen. Calcula los progresos y retorna una evaluacion.
        :param topics:
        :return:
        """
        progress = 0
        topics_progress = functionality_progress = 0
        for topic in topics:
            topics_progress += 0.5 * self.topic_knowledge[topic] + \
                0.1 * self.programming_level + \
                0.4 * self.confidence
            functionality_progress += 0.3 * self.topic_knowledge[topic] + \
                0.2 * self.programming_level + \
                0.5 * self.confidence
            progress += 0.3 * functionality_progress + 0.7 * topics_progress
        progress /= 8

        expected_grade = 0
        for i in self.topic_hours_history.items():
            if i[0] in topics:
                expected_grade += self.get_grade(i[0], i[1])
        expected_grade /= 8

        exam = Assessment(1, self.id, progress, expected_grade)
        return exam

    def evaluate_withdrawal(self):
        """
        Se encarga de decidir si botar el ramo o no
        :return:
        """
        s = (self.confidence * 0.8) + (self.gpa * 0.2)
        if s < 20:
            self.active = True
            return True
        else:
            return False

    def request_deadline_extension(self):
        """
        Se implementa en otra parte
        :return:
        """
        pass

    def take_lecture(self, topic, time):
        """
        Modifica los niveles de programacion.
        :param topic:
        :param time:
        :return:
        """
        day = time % 7
        if day == 0:
            day = 7
        topic_hours = 0.3 * self.work_hours * day / 7
        self.topic_knowledge[topic] = (1 / self.get_difficulty(topic)) \
            * topic_hours
        if random.random() <= self.prob_of_paying_attention:
            self.topic_knowledge[topic] *= 1.1

    def update(self):
        """
        Actualiza las horas de trabajo, nivel de programacion.
        :return:
        """
        self.work_hours = self.get_hours(self.units)
        self.hours_history.append(self.work_hours)
        self.programming_level_history.append(self.programming_level)

    def recalculate_confidence(self):
        """
        Recalculo de la confianza
        :return:
        """
        self.confidence = self.init_confidence
        for activity in self.assessments['AC'].values():
            self.confidence += 3 * (activity.grade - activity.expected_grade)

        for homework in self.assessments['HW'].values():
            self.confidence += 5 * (homework.grade - homework.expected_grade)

        for quiz in self.assessments['Q'].values():
            self.confidence += quiz.grade - quiz.expected_grade

    def recalculate_gpa(self):
        """
        Recalcula el promedio
        :return:
        """
        if len(list(self.assessments['HW'].values())) > 0:
            hw_gpa = sum([x.grade for x in self.assessments['HW'].values()])
            hw_gpa /= len(list(self.assessments['HW'].values()))
            hw_k = 15
        else:
            hw_gpa = hw_k = 0

        if len(list(self.assessments['Q'].values())) > 0:
            q_gpa = sum([x.grade for x in self.assessments['Q'].values()])
            q_gpa /= len(list(self.assessments['Q'].values()))
            q_k = 20
        else:
            q_gpa = q_k = 0

        if len(list(self.assessments['AC'].values())) > 0:
            ac_gpa = sum([x.grade for x in self.assessments['AC'].values()])
            ac_gpa /= len(list(self.assessments['AC'].values()))
            ac_k = 25
        else:
            ac_gpa = ac_k = 0

        if self.assessments['EX']:
            exam = self.assessments['EX'][0].grade
            exam_k = 15
        else:
            exam = exam_k = 0

        self.gpa = (ac_gpa * ac_k) + (hw_gpa * hw_k) + (q_gpa * q_k) + \
                   (exam * exam_k)
        self.gpa /= ac_k + hw_k + q_k + exam_k

    def update_topics_knowledge(self, time):
        """
        Actializa el manejo de contenidos
        :param time:
        :return:
        """
        day = time % 7
        if day == 0:
            day = 7
        topic = math.ceil(time / 7)
        topic_hours = 0.3 * self.work_hours * day / 7
        self.topic_knowledge[topic] = (1 / self.get_difficulty(topic)) \
            * topic_hours

    def visit_professor(self):
        """
        Decide si visitar al profesor o no.
        :return:
        """
        if self.gpa is None:
            return False
        if self.gpa <= 5:
            return True
        if self.gpa > 5 and random.random() <= 0.2:
            return True
        return False

