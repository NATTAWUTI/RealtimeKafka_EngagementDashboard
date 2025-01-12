import random
import json
from datetime import datetime
from faker import Faker
from confluent_kafka import Producer
import avro.schema
import avro.io
import io
import time  # Import time to use sleep
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro import CachedSchemaRegistryClient

# Create a Faker instance
faker = Faker()

# Set up schema registry client
schema_registry = CachedSchemaRegistryClient('http://localhost:8081')  # Change this to your Schema Registry URL == 
my_schema = schema_registry.get_by_id(1) ##schema version
print("my_schema",my_schema)

# Define the Avro producer
avro_producer = AvroProducer(
    {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker address
        'schema.registry.url': 'http://localhost:8081',  # Change this to your Schema Registry URL == 
    },
    default_value_schema=my_schema
)

topic = 'users_engagement'
loop = 1000

## data mock
cn = ["Facebook", "Twitter", "IG" ,"You tube" , "Pinterest" ,"Organic" ,"Web"]
lv = ["Gold", "Silver", "Platinum"]
dv = ["android","IOS","Other"]
at = ["view","like","share","comment","post"]


records = []
for _ in range(loop):
    current_time = current_time = datetime.now().strftime("%Y-%m-%d")
    record = {
        # 'title': random.choice(titles),
        # 'sale_ts': current_time,
        # 'ticket_total_value': random.choice(prices),
        "USER_ID": f"User_{random.randint(0, 500)}",
        "PAGE": f"Page_{random.randint(1, 100)}",
        "LANDING_DT": faker.date_time_this_decade().strftime("%Y-%m-%d"),
        "CHANNEL": random.choice(cn),
        "COUNTRY": faker.country(),
        "DEVICE": random.choice(dv),
        "ACTION": random.choice(at),
        "LEVEL": random.choice(lv)
    }
    records.append(record)

# Produce records to Kafka
for record in records:
    avro_producer.produce(topic=topic, value=record)
    print(f"Produced record: {record}")
    time.sleep(random.randint(1,2)) ##sleep time


avro_producer.flush()
