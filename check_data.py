import snowflake.connector
import pandas as pd
import model_create
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT = os.getenv("ACCOUNT")   # example: abc12345.ap-south-1.aws

WAREHOUSE = os.getenv("WAREHOUSE")
DATABASE = os.getenv("DATABASE")
SCHEMA = os.getenv("SCHEMA")
TABLE_NAME = os.getenv("TABLE_NAME")

# -----------------------------
# CONNECT TO SNOWFLAKE
# -----------------------------
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)

cur = conn.cursor()

try:
    # Query the table
    query = f'SELECT * FROM "{DATABASE}"."{SCHEMA}"."{TABLE_NAME}"'
    cur.execute(query)

    # Fetch all rows
    rows = cur.fetchall()

    # Get column names
    columns = [desc[0] for desc in cur.description]

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=columns)

    print("Data from Snowflake Table:\n")
    print(df)
    model_create.main(df)

finally:
    cur.close()
    conn.close()
