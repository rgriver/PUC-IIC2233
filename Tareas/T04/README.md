# Tarea 4

Como en las tareas anteriores se utilizó PyQt5 para la interfaz que se implementa en la clase View. La clase principal es `Simulator` que posee métodos encargados de realizar las acciones que el usuario solicite. Cada evento es representado con una clase particular. Todas estas clases tienen el método `simulate` que realiza los cambios correspondientes a ese evento. Los parámetros se obtienen de la clase `Parameters` que lee los archivos escenarios.csv y parametros.csv.

## Programación

![alt text](https://github.com/IIC2233/rgriver-iic2233-2017-1/blob/master/Tareas/T04/eventos.png "Programación")

Aquí se muestra la programación de los eventos. Esto claramente puede cambiar en casos como el atraso de la publicación de notas. En la imagen no se muestra el evento examen.

## Detalles

Para calcular el promedio del alumno en un momento dado se consideran solo las notas disponibles. El promedio se calcula usando las ponderaciones de la nota final del curso. Este resultado se para conocer el mes con mayor aprobación y cualquier otro calculo que necesite el promedio del alumno.

El día en que los profesores aceptana los alumnos es el miércoles.

Cualquier nota se publica 14 días despues de la rendir cualquier tipo de evaluación.

En el gráfico de salida final, algunas veces aparecen dos evaluaciones para una misma semana. Esto ocurre porque se utilizó como día el de la publicación de notas y no el día en que se realizan las evaluaciones. Si ocurre algún atraso, es posible que dos evaluaciones se publiquen en la misma semana.
