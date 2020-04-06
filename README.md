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

Order Progress
--------------

```
GET /stats
```

Get the number and status of each part in the Maker Production table.
Additionally, get the number of users.

output:

```
{
    "job counts": {
        "Clear Face Shield Long (Long_Wide_240) @1": {
            "": 15,
            "Contacted": 50
        },
        "Face Mask Buckle @1": {
            "": 319
        },
        "Prusa Headband @RC1": {
            "": 60,
            "Contacted": 30,
            "Scheduled 4 Drop Off": 20
        },
        "Prusa Headband @RC2": {
            "": 218,
            "Contacted": 59,
            "Delivery Out": 38,
            "Dropped Off": 45,
            "Picked Up": 230,
            "Scheduled 4 Drop Off": 90,
            "Scheduled 4 Pick Up": 67
        },
        "Prusa Headband @RC3": {
            "": 1503,
            "Collected": 530,
            "Contacted": 310,
            "Dropped Off": 25,
            "Picked Up": 374,
            "Scheduled 4 Drop Off": 120
        }
    },
    "total jobs": "130",
    "total members": "1431",
    "total requests": "82"
}

```

