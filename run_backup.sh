#!/bin/bash
OUT=$HOME/backups
python3 /home/shawn/make4covid_private/m4c-statistics/app/airtable.py --download_table "README;Equipment%20Requests;Users(new);Maker%20Information;Maker%20Production;Maker%20Supply%20Requests;Key%20Locations;Users;_Shipping%20WIP;Shipping;Orders%20(will%20delete);_Parts;Drivers;Manufacturer%20Intake;Shipping%20V2;Expense%20Tracker" --out_folder "$OUT"

