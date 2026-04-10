"""notification-service – consumer que loggea notificaciones de pago.

ESTE SERVICIO ESTÁ INCOMPLETO. Tu trabajo es resolver los TODOs de abajo.

El servicio debe consumir eventos `payment.completed` y `payment.failed` del
exchange `hotel`, y por cada uno loggear de forma estructurada el "envío" de
la notificación. No se manda email real: solo se loggea con un formato
específico que se evalúa.

Formato del log esperado:
[NOTIFICATION] booking_id=<id> event=PAYMENT_COMPLETED guest=<name> channel=email status=SENT

Pista: copia el patrón de availability-service/app/main.py, pero adaptado a
los routing keys de pago. Usa ack manual.
"""

import json
import logging
import os

import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("notification-service")

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


def main() -> None:
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # TODO 1: declarar el exchange 'hotel' (tipo topic) y bindear una queue
    # llamada 'notifications' a los routing keys 'payment.completed' y
    # 'payment.failed'. Recuerda que un binding va de exchange → queue con
    # un routing key específico, y puedes hacer dos bindings sobre la misma
    # queue. ✅✅
    # El exchange de hotel es de tipo topic, lo que permite usar routing keys con formato "payment.completed" y "payment.failed".
    channel.exchange_declare(exchange="hotel", exchange_type="topic")

    # La queue "notifications" se declara como durable para que sobreviva a reinicios del broker.
    channel.queue_declare(queue="notifications", durable=True)
    # Bind de la queue "notifications" al exchange "hotel" con los routing keys específicos para eventos de pago.
    channel.queue_bind(exchange="hotel", queue="notifications", routing_key="payment.completed")
    channel.queue_bind(exchange="hotel", queue="notifications", routing_key="payment.failed")

    # TODO 2: implementar el callback que reciba (ch, method, properties, body),
    # parsee el JSON, y loggee con el formato exacto:
    #   [NOTIFICATION] booking_id=<id> event=<EVENT> guest=<name> channel=email status=SENT
    # No olvides hacer ack manual al final del callback (ch.basic_ack). ✅✅
    # El callback procesa cada mensaje recibido, extrae los campos necesarios del JSON, y loggea la notificación con el formato requerido. 
    # El ack manual asegura que el mensaje se marca como entregado solo después de procesarlo correctamente.
    def callback(ch, method, properties, body):
        data = json.loads(body)
        booking_id = data.get("booking_id", "unknown")
        guest = data.get("guest", "unknown")
        event = data.get("event", "unknown")

        # El log debe seguir el formato exacto requerido, incluyendo los campos booking_id, event, guest, channel=email, y status=SENT.
        logger.info(f"[NOTIFICATION] booking_id={booking_id} event={event} guest={guest} channel=email status=SENT")

        # Acknowledgment manual del mensaje para asegurar que se marca como entregado solo después de procesarlo correctamente.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # TODO 3: iniciar el consumer con channel.basic_consume(...) usando ack
    # manual y luego channel.start_consuming(). ✅✅
    # El consumer se inicia sobre la queue "notifications" y utiliza el callback definido anteriormente para procesar los mensajes entrantes.
    channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=False)

    logger.info("notification-service iniciado, esperando eventos de pago...")
    # Mientras los TODOs no se resuelvan, este servicio no consume nada.
    # Reemplaza este loop infinito con tu lógica.
    channel.start_consuming()


if __name__ == "__main__":
    main()
