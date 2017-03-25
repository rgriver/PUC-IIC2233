# Tarea 1

En esta tarea se utilizó PyQt para implementar una bonita interfaz gráfica. Sin embargo, en algunos casos se usa la consola para mostrar información al usuario (se especifica cuando esto sucede en cada caso).

Existen algunos detalles que pueden provocar que el programa se caiga debido a cambios de ultimo minuto (Why?!!!!!!). El único problema conocido es la creación de un archivo en blanco en la carpeta donde se guardan los reportes. Si se crea manualmente un archivo o el programa genera uno (al tratar de optimizar un incendio antes de que ocurra), al tratar de acceder información de incendios o recursos... Crash! Esto sucede porque se intenta acceder información que no existe y se genera la excepcion `StopIteration` por usar `data = next(file)`.

Solo se implementó el algoritmo que minimiza el tiempo. Además falto el uso mostrar la información de recursos más usados y efectivos.

El código está está organizado de la siguiente forma: una clase, un archivo.

Comenté la línea 29 de basic_menu.py minutos antes de entregar la tarea como solución para arreglar el desastre que había provocado. No estoy seguro de las consecuencias de esto. Aparentemente ninguna, pero aconsejo tener esto en mente en caso de emergencia.

## Clases

`AnafMenu`  
Corresponde al menu avanzado que se genera solo si un usuario Anaf accede. Contiene referencias a otras clases que permiten realizar acciones complejas como editar las bases de datos, planificar estrategias, etc.

`BasicMenu`  
Menú básico disponible solo si el usuario no es Anaf.

`Window`  
La ventana principal del programa (hereda de QMainWindow) que muestra el menú asignado a cada usuario. Cada vez que se inicia sesión se instancia un nuevo objecto (AnafMenu o BasicMenu) y llamamos al método `setCentralWidget()`.

`Login`  
Se encarga de controlar el acceso al programa al reviasar las bases de datos.

`UserDate`  
Clase derivada de QWidget y DateTime que almacena la fecha ingresada por el usuario.

`DataCollection`  
Encapsula las bases de datos usadas.

`Database`  
Provee metodos para leer y editar los archivos.

`DateTime`  
Define métodos necesarios para trabajar con las fechas.

`FireChecker`  
Revisa los reportes generados para conocer la información actual de los recursos.

`FireEditor`  
Permite editar la base de datos de incendios y acceder a la información de incendios.

`Fires`  
Es la base de datos de incendios, derivada de la clase Database.

`ForecastEditor`  
Esta clase permite agregar nuevos pronósticos.

`Forecasts`  
Base de datos de incendios.

`Optimizer`  
Es la superclase de cualquier optimizador (tiempo, costo y recursos). Define algunos parámetros de simulación como la referencia de tiempo (step size).

`Planner`  
Widget disponible solo en el menú Anaf que permite al usuario realizar la planificación de estrategias.

`Resource Editor`  
Editor de recursos

`ResourceState`  
Almacena el estado actual de un recurso de acuerdo a la fecha se defina.

`Resources`  
Base de datos de recursos

`SimulationResource`
Es usado por el optimizador para simular los eventos que cada recurso debe hacer para acabar con el incendio. Una instancia de `SimlationResource` por cada recurso al momento de simualar.

`TimeOptimizer`  
Clase derivada de Optimizer que se encarga de optimizar el tiempo necesario para acabar con el incencio.

`Users`  
Base de datos de usuarios.
