import sys
import numpy as np
import math
import random
import json
import requests
import time
import gym
import gym_maze
from gym_maze.envs.maze_manager import MazeManager
from riddle_solvers import *
import logging

logging.basicConfig(filename=r"D:\Github\DigitalSquad\gym-maze\logging.log", level=logging.DEBUG, filemode='w')
logging.debug('This message should appear on the console') 

flag = 0
reach_END = False
backToEnd = []
dir = [[0 for i in range(10)] for j in range(10)]             # number of avalible directions
visited = [[False for i in range(11)] for j in range(11)]     # bool for visited nodes
come_from = [[[-1,-1] for i in range(10)] for j in range(10)] # previous node for each node
blocked = [[[] for i in range(11)] for j in range(11)]        # Blocked
prev_state = [0, 0]
temp = [1,1]
N_Visited = set()
go_back = False
End_path = []


# logging.debug (blocked)
# def reverse_action():
#   global End_path
#   actions = ['N', 'S', 'E', 'W']
#   for action in End_path:
#     a = actions.index(action)
#     if (a == 1 or a == 3):
#       a -= 1
#     else:
#       a += 1

def GoToExit(steps_back, rescue_items):
  score_now = ((rescue_items *  250) * (rescue_items/steps)) * 0.8
  goto_exit = ((rescue_items *  250) * (rescue_items/steps + steps_back))
  if(score_now > goto_exit):
    manager.set_done(agent_id)
    return 0
    
  

def select_action(state):
    # logging.debug (state)
    global prev_state
    global flag
    global go_back
    global N_Visited
    global End_path
    idx = [(0, -1),(0,1),(1,0),(-1,0)]
    # idx = [(0,1),(0, -1),(1,0),(-1,0)]
    # idx = [(1,0),(0,1),(0, -1),(-1,0)]
    # This is a random agent 
    # This function should get actions from your trained agent when inferencing.
    actions = ['N', 'S', 'E', 'W']
    # actions = [ 'S','N', 'E', 'W']
    # actions = [ 'E','S','N',  'W']
    x = state[0][0]
    y = state[0][1]
    N_Visited.add((x,y))
    
    logging.debug (f"init {state[0][0]}, {prev_state}, { dir[x][y]} ")
    
    while (True):
      if ((x,y) == (0,0)):
        
        if (flag%2 == 0):
          logging.debug("first node")
          action = actions[1]
          flag += 1
        else:
          action = actions[2]
        
        logging.debug (f"action ({x},{y}")
        visited [x][y] = True
        action_index = actions.index(action)
        dir[x][y] += 1 # add direction taken
        prev_state = [0,0]
        logging.debug(action)
        return action, action_index
      
      if (state[0][0] == prev_state[0] and state[0][1] == prev_state[1] and dir[x][y] < 4): # have direction move (same location)
        go_back = False
        logging.debug (f"try another direction {prev_state}, {state[0]}, {dir[x][y]}")
        
        next = dir[x][y]
        
        blocked_idx = next -1
        b1 = x + idx[blocked_idx][0]
        b2 = y + idx[blocked_idx][1]
        blocked[b1][b2].append((x,y))
        logging.debug(f"Current: { state[0]}, blocked: {blocked[x][y]}")
        # check that it is not prev
        a = x + idx[next][0]
        b = y + idx[next][1]
        
        logging.debug(f"temp: {temp}")
        if (a >= 0 and a < 10 and b >= 0 and b < 10): # if valid
          if (come_from[x][y] != [a,b]): # not comming from upcomong node
            if ((a,b) not in blocked[x][y]):
              action = actions[next]
              action_index = actions.index(action)
              logging.debug(action)
              dir[x][y] += 1 # add direction take
              return action, action_index
        dir[x][y] += 1 # add direction take
        continue
      elif ( dir[x][y] >= 4 ): # go back
        logging.debug (f"go back {prev_state} {state[0]} {come_from[x][y]}")
        prev_state = [x,y]
        z = x - come_from[x][y][0]
        s = y - come_from[x][y][1]
        logging.debug(f"{z},{s}")
        Rback = idx.index((z,s))
        if (Rback == 1 or Rback == 3):
          Rback -= 1
        else:
          Rback += 1
        action = actions[Rback]
        action_index = actions.index(action)
        logging.debug(action)
        return action, action_index
      elif ((state[0][0] != prev_state[0] or state[0][1] != prev_state[1]) and dir[x][y] < 4): # move
        go_back = False
        logging.debug (f"move {state[0]} {state[0]} {prev_state} {dir[x][y]}")
        
        visited[x][y] = True
        if(come_from[x][y] == [-1,-1]):
          come_from[x][y] = prev_state
        prev_state = [x,y]
        
        next = dir[x][y] 
        a  = x + idx[next][0]
        b  = y + idx[next][1]
        # if(come_from[x][y][0] )
        # logging.debug (temp)
        logging.debug(f"temp {temp}")
        if (a >= 0 and a < 10 and b >= 0 and b < 10):
          if((a,b) not in N_Visited):
            if ((a,b) not in blocked[x][y]):
              action = actions[next]
              action_index = actions.index(action)
              logging.debug(action)
              dir[x][y] += 1 # add direction taken
              return action, action_index
          dir[x][y] += 1 # add direction take
          continue
      else:
        logging.debug ("prev {prev_state}, {state[0]}, {dir[x][y]}")
        logging.debug("Dead End")
        # break
        
        
      
      # action = actions[next]
      # action_index = actions.index(action)
      # return action, action_index

