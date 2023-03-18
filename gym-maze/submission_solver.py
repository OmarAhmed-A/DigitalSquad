import sys
import numpy as np
import math
import random
import json
import requests

from riddle_solvers import *
import logging

logging.basicConfig(filename=r"D:\Github\DigitalSquad\gym-maze\logging.log", level=logging.DEBUG, filemode='w')
logging.debug('This message should appear on the console') 

### the api calls must be modified by you according to the server IP communicated with you
#### students track --> 16.170.85.45
#### working professionals track --> 13.49.133.141
server_ip = '16.170.85.45'


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


dir = [[0 for i in range(10)] for j in range(10)]             # number of directions
visited = [[False for i in range(11)] for j in range(11)]     # bool 
come_from = [[[-1,-1] for i in range(10)] for j in range(10)] # previous node
blocked = [[[] for i in range(11)] for j in range(11)]   # Blocked
prev_state = [0, 0]
temp = [1,1]
N_Visited = set()
go_back = False
End_path = []


# print (blocked)
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

   

def move(agent_id, action):
    response = requests.post(f'http://{server_ip}:5000/move', json={"agentId": agent_id, "action": action})
    return response

def solve(agent_id,  riddle_type, solution):
    response = requests.post(f'http://{server_ip}:5000/solve', json={"agentId": agent_id, "riddleType": riddle_type, "solution": solution}) 
    print(response.json()) 
    return response

def get_obv_from_response(response):
    directions = response.json()['directions']
    distances = response.json()['distances']
    position = response.json()['position']
    obv = [position, distances, directions] 
    return obv

steps = 0 
riddles_counter = set()

def submission_inference(riddle_solvers):
  
    response = requests.post(f'http://{server_ip}:5000/init', json={"agentId": agent_id})
    obv = get_obv_from_response(response)
    global steps
  
    while(steps < 320):
      steps +=1
      print ("steps: ", steps)
      if (steps > 51):
        if (steps > 50 and steps < 120):
          # Select an action
          # time.sleep(0.001)
          state_0 = obv
          action, action_index = select_action(state_0) # Random action
          response = move(agent_id, action)
          
          with open("output.txt", "a") as f:
            print(response, file=f)
          if not response.status_code == 200:
            print(response)
            break
          
          obv = get_obv_from_response(response)
          print(response.json())
          print ("rescued from info",response.json()['rescuedItems'])
          
          if not response.json()['riddleType'] == None:
            solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
            response = solve(agent_id, response.json()['riddleType'], solution)
            riddles_counter.add(response.json()['riddleType'])
          
          if (steps < 65 and  response.json()['rescuedItems'] > 1): # 2 riddles
            print (f"out within 60 with 2 in {steps} steps")
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
          
          if ( response.json()['rescuedItems'] > 2):
            print (f"out within 110 with 2 in {steps} steps")
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
          
          
        elif(steps > 119 and steps < 200):
          state_0 = obv
          action, action_index = select_action(state_0) 
          response = move(agent_id, action)
          
          with open("output.txt", "a") as f:
            print(response, file=f)
          if not response.status_code == 200:
            print(response)
            break
          
          obv = get_obv_from_response(response)
          print(response.json())
          
          # print ("rescued from info",info['rescued_items'])
          if not response.json()['riddleType'] == None:
            solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
            response = solve(agent_id, response.json()['riddleType'], solution)
            riddles_counter.add(response.json()['riddleType'])
          
          if ( response.json()['rescuedItems'] > 3):
            print (f"out within 200 with 4 in {steps} steps")
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
        
        elif (steps > 199):
          if np.array_equal(response.json()['position'], (9,9)) and response.json()['rescuedItems'] > 2:
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
          
          elif (response.json()['rescuedItems'] > 2):
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
          
          else:
            state_0 = obv
            action, action_index = select_action(state_0) # Random action
            response = move(agent_id, action)
            if not response.status_code == 200:
                print(response)
                break

            obv = get_obv_from_response(response)
            print(response.json())

            if not response.json()['riddleType'] == None:
                solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
                response = solve(agent_id, response.json()['riddleType'], solution)
        else:
          print ("A& FINAL")
          response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
          break # Stop Agent
        
        
      else:
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        response = move(agent_id, action)
        with open("output.txt", "a") as f:
            print(response, file=f)
        if not response.status_code == 200:
          print(response)
          break
        
        obv = get_obv_from_response(response)
        print(response.json())
        
        if not response.json()['riddleType'] == None:
          solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
          response = solve(agent_id, response.json()['riddleType'], solution)
          riddles_counter.add(response.json()['riddleType'])
        

      


if __name__ == "__main__":
    
    with open("output.txt", "w") as f:
      print("start", file=f)
    
    agent_id = "3xP6rEjN7k"
    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    submission_inference(riddle_solvers)
    print (riddles_counter, len(riddles_counter))
    
    with open("output.txt", "a") as f:
      print("END", file=f)
    f.close()
    
    
