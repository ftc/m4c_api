from app import app
from flask import jsonify
from flask_caching import Cache

from app.airtable import AirTable

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

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
@app.route('/stats', methods=['GET'])
@cache.cached(timeout=cache_time)
def manual_stats():
    manual_statistics_table = AirTable('Manual%20Statistics')
    jsdata = manual_statistics_table.json_data
    out = {}
    for row in jsdata:
        row_data = {}
        for field in MANUAL_STATS_FIELDS:
            row_data[field] = row['fields'][field]
        out[row['fields']['Name']] = row_data

    return jsonify(out)

@app.route('/stats_auto', methods=['GET'])
@cache.cached(timeout=cache_time)
def total_jobs():

    # Get Raw AirTable Data
    jobs = AirTable("Maker%20Production")
    users = AirTable("Users(new)")
    requests = AirTable("Equipment%20Requests")
    parts = AirTable("_Parts")

    # job_statuses = jobs.unique_column_values('Status')

    job_counts = jobs.sum_unique(['Part', 'Status'], 'Quantity')

    # Reformat job status counts without tuples and swap db id for human ID
    job_counts_for_human = {}
    for job_count_key in job_counts:
        if job_count_key[0] is None:
            continue
        human_readable_part = parts.column_by_id(job_count_key[0][0],'ID', "")
        if human_readable_part not in job_counts_for_human:
            job_counts_for_human[human_readable_part] = {}
        status = "" if job_count_key[1] is None else job_count_key[1]
        job_counts_for_human[human_readable_part][status] = job_counts[job_count_key]

    return jsonify({
        "total jobs":str(len(jobs)),
        "total members": str(len(users)),
        "total requests": str(len(requests)),
        "job counts": job_counts_for_human
    })
