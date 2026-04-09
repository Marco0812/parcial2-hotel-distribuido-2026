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

**Cómo los implementé:**

**Decisiones de diseño que tomé:**

---

## Bugs arreglados (Tier 2)

### B4 — Overlap de fechas

### B5 — Race condition con `with_for_update()`

### B7 — Idempotencia

---

## Bonus que implementé (si aplica)

---

## Cosas que decidí NO hacer

(Ej: "no agregué tests porque preferí enfocarme en el flujo end-to-end", "no implementé saga porque no me dio tiempo", etc.)

---

## Si tuviera más tiempo, lo siguiente que mejoraría sería:
