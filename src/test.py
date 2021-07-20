def update(month, day):
    day = day + 1
    if month == 2 and day == 29:
        month = 3
        day = 1
    elif day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
        month = month + 1
        day = 1
    elif day == 32:
        day = 1
        month = month + 1
        if month == 13:
            month = 1
    return month, day


month = 6
day = 3
for i in range(0,100):
    month, day = update(month,day)
    print([month, day])
