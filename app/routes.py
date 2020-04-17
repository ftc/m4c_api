from app import app
from flask import jsonify, render_template
from flask_caching import Cache
from flask_cors import CORS

from app.airtable import AirTable
from app.airtable_sql import sql_airtable

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
CORS(app)


import requests


# Airtable authentication keys


cache_time = 300

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    response = "Internal server error, please try again later."
    return response,500



def is_made(job):
    return 'Made' in job['fields'] and job['fields']['Made']

MANUAL_STATS_FIELDS = ["Notes",'Date Updated','Count','Status']
AUTO_STATS_FIELDS = ["Notes",'Status']
@app.route('/stats', methods=['GET'])
@cache.cached(timeout=cache_time)
def manual_stats():
    manual_statistics_table = AirTable('Manual%20Statistics')
    jsdata = manual_statistics_table.json_data
    out = {}
    for row in jsdata:
        row_data = {}
        if 'Status' in row['fields'] and row['fields']['Status'] == ["Calculate From SQL"]:
            table_list = row['fields']['From Tables'].split(",")
            try:
                query_result = sql_airtable(table_list, row['fields']['SQL Query'])
            except:
                query_result = "Query Error"
            row_data["Query Result"] = query_result
            for field in AUTO_STATS_FIELDS:
                row_data[field] = row['fields'][field]
        else:
            for field in MANUAL_STATS_FIELDS:
                row_data[field] = row['fields'][field]
        out[row['fields']['Name']] = row_data

    return jsonify(out)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')


