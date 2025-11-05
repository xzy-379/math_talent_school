import json
import math
import sys
from datetime import datetime

import pgeocode

# constants
DEBUG = False

PZN_PATH = "actual_pzn.csv"
DETAILS_PATH = "actualdetails_teststelle.csv"

MIN_DIST = 50  # km
MAX_DIST = 100  # km


SAFE_TEST_TIME = (30, 45)
MAX_TEST_TIME = 180


def pzn_check(pzn):
    with open(PZN_PATH, "r") as file:
        text = file.read()
        pzn_list = text.splitlines()
        for legit_pzn in pzn_list:
            if pzn == legit_pzn:
                return 1

        return 0


def name_check(name):
    return True


def distance_check(distance):
    if math.isnan(distance):
        return 0

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
    patienten_postleitzahl = data["patienten_postleitzahl"]
    teststelle_postleitzahl = data["teststelle"]["Postleitzahl"]
    time_test = data["teststelle"]["datum"]
    time_result = data["datum"]

    name = data["teststelle"]["name"]
    pzn = data["pzn"]

    distance = get_distance(patienten_postleitzahl, teststelle_postleitzahl)
    time = get_time(time_test, time_result)

    checked_name = name_check(name)
    checked_pzn = pzn_check(pzn)
    checked_time = time_check(time)
    checked_distance = distance_check(distance)

    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check(sys.argv[1])

    else:
        check(input("input name of document: "))
