import boto3
import json
import time
import random
import datetime
from faker import Faker

# Configuration
STREAM_NAME = 'climate-stream'
REGION_NAME = 'us-east-1'
SIMULATION_MODE = True # Set to False if you have AWS Credentials configured

# Initialize Kinesis Client
if not SIMULATION_MODE:
    kinesis = boto3.client('kinesis', region_name=REGION_NAME)
else:
    kinesis = None
    print("[INFO] Running in SIMULATION MODE. Data will be printed, not sent to AWS.")

fake = Faker()

# Mock Cities
CITIES = ["Bangkok", "London", "New York", "Tokyo", "Sydney", "Paris", "Berlin", "Moscow"]

def get_climate_data():
    """Generate mock climate data."""
    city = random.choice(CITIES)
    # Simulate realistic ranges
    temp = round(random.uniform(15.0, 42.0), 2) if city == "Bangkok" else round(random.uniform(-5.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 90.0), 1)
    co2 = random.randint(350, 450)
    
    data = {
        'city': city,
        'temperature': temp,
        'humidity': humidity,
        'co2_ppm': co2,
        'timestamp': datetime.datetime.now().isoformat(),
        'sensor_id': fake.uuid4()
    }
    return data

def send_data():
    if not SIMULATION_MODE:
        print(f"Starting data stream to {STREAM_NAME}...")
    else:
        print(f"Starting SIMULATION data stream...")

    try:
        while True:
            data = get_climate_data()
            partition_key = data['city']
            
            if not SIMULATION_MODE:
                response = kinesis.put_record(
                    StreamName=STREAM_NAME,
                    Data=json.dumps(data),
                    PartitionKey=partition_key
                )
                print(f"[AWS Kinesis] Sent: {data}")
            else:
                 print(f"[SIMULATION] Generated: {data}")
            
            time.sleep(1) # Send 1 record per second
    except KeyboardInterrupt:
        print("\nStopping data stream.")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == '__main__':
    # Ensure credentials are set up (e.g., via 'aws configure')
    send_data()
