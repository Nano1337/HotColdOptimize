import pyodbc
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os

# Access .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Provide database specific information with Secure Authentication
cnxn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=" + str(os.getenv("Server1")) + ";"
    "Database=" + str(os.getenv("Database1")) + ";"
    "UID=" + str(os.getenv("UID1")) + ";"
    "PWD=" + str(os.getenv("PWD1")) + ";"
)

# connect to database
cnxn = pyodbc.connect(cnxn_str)

# Define SQL Query
SQL_Query = "SELECT TOP(1000) * FROM [DataManagementSvc].Project"

# Extract results of SQL Query using Pandas
data = pd.read_sql(SQL_Query, cnxn)

print(data)
