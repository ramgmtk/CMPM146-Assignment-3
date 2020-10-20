from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    leaf_node = node
    leaf_state = state
    current_ucbt = float('-inf')
    opponents_turn = False;
    
    if not leaf_node.untried_actions: #if the node still has untried actions we are at a leaf node
        best_child, best_state = None, None
        if not leaf_node.child_nodes: #edge case for if we are evaluating a node that corresponds to a finished game state.
            return best_child, leaf_state
        if board.current_player(leaf_state) != identity : #used for adjusting ucbt value
            opponents_turn = True
        for move, child in leaf_node.child_nodes.items():
            ucbt_of_child = upper_common_bound(child, leaf_node, opponents_turn)
            if current_ucbt < ucbt_of_child:
                current_ucbt = ucbt_of_child
                best_child = child
                best_state = board.next_state(leaf_state, move)
        leaf_node, leaf_state = traverse_nodes(best_child, board, best_state, identity)
    
    return leaf_node, leaf_state
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    move = choice(node.untried_actions)
    node.untried_actions.remove(move)
    
    new_state = board.next_state(state, move)
    new_node = MCTSNode(node, move, board.legal_actions(new_state))
    #if not new_node.untried_actions:
        #print(board.is_ended(new_state))
    new_node.parent = node
    new_node.parent_action = move

    node.child_nodes[move] = new_node    
    return new_node, new_state
    # Hint: return new_node

#pass in the new_nodes state
def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    new_state = state 
    while not board.is_ended(new_state): #this should be changed if we want a bound for how far we simulate
        move = choice(board.legal_actions(new_state))
        new_state = board.next_state(new_state, move)
        
    return new_state


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if node == None:
        return
    if won:
        node.wins += 1
    node.visits += 1
    backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    best_move = None
    most_visits = 0

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf_node, current_state = traverse_nodes(node, board, sampled_game, identity_of_bot)
        if leaf_node != None: #only none if we are on end game board
            new_node, current_state = expand_leaf(leaf_node, board, current_state)
        current_state = rollout(board, current_state)
        result = rollout_result(board, identity_of_bot, current_state)
        backpropagate(new_node, result)
        
        if new_node.visits > most_visits:
            most_visits = new_node.visits
            best_move = new_node.parent_action
    
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return best_move

#determines if the final state evaluated i rollout is a win for the bot or not
def rollout_result(board, current_player, current_state):
    
    results = board.points_values(current_state)
    result = False
    if results[current_player] > 0:
        result = True
    return result
    #return results[current_player]

def upper_common_bound(node, parent_node, opponent_turn) :
    w = node.wins
    si = node.visits
    sp = parent_node.visits
    win_rate = w / si
    if opponent_turn:
        win_rate = 1 - win_rate
    ucbt = win_rate + (explore_faction * sqrt(log(sp) / si))
    return ucbt