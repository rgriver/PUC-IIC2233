# Tarea 1

En esta tarea se utilizó PyQt para implementar una bonita interfaz gráfica. Sin embargo, en algunos casos se usa la consola para mostrar información al usuario (se especifica cuando esto sucede en cada caso).

Existen algunos detalles que pueden provocar que el programa se caiga debido a cambios de ultimo minuto (Why?!!!!!!). El único problema conocido es la creación de un archivo en blanco en que la carpeta donde se guardan los reportes. Si se crea manualmente un archivo o el programa genera uno (al tratar de optimizar un incendio antes de que ocurra), al tratar de acceder información de incendios o recursos... Crash! Esto sucede porque se intenta acceder información que no existe y se genera la excepcion StopIteration por usar data = next(file). Esto no pasaba antes de hacer un cambio de ultimo minuto y al tratar deshacer el cambio esto pasó (sucks to be me).

Solo se implementó el algoritmo que minimiza el tiempo. Además falto el uso mostrar la información de recursos más usados y efectivos.

El código está está organizado de la siguiente forma: una clase, un archivo.

Comenté la línea 29 de basic_menu.py minutos antes de entregar la tarea como solución para arreglar el desastre que había provocado. No estoy seguro de las consecuencias de esto. Aparentemente ninguna, pero aconsejo tener esto en mente en caso de emergencia

HOW TO FIX THE ISSUE:
En las funciones `view_active_fires` y `view_ex_fires` en el archivo `fire_editor.py` se debe cambiar lo siguiente:
Para `view_active_fires`:
Before:
```
.
.
.
102                fire_id = next(f).strip()
.
.
.
```
After:
```
.
.
.
102                fire_id = next(f, None)
103                    if fire_id is None:
104                    break
105                fire_id = fire_id.strip()
.
.
.
```
Line 102: `view_active_fires`
