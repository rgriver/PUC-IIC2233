class Assessment:
    """
    Representa una evaluacion: T, C, AC.
    """
    def __init__(self, num, student_id, progress, expected_grade):
        self.num = num
        self.student_id = student_id
        self._progress = progress
        self.expected_grade = expected_grade
        self._grade = None

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        self._grade = grade

    @property
    def progress(self):
        return self._progress


