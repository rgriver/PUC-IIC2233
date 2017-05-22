import random


class Professor:
    """
    Representa un profesor del curso. Contiene un método que recibe un conjunto
    de alumnos y los atiende.
    """
    def __init__(self, name, section):
        self.name = name
        self.section = section
        self.attended_students = []

    def __repr__(self):
        return self.name

    def attend_students(self, students, week):
        """
        Recibe un grupo de alumnos y realiza las modificaciones del nivel de
        programación.
        :param students: Lista de alumnos
        :param week: Semana
        :return:
        """
        final_students = []

        for student in students:
            if student not in self.attended_students:
                final_students.append(student)

        if len(final_students) > 10:
            final_students = random.sample(final_students, 10)

        for student in final_students:
            student.programming_level *= 1.08

        self.attended_students = final_students

        num_attended_students = len(final_students)
        if num_attended_students:
            print('{} atendió a {} alumnos la semana {}'
                  .format(self, len(final_students), week))
