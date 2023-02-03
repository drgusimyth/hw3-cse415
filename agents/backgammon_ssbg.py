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

        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        moves = self.get_all_moves()
        if len(moves) == 0:
            return "NO MOVES COULD BE FOUND"
        best_move = None
        best_score = -2147483649
        for x in moves:
            score = expectimax(x, maxply, True);
            if score > best_score:
                best_move = x
        return best_move


    def expectimax(self, state, maxply, maxPlayer):
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        moves = self.get_all_moves()
        if maxply == 0:
            return self.staticEval(self,state)
        if maxPlayer: # max player's turn
            maxEval = -2147483649
            for x in moves:
                eval = self.expectimax(x, maxply - 1, False)
                maxEval = max(eval, maxEval)
            return maxEval
        else: #random player's turn
            total_eval = 0
            for x in moves:
                total_eval += self.expectimax(x, maxply - 1, True)
            expected = total_eval / len(moves)
            return expected


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        if self.special is not None:
            return self.special(state)

        self.evalCount = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        for i in range(4):
            for x in self.pointLists[i * 6:(i + 1) * 6]:
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

        return 100 * (self.evalCount[0][6] - self.evalCount[1][6]) + 90 * (
                    self.evalCount[0][4] - self.evalCount[1][1]) + 50 * (
                    self.evalCount[0][3] - self.evalCount[1][2]) - 50 * (
                    self.evalCount[0][2] - self.evalCount[1][3]) - 90 * (
                    self.evalCount[0][1] - self.evalCount[1][4]) - 100 * (self.evalCount[0][5] - self.evalCount[1][5])


