"""Driver: python stream/driver.py NAME PATTERN

Declares a private (exclusive, auto-named) queue, binds it to the exchange with PATTERN,
prints each request, and ACKs good messages. A message without 'zone' is rejected with
basic_nack(requeue=False) so it is discarded instead of being redelivered forever.
"""
import json
import os
import sys

import pika

EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python stream/driver.py NAME PATTERN")
    name, pattern = sys.argv[1], sys.argv[2]

    url = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")
    queue = ch.queue_declare(queue="", exclusive=True).method.queue
    ch.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)

    def on_message(channel, method, properties, body):
        try:
            msg = json.loads(body)
        except json.JSONDecodeError:
            msg = {}
        if "zone" not in msg:
            print(f"[{name}] REJECT key={method.routing_key} id={msg.get('id')}  (missing zone)",
                  flush=True)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return
        print(f"[{name}] got    key={method.routing_key:32s} id={msg['id']}", flush=True)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
    print(f"[{name}] waiting for pattern '{pattern}' (Ctrl+C to stop)", flush=True)
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    main()
