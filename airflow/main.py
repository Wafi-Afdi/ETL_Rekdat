from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import functions from separate files
from scrape_game import main as scrape_game
from extract_steam_price import main as extract_steam_price
from fetch_data_steam import main as fetch_data_steam
from scrape_steam_chart import main as scrape_steam_chart
from tf_steam_price import main as tf_steam_price
from tf_data_steam import main as tf_data_steam
from tf_steam_chart import main as tf_steam_chart
from fetch_stock import main as fetch_stock
from transform_daily_monthly import main as transform_daily_monthly
from load_daily_monthly import main as load_daily_monthly

# Default args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='etl_pipeline_steam',
    default_args=default_args,
    description='An ETL pipeline for Steam and stock data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 11, 20),
    catchup=False,
) as dag:

    # Define tasks
    task_scrape_game = PythonOperator(
        task_id='scrape_game',
        python_callable=scrape_game
    )

    task_extract_steam_price = PythonOperator(
        task_id='extract_steam_price',
        python_callable=extract_steam_price
    )

    task_fetch_data_steam = PythonOperator(
        task_id='fetch_data_steam',
        python_callable=fetch_data_steam
    )

    task_scrape_steam_chart = PythonOperator(
        task_id='scrape_steam_chart',
        python_callable=scrape_steam_chart
    )

    task_tf_steam_price = PythonOperator(
        task_id='tf_steam_price',
        python_callable=tf_steam_price
    )

    task_tf_data_steam = PythonOperator(
        task_id='tf_data_steam',
        python_callable=tf_data_steam
    )

    task_tf_steam_chart = PythonOperator(
        task_id='tf_steam_chart',
        python_callable=tf_steam_chart
    )

    task_fetch_stock = PythonOperator(
        task_id='fetch_stock',
        python_callable=fetch_stock
    )

    task_transform_daily_monthly = PythonOperator(
        task_id='transform_daily_monthly',
        python_callable=transform_daily_monthly
    )

    task_load_daily_monthly = PythonOperator(
        task_id='load_daily_monthly',
        python_callable=load_daily_monthly
    )

    # Define task dependencies
    task_scrape_game >> [task_extract_steam_price, task_fetch_data_steam, task_scrape_steam_chart]
    task_extract_steam_price >> task_tf_steam_price
    task_fetch_data_steam >> task_tf_data_steam
    task_scrape_steam_chart >> task_tf_steam_chart
    task_fetch_stock >> task_transform_daily_monthly >> task_load_daily_monthly
