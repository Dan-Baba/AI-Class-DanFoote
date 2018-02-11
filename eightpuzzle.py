import sys
import copy
import heapq



class Agent:
    priority_queue = []
    def __init__(self, board, goal):
        self.goal = goal
        self.steps = 0
        self.expand_node(Node(board, [], 0))

    def solve(self):
        while True:
            if (heuristic(self.priority_queue[0].board, self.goal) == 0):
                return self.priority_queue[0].actions
            self.expand_node(heapq.heappop(self.priority_queue))
            print(self.priority_queue[0].board)


    def expand_node(self, node):
        list_moves = possible_moves(node.board)
        if (node.actions):
            remove_backtrack(list_moves, node.actions[len(node.actions) - 1])

        for move in list_moves:
            self.steps += 1
            new_moves = copy.deepcopy(node.actions)
            new_moves.append(move)
            new_board = copy.deepcopy(node.board)
            new_board = do_move(new_board, move)
            # Total heuristic should account for moves
            new_heuristic = heuristic(new_board, self.goal) + len(new_moves)
            heapq.heappush(self.priority_queue, Node(new_board, new_moves, new_heuristic))

class Node:
    def __init__(self, board, actions, heuristic):
        self.board = board
        self.actions = actions
        self.heuristic = heuristic

    def __str__(self):
        return self.board + "\nBy taking actions: " + self.actions
    def __eq__(self, other):
        return self.heuristic == other.heuristic
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    def __gt__(self, other):
        return self.heuristic > other.heuristic

class Board:
    # size, current, goal
    def __init__(self, size, board):
        self.size = size
        self.board = []
        inboard = ""
        for tile in board:
            if (tile == "0"):
                inboard += " "
            else:
                inboard += tile 
        
        #Load the board in a 2D array
        for x in range(size):
            self.board.append(list(inboard[x*size:(x+1)*size]))

    def __str__(self):
        message = ""
        for y in range(self.size):
            for x in range(self.size):
                message += str(self.board[y][x]) + " "
            message += "\n"
        return message

# I could have just returned x and y, but I wanted to contain results a little better...
class Coords:
    """Container for x y coords on the board"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

# Replaced enum with combo of Direction and Move classes, so that I can use it as Move.UP and yet have it represent itself in a list in a human readable way.
class Direction:
    def __init__(self, direction):
        self.direction = direction 
    def __str__(self):
        if (self.direction == 1):
            return "UP"
        elif (self.direction == 2):
            return "RIGHT"
        elif (self.direction == 3):
            return "DOWN"
        elif (self.direction == 4):
            return "LEFT"
    def __repr__(self):
        return str(self)

class Move:
    UP = Direction(1)
    RIGHT = Direction(2)
    DOWN = Direction(3)
    LEFT = Direction(4)

def possible_moves(board):
    spaceLoc = find_tile(board, " ")
    moves = []
    # Can we move up?
    if (spaceLoc.y != 0):
        moves.append(Move.UP)
    # Can we move right?
    if (spaceLoc.x != board.size - 1):
        moves.append(Move.RIGHT)
    # Can we move down?
    if (spaceLoc.y != board.size - 1):
        moves.append(Move.DOWN)
    # Cane we move left?
    if (spaceLoc.x != 0):
        moves.append(Move.LEFT)
    
    return moves

def do_move(board, move):
    space_loc = find_tile(board, " ")
    x, y = space_loc.x, space_loc.y
    # Move up
    if (move == Move.UP):
        board.board[y][x], board.board[y-1][x] = board.board[y-1][x], board.board[y][x]
    # Move Right
    elif (move == Move.RIGHT):
        board.board[y][x], board.board[y][x+1] = board.board[y][x+1], board.board[y][x] 
    # Move Down
    elif (move == Move.DOWN):
        board.board[y][x], board.board[y+1][x] = board.board[y+1][x], board.board[y][x]
    # Move Left
    elif (move == Move.LEFT):
        board.board[y][x], board.board[y][x-1] = board.board[y][x-1], board.board[y][x]
    return board

def find_tile(board, target):
    for x in range(board.size):
        for y in range(board.size):
            if (board.board[x][y] == target):
                return Coords(y, x)
    raise Exception("Didn't find target: " + target)

def heuristic(board, goal):
    heuristic_total = 0
    for x in range(board.size):
        for y in range(board.size):
            if (board.board[y][x] != " "):
                target_loc = find_tile(goal, board.board[y][x])
                heuristic_total += abs(target_loc.x - x) + abs(target_loc.y - y)
    return heuristic_total

def linear_conflict_heuristic(board, goal):
    heuristic_total = 0
    for x in range(board.size):
        for y in range(board.size):
            if (board.board[y][x] != " "):
                target_loc = find_tile(goal, board.board[y][x])
                # Check horizontal, if it's supposed to be to left of item, it takes more turns to get it to correct position.
                for tile in goal.board[y]:
                     if (find_in_list(tile, board.board[y]) > x and goal.board[y].index(tile) < x):
                         heuristic_total += 3 # It takes minimum of 2 turns to swap them? Maybe 3 or 4
                heuristic_total += abs(target_loc.x - x) + abs(target_loc.y - y)
    return heuristic_total

def out_row_and_column_heuristic(board, goal):
    heuristic_total = 0
    for x in range(board.size):
        for y in range(board.size):
            if (board.board[y][x] != " "):
                target_loc = find_tile(goal, board.board[y][x])
                # If not in right row or column, increment.
                if (target_loc.x != x):
                    heuristic_total += 1
                if (target_loc.y != y):
                    heuristic_total += 1
    return heuristic_total


def find_in_list(element, list):
    try:
        index = list.index(element)
        return index
    except ValueError:
        return -1

# If the opposite of the last action performed is in the potential actions, remove it.
def remove_backtrack(potential_actions, last_action):
    if (last_action == Move.UP):
        action = Move.DOWN
    elif (last_action == Move.RIGHT):
        action = Move.LEFT
    elif (last_action == Move.DOWN):
        action = Move.UP
    elif (last_action == Move.LEFT):
        action = Move.RIGHT
    
    for i in range(len(potential_actions)):
        if (last_action and potential_actions[i] == action):
            del potential_actions[i]
            return

print(Board(3, sys.argv[1:10]))
print(Board(3, sys.argv[10:]))
# 3x3 is the only size that seems to work reliably.
# starting_board = Board(puzzle_size, str(input("Please input starting state (1 character per tile, 0 for blank)")))
# goal_board = Board(puzzle_size, str(input("Please input the final state desired (1 character per tile, 0 for blank)")))
# print ("Starting Board")
# print (starting_board)
# print ("Goal Board")
# print (goal_board)
# agent = Agent(starting_board, goal_board)
# print ("Trying to solve...")
# print (agent.solve())
# print (str(agent.steps) + " nodes expanded")
