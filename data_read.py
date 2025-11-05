import json
import math
import os
from datetime import datetime

import pgeocode

# constants
MIN_DIST = 50  # km
MAX_DIST = 100  # km


SAFE_TEST_TIME = (30, 45)
MAX_TEST_TIME = 180
# --- inputs ---
"""
{
  "patienten_id":0,
  "patienten_postleitzahl":"00000",
  "teststelle":{
    "Teststelle":"NAME",
    "Postleitzahl":"00000",
    "datum":"2025-11-04 16:10"
  },
  "pzn":"000-000-000",
  "datum":"2025-11-04 16:11"
}
"""


def distance_check(distance):
    if distance <= MIN_DIST:
        return 1
    elif distance <= MAX_DIST:
        return (MAX_DIST - distance) / (MAX_DIST - MIN_DIST)
    else:
        return 0


def get_distance(postcode_patient, postcode_testcenter):

    geo_dist = pgeocode.GeoDistance("de")
    distance = geo_dist.query_postal_code(
        postcode_patient, postcode_testcenter)
    return distance


def time_check(difference_minutes):
    if difference_minutes <= SAFE_TEST_TIME[0]:
        return math.sin(difference_minutes * math.pi / (2 * SAFE_TEST_TIME[0]))
    if difference_minutes <= SAFE_TEST_TIME[1]:
        return 1

    if difference_minutes <= MAX_TEST_TIME:
        return math.cos(
            (difference_minutes - SAFE_TEST_TIME[1])
            * math.pi
            / (2 * MAX_TEST_TIME - 2 * SAFE_TEST_TIME[1])
        )

    return 0


def get_time(time_test, time_result):
    input_format = "%Y-%m-%d %H:%M"
    time_test_convertet = datetime.strptime(time_test, input_format)
    time_result_convertet = datetime.strptime(time_result, input_format)

    difference = time_result_convertet - time_test_convertet
    difference_minutes = difference.total_seconds() / 60
    return difference_minutes


def check(path):
    # Auslesen der Datei

    with open(path, "r") as file:
        data = json.load(file)

    print(data["teststelle"]["datum"])
    patienten_postleitzahl = data["patienten_postleitzahl"]
    teststelle_postleitzahl = data["teststelle"]["Postleitzahl"]
    get_distance(patienten_postleitzahl, teststelle_postleitzahl)


if __name__ == "__main__":
    check(input("hier Dateiname eingeben: "))

