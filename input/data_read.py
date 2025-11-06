import json
import math
import sys
import os
from datetime import datetime
from sus_test import estimate_Oliver

import matplotlib.pyplot as plt
import pgeocode

# constants
DEBUG = False

PATH = os.getcwd()

PZN_PATH = PATH + "/input/actual_pzn.csv"
DETAILS_PATH = PATH + "/input/actualdetails_teststelle.csv"

MIN_DIST = 50  # km
MAX_DIST = 100  # km

SAFE_TEST_TIME = (30, 45)
MAX_TEST_TIME = 180

def pzn_check(pzn):
    with open(PZN_PATH, "r") as file:
        pzn_list = file.read().splitlines()

    for legit_pzn in pzn_list:
        if pzn == legit_pzn:
            return 1

    return 0


def name_check(name):
    with open(DETAILS_PATH, "r") as file:
        details = file.read().splitlines()

    for detail in details[1:]:
        stelle = detail.split(",")[1]
        if name == detail.split(",")[1]:
            return 1
    return 0


def distance_check(distance):
    if distance is int:
        return 1
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
    with open("dateien/patienten/" + path, "r") as file:
        data = json.load(file)
    patienten_postleitzahl = data["patienten_postleitzahl"]
    teststelle_postleitzahl = data["teststelle"]["postleitzahl"]
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

    return checked_name, checked_pzn, checked_time, checked_distance


if __name__ == "__main__":
    for i in range(30):
        (estimated_distance, estimated_name, estimated_pzn, estimated_time) = check(str(i+1)+".json")
        sus = estimate_Oliver(distance_check=estimated_distance, time_check=estimated_time, name_check=estimated_name, pzn_check=estimated_pzn)
        print("sus level"+str(i)+": " + str(sus))
    
    # graph for time
    x = [i for i in range(int(MAX_TEST_TIME*1.1))]
    y= [time_check(i) for i in x]

    plt.plot(x, y)
    plt.ylabel("checked_time")
    plt.xlabel("time in minutes")
    plt.savefig("time.png")
    plt.close()
    # graph for distance
    x= [i for i in range(int(MAX_DIST*1.1))]
    y= [distance_check(i) for i in x]

    plt.plot(x, y)
    plt.ylabel("checked_distance")
    plt.xlabel("distance in km")
    plt.savefig("distance.png")
