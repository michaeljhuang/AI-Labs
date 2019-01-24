import pickle
import time
from math import pi , acos , sin , cos
import heapq
import collections
import random
from tkinter import *
#
def calcd(point1,point2):
   #
   (y1,x1) = point1
   (y2,x2) = point2
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   #
   R   = 3958.76 # miles
   #
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #
   # approximate great circle distance with law of cosines
   #
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R



class Graph():
    def __init__(self, graph, name_to_coords, code_to_city):
        self.data = graph
        self.coords = name_to_coords
        self.names = code_to_city

    def get_neighbors(self,v):
        return self.data[v].keys()

    def get_edge_length(self, v1, v2):
        return (self.data[v1][v2])

def initdict():
    graph = {}
    coords = {}
    names = {}
    fEdges = open("rrEdges.txt", "r")
    fNodes = open("rrNodes.txt", "r")
    fNames = open("rrNodeCity.txt","r")
    for line in fNodes:
        temp = line.split()
        coords[temp[0]] = (temp[1],temp[2])
    for line in fNames:
        temp = []
        temp.append(line[:7])
        temp.append(line[8:-1])
        names[temp[0]] = (temp[1])
        names[temp[1]] = temp[0]

    for edge in fEdges:
        (a,b) = (edge.split()[0],edge.split()[1])
        temp = graph.get(a)
        dist = calcd(coords[a],coords[b])
        if(temp is None):
            d = {b:(dist,0)}
            graph[a] = d
        if(temp is not None):
            temp[b] = (dist,0)
            graph[a] = temp
        temp = graph.get(b)
        if (temp is None):
            d = {a: (dist,0)}
            graph[b] = d
        if (temp is not None):
            temp[a] = (dist,0)
            graph[b] = temp
    f = open('picklegraph.pickle', 'wb')
    g = Graph(graph,coords,names)
    pickle.dump(g, f)
    return g


def main():
    #initdict()
    graph = pickle.load(open("picklegraph.pickle","rb"))
    #print(graph.data)
    start = input("Input Starting Point: ").strip()
    dest = input("Input Destination: ").strip()

    (d,c) = image(graph)
    tic = time.time()
    print(AStar(start,dest,graph,d,c))
    #print(AStarNoMap(start,dest,graph))
    toc = time.time()
    #print(graph.data)
    print(toc-tic)

def image(graph):
    lat_min = 14.686730
    lon_min = -100.000
    scale = 13
    h_buffer = 550
    v_buffer = -450
    master = Tk()
    canvas = Canvas(master,width = 1920, height = 1080)
    canvas.pack()
    dict = {}
    for i in graph.coords.keys():
        for z in graph.get_neighbors(i):
            (i_lat,i_lon) = graph.coords[i]
            (z_lat,z_lon) = graph.coords[z]
            i_lat = float(i_lat)
            i_lon = float(i_lon)
            z_lat = float(z_lat)
            z_lon = float(z_lon)
            #a = (i_lon-lon_min)
            #b = 1080-(i_lat-lat_min)
            #c = (z_lon-lon_min)
            #d = 1080-(z_lat-lat_min)
            line = canvas.create_line((i_lon-lon_min)*scale+h_buffer,1080-(i_lat-lat_min)*scale+v_buffer,(z_lon-lon_min)*scale+h_buffer, 1080-(z_lat-lat_min)*scale+v_buffer, fill = "cyan")
            #line = canvas.create_line(a,b,c,d)
            dict[(i,z)] = line
    return dict,canvas
def AStar(start, dest, graph,lines,c):
    names = graph.names
    data = graph.data
    startID = names[start]
    endID = names[dest]
    prevs = {}
    fringe = []
    fringe.append((calcd(graph.coords[startID], graph.coords[endID]),0,startID,None))
    master = Tk()
    canvas = c
    canvas.pack()

    #because im bad
    heapq.heapify(fringe)

    visited= set()
    while (len(fringe) > 0):
        (oldf,oldg,curr,parent) = heapq.heappop(fringe)
        if(parent is not None):
            canvas.itemconfig(lines[(curr,parent)], fill = "deep pink")
            canvas.itemconfig(lines[(parent,curr)], fill= "deep pink")
        if (curr == endID):
            # testing purposes
            path = []
            path.append(curr)
            while(parent is not None):
                path.append(parent)
                curr = parent
                parent = prevs[curr]
                if(parent is not None):
                    canvas.itemconfig(lines[curr, parent], fill= "spring green", width = 3)
                    canvas.itemconfig(lines[parent, curr], fill= "spring green", width = 3)
            print(path[::-1])
            master.mainloop()
            return oldf
        if(curr not in visited):
            prevs[curr] = parent
            for (child,dist) in data[curr].items():
                if(child not in visited):
                    h = calcd(graph.coords[child], graph.coords[endID])
                    g = oldg + dist
                    f = h + g
                    heapq.heappush(fringe, (f, g,child,curr))
        visited.add(curr)

    return None

def AStarNoMap(start, dest, graph):
    names = graph.names
    data = graph.data
    startID = names[start]
    endID = names[dest]
    prevs = {}
    fringe = []
    fringe.append((calcd(graph.coords[startID], graph.coords[endID]),0,startID,None))

    #because im bad
    heapq.heapify(fringe)

    visited= set()
    while (len(fringe) > 0):
        (oldf,oldg,curr,parent) = heapq.heappop(fringe)
        if (curr == endID):
            # testing purposes

            path = []
            path.append(curr)
            while(parent is not None):
                path.append(parent)
                curr = parent
                parent = prevs[curr]
            print(path[::-1])

            return oldf
        if(curr not in visited):
            prevs[curr] = parent
            for (child,dist) in data[curr].items():
                if(child not in visited):
                    h = calcd(graph.coords[child], graph.coords[endID])
                    g = oldg + dist
                    f = h + g
                    heapq.heappush(fringe, (f, g,child,curr))
        visited.add(curr)

    return None



if __name__ == "__main__":
    main()

