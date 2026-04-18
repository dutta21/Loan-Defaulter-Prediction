import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

CSV_FILE_PATH = r"C:\Users\Dell\Desktop\new_append.csv"
df = pd.read_csv(CSV_FILE_PATH)

conn = snowflake.connector.connect(
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    account=os.getenv("ACCOUNT"),
    warehouse=os.getenv("WAREHOUSE"),
    database=os.getenv("DATABASE"),
    schema=os.getenv("SCHEMA")
)

success, nchunks, nrows, _ = write_pandas(conn, df, "DEFAULTER")

print("Appended:", nrows)

conn.close()
