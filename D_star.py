#!/usr/bin/env python
import math , time
from sys import maxsize

def sgn(x):
    if x>0:
        return 1
    elif x==0:
        return 0
    else:
        return -1

class State(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.state = "."
        self.t = "new"
        self.h = 0
        self.k = 0


    def cost(self, state):
        if self.state in ["#","v"] or state.state in ["#","v"]:
            return maxsize
        # determin the num of obstacle
        return math.sqrt(math.pow((self.x - state.x), 2) +
                         math.pow((self.y - state.y), 2))
    # use the Eular distance in the cost
    def set_state(self, state):
        if state not in ["s", ".", "#", "e", "*", "v"]:
            return
        self.state = state


class Map(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.map = self.init_map()

    def init_map(self):
        map_list = []
        for i in range(self.row):
            tmp = []
            for j in range(self.col):
                tmp.append(State(i, j))
            map_list.append(tmp)
        return map_list
# adding the map using list (state)
    def print_map(self):
        for i in range(self.row):
            tmp = ""
            for j in range(self.col):
                tmp += self.map[i][j].state + " "
            print(tmp)
# remrnber the way to print a matrix #
    def get_neighbers(self, state):
        state_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if state.x + i < 0 or state.x + i >= self.row:
                    continue
                if state.y + j < 0 or state.y + j >= self.col:
                    continue
                state_list.append(self.map[state.x + i][state.y + j])
        return state_list
# good way to get neighbors

    def set_obstacle(self, point_list):
        for x, y in point_list:
            if x < 0 or x >= self.row or y < 0 or y >= self.col:
                continue
            self.map[x][y].set_state("#")


    def set_Virtual_obstacle(self, point_list):
        for x, y in point_list:
            if x < 0 or x >= self.row or y < 0 or y >= self.col:
                continue
            self.map[x][y].set_state("v")


class Dstar(object):

    def __init__(self, maps):
        self.map = maps
        self.open_list = set()


    def detect_sign(self,sign):
        for i in range(self.map.col):
            for j in range(self.map.row):
                if self.map.map[i][j].state == sign:
                    place= [i, j]
        return place

    def detect_Obs(self,state):
        obs = []
        for y in self.map.get_neighbers(state):
            if y.state in ['#', 'v']:
                obs.append((y.x, y.y))
        if len(obs) >= 3: # obtain the trap style and the vertical style
            sumx = sum([i[0] - state.x for i in obs])
            sumy = sum([i[1] - state.y for i in obs])
            if [sgn(end.x - state.x), sgn(end.y - state.y)] == [sumx/3, sumy]:
                print('Type Obstacle')
                self.map.set_Virtual_obstacle([(state.x, state.y)])
                return 1
            else:
                return 0
    # think : break the loop and add a obstacle
    # calculate the Type mode  and fix the Obs problem 2018/10/15

    def process_state(self):
        x = self.min_state()
    ## back to the early tmp point
        if x is None:
            return -1
        k_old = self.get_kmin()
        self.remove(x)
        # dealing with the trap obstacle;
        #if x.state =='*' and  self.detect_Obs(x):
        if x.t =='close' and  self.detect_Obs(x):
            for y in self.map.get_neighbers(x):
                if y.t == 'close' and y.h > k_old and y.state == '*':
                    x.parent = y
                    self.insert(y, y.h)
        # How to search back the early point and start the main loop?

        elif k_old < x.h:
            for y in self.map.get_neighbers(x):
                if y.h <= k_old and x.h > y.h + x.cost(y):
                    x.parent = y
                    x.h = y.h + x.cost(y)
        elif k_old == x.h:
            for y in self.map.get_neighbers(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y) \
                        or y.parent != x and y.h > x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
        else:
            for y in self.map.get_neighbers(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
                else:
                    if y.parent != x and y.h > x.h + x.cost(y):
                        self.insert(y, x.h)
                    else:
                        if y.parent != x and x.h > y.h + x.cost(y) \
                                and y.t == "close" and y.h > k_old:
                            self.insert(y, y.h)
        return self.get_kmin()

    def min_state(self):
        if not self.open_list:
            return None
        min_state = min(self.open_list, key=lambda x: x.k)
        return min_state

    def get_kmin(self):
        if not self.open_list:
            return -1
        k_min = min([x.k for x in self.open_list])
        return k_min

    def insert(self, state, h_new):
        if state.t == "new":
            state.k = h_new
        elif state.t == "open":
            state.k = min(state.k, h_new)
        elif state.t == "close":
            state.k = min(state.h, h_new)
        state.h = h_new
        state.t = "open"
        self.open_list.add(state)

    def remove(self, state):
        if state.t == "open":
            state.t = "close"
        self.open_list.remove(state)

    def modify_cost(self, x):
        if x.t == "close":
            self.insert(x, x.parent.h + x.cost(x.parent))

    def run(self, start, end):
        self.open_list.add(end)
        while True:
            self.process_state()
            if start.t == "close":
                break
        start.set_state("s")
        s = start
        while s != end:
            s.set_state("s")
            s = s.parent
        s.set_state("e")
        self.map.print_map()
        tmp = start
        #self.map.set_obstacle([(11,5),(10,5),(10,6),(9,6),(9,7),(9,8),(9,9),(9,10)])
        #self.map.set_obstacle([(11,5),(10,5),(10,6),(10,7),(10,8),(9,8),(9,9),(9,10)])
        self.map.set_obstacle([(10,2),(10,3), (10, 4),(10,5),(10,6),(15,10),(15,11),(15, 12),(15,13)]) # type C Obstact
        #self.map.set_obstacle([(13,10),(14,9),(14,10),(14,8)]) #Type B Obstact
        #self.map.set_obstacle([(14,7),(14,8),(14,9),(13,9)]) # type A Obstact
        while tmp != end:
            if tmp.state == 'v':
                tmp.set_state('v')
            else:
                tmp.set_state("*")
            self.map.print_map()
            print("")
            # print every step of the tmp_map
            #time.sleep(2.0)
            if tmp.parent.state in ["#","v"]:
                self.modify(tmp)
                continue
            tmp = tmp.parent
        tmp.set_state("e")

    def modify(self, state):
        self.modify_cost(state)
        while True:
            k_min = self.process_state()
            if state.state == 'v' :
                break
            elif k_min >= state.h: # the v.h is of maxsize ....
                break


if __name__ == '__main__':
    m = Map(20, 20)
    m.set_obstacle([(4, 3), (4, 4), (4, 5), (4, 6), (5, 3), (6, 3), (7, 3)])
    start = m.map[1][1]
    end = m.map[17][12]
    #start = m.map[1][2]
    #end = m.map[17][11]
    dstar = Dstar(m)
    dstar.run(start, end)

m.print_map()