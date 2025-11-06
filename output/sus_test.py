def evaluate(teststelle, PZN, time_diff, add_diff):
    highsus = 0
    midsus = 0
    midsus1 = 0
    midsus2 = 0
    lowsus = 0
    if teststelle == 0 or PZN == 0:
        highsus = 1

    if time_diff >= 0 and time_diff <= 0.15:
        midsus1 = 0.1

    elif time_diff > 0.1 and time_diff <= 0.33:
        midsus1 = 0.33
    elif time_diff > 0.33 and time_diff <= 0.66:
        midsus1 = 0.66
    elif time_diff > 0.66 and time_diff < 0.8:
        midsus1 = 0.67
    else:
        midsus1 = 1

    if add_diff >= 0 and add_diff <= 0.15:
        midsus2 = 0.1
    elif add_diff > 0.1 and add_diff <= 0.33:
        midsus2 = 0.33
    elif add_diff > 0.33 and add_diff <= 0.66:
        midsus2 = 0.66
    elif add_diff > 0.66 and add_diff > 0.8:
        midsus2 = 0.67
    else:
        midsus2 = 1
    if add_diff == 0 or time_diff == 0 or PZN == 1 or teststelle == 1:
        lowsus = 0.2

    midsus = round(((midsus1 + midsus2)) / 2, 3)
    if teststelle == 0 or PZN == 0:
        output = 1
    else:
        output = round((midsus * 0.8 + lowsus) - 0.2, 3)

    return (output, (highsus, midsus, lowsus))

def estimate_Oliver(distance_check, name_check, time_check, pzn_check):
    
    highsus = 0
    midsus = 0
    lowsus = 0
    if name_check == 0 or pzn_check == 0:
        highsus = 1
        midsus = 1
        lowsus = 1

    if time_check <= 0.6 or distance_check <= 0.6:
        highsus = max(time_check, distance_check) * 0.5
        midsus = max(time_check, distance_check)
        lowsus = 1
    if time_check > 0.6 and distance_check > 0.6:
        lowsus = min(time_check, distance_check)

    sus = 0.6 * highsus + 0.3 * midsus + 0.1 * lowsus
    return sus