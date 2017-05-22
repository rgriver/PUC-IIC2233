from PyQt5.QtWidgets import *


class View(QWidget):
    def __init__(self, simulator):
        super(View, self).__init__()
        self.simulator = simulator
        run_box = QGroupBox('Single Simulation')
        analysis_box = QGroupBox('Multiple Scenario Analysis')
        statistics_box = QGroupBox('Statistics')
        single_simulation_button = QPushButton('Run')
        multiple_simulation_button = QPushButton('Run')
        grades_button = QPushButton('Show Grades')
        characteristics_button = QPushButton('Show Characteristics')
        compare_button = QPushButton('Compare Results')
        self.students_combo = QComboBox()
        for student in self.simulator.students:
            self.students_combo.addItem(str(student.id) + ': ' + student.name)
        run_layout = QHBoxLayout()
        analysis_layout = QVBoxLayout()
        statistics_layout = QVBoxLayout()
        run_layout.addWidget(single_simulation_button)
        run_box.setLayout(run_layout)
        student_layout = QHBoxLayout()
        student_layout.addWidget(QLabel('Student:'))
        student_layout.addWidget(self.students_combo)
        statistics_layout.addLayout(student_layout)
        statistics_layout.addWidget(grades_button)
        statistics_layout.addWidget(characteristics_button)
        statistics_box.setLayout(statistics_layout)
        analysis_layout.addWidget(multiple_simulation_button)
        analysis_layout.addWidget(compare_button)
        analysis_box.setLayout(analysis_layout)
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(run_box)
        left_layout.addWidget(analysis_box)
        main_layout.addLayout(left_layout)
        main_layout.addWidget(statistics_box)
        single_simulation_button.clicked.connect(self.run_simulation)
        grades_button.clicked.connect(self.show_grades)
        multiple_simulation_button.clicked.connect(
            self.run_multiple_simulation)
        compare_button.clicked.connect(self.show_comparison)
        characteristics_button.clicked.connect(self.show_characteristics)
        self.setLayout(main_layout)
        self.show()

    def run_simulation(self):
        self.simulator.run()

    def show_grades(self):
        student_id = int(self.students_combo.currentText().split(':')[0])
        self.simulator.print_grades(student_id)

    def run_multiple_simulation(self):
        self.simulator.analyze_scenarios()

    def show_comparison(self):
        self.simulator.print_best_scenario()

    def show_characteristics(self):
        student_id = int(self.students_combo.currentText().split(':')[0])
        self.simulator.print_characteristics(student_id)



