from pulp import *
import math, csv, sys
from datetime import date
pi = math.pi
d0 = date(1975, 11, 30)

tmax = []
tmin = []
average = []
day = []

def days_passed(element):
    start = count = 0

    while True:
        if count == 10:
            break

        if element[start] == ',':
            count += 1

        start += 1

    end = start + 4
    yr = int(element[start:end])

    start += 4
    end += 2

    mn = int(element[start:end])

    start += 2
    end += 2

    dy = int(element[start:end])

    d1 = date(yr, mn, dy)

    delta = d1 - d0
    
    day.append(int(delta.days))
    
def avgs():
    count = 0

    for x in tmax:
        tmp1 = float(x / 10)
        tmp2 = float(tmin[count] / 10)
        average.append((tmp1 + tmp2) / 2)
        count += 1


def parse2(element):
    start = count = 0

    while True:
        if count == 11:
            break

        if element[start] == ',':
            count += 1

        start += 1

    end = start

    while True:
        if element[end] == ',':
            break
        
        end += 1

    tmax.append(int(element[start:end]))

    start = end + 1

    tmin.append(int(element[start:len(element)]))

def parse(element):
    start = end = 27

    while True:
        if element[end] == ';':
            break
        end += 1

    tmax.append(int(element[start:end]))

    start = end = end + 1


    while True:
        if element[end] == ';':
            break
        end += 1

    tmin.append(int(element[start:end]))

    end = end + 6

    count = 0
    
    #skip over date
    while True:
        if element[end] == ';':
            count += 1
        
        if count == 2:
            break

        end += 1

    start = end = end + 1

    while True:
        if element[end] == ';':
            break
        end += 1

    average.append(float(element[start:end]))

    end = end + 1

    day.append(int(element[end:len(element)]))



def solve():
    prob = LpProblem("min abs dev", LpMinimize)
    tvar = LpVariable("tvar")
    dvar = LpVariable("dvar")
    x0var = LpVariable("x0var")
    x1var = LpVariable("x1var")
    x2var = LpVariable("x2var")
    x3var = LpVariable("x3var")
    x4var = LpVariable("x4var")
    x5var = LpVariable("x5var")

    prob += tvar
    
    count = 0
    for d in day:
        prob += average[count] - x0var - x1var * d - x2var * math.cos((2 * pi * d) / 365.25) - x3var * math.sin((2 * pi * d) / 365.25) - x4var * math.cos((2 * pi * d) / (365.25 * 10.7)) - x5var * math.sin((2 * pi * d) / (365.25 * 10.7)) <= tvar

        prob += average[count] - x0var - x1var * d - x2var * math.cos((2 * pi * d) / 365.25) - x3var * math.sin((2 * pi * d) / 365.25) - x4var * math.cos((2 * pi * d) / (365.25 * 10.7)) - x5var * math.sin((2 * pi * d) / (365.25 * 10.7)) >= -tvar

        count += 1

    status = prob.solve()

    if prob.status == 1:
        print("Optimal solution found.")

        print("Objective: " + str(value(prob.objective)))
        print("x0: " + str(value(x0var)))
        print("x1: " + str(value(x1var)))
        print("x2: " + str(value(x2var)))
        print("x3: " + str(value(x3var)))
        print("x4: " + str(value(x4var)))
        print("x5: " + str(value(x5var)))

    elif prob.status == 0:
        print("Not solved.")

    elif prob.status == -1:
        print("Infeasible.")

    elif prob.status == -2:
        print("Unbounded.")

    elif prob.status == -3:
        print("Undefined.")
    
def main():
    if sys.argv[1] == "1":
        corvallis = csv.reader(open('Corvallis.csv'), delimiter=' ', quotechar='|')

        next(corvallis)

        for row in corvallis:
            parse(', '.join(row))


    elif sys.argv[1] == "2":
        ny = csv.reader(open('NewYork.csv'), delimiter=' ', quotechar='|')

        next(ny)

        for row in ny:
            parse2(', '.join(row))
            days_passed(', '.join(row))

        avgs()

    solve()

main()

