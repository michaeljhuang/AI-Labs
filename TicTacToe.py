user = "X"
cpu = "O"
wins = {(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)}
def main():
    print("Input 1 to start, input 2 to allow CPU to start")
    s = input()
    if(s == "2"):
        cpu = "X"
        user = "O"
        play(False,".........",0)
    else:
        play(True, ".........",0)

def play(turn, state,count):
    pboard(state)
    if(score(state) ==1):
        print("CPU Wins")
        return True
    if (score(state) == -1):
        print("USER Wins")
        return True
    if(count == 9):
        print("Tie")
        return True
    if(turn):
        works = False
        while(not works):
            print("Please Insert Square (0 is top left, 8 is bottom right)")
            val = int(input())
            if(state[val] == "."):
                state = state[:val] +  user + state[val+1:]
                works = True
                play(False,state,count+1)
    if(not turn):
        minval = -1
        minloc = 0
        for i in range(9):
            val = -1
            if(state[i] =="."):
                val = minmax(False, state[:i] +  cpu + state[i+1:],count+1)
            if(val>minval):
                minloc = i
                minval = 1
        state = state[:minloc] + cpu + state[minloc + 1:]
        play(True, state, count + 1)
def minmax(isCPU, state,count):
    if (count == 9):
        return score(state)
    else:
        if(score(state) != 0):
            return score(state)
    if(isCPU):
        max = -1
        for i in range(9):
            if(max == 1):
                return 1
            if(state[i] == "."):
                if(minmax(False,state[:i] +  cpu + state[i+1:],count+1) > max):
                    max = minmax(False,state[:i] +  cpu + state[i+1:],count+1)
        return max
    else:
        min = 1
        for i in range(9):
            if (min == -1):
                return -1
            if (state[i] == "."):
                if (minmax(True, state[:i] + user + state[i + 1:], count + 1) < min):
                    min = minmax(True,  state[:i] + user + state[i + 1:], count + 1)
        return min
def pboard(state):
    print("_______")
    line = "|"
    for i in range(3):
        line = line + state[i] + "|"
    print(line)
    line = "|"
    for i in range(3):
        line = line + state[i+3] + "|"
    print(line)
    line = "|"
    for i in range(3):
        line = line + state[i+6] + "|"
    print(line)
    print("_______")
    print()
def score(state):
    for w in wins:
        (a,b,c) = w
    #    print((a,b,c))
        if(state[a] == state[b] == state[c] == "O"):
            return 1
        if (state[a] == state[b] == state[c] == "X"):
            return -1
    return 0
if __name__ == '__main__':
    main()