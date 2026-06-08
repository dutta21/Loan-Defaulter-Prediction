import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
from dotenv import load_dotenv

load_dotenv()

CSV_FILE_PATH = r"C:\Users\Dell\Desktop\Defaulter.csv"   # change this


USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT = os.getenv("ACCOUNT")   # example: abc12345.ap-south-1.aws

WAREHOUSE = os.getenv("WAREHOUSE")
DATABASE = os.getenv("DATABASE")
SCHEMA = os.getenv("SCHEMA")
TABLE_NAME = os.getenv("TABLE_NAME")


df = pd.read_csv(CSV_FILE_PATH)

# Optional: make column names Snowflake-friendly
df.columns = [col.replace(" ", "_") for col in df.columns]


conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT
)

cur = conn.cursor()

try:
    
    cur.execute(f'USE WAREHOUSE "{WAREHOUSE}"')
    cur.execute(f'USE DATABASE "{DATABASE}"')
    cur.execute(f'USE SCHEMA "{SCHEMA}"')

    
    col_defs = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype):
            col_defs.append(f'"{col}" INT')
        elif "float" in str(dtype):
            col_defs.append(f'"{col}" FLOAT')
        else:
            col_defs.append(f'"{col}" STRING')

    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS "{TABLE_NAME}" (
        {", ".join(col_defs)}
    )
    '''
    cur.execute(create_table_sql)

    success, nchunks, nrows, _ = write_pandas(conn, df, TABLE_NAME)

    print("Upload Success:", success)
    print("Chunks Uploaded:", nchunks)
    print("Rows Inserted:", nrows)

    
    cur.execute(f'SELECT COUNT(*) FROM "{TABLE_NAME}"')
    print("Total Rows in Table:", cur.fetchone()[0])

finally:
    cur.close()
    conn.close()
