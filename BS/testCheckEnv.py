import sys
import numpy as np
import math
import random
import json
import requests
import random
import numpy as np
import gym


sys.path.append('c://Users/omara/Desktop/VSCODE/DigitalSquad/gym-maze/')
import gym_maze
from gym_maze.envs.maze_manager import MazeManager
from riddle_solvers import *
from stable_baselines3.common.env_checker import check_env


sample_maze = np.load("hackathon_sample.npy")
agent_id = "9" # add your agent id here
    
manager = MazeManager()
manager.init_maze(agent_id, maze_cells=sample_maze)
env = manager.maze_map[agent_id]
check_env(env)