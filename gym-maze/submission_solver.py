import sys
import numpy as np
import math
import random
import json
import requests

from riddle_solvers import *

### the api calls must be modified by you according to the server IP communicated with you
#### students track --> 16.170.85.45
#### working professionals track --> 13.49.133.141
server_ip = '16.170.85.45'

def select_action(state):
    # This is a random agent 
    # This function should get actions from your trained agent when inferencing.
    actions = ['N', 'S', 'E', 'W']
    random_action = random.choice(actions)
    action_index = actions.index(random_action)
    return random_action, action_index

flag = 0
dir = [[0 for i in range(10)] for j in range(10)] # number of directions
visited = [[False for i in range(11)] for j in range(11)] # bool 
come_from = [[[-1,-1] for i in range(10)] for j in range(10)] # previous node
prev_state = [0, 0]
temp = [1,1]
N_Visited = 0
go_back = False

def select_action(state):

    global prev_state
    global flag
    global go_back
    global N_Visited
    global End_path
    idx = [(0, -1),(0,1),(1,0),(-1,0)]
    # This is a random agent 
    # This function should get actions from your trained agent when inferencing.
    actions = ['N', 'S', 'E', 'W']
    x = state[0][0]
    y = state[0][1]
    print ("init", state[0], prev_state, dir[x][y])
    while (True):
      if ((x,y) == (0,0)):
        
        if (flag%2 == 0):
          print("ZZZZZZZZZZ")
          action = actions[2]
          flag += 1
        else:
          action = actions[1]
        print (action, (x,y))
        visited [x][y] = True
        N_Visited += 1
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
          if (come_from[x][y] != temp and visited[temp[0]][temp[1]] == False): # not comming from upcomong node
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
        N_Visited += 1
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
          if(visited[temp[0]][temp[1]] == False):
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
        break
  

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

cnt = 0 
def submission_inference(riddle_solvers):

    response = requests.post(f'http://{server_ip}:5000/init', json={"agentId": agent_id})
    obv = get_obv_from_response(response)
    global cnt
    while(True):
      if (cnt < 250):
        cnt +=1
        print (cnt)
        # Select an action
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


        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        if np.array_equal(response.json()['position'], (9,9)):
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break
      else:
        response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
        break


if __name__ == "__main__":
    
    agent_id = ""
    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    submission_inference(riddle_solvers)
    
