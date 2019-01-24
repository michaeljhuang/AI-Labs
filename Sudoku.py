import random
import collections
import time
import math

Squares = set()
Peers = dict()
Units = []
r = "ABCDEFGHI"
c = "123456789"
NODE_COUNTER  = 0

def init():
    for a in r:
        for b in c:
            Squares.add(a+b)
    for a in r:
        temp = set()
        for b in c:
            temp.add(a+b)
        Units.append(temp)
    for a in c:
        temp = set()
        for b in r:
            temp.add(b + a)
        Units.append(temp)

    for i in range(3):
        for j in range(3):
            temp = set()
            for a in c[3*i:3*i+3]:
                for b in r[3*j:3*j+3]:
                    temp.add(b + a)
            Units.append(temp)
    for square in Squares:
        temp = set()
        for unit in Units:
            if(square in unit):
                temp  = temp|unit
        temp.remove(square)
        Peers[square] = temp
class SudokuMRV:
    def __init__(self,state,count, fin):
        global NODE_COUNTER
        NODE_COUNTER +=1
        self.state = state
        self.count = count
        self.fin = fin
        self.s = ""
        for a in r:
            for b in c:
                if((a+b) in fin):
                    self.s = self.s + state.get((a+b))
                else:
                    self.s += "."
    def isGoal(self):
        return self.count == 81
    def assign(self):
        minval = 10
        minlocs = []
        for (a,b) in self.state.items():
            if(a not in self.fin):
                if(len(b) == minval):
                    minlocs.append(a)
                if(len(b)<minval):
                    minval = len(b)
                    minlocs.clear()
                    minlocs.append(a)
        random.shuffle(minlocs)
        if(minval!= 0):
            #print(minval)
            return minlocs

    def generateChild(self,loc,val):
        temp = self.state.copy()
        f = self.fin.copy()
        f.add(loc)
        for square in Peers[loc]:
            temp[square] = temp[square].replace(val,"")
            if(len(temp[square]) == 0):
                return None
        temp[loc] = val
        return(SudokuMRV(temp,self.count+1,f))
def main():
    init()
    #print(Squares)
    #print(Units)
    #print(Peers)
    print("Please input starting position:")
    #start = input()
    start = "......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3."
    #print(len(start))
    print(Peers["A1"])
    count = 0
    temp = {}
    fin  = set()
    for i in Squares:
        temp[i] = c
    for i in range(len(start)):
        if (start[i] != '.'):
            loc = r[i//9] + c[i%9]
            fin.add(loc)
            count+=1
            for square in Peers[loc]:
                temp[square] = temp[square].replace(start[i], "")
            temp[loc] = start[i]
    #print(count)
    ##print(temp)
    #print(fin)
    board = None
    global  NODE_COUNTER
    while(board is None):
        NODE_COUNTER = 0
        board = csp(SudokuMRV(temp,count,fin))
    #    print("ye")
    print(board.state)
    print(board.fin)
    #print(NODE_COUNTER)
def csp(root):
    global NODE_COUNTER
    if(root is None):
        return None
    if(NODE_COUNTER>120):
        return None
    if(root.isGoal()):
        return root
    l = root.assign()
    #print(root.state)
    #input()
    if(l is not None ):
        for loc in l:
            for num in root.state[loc]:
                #print(loc + " " + num + " " + str(root.count) + " " + str(len(root.state[loc])))
                newNode = root.generateChild(loc,num)
                result = csp(newNode)
                if(result is not None):
                    return result
    return None

if __name__ == '__main__':
    main()