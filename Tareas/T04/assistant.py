import random
from collections import defaultdict
from event import PublishGradesEvent
import math


class Assistant:
    """
    Es la clase que describe a un ayudante
    """
    def __init__(self, name):
        self.name = name
        self.topics = random.sample(range(1, 13), 3)


class TeachingAssistant(Assistant):
    """
    Clase que representa un tareo.
    """
    def __init__(self, name):
        super(TeachingAssistant, self).__init__(name)


class HomeworkAssistant(Assistant):
    """
    Ayudante de cátedra
    """
    def __init__(self, name):
        super(HomeworkAssistant, self).__init__(name)


class CoordinationAssistant(Assistant):
    """
    Ayudante coordinador. Se encarga de almacenar las notas que recibe de los
    otros ayudantes y actualiza las notas.
    """
    def __init__(self, name, students, get_delay, get_discount, add_event,
                 get_difficulty):
        self.add_event = add_event
        self.students = students
        self.homework_grades = defaultdict(list)
        self.quiz_grades = defaultdict(list)
        self.activity_grades = defaultdict(list)
        self.get_difficulty = get_difficulty

        self.assessments = {'HW': {}, 'AC': {}, 'Q': {}, 'EX': {}}
        self.get_delay = get_delay
        self.get_discount = get_discount

        self.homework_data = {}
        self.quiz_data = {}
        self.activity_data = {}
        self.discount_dates = []

        self.dates = {'HW': [], 'Q': [], 'AC': [], 'EX': []}

        self.grades_history = {'HW': {}, 'AC': {}, 'Q': {}, 'EX': {}}

        self.discount_info = None
        self.discount_time = 1
        self.delta = {}
        self.discount_count = 0
        super(CoordinationAssistant, self).__init__(name)

    def publish_grades(self, time, assessment_type, assessment_num):
        """
        Se encarga de actualizar las notas. Cada alumno actualiza su promedio.
        Decide si hacer o no un descuento. Tambien se encarga de programar un
        nuevo evento de publicacion de notas si decide retrasarla.
        :param time: Tiempo actual (día)
        :param assessment_type: String que representa el tipo de evaluacion
        :param assessment_num:
        :return:
        """
        assessment_str = {
            'HW': 'de la Tarea',
            'AC': 'de la Actividad',
            'Q': 'del Control'
        }

        if self.discount_info is not None:
            for a in self.assessments[self.discount_info[0]][self.discount_info[1]]:
                a.grade += self.delta[a.student_id]
            fix_str = assessment_str[self.discount_info[0]]
            self.delta = {}
            print('Se eliminó el descuento de las notas {} {}'
                  .format(fix_str, self.discount_info[1]))
            self.discount_info = None

        discount = self.get_discount()
        if discount and assessment_type != 'EX' and \
                time - self.discount_time > 30 and self.discount_count < 3:
            discount_str = assessment_str[assessment_type]
            print('Se realizó un descuento despiadado a la notas {} {}'
                  .format(discount_str, assessment_num))
            self.discount_count += 1
            self.discount_time = time
            self.discount_info = (assessment_type, assessment_num)
            for a in self.assessments[assessment_type][assessment_num]:
                if a.grade < 1.5:
                    self.delta[a.student_id] = a.grade - 1
                else:
                    self.delta[a.student_id] = 0.5
                a.grade -= self.delta[a.student_id]

        temp = self.assessments[assessment_type][assessment_num]
        for student in self.students:
            for assessment in temp:
                if assessment.student_id == student.id:
                    student.assessments[assessment_type][assessment_num] \
                        = assessment

        self.dates[assessment_type].append(math.ceil(time / 7))

    def receive_grades(self, assessment_list, time):
        """
        Recibe el conjunto de evaluaciones y el tiempo. Guarda las
        evaluaciones. Programa el evento de publicar las notas considerando
        si decidio o no retrasar el envio. Si no retrasa la publicacion, el
        tiempo del nuevo evento es el mismo.
        :param assessment_list: Lista de evaluaciones
        :param time:
        :return:
        """
        assessment_type = assessment_list[0]
        assessment_num = assessment_list[1]

        self.assessments[assessment_type][assessment_num] = \
            assessment_list[2:]

        info = (assessment_type, assessment_num)

        info_str = {
            'HW': 'de la Tarea {}'.format(assessment_num),
            'Q': 'del Control'.format(assessment_num),
            'AC': 'de la Actividad'.format(assessment_num),
            'EX': 'del Examen'
        }[assessment_type]

        delay = self.get_delay()
        if delay and assessment_type != 'EX':
            self.add_event(PublishGradesEvent(time + delay,
                           self.students, self.publish_grades, info,
                           self.add_event, self.receive_grades,
                           self.get_difficulty))
            print('Se retraso la entrega de notas {} en {} día(s).'
                  .format(info_str, delay))
        else:
            self.add_event(PublishGradesEvent(time, self.students,
                           self.publish_grades, info, self.add_event,
                           self.receive_grades, self.get_difficulty))



