import requests #interact with APIs
import pandas as pd #for data manipulation
from sqlalchemy import create_engine
import configparser
import psycopg2 

def etl_process():
    # Load my confidentials from my config
    config = configparser.ConfigParser()
    config.read('config.ini')

    #create postgres engine
    postgres_config = config['postgres']

    engine = create_engine(
        f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}"        
    )

    # Northwind API request for order
    endpoint_url = 'https://demodata.grapecity.com/northwind/api/v1/Customers'
    api_reponse = requests.get(endpoint_url)
    data = api_reponse.json()

    # Load data into Postgres
    df = pd.json_normalize(data)
    df.to_sql('customers', engine, if_exists = 'replace', index = False)
    engine.dispose()

etl_process()