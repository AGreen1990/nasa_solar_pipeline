import requests
import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery

#Loads the hidden passwords from dotenv file
load_dotenv()
#Grab the API key
api_key = os.getenv("NASA_API_KEY")

#1 -- Authenticate with Google Cloud
#Tells BigQuery library exactly where to find JSON Keycard
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="gcp_key.json"
client = bigquery.Client()

# --2. The Extract --
url = f"https://api.nasa.gov/DONKI/CME?api_key={api_key}"

print("Fetching data from NASA. . .")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Success! Grabbed {len(data)} CME records.")

    # Bronze Prep
    #converts every rec into a single JSON string wrapped in a dict
    bronze_data =[{"raw_payload": json.dumps(record)} for record in data]

    #-- 3. The Load
    # Format: "your-project-id.dataset_name.table_name"
    table_id = "space-weather-monitor-501822.nasa_bronze.raw_cme"

    #config how BigQuery should handle data
    job_config = bigquery.LoadJobConfig(
        #WRITE_TRUNCATE "wipe clean old table and replace with this fresh data"
        write_disposition="WRITE_TRUNCATE",
        # autodetect=True tells BQ to figure out the nested JSON schema automatically
        autodetect=True,
        schema=[
            bigquery.SchemaField("raw_payload", "JSON")
        ]
    )

    print("Loading data into BigQuery. . .")
    #push the python dict directly into the BQ table
    job = client.load_table_from_json(bronze_data, table_id, job_config=job_config)

    #waits for cloud to finish processing job
    job.result()

    print(f"Boom! Successfully load {job.output_rows} rows into {table_id}.")
else: 
    print(f"Something went wrong. Status Code: {response.status_code}") 