'''
Name(s): yishu fang, tommy zhao
UW netid(s): yishuf, tommzh
'''

from game_engine import genmoves
#from game_engine import boardState
NUM = 5

class BackgammonPlayer:


    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxply = 2
        self.special = None
        self.evalCount = None
        self.prune = None

        # counters
        self.states_created = 0
        self.ab_cutoffs = 0

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "yishuf" + " " + "tommzh"
    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        if prune != None:
            self.prune = prune

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containing states and cutoff
        return (self.states_created, self.ab_cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxply = maxply


    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func is not None:
            self.special = func


    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        maxPlayer = state.whose_move
        self.initialize_move_gen_for_state(state, state.whose_move, 1, 6)
        moves = self.get_all_possible_moves()
        if moves == 'p':
            return 'no moves, pass'
        best_move = None
        best_score = -1e20
        if self.prune == False:
            for x in moves:
                self.states_created += 1
                s = getSourceAndTargetFromMove(state,x,[die1,die2])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[0]) > 23 or sum(s[0]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0:
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                        1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                score = self.minimax(temp_state, self.maxply, maxPlayer)
                if score > best_score:
                    best_move = x
                    best_score = score
            return best_move

        else:
            for x in moves:
                self.states_created += 1
                s = getSourceAndTargetFromMove(state,x, [die1,die2])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[0]) > 23 or sum(s[0]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                        1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                score = self.minimaxAB(temp_state, self.maxply, -1000000, 1000000, maxPlayer)
                if score > best_score:
                    best_move = x
                    best_score = score
            return best_move



    def minimax(self, state, maxply, maxPlayer):
        #how to use the number for dice

        if maxply == 0:
            return self.staticEval(state)

        self.initialize_move_gen_for_state(state, maxPlayer, 1, 6)
        if maxPlayer == state.whose_move:
            maxEval = -1e20
            for x in self.get_all_possible_moves():
                self.states_created += 1
                s = getSourceAndTargetFromMove(state,x, [1, 6])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state,temp_state.whose_move,sum(s[0]), 1- temp_state.whose_move)
                    elif sum(s[0]) > 23 or sum(s[0]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state,temp_state.whose_move,s[0][0], 1-temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]), 1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state,temp_state.whose_move,sum(s[1]), 1- temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0:
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state,temp_state.whose_move,s[1][0], 1-temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]), 1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                eval = self.minimax(temp_state, maxply - 1, maxPlayer)
                maxEval = max(eval,maxEval)
            return maxEval
        else:
            minEval = 1e20
            for x in self.get_all_possible_moves():
                self.states_created += 1
                s = getSourceAndTargetFromMove(state,x, [1, 6])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[0]) > 23 or sum(s[0]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                           1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                        1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                eval = self.minimax(temp_state, maxply - 1, maxPlayer)
                minEval = min(eval,minEval)
            return minEval




    def minimaxAB(self, state, maxply, alpha,beta, maxPlayer):
        self.initialize_move_gen_for_state(state,maxPlayer,1,6)
        if maxply == 0:
            return self.staticEval(state)
        if maxPlayer == state.whose_move:
            maxEval = -1000000
            for x in self.get_all_possible_moves():
                self.states_created += 1
                s = getSourceAndTargetFromMove(state,x,[1,6])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[0]) > 23 or sum(s[0]) < 0:
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0 :
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]), 1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                eval = self.minimaxAB(temp_state, maxply - 1, alpha,beta, maxPlayer)
                maxEval = max(eval,maxEval)
                alpha = max(alpha,eval)
                if eval <= alpha:
                    self.ab_cutoffs += NUM
                    alpha = -1000000
                    break
            return maxEval
        else:
            minEval = 1000000
            for x in self.get_all_possible_moves():
                s = getSourceAndTargetFromMove(state,x, [1, 6])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif (sum(s[0]) > 23 or sum(s[0]) < 0):
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[0][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[0][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        if temp_state.bar != []:
                            genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23 or sum(s[1]) < 0:
                        if genmoves.bearing_off_allowed(temp_state, temp_state.whose_move):
                            if temp_state.pointLists[s[1][0]] != []:
                                temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        if temp_state.pointLists[s[1][0]] != []:
                            temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                        1 - temp_state.whose_move)
                s = temp_state.whose_move

                temp_state.whose_move = 1 - temp_state.whose_move
                eval = self.minimaxAB(temp_state, maxply - 1, alpha,beta,maxPlayer)
                minEval = min(eval,minEval)
                beta = min(beta,eval)
                if eval >= beta:
                    self.ab_cutoffs += NUM
                    beta = 100000
                    break
            return minEval


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        if self.special != None:
            return self.special(state)

        evalCount = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        for i in range(4):
            for x in state.pointLists[i * 6 : (i + 1) * 6]:
                if x != []:
                    if x[0] == 0:
                        evalCount[0][i] += len(x)
                    else: #if x[0] == 1:
                        evalCount[1][i] += len(x)
        evalCount[0][4] = 0 if state.white_off == [] else len(state.white_off)
        evalCount[1][4] = 0 if state.red_off == [] else len(state.red_off)
        for x in state.bar:
            if x != []:
                if x == 0:
                    evalCount[0][5] += 1
                else: #x == 1
                    evalCount[1][5] += 1

        #print(evalCount)
        return 2000 * (evalCount[0][4] - evalCount[1][4]) + 1600 * (
                      evalCount[0][3] - evalCount[1][0]) + 700 * (
                      evalCount[0][2] - evalCount[1][1]) + 100 * (
                      evalCount[0][1] - evalCount[1][2]) + 10 * (
                      evalCount[0][0] - evalCount[1][3]) - 100 * (
                      evalCount[0][5] - evalCount[1][5])

    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)  # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m[0])  # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list

