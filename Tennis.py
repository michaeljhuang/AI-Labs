import pandas as pd
import math
def main():
    data = pd.read_csv("play_tennis.csv")
    data = data.drop("Day",axis = 1)
    tree = decisionTree(data)
    for i in range(len(data)):
        row = data.iloc[i,:]
        print(classify(tree,row))
def entropy(data,var,value):
    series = data[data[var] == value]
    vals = ("Yes", "No")
    probabilities = {x: len(series[series["Play?"] == x]) / len(series) for x in vals}
    sum = 0
    for x in vals:
        if probabilities[x] != 0:
            sum -= math.log2(probabilities[x]) * probabilities[x]
    return sum
def info(data, var):
    types = {x for x in data[var]}
    probabilities = {x:len(data[data[var] == x])/len(data[var]) for x in types}
    return sum(probabilities[x] * entropy(data,var,x) for x in types)

def decisionTree(data):
    best = min([x for x in list(data) if x!= list(data)[-1]], key = lambda x: info(data,x))
    node = Node(best)
    for i in {x for x in data[best]}:
        new_data = data[data[best] == i]
        if(entropy(data,best,i))!= 0:
            node.children[i]  = decisionTree(new_data)
        else:
            node.children[i] = list({x for x in new_data[list(data)[-1]]})[0]
    return node

def classify(tree,row):
    while(type(tree) != str):
        tree = tree.children[row[tree.feature]]
    return tree

class Node:
    def __init__(self,feature):
        self.feature = feature
        self.children = {}



if __name__ == '__main__':
    main()
