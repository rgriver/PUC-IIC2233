import csv
from parameters import Parameters
from professor import Professor
from student import Student
from assistant import CoordinationAssistant, TeachingAssistant, \
    HomeworkAssistant
from collections import defaultdict
from event import *
import random
from matplotlib import pyplot as plt


class Simulator:
    """
    Clase principal que se encarga de almacenar los metodos que desencadenan
    los eventos. Contiene varias variables de estado.
    """
    def __init__(self):
        Student.id = 0
        self.time = 0
        self.homework_num = None
        self.students = []
        self.num_of_withdrawals = 0
        self.homework_assistants = []
        self.teaching_assistants = []
        self.professors = []
        self.coordinator = None
        self.parameters = Parameters()
        self.sections = []
        self.set_people()
        self.init_confidence = sum([s.init_confidence for s in self.students])
        self.init_confidence /= len(self.students)
        self.num_init_students = len(self.students)
        self.num_extension_requests = 0
        self.deadline_extended = False
        self.events = []
        self.topic = 1
        self.week = 1
        self.homework = {}
        self.quizzes = {}
        self.activities = {}
        self.homework_levels = {}
        self.quiz_levels = {}
        self.activity_levels = {}
        self.scenario_results = {}

    def run(self):
        self.__init__()
        self.initialize_events()
        while self.events:
            event = self.events.pop(0)
            self.time = event.time
            event.simulate()
        self.print_results()

    @staticmethod
    def get_parameters(self, scenario):
        data = {}
        with open('escenarios.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            num_of_scenarios = len(list(next(reader))) - 1
            if scenario > num_of_scenarios:
                return None
            for row in reader:
                if row[scenario] != '-':
                    data[row[0]] = row[scenario]
        return data

    def set_people(self):
        """
        Se encarga de crear a los integrantes del curso y los guarda en las
        variables correspondientes.
        :return:
        """
        id = 0
        with open('integrantes.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[1] == 'Profesor':
                    self.professors.append(Professor(row[0], int(row[2])))
                elif row[1] == 'Alumno':
                    self.students.append(Student(
                        row[0],
                        int(row[2]),
                        self.parameters.get_units,
                        self.parameters.get_hours,
                        self.parameters.get_confidence,
                        self.parameters.get_difficulty,
                        self.parameters.get_grade))
                    if int(row[2]) not in self.sections:
                        self.sections.append(int(row[2]))
                elif row[1] == 'Coordinación':
                    self.coordinator = CoordinationAssistant(
                        row[0],
                        self.students,
                        self.parameters.get_delay,
                        self.parameters.get_discount,
                        self.add_event,
                        self.parameters.get_difficulty)
                elif row[1] == 'Tareas':
                    self.homework_assistants.append(HomeworkAssistant(row[0]))
                else:
                    self.teaching_assistants.append(TeachingAssistant(row[0]))

    def add_event(self, event):
        """
        Este metodo añade un evento a la lista de eventos y procede a
        ordenarlos de acuerdo al tiempo y luego considerando una prioridad
        definida en cada clase.
        :param event:
        :return:
        """
        self.events.append(event)
        self.events.sort(key=lambda x: (x.time, x.priority))

    def print_grades(self, student_id):
        """
        Imprime la informacion de notas de cada alumno
        :param student_id: ID del alimno (int)
        :return:
        """
        info_student = None
        for student in self.students:
            if student_id == student.id and student.active:
                info_student = student
        if info_student is None:
            print('El estudiante botó el ramo.')
        else:
            print(info_student.name)
            print('Notas:')
            for hw in info_student.assessments['HW'].values():
                print('T{}: {}'.format(hw.num, round(hw.grade, 3)))
            for q in info_student.assessments['Q'].values():
                print('C{}: {}'.format(q.num, round(q.grade, 3)))
            for ac in info_student.assessments['AC'].values():
                print('AC{}: {}'.format(ac.num, round(ac.grade, 3)))
            if info_student.assessments['EX']:
                print('EX: {}'.format(info_student.assessments['EX'][0].grade))
                print('Promedio final: ', round(info_student.gpa, 4))

    def initialize_events(self):
        """
        Se encarga de reiniciar los valores de las variables de clase de los
        eventos para generar una nueva simulacion.
        :return:
        """
        SendGradesEvent.homework_levels = {}
        SendGradesEvent.quiz_levels = {}
        SendGradesEvent.activity_levels = {}
        SendGradesEvent.levels = {'HW': {}, 'AC': {}, 'Q': {}, 'EX': {}}

        LectureEvent.temp_quiz_count = 0
        LectureEvent.num_quizzes = 0
        LectureEvent.max_num_quizzes = 5
        LectureEvent.quiz_dates = {}

        SubmitHomeworkEvent.deadline_extended = False
        SubmitHomeworkEvent.homework_num = 1

        HomeworkReunionEvent.homework_num = 1

        for i in range(12, 83, 14):
            self.add_event(HomeworkReunionEvent(i,
                           self.parameters.get_difficulty))

        for i in range(7, 98, 7):
            self.add_event(UpdateStudentsEvent(i, self.students))

        for i in range(4, 82, 7):
            self.add_event(LectureEvent(i, self.students, self.add_event,
                                        self.coordinator.receive_grades))

        for i in range(9, 87, 7):
            self.add_event(AssistantshipEvent(i, self.teaching_assistants,
                                              self.students))

        for i in range(1, 79, 7):
            self.add_event(ActivityReunionEvent(
                i,
                self.parameters.get_difficulty))

        for i in range(26, 97, 14):
            self.add_event(SubmitHomeworkEvent(
                i, self.add_event, self.students,
                self.coordinator.receive_grades
            ))

        for i in range(3, 109, 7):
            self.add_event(OfficeReunionEvent(
                i, self.students, self.professors
            ))

    def analyze_scenarios(self):
        """
        Permite correr la simulacion de los disintos escenarios.
        :return:
        """
        percentages = {}

        num_of_scenarios = self.parameters.get_num_scenarios()
        scenario = 1
        while scenario <= num_of_scenarios:
            print('\n****** ESCENARIO {} ******'
                  .format(scenario - 1))
            self.__init__()
            self.initialize_events()
            self.parameters.set_scenario(scenario)

            while self.events:
                event = self.events.pop(0)
                self.time = event.time
                event.simulate()

            p = sum([s.gpa >= 4 for s in self.students]) / len(self.students)
            p *= 100
            p = round(p, 4)
            percentages[scenario] = p
            scenario += 1
        self.scenario_results = percentages

    def set_num_of_withdrawals(self, num_of_withdrawals):
        self.num_of_withdrawals = num_of_withdrawals

    def print_results(self):
        """
        Imprime en consola los resultados finales. Realiza cálculos con la
        informacion de cada alumno, coordinador...
        :return:
        """
        print('\n******* Estadísticas finales *******')
        num_of_withdrawals = self.num_init_students - len(self.students)
        print('Cantidad de alumnos que botaron el ramo:', num_of_withdrawals)
        print('Promedio de confianza al inicio:', self.init_confidence)
        final_confidence = sum([s.confidence for s in self.students])
        final_confidence /= len(self.students)
        print('Promedio de confianza al final:', final_confidence)

        course_gpa = defaultdict(int)
        for student in self.students:
            for i in student.gpa_history.items():
                course_gpa[i[0]] += i[1]
        for i in course_gpa.items():
            course_gpa[i[0]] /= len(self.students)

        last_month = math.ceil(max(course_gpa) / 30)
        group = {}
        for m in range(1, last_month + 1):
            l = list(course_gpa.items())
            l = [x[1] for x in l if 30 * (m - 1) <= x[0] <= 30 * m]
            group[m] = sum(l) / len(l)

        max_month = max(group, key=group.get)

        print('Mes con mayor aprobación:', max_month)
        print('Porcentaje de aprobación por evaluación')
        for hw in range(1, 7):
            ratio = sum([s.assessments['HW'][hw].grade > 4
                         for s in self.students])
            ratio /= len(self.students)
            percentage = ratio * 100
            print('    T{}: {}%'.format(hw, round(percentage, 4)))

        for ac in range(1, 13):
            ratio = sum([s.assessments['AC'][ac].grade > 4
                         for s in self.students])
            ratio /= len(self.students)
            percentage = ratio * 100
            print('    AC{}: {}%'.format(ac, round(percentage, 4)))

        for q in range(1, LectureEvent.num_quizzes + 1):
            ratio = sum([s.assessments['Q'][q].grade > 4
                         for s in self.students])
            ratio /= len(self.students)
            percentage = ratio * 100
            print('    C{}: {}%'.format(q, round(percentage, 4)))

        ratio = sum([s.assessments['EX'][0].grade > 4
                     for s in self.students])
        ratio /= len(self.students)
        percentage = ratio * 100
        print('    EX: {}%'.format(round(percentage, 4)))

        hw_x = self.coordinator.dates['HW']
        hw_y = []
        for i in range(1, 7):
            mean = sum([s.assessments['HW'][i].grade for s in self.students])
            mean /= len(self.students)
            hw_y.append(mean)
        plt.plot(hw_x, hw_y, 'r', marker='o', label='Tareas')

        q_x = self.coordinator.dates['Q']
        q_y = []
        for i in range(1, LectureEvent.num_quizzes + 1):
            mean = sum([s.assessments['Q'][i].grade for s in self.students])
            mean /= len(self.students)
            q_y.append(mean)
        plt.plot(q_x, q_y, 'g', marker='o', label='Controles')

        ac_x = self.coordinator.dates['AC']
        ac_y = []
        for i in range(1, 13):
            mean = sum([s.assessments['AC'][i].grade for s in self.students])
            mean /= len(self.students)
            ac_y.append(mean)
        plt.plot(ac_x, ac_y, 'b', marker='o', label='Actividades')
        plt.legend(loc='upper left')
        plt.show()

    def print_best_scenario(self):
        best_scenario = max(self.scenario_results,
                            key=self.scenario_results.get)

        sorted_scenarios = list(self.scenario_results.items())
        sorted_scenarios = sorted(sorted_scenarios, key=lambda x: x[1])

        for scenario in sorted_scenarios:
            extra_left = extra_right = ''
            if scenario[0] == best_scenario:
                extra_right = '*** Maximiza la cantidad de aprobaciones'

            print('Escenario {}: {}% {}'
                  .format(scenario[0], scenario[1], extra_right))

    def print_characteristics(self, student_id):
        """
        Imprime caracteristicas de cada alumno.
        :param student_id:
        :return:
        """
        info_student = None
        for student in self.students:
            if student_id == student.id and student.active:
                info_student = student
        if info_student is None:
            print('El estudiante botó el ramo.')
        else:
            programming_mean = sum(info_student.programming_level_history)
            if info_student.programming_level_history:
                programming_mean /= len(info_student.programming_level_history)
            else:
                programming_mean = info_student.programming_level
            print('Nivel de programación promedio:', programming_mean)
            print('Confianza:', info_student.confidence)
            print('Manejo de contenidos:')
            topic_str = {
                1: '    OOP:',
                2: '    Herencia, composición y agregación:',
                3: '    Listas, set y diccionario:',
                4: '    Árbol y grafos:',
                5: '    Funcional:',
                6: '    Metaclases:',
                7: '    Simulación:',
                8: '    Threading:',
                9: '    GUI:',
                10: '    Bytes y serialización:',
                11: '    Networking:',
                12: '    Webservices:'
            }
            for topic in info_student.topic_knowledge.items():
                print(topic_str[topic[0]], topic[1])












