import pandas as pd
import math
from matplotlib import pyplot as plt
import random
COUNT = 0
LEAVES = 0
TOTALDEPTH = 0
def main():
    global E0
    data = pd.read_csv("house-votes-84.csv")
    data = data.drop("Label",axis = 1)
    old_data = data.copy()
    for column in list(data):
        data = data[data[column] != '?']
    rest = old_data.drop(data.index)
    tree = decisionTree(data,True)
    print(printTree(tree))
    print("Nodes: " + str(COUNT))
    print("Average Path Length:" + str(TOTALDEPTH/LEAVES))
    for i in range(len(data)):
        row = data.iloc[i,:]
        result = classify(tree, row)
        assert result == row[list(data)[-1]]
    x_series = []
    y_series = []
    '''for i in range(5, 183,10):
        print(i)
        samples = []
        for j in range(10):
            test = old_data.sample(n=50)
            #new_data = data.drop(test.index)
            training = data.sample(n=i)
            t = decisionTree(training)
            samples.append(accuracy(t, test))
        x_series.append(i)
        y_series.append(sum(samples) / 10)
        '''
    for i in range(2,11):
        x_series.append(i)
        y_series.append(math.pow(2,i)-1)
    plt.plot(x_series, y_series)
    plt.show()




def entropy(data,var,value):
    series = data[data[var] == value]
    vals = {x for x in series[list(data)[-1]]}
    probabilities = {x: len(series[series[list(data)[-1]] == x]) / len(series) for x in vals}
    sum = 0
    for x in vals:
        if probabilities[x] != 0:
            sum -= math.log2(probabilities[x]) * probabilities[x]
    return sum
def info(data, var):
    types = {x for x in data[var]}
    probabilities = {x:len(data[data[var] == x])/len(data[var]) for x in types}
    return sum(probabilities[x] * entropy(data,var,x) for x in types)


def decisionTree(data,depth = 1,ig = False):
    E0 = 0
    types = {x for x in data[list(data)[-1]]}
    probabilities = {x: len(data[data[list(data)[-1]] == x]) / len(data[list(data)[-1]]) for x in types}
    if(ig):
        for x in ("democrat", "republican"):
            if probabilities[x] != 0:
                E0 -= math.log2(probabilities[x]) * probabilities[x]
    global COUNT,TOTALDEPTH,LEAVES
    best = min([x for x in list(data) if x!= list(data)[-1]], key = lambda x: info(data,x))
    node = Node(best)
    node.entropy = info(data,best)
    node.infogain = E0- node.entropy
    if(len(list(data)) == 1):
        return
    for i in {x for x in data[best]}:
        new_data = data[data[best] == i]
        new_data=new_data.drop(best, axis=1)
        if(entropy(data,best,i))!= 0:
            node.children[i] = decisionTree(new_data, depth+1,ig)
        else:
            COUNT+=1
            LEAVES+=1
            TOTALDEPTH+=depth+1
            node.children[i] = list({x for x in new_data[list(data)[-1]]})[0]
    return node

def classify(tree,row):
    if(type(tree) != str):
        if(row[tree.feature] == '?'):
            a = classify(tree.children['n'],row)
            b = classify(tree.children['y'],row)
            if(a==b):
                return a
            else:
                if(random.random()<0.5):
                    return a
                return b
        return classify(tree.children[row[tree.feature]],row)
    return tree
def printTree(tree,depth = 1):

    if(type(tree) == str):
        return tree
    ret = ""
    ret += tree.feature + ' (' + str(tree.infogain) + ")"
    for child in tree.children:
        ret +="\n" + "\t" * (depth)
        ret += child + ":" + printTree(tree.children[child],depth+1)
    return ret
def accuracy(tree, data):
    output = [classify(tree, data.iloc[row, :]) for row in range(len(data))]
    correct = sum(1 for i in range(len(data)) if data.iloc[i, -1] == output[i])
    return correct / len(output)


class Node:
    def __init__(self,feature):
        self.feature = feature
        self.children = {}
        global COUNT
        COUNT +=1
        self.infogain = 0
        self.entropy = 0



if __name__ == '__main__':
    main()
