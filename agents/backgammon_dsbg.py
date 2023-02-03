'''
Name(s): yishu fang, tommy zhao
UW netid(s): yishuf,
'''

from game_engine import genmoves

class BackgammonPlayer:


    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxply = 2
        # feel free to create more instance variables as needed.

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "yishuf"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        self.prune = prune

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containing states and cutoff
        return (-1,-1)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxply = maxply


    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func != None:
            self.func = func


    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        if self.get_all_possible_moves(self) == []:
            # pass move
            pass
        if self.prune == False:
            # use minimax
            #if no move avaliable ( == 0)
                #pass, so return current state
            pass
        else:
            # use alphabeta pruning
            pass
        pass


    def minimax(self, state, maxply, maxPlayer):
        #how to use the number for dice
        if maxply == 0:
            return self.staticEval(self,state)
        if maxPlayer:
            maxEval = -1000000
            for x in self.get_all_possible_moves(self):
                eval = self.minimax(x, maxply - 1, False)
                maxEval = max(eval,maxEval)
            return maxEval
        else:
            minEval = 1000000
            for x in self.get_all_possible_moves(self):
                eval = self.minimax(x, maxply - 1, True)
                minEval = min(eval,minEval)
            return minEval




    def minimaxAB(self, state, maxply, maxPlayer):
        pass

    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        self.evalCount = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for i in range(4):
            for x in self.pointLists[i*6:(i+1)*6]:
                if x != None:
                    if x[0] == 0:
                        self.evalCount[0][i] += len(x)
                    elif x[0] == 1:
                        self.evalCount[1][i] += len(x)
        self.evalCount[0][5] = state.white_off
        self.evalCount[1][5] = state.red_off
        for x in state.bar:
            if x == 0:
                self.evalCount[0][6] += 1
            elif x == 1:
                self.evalCount[1][6] += 1

        return 100*(self.evalCount[0][6]-self.evalCount[1][6]) + 90*(self.evalCount[0][4]-self.evalCount[1][1]) + 50*(self.evalCount[0][3]-self.evalCount[1][2])- 50*(self.evalCount[0][2]-self.evalCount[1][3])-90*(self.evalCount[0][1]-self.evalCount[1][4])-100*(self.evalCount[0][5]-self.evalCount[1][5])
    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m[0])    # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list





