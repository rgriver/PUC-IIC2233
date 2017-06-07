# Tarea 5

Se dividió la parte gráfica de la lógica del juego. Existen dos clases principales: `View` y `Game` que representan el frontend y el backend respectivamente.

## Información importante
El comportamiento del enemigo puede ser Noob o Pro. Se testeó bastante el Noob, pero el Pro no tanto. Por eso es que no se asegura un funcionamiento perfecto si el enemigo es Pro. Para definir un comportamiento se debe cambiar en la clase `EnemyController` el atributo `behavior` que es definido de la siguiente manera: `behavior = random.chose([NoobBehavior(), ProBehavior()])`.

Si por algun motivo el jugador queda atrapado por otros personajes, evitar moverse con las teclas A y D. Esto provoca que la dirección de referencia que el sprite usa para mirar cambie y provocará que el personaje al moverse mire con un ángulo desfasado. Si no le toca enfrentar esta situación, muévase con tranquilidad.

El inhibidor muere y revive en la misma posición. Esto significa que si alguna entidad se ubica en esa posición a la hora de resurrección del inhibidor, quedará atrapada debajo y no podrá moverse. Sádico, no cree?

El movimiento con las teclas A y D describe una circunferencia cuyo centro es la posicion del mouse. Esto se preguntó en una issue [#551](https://github.com/IIC2233/Syllabus/issues/551)
