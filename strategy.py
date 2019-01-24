import random
import math
import collections
#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N + E, S + E, N + W, S + W
DIRECTIONS = (N, NE, S, SE, E, SW, W, NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}
MATRIX = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,  20,  -3,  11,   8,   8,   11, -3,  20,   0,
    0,  -3,  -7,  -4,   1,   1,  -4,  -7,  -3,   0,
    0,  11,  -4,   2,   2,   2,   2,  -4,  11,   0,
    0,   8,  -5,   2,  -3,  -3,   2,  -1,   8,   0,
    0,   8,  -5,   2,  -3,  -3,   2,  -1,   8,   0,
    0,  11,  -4,   2,   2,   2,   2,  -4,  11,   0,
    0,  -3,  -7,  -4,  -1,  -1,  -4,  -7,  -3,   0,
    0,  20,  -3,  11,   8,   8,  11,  -3,  20,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################

class Strategy():
    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        start = ""
        border = OUTER * 10
        line = OUTER + EMPTY * 8 + OUTER
        r4 = OUTER + EMPTY * 3 + WHITE + BLACK + EMPTY * 3 + OUTER
        r5 = r4[::-1]
        start = border + 3 * line + r4 + r5 + 3 * line + border
        #print(self.get_pretty_board(start))
        return (start)

    def get_pretty_board(self, board):
        """Get a string representation of the board."""
        pretty_board = ""
        for i in range(1,9):
            pretty_board+= board[10 * i+1:10 * i + 9] + '\n'
        return pretty_board

    def opponent(self, player):
        """Get player's opponent."""
        if (player == BLACK):
            return WHITE
        if (player == WHITE):
            return BLACK
        return None


    def find_match(self, board, player, square, direction):
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        if (board[square + direction] == self.opponent(player)):
            current = square + 2 * direction
            while (board[current] == self.opponent(player)):
                current += direction
            if (board[current] == player):
                return current
        return None

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        if (board[move] != EMPTY):
            return False
        for d in DIRECTIONS:
            if (self.find_match(board, player, move, d) is not None):
                return True
        return False

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        board = list(board)
        board[move] = player
        for d in DIRECTIONS:
            loc = self.find_match(board,player,move,d)
            if(loc is not None):
                for i in range(move,loc,d):
                    board[i] = player
        return "".join(board)
    def get_valid_moves(self, board, player):
        """Get a list of all legal moves for player."""
        ret = []
        for i in range(1,9):
            for j in range(1,9):
                if (self.is_move_valid(board, player, 10 * i + j)):
                    ret.append(10 * i + j)
        return ret

    def has_any_valid_moves(self, board, player):
        """Can player make any moves?"""
        return (len(self.get_valid_moves(board, player)) != 0)

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if (self.has_any_valid_moves(board, self.opponent(prev_player))):
            return self.opponent(prev_player)
        if (self.has_any_valid_moves(board, prev_player)):
            return prev_player
        return None

    def score(self, board, player=BLACK, over = False):
        """Compute player's score (number of player's pieces minus opponent's)."""
        #
        BScore = 0
        WScore = 0
        BCount = 0
        WCount = 0
        WS = set()
        BS = set()
        for i in range(10):
            BS.add(i)
            WS.add(i)
            BS.add(90+i)
            WS.add(90+i)
            BS.add(i*10)
            WS.add(i*10)
            BS.add(i*10+9)
            WS.add(i*10+9)
        fringe = collections.deque()
        corners = {11,18,81,88}
        for corner in corners:
            if(board[corner] == BLACK):
                fringe.append(corner)
        while(len(fringe)>0):
            st = fringe.popleft()
            if(st not in BS and board[st] == BLACK):
                if(st+N in BS and st+E in BS):
                    BS.add(st)
                    for d in DIRECTIONS:
                        if(st+d) not in BS:
                            fringe.append(st+d)
                elif (st+S in BS and st+E in BS ):
                    BS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in BS:
                            fringe.append(st + d)
                elif (st+N in BS and st+W in BS ):
                    BS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in BS:
                            fringe.append(st + d)
                elif (st+ S in BS  and st+W in BS ):
                    BS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in BS:
                            fringe.append(st + d)
        for corner in corners:
            if(board[corner] == WHITE):
                fringe.append(corner)
        while(len(fringe)>0):
            st = fringe.popleft()
            if(st not in WS and board[st] == WHITE):
                if(st+N in WS and st+E in WS):
                    WS.add(st)
                    for d in DIRECTIONS:
                        if(st+d) not in WS:
                            fringe.append(st+d)
                elif (st+S in WS and st+E in WS ):
                    WS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in WS:
                            fringe.append(st + d)
                elif (st+N in WS and st+W in WS ):
                    WS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in WS:
                            fringe.append(st + d)
                elif (st + S in WS  and st+ W in WS ):
                    WS.add(st)
                    for d in DIRECTIONS:
                        if (st + d) not in WS:
                            fringe.append(st + d)


        for i in range(100):
            if(board[i] == BLACK):
                BScore += MATRIX[i]
                BCount+=1
            if(board[i] == WHITE):
                WScore += MATRIX[i]
                WCount+=1

        if(BCount+WCount==64 or over):
            return 10000*(BCount-WCount)
        if(BCount+WCount>40):
            for i in range(100):
                if(i not in BS and i not in WS):
                    stable = True
                    for d in DIRECTIONS:
                        curr = i
                        while(board[curr]!= OUTER and stable):
                            if(board[curr] != EMPTY):
                                curr+=d
                            else:
                                stable = False
                    if(stable and board[i] == BLACK):
                        BS.add(i)
                    if(stable and board[i] == WHITE):
                        WS.add(i)
        BFCount = 0
        WFCount = 0
        for i in range(100):
            if(board[i] == EMPTY):
                white = False
                black = False
                for d in DIRECTIONS:
                    if(board[i+d] == WHITE and board[i+d] not in WS):
                        white = True
                    if(board[i+d] == BLACK and board[i+d] not in BS):
                        black = True
                if(white):WFCount+=1
                if(black):BFCount+=1
        moves = len(self.get_valid_moves(board,BLACK)) - len(self.get_valid_moves(board,WHITE))
        return (BScore - WScore + 4*len(BS) - 4*len(WS)+((80-BCount-WCount)*(WFCount-BFCount)/80)+ moves)
        #return (BScore - WScore + 50 * len(BS) - 50 * len(WS))
    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        return (self.has_any_valid_moves(board, WHITE) == False and self.has_any_valid_moves(board, BLACK) == False)

    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################
    def get_children(self,board,player):
         ret = []
         for move in self.get_valid_moves(board,player):
             ret.append((move,self.make_move(board,player,move)))
         return ret
    def minmax_search(self, board, player, depth,alpha, beta):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters

        if(self.game_over(board,player)):
            return self.score(board,player,True)*10000,None
        if(depth == 0):

            return self.score(board,player),None
        if(player  == BLACK):
            v = -1000000000
            best_move = None
            for move in self.get_valid_moves(board,player):
                child = self.make_move(board,player,move)
                min_max = self.minmax_search(child,self.next_player(child,player),depth-1,alpha,beta)
                if(min_max[0] > v):
                    v,best_move = min_max[0], move
                if(v>alpha):
                    alpha = v
                if beta<= alpha:
                    break
            return(v,best_move)
        elif (player == WHITE):
            v = 1000000000
            best_move = None
            for move in self.get_valid_moves(board, player):
                child = self.make_move(board, player, move)
                min_max = self.minmax_search(child, self.next_player(child,player), depth - 1, alpha, beta)
                if (min_max[0] < v):
                    v, best_move = min_max[0], move
                if (v < beta):
                    beta = v
                if beta <= alpha:
                    break
            return (v, best_move)

    def minmax_strategy(self, board, player, depth = 7):
        if(depth<60):
            print(depth)
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        h, best_move = self.minmax_search(board,player,depth,-10000000000,10000000000)
        if(best_move is not None):
            return best_move
        else:
            return random.choice(self.get_valid_moves(board,player))
    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while (True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.minmax_strategy(board, player,depth)
            depth += 1
    standard_strategy = minmax_strategy


###############################################
# The main game-playing code
# You can probably run this without modification
################################################
import time
from multiprocessing import Value, Process
import os, signal

silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.standard_strategy, WHITE: white.standard_strategy}
        print(ref.get_pretty_board(board))
        while player is not None:

            valid_moves = ref.get_valid_moves(board,player)
            if player == WHITE:
                print(valid_moves)
                move = int(input("MOVE:"))
                while(move not in valid_moves):
                    move = int(input("MOVE:"))
            else:
                move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))
        return ref.score(board)


#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():
    def __init__(self, time_limit=2):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.best_strategy
        while player is not None:
            best_shared = Value("i", -1)
            best_shared.value = 11
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent: print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        black_score = ref.score(board, BLACK)
        if black_score > 0:
            winner = BLACK
        elif black_score < 0:
            winner = WHITE
        else:
            winner = "TIE"

        return board, ref.score(board, BLACK)


#################################################
# The main routine
################################################

if __name__ == "__main__":
    #game = StandardPlayer()
    game = ParallelPlayer()
    game.play()
