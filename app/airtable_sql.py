# import pandasql
# import seaborn as sns
import tempfile
import os

import pandas as pd
import numpy as np

# data = sns.load_dataset('iris')
#
# res = pandasql.sqldf("SELECT * FROM data WHERE petal_length > 5.0;", {"data":data})
# # print(res)
#
# d = {"col1": [1,2,3], "col2" : [3,4,4]}
#
# df = pd.DataFrame(data=d, dtype=np.int8)
#
# res = pandasql.sqldf("select col2,SUM(col1) from d GROUP BY col2;", {'d':df})
# print(res)
from sqlalchemy import create_engine

from app.airtable import AirTable

def is_empty(row):
    for v in row:
        if v != '':
            return False
    return True
def convert_sql_results(res):
    results_out = []
    for v in res:
        row_out = []
        for v1 in v:
            row_out.append(v1)
        if not is_empty(row_out):
            results_out.append(row_out)
    return results_out

def convert_single_val(v):
    if len(v) == 1 and len(v[0]) == 1:
        return v[0][0]
    else:
        return None

def sql_airtable(table_list, query):
    try:
        sqlfile = tempfile.mkstemp()
        sql_url = 'sqlite:///%s' % sqlfile[1]
        sqlengine = create_engine(sql_url, echo=False)

        for t in table_list:
            AirTable(t).sync_sql(sqlengine)

        out = sqlengine.execute(query).fetchall()

        # Unwrap single value
        single_val = convert_single_val(out)
        if convert_single_val(out) is not None:
            return single_val
        else:
            return convert_sql_results(out)
    finally:
        os.remove(sqlfile[1])



if __name__ == "__main__":
    # d = {'col1': ['1', '2'], 'col_2': ['4*', 4]}
    # df = pd.DataFrame(np.array([[1,2],['3*',4]]), columns=['a','b'])
    # print(str(df))
    # res = pandasql.sqldf("SELECT * FROM d;",{'d':df})
    # print(res)
    out = sql_airtable(["Users(new)"], 'SELECT count(*) from "Users(new)";')
    print("user count: " +  str(out))

    out = sql_airtable(["Users(new)"], 'SELECT count(*) from "Users(new)";')
    print("user count: " +  str(out))

    out = sql_airtable(["Equipment Requests"], 'SELECT DISTINCT Organization from "Equipment Requests";')
    print("organizations: " + str(out))

