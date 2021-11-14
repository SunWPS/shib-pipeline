# SHIB Data Pipeline

Building batch and streaming data pipelines that extract data from the Twitter API and Binance about Shiba Inu coin by using GCP, including Cloud Pub/Sub, Functions, Composer, and BigQuery


## Data
Twitter API: https://developer.twitter.com/en (Tweets that mention to Shiba Inu coin)

Binance: https://www.binance.com/en (SHIB/USDT and DOGE/USDT)

## Tool
For this project, I built the pipelines using a tool on the Google Cloud Platform.

- Pub/Sub: message queue
- Functions: pull messages and load data into BigQuery
- Composer: scheduling tasks (using Apache Airflow 2)
- BigQuery: store data (data warehouse)


## Design
1. Extract tweet from Twitter
   - The Publisher application publishes messages to Pub/Sub. Then, Cloud Functions pull messages from Pub/Sub and load them into BigQuery.
2. Extract data from Binance
   - Use Cloud Composer to run Apache Airflow to schedule tasks to extract data from Binance every 1 hour and load data into BigQuery.

<p align="center">
    <img widht="480" height="320" src="https://github.com/SunWPS/shib-pipeline/blob/master/images/design.jpg?raw=true">
</p>

## Reference
- https://airflow.apache.org/docs/
- https://cloud.google.com/docs
- https://www.tweepy.org/
- https://python-binance.readthedocs.io/en/latest/
## Follow Me On
[Linkedin: Wongsakorn Pinvasee](https://www.linkedin.com/in/wongsakorn-pinvasee-b57b34186/)
