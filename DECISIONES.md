# Decisiones técnicas

> Documenten brevemente las decisiones que tomaron resolviendo el examen. No copien del enunciado: expliquen con sus palabras qué hicieron y por qué. La intención es que al revisar pueda entender el razonamiento, no que repitan el problema.

---

## Bugs arreglados (Tier 1)

### B1 — Routing key
**Qué encontré:** 
Que el booking-api y el availability-service no estaban 'coordinados' y cuando llegaba el mensaje no había ninguna cola que espera esos mensajes
 
**Cómo lo arreglé:**
Cambiando el routing-key en rabbitmq de "booking.create" a "booking.requested"

**Por qué esto era un problema:**
Porque al no tener el routing-key correcto de forma 'coordinada' por más que se envíe el mensaje no había quien lo recibiera.

---

### B2 — Manejo de error en publish
**Qué encontré:**
Al momento de querer crear una reserva no había un manejo de errores en el caso de que hubiera alguna falla en el broker, y no había un feedback sobre el problema.

**Cómo lo arreglé:**
Cuando surgiera el error se mandara el mensaje que hubo un error al publicar el evento devolviendo un "HTTP 503 Error al procesar la reserva"

**Por qué esto era un problema:**
Porque al querer realizar una reserva y que esta no se lograra con éxito el cliente no podía saber que no se había realizado debido a que no llegaba un mensaje de que había fallado.
---

### B3 — Ack manual
**Qué encontré:**
Que en availability-service estaba "autotrack=True" lo que provocaba que rabbitmq marcara el mensaje como entregado de forma inmediata cuando se enviara.

**Cómo lo arreglé:**
Cambiando el "autotrack=True" a "autotrack=False" para evitar que lo marcara de forma inmediata, mover la confirmacion de forma manual y en el caso de error mandarlo a intentarlo de nuevo.

**Por qué esto era un problema:**
Porque si lo marcaba entregado desde el principio sin verificarlo podría mandar una falso verdadero, y de esta forma se verifica que si se haya mandado y en caso de que no lo reintenta.
---

### B6 — Credenciales en env vars
**Qué encontré:**
La conexión a la base de datos de payment-service estaban hardcodeados directamente en el código.

**Cómo lo arreglé:**
Importé la librería 'os' y reemplacé la URL por una 'DATABASE_URL' para los campos user, password, db, host y port.

**Por qué esto era un problema:**
Porque las credenciales quedan expuestas a quien sea, además de que no se pueden cambiar sin reconstruir la imagen.
---

## notification-service completado

**Qué TODOs había:**
Dentro del proyecto había 3 TODOs, declarar el exchange hotel y bindear una queue para payment.completed y payment.failed, implementar el callback que loggee de forma estructurada el "envío" de la notificación e iniciar el consumer con channel.basic_consume(...) y channel.start_consuming()

**Cómo los implementé:**
En el TODO 1 se declaró el exchange de 'hotel', se creó una queue de 'notifications' y dos bindings el de 'payment.completed' y 'payment.failed'. 
En el TODO 2 se implementó un ack manual para asegurar que el mensaje se marca como entregado después de que se procese de forma correcta.
En el TODO 3 se realizó el consumer sobre la queue de 'notifications' y utiliza el callback definido anteriormente para procesar los mensajes entrantes.

**Decisiones de diseño que tomé:**
Que fuera una sola queue con las dos bindings ya que los eventos de 'payment.completed' y 'payment.failed' se llevan a cabo de la misma manera.

---

## Bugs arreglados (Tier 2)

### B4 — Overlap de fechas
Reemplace el filtro de conflictos por dos condiciones que juntas cubren cualquier cruce posible entre rangos de fechas.
Queria que la validacion la hiciera PostgreSQL directamente, sin traer registros a Python para compararlos. 

### B5 — Race condition con `with_for_update()`
Agregue -with_for_update() a la consulta para que PostgreSQL bloquee las filas mientras la transaccion esta activa. El segundo proceso tiene que esperar y cuando retoma, ya encuentra el conflicto.
Es la solucion mas directa, el lock vive en la base de datos compartida, asi que funciona aunque haya multiples instancias del servicio corriendo al mismo tiempo.
### B7 — Idempotencia
Cree una tabla processed_events, donde registro el identificador de cada reserva antes de cobrar. Si el registro falla porque ya existe, el mensaje se ignora sin cobrar.
Hacer que la base de datos se encargue de que no haya  duplicados con una llave primaria es algo automatico y seguro.

## Bonus que implementé (si aplica)

---

## Cosas que decidí NO hacer

(Ej: "no agregué tests porque preferí enfocarme en el flujo end-to-end", "no implementé saga porque no me dio tiempo", etc.)

Para el overlap de fechas, descarte filtrar las fechas en python despues de la consulta porque es mas lento y mas dificil de mantener.

Para el Race conditions con with_for_update(), descarte bloquear a nivel de aplicacion porque solo funcionaria dentro de un mismo proceso, no entre instancias separadas.

Para la idempotencia, evite consultar primero si el identificador ya existia y luego insertar, porque ese patron tiene la misma race condition que queria resolver.
## Si tuviera más tiempo, lo siguiente que mejoraría sería:
