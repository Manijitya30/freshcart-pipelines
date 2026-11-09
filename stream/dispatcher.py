"""Dispatcher: publishes one request every 2 s to the topic exchange 'rapido-dispatch'.

Routing key = city.zone.type   e.g. bangalore.koramangala.food
Every BAD_EVERY-th message is deliberately malformed (no 'zone' field) for part D3.

Broker URL comes from the AMQP_URL environment variable (never commit it).
"""
import json
import os
import random
import time
import uuid

import pika

EXCHANGE = "rapido-dispatch"
INTERVAL = float(os.getenv("INTERVAL", "2"))
BAD_EVERY = int(os.getenv("BAD_EVERY", "10"))
ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "velachery", "adyar"],
}
TYPES = ["ride", "food"]


def main():
    url = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")

    n = 0
    try:
        while True:
            n += 1
            city = random.choice(list(ZONES))
            zone = random.choice(ZONES[city])
            typ = random.choice(TYPES)
            key = f"{city}.{zone}.{typ}"
            msg = {"id": uuid.uuid4().hex[:8], "city": city, "zone": zone,
                   "type": typ, "ts": time.time()}
            tag = ""
            if n % BAD_EVERY == 0:
                del msg["zone"]          # D3: bad message, 'zone' is missing
                tag = "  <-- BAD (no zone)"
            ch.basic_publish(exchange=EXCHANGE, routing_key=key, body=json.dumps(msg))
            print(f"#{n:03d} sent  key={key:32s} id={msg['id']}{tag}", flush=True)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    main()