def getSourceAndTargetFromMove(state, move,dice=[1,6]):
    checker_positions = move.split(",")
    if state.whose_move == 1:
        dice[0] = -dice[0]
        dice[1] = -dice[1]

    #return [[],[]]
    if len(checker_positions) != 0 and checker_positions != [] and checker_positions != None:
        if len(checker_positions) == 1:
            return [[],[]]
        elif len(checker_positions) == 2:
            if checker_positions[0] == 'p':
                first_part = [int(checker_positions[1]) -1, dice[1]]
                if int(checker_positions[1]) -1 + dice[1] > 23:
                    second_part = []
                else:
                    second_part = [int(checker_positions[1]) -1 + dice[1], dice[0]]
            elif checker_positions[1] == 'p':
                first_part = [int(checker_positions[0]) - 1, dice[0]]
                if int(checker_positions[0]) -1 + dice[0] > 23:
                    second_part = []
                else:
                    second_part = [int(checker_positions[0]) - 1 + dice[0], dice[1]]
            else:
                first_part = [int(checker_positions[0]) - 1, dice[0]]
                second_part = [int(checker_positions[1]) - 1, dice[1]]
            return [first_part, second_part]
        else:
            if checker_positions[2] == 'R':
                if checker_positions[0] == 'p':
                    first_part = [int(checker_positions[1]) - 1, dice[0]]
                    if int(checker_positions[1]) - 1 + dice[0] > 23:
                        second_part = []
                    else:
                        second_part = [int(checker_positions[1]) - 1 + dice[0], dice[1]]
                elif checker_positions[1] == 'p':
                    first_part = [int(checker_positions[0]) - 1, dice[1]]
                    if int(checker_positions[0]) - 1 + dice[1] > 23:
                        second_part = []
                    else:
                        second_part = [int(checker_positions[0]) - 1 + dice[1], dice[0]]
                else:
                    first_part = [int(checker_positions[0]) - 1, dice[1]]
                    second_part = [int(checker_positions[1]) - 1, dice[0]]
                return [first_part, second_part]
            else:
                return [[],[]]
    else:
        return [[],[]]








