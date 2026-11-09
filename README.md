# freshcart-pipelines

From Git to Gold: Git + CI, FreshCart ELT on Snowflake, a Mage Iris pipeline, and a RabbitMQ stream.

| Folder | Part |
|---|---|
| `elt/` | FreshCart notebook (Part B) |
| `iris_project/` | Mage project (Part C) |
| `stream/` | dispatcher, driver and bonus consumer (Part D) |
| `tests/` | pytest for the Mage prepare_data block |

Secrets (Snowflake password, AMQP URL) come from environment variables / Colab Secrets and are never committed.
