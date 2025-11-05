teststelle = 1
PZN = 1
time_diff = 1
add_diff = 1

highsus = 0
midsus = 0
midsus1 = 0 
midsus2 = 0
lowsus = 0



if teststelle == 0 or PZN == 0:
    highsus = 1


    midsus = 1
    lowsus = 1

if time_diff >= 0.4 or add_diff >= 0.4:
    midsus = max(time_diff, add_diff)
    lowsus = 1
if time_diff > 0.4 and add_diff > 0.4:
    lowsus = min(time_diff, add_diff)

sus = 0.6 * highsus + 0.3 * midsus + 0.1 * lowsus


if time_diff >= 0 and time_diff <= 0.15:
    midsus1 = 0.1

elif time_diff > 0.1 and time_diff <= 0.33:
    midsus1 = 0.33
elif time_diff > 0.33 and  time_diff <= 0.66:
    midsus1 = 0.66 
elif time_diff > 0.66 and time_diff < 0.8:
    midsus1 = 0.67
else:
    midsus1 = 1

if add_diff >= 0 and add_diff <= 0.15:
    midsus2 = 0.1
elif add_diff > 0.1 and add_diff <= 0.33:
    midsus2 = 0.33
elif add_diff > 0.33 and  add_diff <= 0.66:
    midsus2 = 0.66 
elif add_diff > 0.66 and add_diff > 0.8:
    midsus2 = 0.67
else:
    midsus2 = 1



if add_diff == 0 or time_diff == 0 or PZN == 1 or teststelle == 1:
    lowsus = 0.2




midsus = round(((midsus1 + midsus2))/2, 3)
if teststelle == 0 or PZN == 0:
    output = 1
else:
    output = round(( midsus*0.8 + lowsus)-0.2, 3)

print(output)

'''print(highsus, midsus, lowsus)'''    


    
