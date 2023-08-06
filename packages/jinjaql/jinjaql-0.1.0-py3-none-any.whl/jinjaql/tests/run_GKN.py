import os
from jinjaql.factory import Snaql
import jinjaql.engine as engine
import pandas as pd

def nwt_engine(query_string: str, connection_string: str):
    """
    :param query_string: The raw query string to execute
    :param connection: Connection string formatted for use by PYODBC
    :return: A pandas DataFrame
    """
    connection = pyodbc.connect(connection_string)
    try:
        return pd.read_sql_query(query_string, connection)
    except Exception as e:
        print(e)
    finally:
        connection.close()

sql_root = os.path.abspath(os.path.dirname(__file__))

snaql = Snaql(sql_root, 'queries', engine=engine.pandas)

gkn_queries = snaql.load_queries('GKN_query.sql')
context = {
    'database':'C1_RDM',
    'station':'View_Station440',
}
result = gkn_queries.top_ten(**context)
print(result)
