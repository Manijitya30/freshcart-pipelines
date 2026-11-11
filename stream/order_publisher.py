"""BONUS: publish FreshCart-style web orders to RabbitMQ (topic exchange 'freshcart-orders').

Messages use the same flat shape as MOCK_WEB_ORDERS, so the existing SQL_10 maps them
without any change. Order ids ORD-2001.. are new, so they never collide with ORD-1001..1006.
Start order_consumer.py FIRST (a queue must exist before messages are published, or the broker drops them).
"""
import argparse
import json
import os

import pika

EXCHANGE = "freshcart-orders"
SAMPLE = [  # (email, name, amount, currency, pincode)
    ("priya.r@gmail.com", "Priya R", "1,500.00", "INR", "600041"),
    ("meera@outlook.com", "Meera S", "850", "INR", "400050"),
    ("arjun.k@yahoo.in",  "Arjun K", "25.00", "USD", "560034"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2001)
    ap.add_argument("--n", type=int, default=3)
    a = ap.parse_args()
    conn = pika.BlockingConnection(pika.URLParameters(
        os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic")
    for i in range(a.n):
        email, name, amount, cur, pin = SAMPLE[i % len(SAMPLE)]
        order = {"order_id": f"ORD-{a.start + i}", "cust_email": email, "cust_name": name,
                 "order_date": "2026-09-02", "amount": amount, "currency": cur,
                 "pincode": pin, "updated_at": "2026-09-02 12:00:00"}
        ch.basic_publish(exchange=EXCHANGE, routing_key="orders.web.new", body=json.dumps(order))
        print("published", order["order_id"])
    conn.close()


if __name__ == "__main__":
    main()
