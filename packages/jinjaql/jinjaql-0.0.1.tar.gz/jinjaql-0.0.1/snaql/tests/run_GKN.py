import os
from snaql.factory import Snaql
import snaql.engine as engine

sql_root = os.path.abspath(os.path.dirname(__file__))

snaql = Snaql(sql_root, 'queries', engine=engine.pandas)

gkn_queries = snaql.load_queries('GKN_query.sql')
context = {
    'database':'C1_RDM',
    'station':'View_Station440',
}
result = gkn_queries.top_ten(**context)
print(result)
