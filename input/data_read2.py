import json
import math
import os
from datetime import datetime
import csv

import pgeocode

# constants
MIN_DIST = 50  # km
MAX_DIST = 100  # km


SAFE_TEST_TIME = (30, 45)
MAX_TEST_TIME = 180

PZN_PATH = "actual_pzn.csv"
DETAILS_PATH = "actualdetails_teststelle.csv"
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
def name_check(name):
    with open(DETAILS_PATH, "r") as file:
        actual_data = csv.DictReader(file)
        for stelle in actual_data:
            if stelle["name"] == name:
                return 1
        return 0
    
def pzn_check(pzn):
    with open(PZN_PATH, "r") as file:
        text = file.read()
        pzn_list = text.splitlines()
        for legit_pzn in pzn_list:
            if pzn == legit_pzn:
                return 1

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
    teststelle_postleitzahl = data["teststelle"]["postleitzahl"]
    teststelle_name = data["teststelle"]["name"]
    time_test = data["teststelle"]["datum"]
    time_result = data["datum"]
    pzn = data["pzn"]

    time = get_time(time_test, time_result)
    distance = get_distance(patienten_postleitzahl, teststelle_postleitzahl)
    estimated_distance = distance_check(distance)
    estimated_name = name_check(teststelle_name)
    estimated_time = time_check(time)
    estimated_pzn = pzn_check(pzn)

    return (estimated_distance, estimated_name, estimated_pzn, estimated_time)
    
def estimate_sus(distance_check, name_check, time_check, pzn_check):
    
    highsus = 0
    midsus = 0
    lowsus = 0

    if name_check == 0 or pzn_check == 0:
        highsus = 1
        midsus = 1
        lowsus = 1

    if time_check <= 0.6 or distance_check <= 0.6:
        midsus = max(time_check, distance_check)
        lowsus = 1
    if time_check > 0.4 and distance_check > 0.4:
        lowsus = min(time_check, distance_check)

    sus = 0.6 * highsus + 0.3 * midsus + 0.1 * lowsus


if __name__ == "__main__":
    (estimated_distance, estimated_name, estimated_pzn, estimated_time) = check(input("hier Dateiname eingeben: "))
    sus = estimate_sus(distance_check=estimated_distance, time_check=estimated_time, name_check=estimated_name, pzn_check=estimated_pzn)
    print("Fraud probability: " + str(sus))
