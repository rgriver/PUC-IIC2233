import csv
import random


class Parameters:
    """
    Encapsula los parametros utilizados por la simulacion. Lee los archivos
    csv y posee funciones que retornan datos usados por las demas clases.
    """
    def __init__(self):
        self.filename = 'parametros.csv'
        self.hour_range = {}
        self.prob_units = []
        self.prob_discount = 0.5

        self.lambda_party = 1/30
        self.lambda_football = 1/70
        self.prob_40_units = 0.1
        self.prob_50_units = 0.7
        self.prob_55_units = 0.15
        self.prob_60_units = 0.05
        self.prob_of_visiting_professor = 20
        self.prob_publishing_delay = 10
        self.confidence_lower_bound = 2
        self.confidence_upper_bound = 12
        self.progress_percentage = 50

        self.current_scenario = 1

        with open(self.filename, 'w') as f:
            f.write('Contenido:int,limite1:int,limite2:int,limite3:int,'
                    'limite4:int,dificultad:int\n')
            f.write('1,2,4,6,7\n')
            f.write('2,3,6,7,8\n')
            f.write('3,1,4,6,7\n')
            f.write('4,2,5,7,8\n')
            f.write('5,3,7,8,9\n')
            f.write('6,4,7,9,10\n')
            f.write('7,3,6,8,9\n')
            f.write('8,2,5,7,8\n')
            f.write('9,1,4,6,7\n')
            f.write('10,4,7,9,10\n')
            f.write('11,2,5,7,8\n')
            f.write('12,2,7,8,9\n\n')

            f.write('Contenido:int,dificultad:int\n')
            f.write('1,2\n')
            f.write('2,2\n')
            f.write('3,3\n')
            f.write('4,5\n')
            f.write('5,7\n')
            f.write('6,10\n')
            f.write('7,7\n')
            f.write('8,9\n')
            f.write('9,1\n')
            f.write('10,6\n')
            f.write('11,6\n')
            f.write('12,5\n\n')

            f.write('Creditos:int,ocurencia:float,limite_inf:int,'
                    'limite_sup:int\n')
            f.write('40,0.1,10,25\n')
            f.write('50,0.7,10,25\n')
            f.write('55,0.05,5,15\n')
            f.write('60,0.05,5,10\n')

        self.set_parameters()

    def get_grade(self, topic, hours):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if int(row[0]) == topic:
                    row = [int(e) for e in row]
                    if 0 <= hours <= row[1]:
                        return random.uniform(1.1, 3.9)
                    elif row[1] + 1 <= hours <= row[2]:
                        return random.uniform(4.0, 5.9)
                    elif row[2] + 1 <= hours <= row[3]:
                        return random.uniform(6.0, 6.9)
                    else:
                        return 7.0

    def get_difficulty(self, topic):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            for i in range(15):
                next(reader)
            for row in reader:
                if int(row[0]) == topic:
                    return int(row[1])

    def get_hours(self, units):
        a, b = self.hour_range[units]
        return random.uniform(a, b)

    def get_units(self):
        x = random.random()
        if 0 <= x < self.prob_units[0]:
            return 40
        elif self.prob_units[0] <= x < sum(self.prob_units[0:1]):
            return 50
        elif sum(self.prob_units[0:1]) <= x < sum(self.prob_units[0:2]):
            return 55
        else:
            return 60

    def get_confidence(self):
        return random.randint(self.confidence_lower_bound,
                              self.confidence_upper_bound)

    def set_parameters(self):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            for i in range(29):
                next(reader)
            for row in reader:
                self.prob_units.append(float(row[1]))
                self.hour_range[int(row[0])] = [int(x) for x in row[2:]]

    def set_scenario(self, scenario):
        data = {}

        with open('escenarios.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')

            current_scenario = scenario
            next(reader)

            for row in reader:
                if row[current_scenario] != '-':
                    data[row[0]] = row[current_scenario]

            for d in data.items():
                data[d[0]] = float(d[1])

            if 'prob_40_creditos' in data:
                self.prob_40_units = data['prob_40_creditos']
            if 'prob_50_creditos' in data:
                self.prob_50_units = data['prob_50_creditos']
            if 'prob_55_creditos' in data:
                self.prob_55_units = data['prob_55_creditos']
            if 'prob_60_creditos' in data:
                self.prob_60_units = data['prob_60_creditos']
            if 'prob_visitar_profesor' in data:
                self.prob_of_visiting_professor = data[
                    'prob_visitar_profesor']
            if 'prob_atraso_notas_Mavrakis' in data:
                self.prob_publishing_delay = data[
                    'prob_atraso_notas_Mavrakis']
            if 'porcentaje_progreso_tarea_mail' in data:
                self.progress_percentage = data[
                    'porcentaje_progreso_tarea_mail']
            if 'fiesta_mes' in data:
                self.lambda_party = data['fiesta_mes']
            if 'partido_futbol_mes' in data:
                self.lambda_football = data['partido_futbol_mes']
            if 'nivel_inicial_confianza_inferior' in data:
                self.confidence_lower_bound = data[
                    'nivel_inicial_confianza_inferior']
            if 'nivel_inicial_confianza_superior' in data:
                self.confidence_upper_bound = data[
                    'nivel_inicial_confianza_superior']

    def get_delay(self):
        if random.random() * 100 <= self.prob_publishing_delay:
            return random.randint(2, 5)
        else:
            return 0

    def get_discount(self):
        if random.random() < self.prob_discount:
            return 0.5
        else:
            return 0

    @staticmethod
    def get_num_scenarios():
        with open('escenarios.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            num_of_scenarios = len(list(next(reader))) - 1
            return num_of_scenarios

    def get_prob_of_visiting_professor(self):
        return self.prob_of_visiting_professor
