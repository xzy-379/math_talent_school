import json
import math
import os
import sys
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pgeocode

# constants
PATH = os.getcwd()

PZN_PATH = PATH + "/input_files/actual_pzn.csv"
DETAILS_PATH = PATH + "/input_files/actualdetails_teststelle.csv"

MIN_DIST = 50  # km
MAX_DIST = 100  # km

SAFE_TEST_TIME = (30, 45)
MAX_TEST_TIME = 180

def pzn_check(pzn):
    with open(PZN_PATH, "r") as file:
        pzn_list = file.read().splitlines()
    min_diff_rate = 1.0
    for legit_pzn in pzn_list:
        if pzn == legit_pzn:
            return 1
        else:
            pzn_diff_rate = rate_name_diff(pzn, legit_pzn)
            if pzn_diff_rate < min_diff_rate:
                min_diff_rate = pzn_diff_rate
    return 1 - (1/(min_diff_rate + 1))


def name_check(name):
    with open(DETAILS_PATH, "r") as file:
        details = file.read().splitlines()
    min_difference_rate = 1.0
    for detail in details[1:]:
        stelle = detail.split(",")[1]
        if name == stelle:
            return 1
        else:
            name_diff_rate = rate_name_diff(stelle, name)
            if name_diff_rate < min_difference_rate:
                min_difference_rate = name_diff_rate
    return 1 - min_difference_rate

def rate_name_diff(name_bogen, name_actual):
    differences = len(name_bogen) - len(name_actual)
    
    for i in range(min(len(name_actual), len(name_bogen))):
        if name_bogen[i] != name_actual[i]:
            differences += 1
    if differences == 0:
        return 0
    return 1 - (1/(differences + 1))

def rate_pzn_diff(pzn_bogen, pzn_actual):
    differences = len(pzn_bogen) - len(pzn_actual)
    
    for i in range(min(len(pzn_actual), len(pzn_bogen))):
        if pzn_bogen[i] != pzn_actual[i]:
            differences += 1
    if differences == 0:
        return 0
    print("pzn diff:" + differences)
    return 1 - (1/(differences + 1))


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
    if difference_minutes <= 0:
        return 0
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
    if difference_minutes <= 0:
        return 0
    return difference_minutes


def check(path):
    with open(path, "r") as file:
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

    original_values = (name, pzn, time, distance)
    return checked_name, checked_pzn, checked_time, checked_distance, original_values


if __name__ == "__main__":
    
    # graph for time
    x = [i for i in range(int(MAX_TEST_TIME * 1.1))]
    y = [time_check(i) for i in x]

    plt.plot(x, y)
    plt.ylabel("checked_time")
    plt.xlabel("time in minutes")
    plt.savefig("time.png")
    plt.close()
    # graph for distance
    x = [i for i in range(int(MAX_DIST * 1.1))]
    y = [distance_check(i) for i in x]

    plt.plot(x, y)
    plt.ylabel("checked_distance")
    plt.xlabel("distance in km")
    plt.savefig("distance.png")
