# Tarea 7

## Ejemplo de comandos

```
/get 12
/post 23 *According to all known laws of aviation, there is no way a bee should be able to fly
/label 356 Apples
/close 2
```

## Informacion importante

Para guardar los IDs de los chats se escribe en un archivo de texto `chats.txt` y las issues con respuesta automática en `auto_issues.txt`, pues la app se reinicia un tiempo después y los datos se pierden. En un principio lo implementé con variables y luego las reemplacé por archivos de texto para ver si se mantentían luego de . Como al final este detalle no era importante y me dio miedo cambiar el código, así que dejé los archivos de texto.

Debido al problema anterior, si la app se llega a reiniciar (tal vez por inactividad) se debe enviar un mensaje cualquiera para que el servidor reconozca al usuario otra vez (puede ser un comando).

La lista de IDs de chats está disponible en https://rgriverapp.herokuapp.com/. Refresque la página y si no hay ningúna ID es porque la app se reinició.

Para buscar el error se da prioridad a la busqueda de bloques de código inline. Si no hay error o simplemente no hay codigo de este estilo se buscan bloques de código de múltiples líneas.

## Clases
`App`: Es la aplicacion Flask.

`RepositoryController`: Se encarga de realiar los cambios en el repo.

`BotController`: Recibe y envía los mensajes del usuario. Habla con `RepositoryController` para hacer los cambios en el repo.

`CommandInterpreter`: Se encarga de interpretar el comando.

`IssueHelper`: Intenta buscar una solución al error cuando corresponde.

:)
