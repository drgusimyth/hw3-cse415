'''
Name(s): yishu fang, tommy zhao
UW netid(s): yishuf, tommzh
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxply = 2
        self.special = None
        self.evalCount = None


    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "yishuf" + " " + "tommzh"

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    def get_all_moves(self):
        """Uses the mover to generate all legal moves."""
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

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. Count the chance nodes
    # as a ply too!
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxply = maxply


    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        if func is not None:
            self.special = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1, die2):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        maxPlayer = state.whose_move
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        moves = self.get_all_moves()
        if moves == 'p':
            return 'no moves, pass'
        best_move = None
        best_score = -1e20
        for x in moves:
            s = getSourceAndTargetFromMove(x, [die1, die2])
            temp_state = genmoves.bgstate(state)
            if s[0] != []:
                if s[0][0] == -1:
                    genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                           1 - temp_state.whose_move)
                elif sum(s[0]) > 23:
                    temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                   1 - temp_state.whose_move)
                else:
                    temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                    1 - temp_state.whose_move)
            if s[1] != []:
                if s[1][0] == -1:
                    genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                           1 - temp_state.whose_move)
                elif sum(s[1]) > 23:
                    temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                   1 - temp_state.whose_move)
                else:
                    temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                    1 - temp_state.whose_move)
            temp_state.whose_move = 1 - temp_state.whose_move
            score = self.expectimax(temp_state, self.maxply, maxPlayer, die1, die2)
            if score > best_score:
                best_move = x
                best_score = score
        return best_move


    def expectimax(self, state, maxply, maxPlayer, die1, die2):
        if maxply == 0:
            return self.staticEval(state)

        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        moves = self.get_all_moves()

        if maxPlayer == state.whose_move:
            maxEval = -1e20
            for x in moves:
                s = getSourceAndTargetFromMove(x, [die1, die2])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        genmoves.move_from_bar(temp_state,temp_state.whose_move,sum(s[0]), 1- temp_state.whose_move)
                    elif sum(s[0]) > 23:
                        temp_state = genmoves.bear_off(temp_state,temp_state.whose_move,s[0][0], 1-temp_state.whose_move)
                    else:
                        temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]), 1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        genmoves.move_from_bar(temp_state,temp_state.whose_move,sum(s[1]), 1- temp_state.whose_move)
                    elif sum(s[1]) > 23:
                        temp_state = genmoves.bear_off(temp_state,temp_state.whose_move,s[1][0], 1-temp_state.whose_move)
                    else:
                        temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]), 1 - temp_state.whose_move)
                temp_state.whose_move = 1 - temp_state.whose_move
                eval = self.expectimax(temp_state, maxply - 1, maxPlayer, die1, die2)
                maxEval = max(eval, maxEval)
            return maxEval
        else:
            total_eval = 0
            for x in moves:
                s = getSourceAndTargetFromMove(x, [die1, die2])
                temp_state = genmoves.bgstate(state)
                if s[0] != []:
                    if s[0][0] == -1:
                        genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[0]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[0]) > 23:
                        temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[0][0],
                                                       1 - temp_state.whose_move)
                    else:
                        temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[0][0], sum(s[0]),
                                                        1 - temp_state.whose_move)
                if s[1] != []:
                    if s[1][0] == -1:
                        genmoves.move_from_bar(temp_state, temp_state.whose_move, sum(s[1]),
                                                            1 - temp_state.whose_move)
                    elif sum(s[1]) > 23:
                        temp_state = genmoves.bear_off(temp_state, temp_state.whose_move, s[1][0],
                                                       1 - temp_state.whose_move)
                    else:
                        temp_state = genmoves.move_from(temp_state, temp_state.whose_move, s[1][0], sum(s[1]),
                                                        1 - temp_state.whose_move)


                temp_state.whose_move = 1 - temp_state.whose_move
                total_eval += self.expectimax(temp_state, maxply - 1, maxPlayer, die1, die2)
            expected = total_eval / len(moves)
            return expected


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
                      evalCount[0][0] - evalCount[1][3]) + 1 * (
                      evalCount[0][5] - evalCount[1][5])


def getSourceAndTargetFromMove(move,dice=[1,6]):
    checker_positions = move.split(",")
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