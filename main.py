import os
import glob
import subprocess 
import pymssql
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASSWORD')
DB = os.getenv('DB_DATABASE')

def runFetcher():
    s = subprocess.check_call("speedtest.exe")
    return s

def readFilesIntoDF():
    path = str(Path.home() / 'Downloads')
    all_files = glob.iglob(os.path.join(path, "*.csv"))
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    return df

def connectToDB(dataFrame):
    conn_str = pymssql.connect(host=HOST, user=USER, password=PASS, database=DB)
    engine = create_engine(f'mssql+pymssql://{USER}:{PASS}@{HOST}/{DB}')
    dataFrame.to_sql(name="test_table", con=engine, schema="REPORT", if_exists="replace", index=False)
    #myCursor = conn_str.cursor() 
    #conn_str.close()

if __name__ == "__main__":
    # if runFetcher() == 0:
    #   df = readFilesIntoDF()

    #   print(df.describe)

    df = readFilesIntoDF()
    #df["resultDate"] = pd.to_datetime(df["resultDate"])
    df.drop(['serverId','serverName'], axis=1, inplace=True)
    #df["testId"] = df["testId"].astype("string")
    print(df.dtypes)
    print(df.describe)
    connectToDB(df)
