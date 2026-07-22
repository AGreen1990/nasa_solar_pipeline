import pandas as pd
import requests
from io import StringIO

#1 Target the CACTUS raw text dump
url = "https://www.sidc.be/cactus/out/latestCMEs.html"
response = requests.get(url)

#2 Preclean the messy html data
# 'split webpage line by line and only keep line that have a pip '|'
#ignore any lines staring with '#'
valid_lines = [line for line in response.text.split('\n') if '|' in line and not line.startswith('#')]
clean_text = '\n'.join(valid_lines)

#3. Definte clean database schema
col_names = [
    'cme_id', 'start_time', 'duration', 'principal_angle', 
    'angular_width', 'speed', 'dv', 'minv', 'maxv', 'halo_threat_level'
]

#4 Parse cleaned text into pandas
df = pd.read_csv(StringIO(clean_text), sep='|', names=col_names, skipinitialspace=True)

#5 Clean up empty values. Empties become 'None'
df['halo_threat_level'] = df['halo_threat_level'].fillna('None').astype(str).str.strip()
df.loc[df['halo_threat_level'] == '', 'halo_threat_level'] = None

#6. Data type conversion
df['start_time'] = pd.to_datetime(df['start_time'])

#7 View the structured table paylod
print(df.head())
print(df.dtypes)

from google.oauth2 import service_account
from google.cloud import bigquery

#1 define exact path to JSON file on local computer
# replace with actual file path and project id
key_path = "gcp_key.json"
project_id = "space-weather-monitor-501822"

#2 load credentials
credentials = service_account.Credentials.from_service_account_file(key_path)

#3 Hands the credentials to BigQuery Client
client = bigquery.Client(credentials=credentials, project=project_id)

#4 define new dataset and new table name
table_id = f"{project_id}.nasa_bronze.raw_cactus_cme"

#Write DataFrame directly to BigQUert (CREATE IF NOT EXIST or WRITE TRUNCATE/APPEND)
print (f"Uploading to {table_id}. . .")
job = client.load_table_from_dataframe(df, table_id)
job.result() #waits for job to complete

print("✅ Successfully loaded CACTUS data to BigQuery!")


#Commenting out previous DONKI API call- Cactus Code upgrade for more real time data
# import requests
# import os
# import json
# from dotenv import load_dotenv
# from google.cloud import bigquery

# #Loads the hidden passwords from dotenv file
# load_dotenv()
# #Grab the API key
# api_key = os.getenv("NASA_API_KEY")

# #1 -- Authenticate with Google Cloud
# #Tells BigQuery library exactly where to find JSON Keycard
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="gcp_key.json"
# client = bigquery.Client()

# # --2. The Extract --
# url = f"https://api.nasa.gov/DONKI/CME?api_key={api_key}"

# print("Fetching data from NASA. . .")
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     print(f"Success! Grabbed {len(data)} CME records.")

#     # Bronze Prep
#     #converts every rec into a single JSON string wrapped in a dict
#     bronze_data =[{"raw_payload":record} for record in data]

#     #-- 3. The Load
#     # Format: "your-project-id.dataset_name.table_name"
#     table_id = "space-weather-monitor-501822.nasa_bronze.raw_cme"

#     #config how BigQuery should handle data
#     job_config = bigquery.LoadJobConfig(
#         #WRITE_TRUNCATE "wipe clean old table and replace with this fresh data"
#         write_disposition="WRITE_TRUNCATE",
#         # autodetect=True tells BQ to figure out the nested JSON schema automatically
#         autodetect=True,
#         schema=[
#             bigquery.SchemaField("raw_payload", "JSON")
#         ]
#     )

#     print("Loading data into BigQuery. . .")
#     #push the python dict directly into the BQ table
#     job = client.load_table_from_json(bronze_data, table_id, job_config=job_config)

#     #waits for cloud to finish processing job
#     job.result()

#     print(f"Boom! Successfully load {job.output_rows} rows into {table_id}.")
# else: 
#     print(f"Something went wrong. Status Code: {response.status_code}") 
