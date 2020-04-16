import os
import tempfile

import requests
import argparse
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import json

app_id = os.environ.get('AIRTABLE_APP_ID')
app_key = os.environ.get('AIRTABLE_KEY')

base_url = "https://api.airtable.com/v0/%s" % app_id

class AirTable:
    def __init__(self, table):
        self.json_data = self.get_records_from_airtable("/" + table)
        self.table_name = table
        if self.json_data is None:
            raise Exception("Fetching table %s failed" % table)
        self.id_cache = None
        self.df = None

    def __len__(self):
        return len(self.json_data)

    def unique_column_values(self, name):
        vals = set()
        for row in self.json_data:
            if name in row['fields']:
                vals.add(row['fields'][name])
        return vals

    def sum_unique(self, group_by_cols, col_to_sum):
        out = {}
        for row in self.json_data:
            key = self.tuple_from_cols(row, group_by_cols)
            out[key] = row['fields'].get(col_to_sum,0) + out.get(key,0)
        return out

    def sum_if_column_matches(self, searched_column, count_column, predicate):
        count = 0
        for row in self.json_data:
            if count_column in row['fields'] and searched_column in row['fields'] and \
                    predicate(row['fields'][searched_column]):
                count += row['fields'][count_column]
        return count

    def column_by_id(self,id,column, default = None):
        if self.id_cache is None:
            self.id_cache = {}
            for row in self.json_data:
                self.id_cache[row['id']] = row
        return self.id_cache[id]['fields'].get(column,default)

    def to_dataframe(self):
        if(self.df is None):
            columns_defaults = {'id':""}
            for line in self.json_data:
                for f in line['fields']:
                    if isinstance(line['fields'][f],str):
                        columns_defaults[f] = ""
                    elif isinstance(line['fields'][f],list):
                        columns_defaults[f] = "[]"
                    else:
                        columns_defaults[f] = 0
            columns = list(columns_defaults)
            out = []
            for line in self.json_data:
                line_dat = []
                for field in columns:
                    column_val = columns_defaults[field]
                    if field in line:
                        column_val = line[field]
                    elif field in line['fields']:
                        column_val = line['fields'][field]
                    if isinstance(column_val, list):
                        column_val = json.dumps(column_val)
                    line_dat.append(column_val)
                out.append(line_dat)
            cleaned_columns = [self.clean_name(n) for n in columns]
            self.df = pd.DataFrame(np.array(out), columns=cleaned_columns)
        return self.df

    def sync_sql(self,sqlengine):
        df = self.to_dataframe()
        df.to_sql(self.table_name, con=sqlengine)

    @staticmethod
    def clean_name(n):
        out = ""
        for c in n:
            if c in ['/','\\','(',')',';',' ']:
                out += '_'
            else:
                out+= c
        return out

    @staticmethod
    def tuple_from_cols(json_obj, cols):
        out = []
        for col in cols:
            if col in json_obj['fields']:
                v = json_obj['fields'][col]
                if isinstance(v,list):
                    out.append(tuple(v))
                else:
                    out.append(v)
            else:
                out.append(None)
        return tuple(out)

    @staticmethod
    def get_records_from_airtable(table):
        user_list = []
        json = {'offset':None}
        while 'offset' in json:
            if json['offset'] is None:
                users = requests.get(base_url + table, headers={"Authorization": "Bearer %s" % app_key})
            else:
                users = requests.get(base_url + table,
                                     headers={"Authorization": "Bearer %s" % app_key},
                                     params={'offset':json['offset']})
            if users.status_code != 200:
                return None
            json = users.json()
            user_list.extend(json['records'])
        return user_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Air Table Data Downloader")
    parser.add_argument('--download_table', help="Specify table to dump to json.")
    parser.add_argument('--out_folder', help="Folder to write backups.")
    args = parser.parse_args()



    tables_to_download = args.download_table.split(";")
    out = {}
    for table in tables_to_download:
        print("Downloading table: %s" % table)
        t = AirTable.get_records_from_airtable("/" + table)
        time.sleep(1)
        out[table] = t

    fname = "airtable_backup" + str(time.time()) + ".json"
    out_file = os.path.join(args.out_folder,fname) if args.out_folder is not None else fname
    with open(out_file,'w') as f:
        f.write(json.dumps(out))


