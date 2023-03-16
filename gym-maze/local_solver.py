import sys
import numpy as np
import math
import random
import json
import requests

import gym
import gym_maze
from gym_maze.envs.maze_manager import MazeManager
from riddle_solvers import *

# def select_action(state):
#     # This is a random agent 
#     # This function should get actions from your trained agent when inferencing.
#     actions = ['N', 'S', 'E', 'W']
#     random_action = random.choice(actions)
#     action_index = actions.index(random_action)
#     return random_action, action_index


# def select_action(state, dst):
#     # Implement maze routing algorithm to find the next action
    
#     # Define helper function to calculate Manhattan distance
#     def MD(pt1, pt2):
#         return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
    
#     cur = state[0]
#     actions = ['N', 'S', 'E', 'W']
#     MD_best = MD(cur, dst)
#     productive_paths = []
    
#     # Check if any of the four neighbors decrease Manhattan distance to destination
#     for action in actions:
#         next_pos = env.move(cur, action)
#         if env.valid_position(next_pos) and MD(next_pos, dst) < MD_best:
#             productive_paths.append(action)
    
#     if productive_paths:
#         # Take the productive path that brings us closer to the destination
#         next_action = random.choice(productive_paths)
#     else:
#         # Calculate the line between current position and destination
#         dx = dst[0] - cur[0]
#         dy = dst[1] - cur[1]
#         line = (dx, dy)
        
#         # Select the first path in the left/right of the line
#         if line[0] >= 0:
#             hand_rule = ['N', 'E', 'S', 'W']
#         else:
#             hand_rule = ['N', 'W', 'S', 'E']
#         next_action = hand_rule[hand_rule.index(actions[0]) - 1]
        
#         # Follow the right-hand/left-hand rule until Manhattan distance to destination is decreased
#         while True:
#             next_pos = env.move(cur, next_action)
#             if env.valid_position(next_pos) and MD(next_pos, dst) < MD_best:
#                 break
#             hand_rule = hand_rule[1:] + [hand_rule[0]]
#             next_action = hand_rule[0]
    
#     action_index = actions.index(next_action)
#     return next_action, action_index

def select_action(state, dst= (9,9)):
    # Get current position and MD to destination
    cur_pos = tuple(state[0])
    MD_best = manhattan_distance(cur_pos, dst)

    # Check if there exists a productive path
    productive_paths = []
    for action in ['N', 'S', 'E', 'W']:
        next_pos, reward, terminated, info = env.step(agent_id, action)
        next_pos = tuple(next_pos)
        MD_next = manhattan_distance(next_pos, dst)
        if MD_next < MD_best:
            productive_paths.append((action, next_pos, MD_next))
        env.step(agent_id, opposite_action(action)) # undo the step

    # Take the productive path if it exists
    if productive_paths:
        productive_paths.sort(key=lambda x: x[2])
        action, next_pos, _ = productive_paths[0]
        cur_pos = next_pos
    else:
        # Update MD_best and select the first path in the left/right of the line
        MD_best = manhattan_distance(cur_pos, dst)
        line = (cur_pos, dst)
        left_or_right = 1 if random.random() < 0.5 else -1
        action, next_pos = first_path(left_or_right, line)
        cur_pos = next_pos

        # Follow the right-hand/left-hand rule
        while manhattan_distance(cur_pos, dst) != MD_best or not productive_paths:
            left_or_right *= -1
            action, next_pos = first_path(left_or_right, line)
            cur_pos = next_pos
            productive_paths = []
            for action in ['N', 'S', 'E', 'W']:
                next_pos, reward, terminated, info = env.step(agent_id, action)
                next_pos = tuple(next_pos)
                MD_next = manhattan_distance(next_pos, dst)
                if MD_next < MD_best:
                    productive_paths.append((action, next_pos, MD_next))
                env.step(agent_id, opposite_action(action)) # undo the step
            if productive_paths:
                productive_paths.sort(key=lambda x: x[2])
                action, next_pos, _ = productive_paths[0]
                cur_pos = next_pos
                break

    # Update states
    state[0] = list(cur_pos)
    action_index = ACTIONS.index(action)
    return action, action_index

def first_path(left_or_right, line):
    """Returns the action and the next position to take for the first path found in the left/right of the given line."""
    if left_or_right == 1:  # left
        if line[1][0] == line[0][0]:  # Vertical line
            if line[1][1] > line[0][1]:
                action = "E"
                next_pos = (line[0][0], line[0][1] + 1)
            else:
                action = "W"
                next_pos = (line[0][0], line[0][1] - 1)
        else:  # Horizontal line
            if line[1][0] > line[0][0]:
                action = "S"
                next_pos = (line[0][0] + 1, line[0][1])
            else:
                action = "N"
                next_pos = (line[0][0] - 1, line[0][1])
    else:  # right
        if line[1][0] == line[0][0]:  # Vertical line
            if line[1][1] > line[0][1]:
                action = "W"
                next_pos = (line[0][0], line[0][1] - 1)
            else:
                action = "E"
                next_pos = (line[0][0], line[0][1] + 1)
        else:  # Horizontal line
            if line[1][0] > line[0][0]:
                action = "N"
                next_pos = (line[0][0] - 1, line[0][1])
            else:
                action = "S"
                next_pos = (line[0][0] + 1, line[0][1])
    return action, next_pos


def opposite_action(action):
    if action == 'N':
        return 'S'
    elif action == 'S':
        return 'N'
    elif action == 'E':
        return 'W'
    elif action == 'W':
        return 'E'

def manhattan_distance(src, dst):
    return abs(src[0] - dst[0]) + abs(src[1] - dst[1])

def move(env, pos, action):
    obs, _, _, _,_ = env.step(action)
    return obs[0]


def local_inference(riddle_solvers):

    obv = manager.reset(agent_id)

    for t in range(MAX_T):
        # Select an action
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)

        if not info['riddle_type'] == None:
            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)

        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        if np.array_equal(obv[0], (9,9)):
            manager.set_done(agent_id)
            break # Stop Agent

        if RENDER_MAZE:
            manager.render(agent_id)

        states[t] = [obv[0].tolist(), action_index, str(manager.get_rescue_items_status(agent_id))]       
        


if __name__ == "__main__":

    sample_maze = np.load("hackathon_sample.npy")
    agent_id = "9" # add your agent id here
    
    manager = MazeManager()
    manager.init_maze(agent_id, maze_cells=sample_maze)
    env = manager.maze_map[agent_id]

    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    maze = {}
    states = {}
    # vis 

    
    maze['maze'] = env.maze_view.maze.maze_cells.tolist()
    maze['rescue_items'] = list(manager.rescue_items_dict.keys())

    MAX_T = 5000
    RENDER_MAZE = True
    

    local_inference(riddle_solvers)

    with open("./states.json", "w") as file:
        json.dump(states, file)

    
    with open("./maze.json", "w") as file:
        json.dump(maze, file)
    