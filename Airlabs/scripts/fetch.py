import requests
from kafka import KafkaProducer
import json
import time
import logging

API_KEY = 'API_KEY'
KAFKA_TOPIC = 'aviationstack_data'
KAFKA_SERVER = 'localhost:9093'  # Ensure this matches the configured external listener port

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_airlabs_data():
    url = f'http://api.aviationstack.com/v1/flights?access_key={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            logger.error("Key 'data' not found in the response")
            return []
    else:
        logger.error(f"Error fetching data from Airlabs API: {response.status_code}")
        return []

while True:
    try:
        data = fetch_airlabs_data()
        if data:
            for item in data:
                producer.send(KAFKA_TOPIC, item)
            logger.info(f"Sent {len(data)} records to Kafka topic {KAFKA_TOPIC}")
    except Exception as e:
        logger.error(f"Error in fetching or sending data: {e}")
    time.sleep(10)

