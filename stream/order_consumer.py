"""BONUS: collect order messages from RabbitMQ for a fixed window and return them as a list.

Use it from the FreshCart notebook:

    from order_consumer import collect_orders
    orders = collect_orders(seconds=60)                 # list of dicts (web shape)
    path = write_landing("web", orders, run_id)         # raw file, same as the batch pipeline
    load_file(path, "bronze.orders_raw", f"orders_web/{run_id}")
    query(f"SET run_id = '{run_id}'"); run_sql(SQL_10_ORDERS_CLEAN); ... run_sql(SQL_40_GOLD)

Messages are ACKed only after they are in the in-memory batch. If the notebook dies before
write_landing(), unacked messages return to the queue (at-least-once delivery).
"""
import json
import os
import time

import pika

EXCHANGE = "freshcart-orders"
QUEUE = "freshcart-orders-batch"     # durable named queue so nothing is lost between batches


def collect_orders(seconds=60, binding="orders.#", url=None):
    url = url or os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")
    ch.queue_declare(queue=QUEUE, durable=True)
    ch.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=binding)

    orders, deadline = [], time.time() + seconds
    while time.time() < deadline:
        left = max(0.1, deadline - time.time())
        method, props, body = next(ch.consume(QUEUE, inactivity_timeout=min(1.0, left)))
        if method is None:
            continue
        try:
            orders.append(json.loads(body))
            ch.basic_ack(method.delivery_tag)
        except json.JSONDecodeError:
            ch.basic_nack(method.delivery_tag, requeue=False)
    ch.cancel()
    conn.close()
    print(f"collected {len(orders)} orders in {seconds}s")
    return orders


if __name__ == "__main__":
    print(collect_orders(int(os.getenv("WINDOW", "60"))))
