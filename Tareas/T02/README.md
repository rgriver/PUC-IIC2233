#Tarea 2

Como en la tarea anterior se utilizó PyQt5 para su comodidad :). En este caso solo se utilizó para recibir inputs del jugador, pues se usó la consola para mostrar la información. Las dos clases principales son ´View´ y ´Game´. La primera encapsula todo lo relacionado con la interfaz gráfica (´PyQt5´), mientras de la segunda es la lógica del juego (y la parte de output también).

El detalle que no se alcanzó a implementar fue el de cargar el juego. Solo se guarda la información del juego en un .txt que es responsabilidad de la clase ´GameWriter´.

La clase ´LinkedList´ proporciona la estructura de datos básica. Existen clases que heredan de esta y añaden nuevos métodos como es el caso de ´MeasuresList´ que almacena las medidas de todos los países.

El archivo ´populations.csv´ no contiene información de los países Haiti y República Dominicana, pues impedían que el jugador ganara al no tener estos conexiones con los demás países. Este archivo se utiliza para generar los países. Si no hay un país en ´population.csv´.

En general el juego termina sobre los 150 días. Es posible que al segundo día el jugador pierda, pues la única persona infectada del país elegido al iniciar un nuevo juego puede morir.

El la constante 0.07 de la fórmula de infección se cambió a 7 para facilitar este proceso.
