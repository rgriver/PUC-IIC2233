# Tarea 6

La comunicación entre ``client_.py`` y el resto de los módulos en el directorio cliente se realizó con señales. La clase ``Client`` es un ``QObject``.

Para obtener los nombres de las canciones se ve el nombre del archivo

Cuando se está enviando la canción al cliente se debe tener cuidado de no cerrar la ventana del salón, porque de otra forma ocurrirá un error.

El tiempo que se de demora en descargar la canción es de aproximadamente 10 segundos.

El HOST y el PORT se editan en los módulos ``server_.py`` y ``client_.py``

En el directorio songs solo deben existir carpetas con canciones. El nombre de cada carpeta se usa para llamar a cada salón.

El artista y el título de la canción se obtienen del nombre del archivo wav. El '-' en el nombre del archivo se usa para separar el artista y el título.
