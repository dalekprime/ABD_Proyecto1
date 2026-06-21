import pyodbc
import json

#Global Variables

SERVER = "localhost"
DATABASE = "StreamUCV"
USERNAME = "sa"
PASSWORD = "Cyber2026*"
DRIVER = "ODBC Driver 17 for SQL Server"
QUERIES_PATH = "queries/mainQueries.json"

#Main Connector
def connectToDB() -> pyodbc.Connection | None:
    connectionData = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
    )
    try: 
        return pyodbc.connect(connectionData)
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

#Query Master
def makeQuery(conexion: pyodbc.Connection, query: str) -> list:
    if conexion is None: return
    cursor = conexion.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()

#Query Loader
def queryLoader(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return {}


#Only for Testing Propouses
actualConnection = connectToDB()
queryList = queryLoader(QUERIES_PATH)
if actualConnection:
    print(makeQuery(actualConnection, queryList["10"]["query"]), queryList["10"]["desc"])
    actualConnection.close()