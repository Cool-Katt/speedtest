import os
import glob
import subprocess 
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASSWORD')
DB = os.getenv('DB_DATABASE')
SCHEMA = os.getenv('DB_SCHEMA')
TABLE_NAME = os.getenv('DB_TABLE_NAME')

def runFetcher():
    """Runs the fetcher companion program to get CSV files."""
    s = subprocess.check_call("speedtest.exe")
    return s

def readFilesIntoDF():
    """
    Returns a Pandas.DataFrame object based on the fetched CSV files from user's Downloads folder
    """
    path = str(Path.home() / 'Downloads')
    all_files = glob.iglob(os.path.join(path, "speedtest-results*.csv"))
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

    # Remove unused columns and format datetime column
    df["resultDate"] = pd.to_datetime(df["resultDate"]).dt.tz_convert(None)
    df.drop(['serverId','serverName'], axis=1, inplace=True)

    return df

def insertDFIntoDB(dataFrame):
    """
    Connects to the DB and inserts the given DataFrame into the Specified table.
    If an entry is already in the specified table, it's skipped.
    """
    engine = create_engine(f'mssql+pymssql://{USER}:{PASS}@{HOST}/{DB}')

    selectExistingQuery = f"""SELECT * FROM {DB}.{SCHEMA}.{TABLE_NAME}"""
    testDF = pd.DataFrame(pd.read_sql_query(selectExistingQuery, engine))
    dataFrame = dataFrame[~dataFrame.testId.isin(testDF.testId)]
    if len(dataFrame) > 0:
        dataFrame.to_sql(name=TABLE_NAME, con=engine, schema=SCHEMA, if_exists="append", index=False)

def cleanup():
    """
    Cleans up the user's Downloads folder from the CSV files used already.
    """
    path = str(Path.home() / 'Downloads')
    all_files = glob.iglob(os.path.join(path, "*.csv"))
    for file in all_files:
        if 'speedtest-results' in file:
            os.remove(file)

if __name__ == "__main__":
    try:
        runFetcher()
    except RuntimeError as e:
       print("Could not fetch data. Check if fetcher works")
       raise

    df = readFilesIntoDF()
    insertDFIntoDB(df)
    cleanup()
