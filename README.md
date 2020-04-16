Make For Covid Statistics
=========================

REST Server for providing production statistics witht the Make 4 Covid group. Implemented using Python Flask.

Running Development Environment:
========
Set the following environment keys: `AIRTABLE_APP_ID` and `AIRTABLE_KEY`.

Use python 3.6. (Note: pyenv can be used to swap python versions on a per project basis https://github.com/pyenv/pyenv)


Install python dependencies: 
```
pip install Flask
pip install Flask-Caching
pip install requests
```

Obtain AirTable app id and API key, place these in the `~/m4c_airtable.sh` script.
```
export AIRTABLE_APP_ID="[ADD APP ID]"
export AIRTABLE_KEY="[ADD KEY]"
```

Set up the environment:
```
source env_setup.sh
```

Run Flask:
```
flask run
```



Endpoints:
==========

AirTable Statistics
--------------

```
GET /stats
```

Generate statistics based on the "Manual Statistics" airtable.  This api either returns a pre defined "Count" from each row or computes the statistics based on other tables using a SQL query.  SQL queries are sandboxed so writes will not affect airtable. We assume those who have access to AirTable are trusted to write code running on the server.

Sample output:

```
{
    "Community Members": {
        "Notes": "Number of Community Members",
        "Query Result": 2016,
        "Status": [
            "Calculate From SQL"
        ]
    },
    "Days": {
        "Notes": "Days in Operation",
        "Query Result": 24.865409629419446,
        "Status": [
            "Calculate From SQL"
        ]
    },
    "Headband Inventory": {
        "Notes": "Headbands in Inventory, sum of Denver and Colorado Springs.",
        "Query Result": 575,
        "Status": [
            "Calculate From SQL"
        ]
    },
    "PPE Requests": {
        "Notes": "Number of Requests for PPE",
        "Query Result": 138,
        "Status": [
            "Calculate From SQL"
        ]
    },
    "PPE Units Delivered": {
        "Notes": "Number of PPE Units Delivered",
        "Query Result": 14335,
        "Status": [
            "Calculate From SQL"
        ]
    },
    "Partner Organizations": {
        "Count": 105,
        "Date Updated": "2020-04-07",
        "Notes": "Number of Organizations Involved",
        "Status": [
            "Valid at time of update"
        ]
    }
}
```


