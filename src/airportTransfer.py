"""
Here we get to retrieve the information from the AirportTransfer website.
Basically we got the URL and headers params from the dev tools and retrieved the information for a day's bookings.
This way we don't have to dig into the website (which has a horrible loading data system, specially in the frontend)
and just automate the blood out of that process too.
"""

import json
import requests
import datetime
from src.utils import colored_print
from datetime import timedelta

def generate_at_bookings():
    # today = datetime.date.today()
    tomorrow = datetime.date.today() + timedelta(days=1)

    # URL to get all bookings from a day, must be changed everyday
    url = f"https://api.airporttransfer.com/api/bookings?filters%5Bselected_date%5D={tomorrow}&pag"

    # I dont think i want to send this to github hahaha
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://airporttransfer.com",
        "Referer": "https://airporttransfer.com/",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMjNiOWZjNmI4MzhhNTVkYjJlY2YyZWVhNDFmNzE0NTQ0ZGYzYzViMjdkZjRkMGIwMzZiNDA0ZTVhOGUwZGViM2E1ODk4ODM1YTg5YTQ0NWUiLCJpYXQiOjE3NDQwNzk3MTQuNDk3MzAyLCJuYmYiOjE3NDQwNzk3MTQuNDk3MzA0LCJleHAiOjE3NzU2MTU3MTQuNDg3OTk5LCJzdWIiOiIyODk0Iiwic2NvcGVzIjpbXX0.JEvYlv7aYr19Nv2XBgsXyKYINAFQs1RJ3VRUL0c2tKgkAv78Ld4DB6wbzqGrUEiZKVYaPmNebLCkOnzSiFSZ_Gml5IFZe8mQYBLzO5B90r6d3bdd1Emo9XV_31xrvzqBokmG3aznCc3dsnhHNiyz6l_1SW8vqmMddP1nstPD2Vvz-4YGlLs4qKKqhWHimY1tvcxtWLaQ4yo0uBRy5N9dE9RbZMI2MG1RGtG1XYbL3Galex4H1mdrr2jGSWuvVzfEsJ-8OC9ElziD_abW7QnceRkZhqsp0SN9G-iQTV7sri4XWCpVp0LbamNTvtvN16buflphtWSpxeSH6HDPh6ZTdI8rRsMpD8evH_fLoh6zSeZXrGNLXUsHRdITVTeufYFVtf0sLcsRDuzVOALon-UrCLrSEpAcEBE4PL1BsisRlH5ZSDlG_L_RLJEQ1COT1ACWLClgVjWldk7SrKbtHbjExsyJs5eNYRz2_TyW0vGfzSp4nUJUaI96cDVtnJPLpzv5jDRDZdYPtzKgczbO8Ag3zKAkO127I4qqWOwCxepqhQ-wW1jCjtNzlXyzimiM3ulVAlgKOrOKqp7DZ3Odqo3wqJsBrLmDODWm1SBrN1WW-MBm9SitDEzTtj7C6ZYrpHBYAwgVZJFha0iblwDfEn9h56qYaOINlhplVmAMdeVRV3I"  # If needed
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        colored_print("Got AirportTransfer's today's data!", "green")

    with open("src/ATbookings.json", "w", encoding="utf-8") as fl:
        if fl:
            data = response.json()
            json.dump(data, fl, indent=4)
        else:
            colored_print("Something went wrong, could not open file.", "red")