steps = 0
def local_inference(riddle_solvers):
    # actions = ['N', 'S', 'E', 'W']
    obv = manager.reset(agent_id)
    # global flag
    global steps
    global N_Visited
    global reach_END
    
    info = {'rescued_items': 0, 'riddle_type': None, 'riddle_question': None}
    
    for t in range(300):
      
      time.sleep(0.01)
      steps +=1
      print("steps: ",steps)
      logging.debug (f"steps: {steps}")
      state_0 = obv
        
      
      if (steps > 51):
        if (steps > 50 and steps < 111): # Worst case with 3 riddles (16 PT)
          # Select an action
          
          action, action_index = select_action(state_0) 
          obv, reward, terminated, truncated, info = manager.step(agent_id, action)
          print ("rescued from info",info['rescued_items'])
          
          if not info['riddle_type'] == None:
              solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
              obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          
          if (steps < 61 and info['rescued_items'] > 1): # 2 riddles
            print (f"out within 60 with 2 in {steps} steps")
            manager.set_done(agent_id)
            break
          
          if (info['rescued_items'] > 2): # 3 riddles
            print (f"out within 110 with 2 in {steps} steps")
            manager.set_done(agent_id)
            break
          
        elif(steps > 110 and steps < 200): # 4 riddles (Worst = 16 PT)
          
          action, action_index = select_action(state_0) 
          obv, reward, terminated, truncated, info = manager.step(agent_id, action)
          print ("resude from info",info['rescued_items'])
          
          if not info['riddle_type'] == None:
              solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
              obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          
          if ( info['rescued_items'] > 3):
            print (f"out within 200 with 3 in {steps} steps")
            manager.set_done(agent_id)
            break
        
        elif( steps >= 200): # have 3 riddles 9 point
          print ((9,9) in N_Visited, len(N_Visited))
          if ((9,9) in N_Visited):
            
            if (info['rescued_items'] > 2):
                manager.set_done(agent_id)
                break # Stop Agent
              # calculate the best desicion to go back or exit
              
            else:
              action, action_index = select_action(state_0) 
              obv, reward, terminated, truncated, info = manager.step(agent_id, action)
              
              if not info['riddle_type'] == None:
                solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
                obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
              print ("resude from info",info['rescued_items'])
          elif ((9,9) not in N_Visited):
            
            action, action_index = select_action(state_0) 
            obv, reward, terminated, truncated, info = manager.step(agent_id, action)
            print ("resude from info",info['rescued_items'])
            if not info['riddle_type'] == None:
                solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
                obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          # elif (info['rescued_items'] > 2 and (9,9) in N_Visited): # calculate the best desicion to go back or exit
          
          
          
          if(info['rescued_items'] > 2 and np.array_equal(obv[0], (9,9))): # Exit at (9,9) with 3 or more
            logging.debug ("out in more that 200 with 3 or more with exit")
            manager.set_done(agent_id)
            break # Stop Agent
        # elif (len(N_Visited)
        else:
          h = 3
          logging.debug ("A&AAAAAAAAAAA")
          manager.set_done(agent_id)
          break # Stop Agent
      else:
        
        action, action_index = select_action(state_0) 
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)
        print("resude from info",info['rescued_items'])
        if not info['riddle_type'] == None:
            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
        # if np.array_equal(obv[0], (9,9)):
      # # IMPLEMENT YOUR OWN TERMINATING CONDITION
        # if np.array_equal(obv[0], (9,9)):s
      if RENDER_MAZE:
        manager.render(agent_id)

      states[t] = [obv[0].tolist(), action_index, str(manager.get_rescue_items_status(agent_id))]   


if __name__ == "__main__":

    sample_maze = np.load(r"D:\Github\DigitalSquad\gym-maze\gym_maze\envs\maze.npy")
    agent_id = "9" # add your agent id here
    
    manager = MazeManager()
    manager.init_maze(agent_id, maze_cells=sample_maze)
    env = manager.maze_map[agent_id]

    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    maze = {}
    states = {}

    
    maze['maze'] = env.maze_view.maze.maze_cells.tolist()
    maze['rescue_items'] = list(manager.rescue_items_dict.keys())

    MAX_T = 5000
    RENDER_MAZE = True
    

    local_inference(riddle_solvers)

    # with open("./states.json", "w") as file:
    #     json.dump(states, file)

    
    # with open("./maze.json", "w") as file:
    #     json.dump(maze, file)
        
