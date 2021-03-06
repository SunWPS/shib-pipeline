import os
import json

from google.cloud import pubsub_v1, bigquery
from concurrent.futures import TimeoutError


ps_credentials = "gcp_private_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ps_credentials

subscriber = pubsub_v1.SubscriberClient()
subscription_path = ""

client = bigquery.Client()
table_id = ""


def callback(message):
    data = [json.loads(message.data)]
    print(data)
    
    # load to bigquery
    errors = client.insert_rows_json(table_id, data)
    
    print("try to loaded")
    
    if errors:
        print("Error while insert rows: " + errors)
    else:
        print("Data have been added.")
        
    message.ack()


streaming_pull = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for messages on " + subscription_path)

def start_consume():
    with subscriber:
        try:
            streaming_pull.result() # add time out in the result(), if you want
        except TimeoutError:
            streaming_pull.cancel()
            streaming_pull.result()
