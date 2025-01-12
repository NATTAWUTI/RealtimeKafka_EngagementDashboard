import random
import json
from datetime import datetime
from faker import Faker
from confluent_kafka import Producer
import time

# Create a Faker instance for data generation
faker = Faker()

# Kafka topic and producer settings
topic = 'users_engagement'
producer = Producer({
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'my-producer'
})

# producer_config = {
#     'bootstrap.servers': '54.179.19.243:9092',  # EC2 instance IP with Kafka port
#     'linger.ms': 500,             # Optional: batching delay
#     'retries': 3,                 # Retry up to 3 times
#     'retry.backoff.ms': 500,      # Wait 0.5 seconds between retries
#     'message.max.bytes': 1000000,  # Set message max bytes as needed
    
# }

# Initialize the Producer
##producer = Producer(producer_config)

# Acknowledgment callback function
def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced to {msg.topic()}")

# Sample data to send
cn = ["Facebook", "Twitter", "IG", "YouTube", "Pinterest", "Organic", "Web"]
lv = ["Gold", "Silver", "Platinum"]
dv = ["android", "IOS", "Other"]
at = ["view", "like", "share", "comment", "post"]

# Send 1000 messages
for i in range(5000):
    data = {
        "USER_ID": f"User_{random.randint(0, 500)}",
        "PAGE": f"Page_{random.randint(1, 100)}",
        "LANDING_DT": faker.date_time_this_decade().strftime("%Y-%m-%d"),
        "CHANNEL": random.choice(cn),
        "COUNTRY": faker.country(),
        "DEVICE": random.choice(dv),
        "ACTION": random.choice(at),
        "LEVEL": random.choice(lv)
    }

    # Produce message to Kafka
    producer.produce(
        topic,
        key=f"key_{i}",
        value=json.dumps(data).encode('utf-8'),
        callback=acked
    )

    # Flush to ensure delivery
    producer.flush()

    # Wait before the next message
    time.sleep(random.uniform(1, 3))

# Ensure all messages are sent
producer.flush()
