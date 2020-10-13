#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random


def print_matrix(m):
    """
    Print passed matrix
    TODO: 1) fix print matrix trailing commas; 2) use list comprehensions
    """
    for row in m:
        for col in row:
            print("{:-5.1f}, ".format(col), end='')
        print()
    print()


def normalize_matrix(m):
    """ Normalize passed matrix to values [0 - 100] """
    max_value = max([max(r) for r in m])
    return [[j / max_value * 100 for j in i] for i in m]


def get_available_actions(state):
    """ Return list of actions available to the agent based on current state """
    return [i for i, n in enumerate(R[state]) if n >= 0]


def sample_next_action(available_actions):
    """ Randomly select an action from the passed list of actions """
    return random.choice(available_actions)


def update(current_state, action, gamma):
    """ Update the Q matrix """
    max_index = [i for i, n in enumerate(Q[action]) if n == max(Q[action])]
    if len(max_index) > 1:
        max_index = int(random.choice(max_index))
    else:
        max_index = int(max_index[0])

    max_value = Q[action][max_index]
    Q[current_state][action] = R[current_state][action] + max_value * gamma


if __name__ == "__main__":
    edge_list = [(0, 4), (4, 3), (4, 5), (3, 2), (5, 1), (1, 3)]

    # Assign a goal state
    goal = 5

    # Create the rewards matrix and initialize all connections to -1
    matrix_size = 6  # number of nodes in the graph
    R = [x[:] for x in [[-1.0] * matrix_size] * matrix_size]
    for edge in edge_list:
        row, col = edge[0], edge[1]  # = 0 "from" edge, 1 = "to" edge
        if edge[1] == goal:
            R[row][col] = 100.0
        else:
            R[row][col] = 0.0
        # Need to set rewards for edge in reverse for undirected graph
        if edge[0] == goal:
            R[col][row] = 100.0
        else:
            R[col][row] = 0.0
    # Make sure the agent stays in the goal state once reached
    R[goal][goal] = 100.0

    # Create and initialize Q values matrix to all zeros.
    Q = [x[:] for x in [[0.0] * matrix_size] * matrix_size]

    # Discount factor for rewards
    gamma = 0.8

    num_episodes = 500
    for i in range(num_episodes):
        current_state = random.randint(0, matrix_size - 1)
        while current_state != goal:
            available_actions = get_available_actions(current_state)
            action = sample_next_action(available_actions)
            update(current_state, action, gamma)
            current_state = action

    normalized_Q = normalize_matrix(Q)

    # Find shortest path to goal node from all other nodes
    for current_state in [0, 1, 2, 3, 4, 5]:
        steps = [current_state]
        while current_state != goal:
            next_step_index = [i for i, n in enumerate(Q[current_state]) if n == max(Q[current_state])]
            if len(next_step_index) > 1:
                next_step_index = int(random.choice(next_step_index))
            else:
                next_step_index = int(next_step_index[0])
            steps.append(next_step_index)
            current_state = next_step_index
        print('Shortest path: {}'.format(steps))
