import pandas as pd
import math
def main():
    data = pd.read_csv("restaurant.csv")
    l = list(data)
    l.remove("WillWait")
    out =[(f, info(data,f)) for f in l]
    out.sort(key = lambda x:x[1])
    for(a,b) in out:
        print (str(a) + " " + str(b))
def entropy(data,var,value):
    series = data[data[var] == value]
    vals = ("Yes", "No")
    probabilities = {x: len(series[series["WillWait"] == x]) / len(series) for x in vals}
    sum = 0
    for x in vals:
        if probabilities[x] != 0:
            sum -= math.log2(probabilities[x]) * probabilities[x]
    return sum
def info(data, var):
    types = {x for x in data[var]}
    probabilities = {x:len(data[data[var] == x])/len(data[var]) for x in types}
    return sum(probabilities[x] * entropy(data,var,x) for x in types)


if __name__ == '__main__':
    main()
