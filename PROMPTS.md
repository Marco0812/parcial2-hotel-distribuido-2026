# Declaración de uso de IA

> Llenen este archivo si alguno de los dos usó alguna herramienta de IA generativa (Claude, ChatGPT, Copilot, Gemini, etc.) durante el examen. Hacerlo es **obligatorio** y se evalúa con honestidad: declarar correctamente no penaliza, lo que penaliza es **no declarar** y que se detecte uso.
>
> Indiquen también **quién** de los dos integrantes la usó (puede ser uno solo, ambos, o ninguno).

## ¿Usaron IA?

- [V] Sí
- [ ] No

## ¿Quién la usó?

- [ ] David
- [V] Marco
- [ ] Ambos

---

## Si la respuesta es "Sí":

### Herramientas usadas
(Ej: Claude.ai, ChatGPT-4, GitHub Copilot, Cursor, etc.)

- Claude.ai y ChatGPT-4

### Prompts principales
Listen los 3-5 prompts más importantes que escribieron y para qué los usaron.

1. **Prompt:** Como funciona with_for_update en SQLAlchemy y cuando conviene usarlo?
   **Para qué:** Entender el mecanismo de bloqueo antes de aplicarlo en la query de disponibilidad
   **Quién lo usó:** Marco
   **Qué tan útil fue:** 4

2. **Prompt:** Cual es la forma correcta de detectar solapamiento entre dos rangos de fechas en SQL?
   **Para qué:** Confirmar la logica de overlap antes de reescribir el filtro de conflictos en find_available_roo
   **Quién lo usó:** Marco
   **Qué tan útil fue:** 4

 3. **Prompt:** Como garantizo idempotencia en un consumer de RabbitMQ usando SQLAlchemy async?
   **Para qué:** Entender el patro de tabla processed_events para el fix de B7 en el payment-service
   **Quién lo usó:** Marco
   **Qué tan útil fue:** 3
    

### ¿En qué partes los apoyó?
(Ej: explicación de `with_for_update()`, generación de boilerplate del notification-service, debugging de un error de aio-pika...)

- Explicacion de como funciona with_for_update() y porque el lock debe vivir en la base de datos y no en el codigo de la aplicacion
- Confirmar la formula de solapamiento de intervalos para aplicarla como filtro
- Orientacion sobre el patron de idempotencia con tabla uxiliar y como manejar el IntegrityError en SQLAlchemy async

### ¿Hubo cosas en las que la IA dio respuestas incorrectas o que tuvieron que corregir?
(Ser honestos aquí suma puntos de criterio)

- La primera sugerencia para B7 incluia un SELECT previo antes del INSERT, lo  cual tiene su propia race condition. Tuve que descartarlo y quedarme solo con el INSERT directo aprovechando la constraint de la Primary Key
- Para el docker-compose.yml, asumio que el notifacation-service necesitaba conexion a Postgres porque los otros consumer la tenian. Al revisar el codigo del servicio manualmente y confirme que no lo tiene, asi que ese depends_on no lo agregue
- Para B5, sugirio colocar el with_for_update() fuera de la transaccion activa, lo cual no tiene efecto porque el lock necesita vivir dentro de la misma sesion donde se ca a insertar la reserva. Tuve que moverlo al lugar correcto revisnado como estaba estructurada la sesion en el codigo original.

### ¿Qué decidieron hacer manualmente sin IA y por qué?

- La identificaciones de los bugs se hizo leyendo el codigo directamente, los comentarios de #BUG, sirvieron como guia y apoyo
- El diseno del modelo ProcessedEvent y decidir en que punto exacto del flujo insertarlo(antes del cobro, no despues)
- La seccion de Decisiones.md se uso las palabras de cada uno ayudandonos de los apoyos de los bugs
- La integracion del notifaction-service en el docker-compose.yml
- Los gran mayoría de los bugs fueron realizados sin IA debido a que estaban bastante claras las formas de resolverlos.

