Make For Covid Statistics
=========================

REST Server for providing production statistics witht the Make 4 Covid group.

Endpoints:
==========

Order Progress
--------------

```
GET /order_progress
```

Track the progress of each order.

Sample output:
```json
[
  {
    "Name": "Stockpile 1000", 
    "Units": 1000, 
    "id": "recEYZdXthygNyqb7", 
    "in_progress": 3538, 
    "made": 0
  }, 
  {
    "Name": "500 to Denver Health", 
    "Units": 500, 
    "id": "recvSFVHM0LMXd2Bh", 
    "in_progress": 30, 
    "made": 0
  }
]
```

Unit Count
----------

`GET /unit_count`

Count the number of in progress and completed units in the jobs table. 

Sample output:
```
{
  "completed_parts": {
    "Clear Face Shield (Short_Wide_v1) @1": 2, 
    "Flat Pack Shield (Laser Only) @1": 50, 
    "Prusa Head Band @RC1": 49
  }, 
  "in_progress_parts": {
    "Clear Face Shield (Short_Wide_v1) @1": 6, 
    "Fastener @1": 25, 
    "Flat Pack Shield (Laser Only) @1": 5, 
    "Prusa Head Band @RC1": 16, 
    "Prusa Headband @RC2": 5, 
    "Prusa Headband @RC3": 9
  }, 
  "job_count": 26
}
```

User Count
----------

`/total_users`

Count the number of users in the group.

Sample output:
```
374
```

Job Count
---------

`/total_jobs`

Count the total number of jobs in the group.

Sample output:
```
26
```
