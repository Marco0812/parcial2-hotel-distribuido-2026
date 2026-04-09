# Decisiones técnicas

> Documenten brevemente las decisiones que tomaron resolviendo el examen. No copien del enunciado: expliquen con sus palabras qué hicieron y por qué. La intención es que al revisar pueda entender el razonamiento, no que repitan el problema.

---

## Bugs arreglados (Tier 1)

### B1 — Routing key
**Qué encontré:**

**Cómo lo arreglé:**

**Por qué esto era un problema:**

---

### B2 — Manejo de error en publish

---

### B3 — Ack manual

---

### B6 — Credenciales en env vars

---

## notification-service completado

**Qué TODOs había:**

**Cómo los implementé:**

**Decisiones de diseño que tomé:**

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
