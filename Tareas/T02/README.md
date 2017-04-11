# Tarea 2

Como en la tarea anterior se utilizó `PyQt5` para su comodidad :). En este caso solo se utilizó para recibir inputs del jugador, pues se usó la consola para mostrar la información. Las dos clases principales son `View` y `Game`. La primera encapsula todo lo relacionado con la interfaz gráfica (`PyQt5`), mientras de la segunda es la lógica del juego (y la parte de output también).

El detalle que no se alcanzó a implementar fue el de cargar el juego. Solo se guarda la información del juego en un .txt que es responsabilidad de la clase `GameWriter`.

La clase `LinkedList` proporciona la estructura de datos básica. Existen clases que heredan de esta y añaden nuevos métodos como es el caso de `MeasuresList` que almacena las medidas de todos los países.

El archivo ´populations.csv´ no contiene información de los países Haiti y República Dominicana, pues impedían que el jugador ganara al no tener estos conexiones con los demás países. Este archivo se utiliza para generar los países. Si no hay un país en `population.csv`.

En general el juego termina sobre los 150 días. Es posible que al segundo día el jugador pierda, pues la única persona infectada del país elegido al iniciar un nuevo juego puede morir.

El la constante 0.07 de la fórmula de infección se cambió a 7 para facilitar este proceso.

## Clases

`Actions`
Acciones principales que el jugador puede realizar durante la partida.

`AirConectionsDatabase`
Clase que encapsula la información de las conexiones aéreas.

`AirportsDatabase`
Aeropuertos de los países

`BordersDatabase`
Encapsula las conexiones terrestres de cada país.

`CountriesCreator`
Se encarga de crear los países al momento de generar una partida.

`Country`
Almacena la información reacionada de cada país.

`CountryValidor`
Tiene como responsabilidad verifcar si un país existe.

`Database`
Clase que define métodos básicos de la mayoría las bases de datos.

`Game`
La clase principal del juego (game logic).

`GameLoader`
Se encarga de cargar el jeugo.

`GameSetter`
Usado al crear un nuevo juego.

`GameWriter`
Guarda la partida actual.

`Government`
El gobierno de cada país.

`HealingCalculator`
Clase que se encarga de cálcular los efectos de la cura en cada país.

`Infection`
Contiene los parámetros de cada infección.

`InfectionCalculator`
Su labor es calcular los efectos de la infección en país.

`LinkedList`
Lista ligada.

`Measure`
Medida generada por el gobierno.

`MeasuresList`
Hereda de LinkedList y almacena las medidas de cada país.

`Menu`
Menu inicial del juego.

`PopulationDatabase`
Encapsula la base de datos de la población de cada país.

`ResearchLab`
Esta clase se encarga de descubrir la infección y crear una cura.

`StatisticsGenerator`
Imprime en consola la información solicitada por el jugador.

`View`
Clase principal de la interfaz grafica.

`World`
Dónde ocurre la acción.
