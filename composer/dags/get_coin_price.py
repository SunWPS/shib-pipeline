import pytz
import datetime as dt
from datetime import timedelta

import pandas as pd
from binance.client import Client 

from airflow import DAG
from airflow.operators.bash_operator import BashOperator 
from airflow.operators.python_operator import PythonOperator 
from airflow.utils.dates import days_ago


# binance config
api_key = "pPnMUhRGd4g2OAgDD1SaWiOcOTDjC6CDQ4vFTYOrkxvgwDEfhBwrwRhfK5OIxymb"
api_secret = "5YKqA2Zv33gK2ywE2hB2zuUMK9FJJ8wTiGg8d1aB1EKpOc0WMI9K375s4RusiGVZ"


def get_data_from_binance():
    data = {"symbol": [], "price": [], "date_time": []}
    client = Client(api_key, api_secret)
    coin_list = ["SHIBUSDT", "DOGEUSDT"]
    
    thai = pytz.timezone('Asia/Bangkok')
    now = dt.datetime.now(thai)

    real_dt = now.strftime("%Y-%m-%d %H:%M:%S %Z")

    tickers = client.get_all_tickers()
    for ticker in tickers:
        for coin in coin_list:
            if ticker["symbol"] == coin:
                price = float(ticker['price'])
                data["symbol"].append(coin)
                data["price"].append(price)
                data["date_time"].append(real_dt)
    
    df = pd.DataFrame(data)
    df.to_csv("/home/airflow/gcs/data/crypto_price.csv", index=False)
    print("get price at " + real_dt + "successed")


default_args = {
    'owner': 'wongsakorn',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


with DAG('Binace_pipeline',
         default_args=default_args,
         description='get SHIB and DOGE price',
         schedule_interval="0 * * * *",
         start_date=days_ago(1),
         catchup=False,
         tags=['PROJECT']) as dag:
    
    t1 = BashOperator(
        task_id='echo_start',
        bash_command='echo "start to get data $(date)"',
    )
    
    t2 = PythonOperator(
        task_id='get_crypto_price',
        python_callable=get_data_from_binance
    )
    
    t3 = BashOperator(
        task_id='load_to_bq',
        bash_command='bq load --source_format=CSV --autodetect shib.crypto_price \
            gs://asia-southeast1-the-pipelin-aacd0a07-bucket/data/crypto_price.csv'
    )
    
    t4 = BashOperator(
        task_id='load_success',
        bash_command='echo "Load to BQ successed"'
    )
    
    [t1, t2] >> t3 >> t4
