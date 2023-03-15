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



# curr = [0,0]
flag = 0
dir = [[0 for i in range(10)] for j in range(10)] # number of directions
visited = [[False for i in range(11)] for j in range(11)] # bool 
come_from = [[[-1,-1] for i in range(10)] for j in range(10)] # previous node
prev_state = [0, 0]
temp = [1,1]
N_Visited = set()
go_back = False
End_path = []


# def reverse_action():
#   global End_path
#   actions = ['N', 'S', 'E', 'W']
#   for action in End_path:
#     a = actions.index(action)
#     if (a == 1 or a == 3):
#       a -= 1
#     else:
#       a += 1

def select_action(state):

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
    
    print ("init", state[0], prev_state, dir[x][y])
    while (True):
      if ((x,y) == (0,0)):
        
        if (flag%2 == 0):
          print("ZZZZZZZZZZ")
          action = actions[1]
          flag += 1
        else:
          action = actions[2]
        print (action, (x,y))
        visited [x][y] = True
        action_index = actions.index(action)
        dir[x][y] += 1 # add direction taken
        prev_state = [0,0]
        print(action)
        return action, action_index
      if (state[0][0] == prev_state[0] and state[0][1] == prev_state[1] and dir[x][y] < 4): # have direction move (same location)
        go_back = False
        print ("try another direction ",prev_state, state[0], dir[x][y])
        next = dir[x][y] 
        # check that it is not prev
        temp[0] = x + idx[next][0]
        temp[1] = y + idx[next][1]
        print("temp", temp)
        if (temp[0] >= 0 and temp[0] < 10 and temp[1] >= 0 and temp[1] < 10): # if valid
          if (come_from[x][y] != temp): # not comming from upcomong node
            action = actions[next]
            action_index = actions.index(action)
            print(action)
            dir[x][y] += 1 # add direction take
            return action, action_index
        dir[x][y] += 1 # add direction take
        continue
      elif ( dir[x][y] >= 4 ): # go back
        print ("go back ",prev_state, state[0], come_from[x][y])
        prev_state = [x,y]
        z = x - come_from[x][y][0]
        s = y - come_from[x][y][1]
        print(z,s)
        Rback = idx.index((z,s))
        if (Rback == 1 or Rback == 3):
          Rback -= 1
        else:
          Rback += 1
        action = actions[Rback]
        action_index = actions.index(action)
        print(action)
        return action, action_index
      elif ((state[0][0] != prev_state[0] or state[0][1] != prev_state[1]) and dir[x][y] < 4): # move
        go_back = False
        print ("move ",state[0],prev_state,  dir[x][y])
        
        visited[x][y] = True
        if(come_from[x][y] == [-1,-1]):
          come_from[x][y]= prev_state
        prev_state = [x,y]
        
        next = dir[x][y] 
        temp[0]  = x + idx[next][0]
        temp[1]  = y + idx[next][1]
        # if(come_from[x][y][0] )
        # print (temp)
        print("temp", temp)
        if (temp[0] >= 0 and temp[0] < 10 and temp[1] >= 0 and temp[1] < 10):
          if((temp[0],temp[1]) not in N_Visited):
            action = actions[next]
            action_index = actions.index(action)
            print(action)
            dir[x][y] += 1 # add direction taken
            return action, action_index
          dir[x][y] += 1 # add direction take
          continue
      else:
        print ("prev",prev_state, state[0], dir[x][y] )
        print("XXXXXXXX")
        # break
        
        
      
      # action = actions[next]
      # action_index = actions.index(action)
      # return action, action_index

cnt = 0
def local_inference(riddle_solvers):
    # actions = ['N', 'S', 'E', 'W']
    obv = manager.reset(agent_id)
    # global flag
    global cnt
    global N_Visited
    info = {'rescued_items': 0, 'riddle_type': None, 'riddle_question': None}
    for t in range(MAX_T):
      cnt +=1
      print ("steps: ", cnt)
      if (cnt > 51):
        if (cnt > 50 and cnt < 92):
          # Select an action
          # time.sleep(0.001)
          state_0 = obv
          action, action_index = select_action(state_0) # Random action
          obv, reward, terminated, truncated, info = manager.step(agent_id, action)
          print ("rescued from info",info['rescued_items'])
          if not info['riddle_type'] == None:
              solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
              obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          if ( info['rescued_items'] > 1):
            print ("A&AAAAAAAAAAA11111")
            manager.set_done(agent_id)
            break
          # print(len(N_Visited))
          # riddle_solvers[info['riddle_type']]
          #   flag = 1
          # if (flag):
          #   End_path.append(action)
        # else:
        #   reverse_action()
        #   End_path.reverse()
        #   for p in End_path:
        #     action, action_index = p, actions.index(p) # Random action
        #     obv, reward, terminated, truncated, info = manager.step(agent_id, action)
        # # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
          # print(visited)
        elif(cnt > 50 and cnt < 130):
          state_0 = obv
          action, action_index = select_action(state_0) # Random action
          obv, reward, terminated, truncated, info = manager.step(agent_id, action)
          print ("resude from info",info['rescued_items'])
          if not info['riddle_type'] == None:
              solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
              obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          if ( info['rescued_items'] > 2):
            print ("A&AAAAAAAAAAA22222222")
            manager.set_done(agent_id)
            break
        
        else:
          h = 3
          print ("A&AAAAAAAAAAA")
          manager.set_done(agent_id)
          break # Stop Agent
      else:
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)
        print ("resude from info",info['rescued_items'])
        if not info['riddle_type'] == None:
            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
        # if np.array_equal(obv[0], (9,9)):
      # # IMPLEMENT YOUR OWN TERMINATING CONDITION
        # if np.array_equal(obv[0], (9,9)):
      if RENDER_MAZE:
        manager.render(agent_id)

      states[t] = [obv[0].tolist(), action_index, str(manager.get_rescue_items_status(agent_id))]   

          
      


if __name__ == "__main__":

    sample_maze = np.load(r"D:\Github\DigitalSquad\RL\sample_maze2.npy")
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

    with open("./states.json", "w") as file:
        json.dump(states, file)

    
    with open("./maze.json", "w") as file:
        json.dump(maze, file)
        
