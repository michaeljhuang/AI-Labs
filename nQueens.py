import math
import random
import collections
import heapq
import time
from matplotlib import pyplot
SIZE =15
NODE_COUNT = 0
RowL = []
ColL = []
Random = []

def inith(size):
    global NODE_COUNT
    global SIZE
    if(size%6 == 3):
        SIZE = size
        RowL.clear()
        ColL.clear()
        Random.clear()
        NODE_COUNT = 0
        for i in range(3, SIZE, 2):
            RowL.append(i)
        RowL.append(1)
        for i in range(4, SIZE, 2):
            RowL.append(i)
        RowL.append(0)
        RowL.append(2)
    elif(size%6 == 2):
        SIZE = size
        RowL.clear()
        ColL.clear()
        Random.clear()
        NODE_COUNT = 0
        for i in range(1,SIZE,2):
            RowL.append(i)
        RowL.append(2)
        RowL.append(0)
        for i in range(6,SIZE,2):
            RowL.append(i)
        RowL.append(4)
    else:
        SIZE = size
        RowL.clear()
        ColL.clear()
        Random.clear()
        NODE_COUNT = 0
        for i in range(1,SIZE,2):
            RowL.append(i)
        for i in range(0,SIZE,2):
            RowL.append(i)




class Node:
    def __init__(self,URDiag,Col,Row,ULDiag,Queens,mySize):
        global NODE_COUNT
        NODE_COUNT = NODE_COUNT+1
        self.ur = URDiag
        self.col = Col
        self.row = Row
        self.ul = ULDiag
        self.q = Queens
        self.size = mySize
        self.tup = tuple(self.q)
    def isGoal(self):
        global SIZE
        return (self.size == SIZE)
    def action(self):
        global SIZE
        global L
        global R
        children = []
        x = self.size
        #x= Random[self.size]
        for y in RowL:
            if(x not in self.col and y not in self.row and (x-y) not in self.ur and (x+y) not in self.ul):
                nextur = self.ur.copy()
                nextur.add((x-y))
                nextul= self.ul.copy()
                nextul.add((x+y))
                nextcol = self.col.copy()
                nextcol.add(x)
                nextrow = self.row.copy()
                nextrow.add(y)
                nextQueens = self.q.copy()
                nextQueens.append((x,y))
                list.sort(nextQueens)
                children.append(Node(nextur,nextcol,nextrow,nextul,nextQueens,self.size+1))

        return children


def main():
    global NODE_COUNT
    #print(RowL)
    #inith(120003)
    tic = time.time()
    #x = dfs()
    #print(x)
    #print(check(x))
    xlist = []
    nodelist = []
    timelist = []
    for i in range(4,200):
        start = time.time()
        inith(i)
        temp = set()
        l = []
        st = Node(temp, temp, temp, temp, l, 0)
        x = recurdfs(set(), st)
        #print(NODE_COUNT)
        xlist.append(i)
        nodelist.append(math.log(NODE_COUNT))
        stop = time.time()
        timelist.append(stop-start)
        #print(str(i) + " " + str(check(x)))
        #print(stop-start)
    """for i in range(6,105):
            start = time.time()
            inith(i)
            x = dfs()
            #print(x)
            xlist.append(i)
            ylist.append(math.log(NODE_COUNT))
            stop = time.time()
            print(str(i) + "  "  + str((stop-start)))
    """
    f, axarr = pyplot.subplots(2,sharex= True)
    axarr[0].plot(xlist,nodelist)
    axarr[1].plot(xlist,timelist)
    pyplot.show()

    toc = time.time()
    print((toc-tic))

    print(NODE_COUNT)


def dfs():#breadth first

    '''if(True):
        ret = []
        for i in range(SIZE):
            ret.append((i,RowL[i]))
        return ret'''
    visited = set()
    temp = set()
    l = []
    start = Node(temp,temp,temp,temp,l,0)
    fringe = collections.deque()
    fringe.append(start)

    while (len(fringe) > 0):
        st = fringe.pop()
        if (st.isGoal()):
            return st.q
        l = st.action()# Finds Children
        for state in l:
            if (not state.tup in visited):
                visited.add(state.tup)
                fringe.append(state)
        #visited.add(st.tup)
    return None
def recurdfs(visited, st):
    if (st.isGoal()):
        return st.q
    l = st.action()  # Finds Children
    for state in l:
        if (not state.tup in visited):
            visited.add(state.tup)
            x = recurdfs(visited, state)
            if(x is not None) :
                return x
            # visited.add(st.tup)

def check(l):
    row =set()
    col = set()
    ur = set()
    ul = set()
    for(x,y) in l:
        if (x not in col and y not in row and (x - y) not in ur and (x + y) not in ul):
            col.add(x)
            row.add(y)
            ur.add(x-y)
            ul.add(x+y)
        else:
            return False
    return True

def recur(size):
    if size<16:
        inith(size)
        return dfs().q
    if size%4 == 0:
        l = recur(size//4)
        sz = len(l)
        ret = []
        order = [1,3,0,2]
        for i in order:
            for (a, b) in l:
                ret.append((len(ret),b+i*sz))
        return ret
    elif size%4 == 1:
        l = recur(size-1)
        l.append((len(l),len(l)))
        return l
    elif size%4 == 2:
        l = recur(size//4)
        sz = len(l)
        ret = []
        order = [1,3,0,2]
        for i in order:
            for (a, b) in l:
                if(i>=2):
                    ret.append((len(ret),b+i*sz+1))
                else:
                    ret.append((len(ret), b + i * sz ))
        ret.append((len(ret),len(ret)+1))
        ret.append((len(ret),len(ret)//2))
        return ret
    elif size%4 == 3:
        l = recur(size-1)
        l.append((len(l), len(l)))
        return l






if __name__ == "__main__":
    main()