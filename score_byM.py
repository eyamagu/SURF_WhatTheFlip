import pandas as pd
import numpy as np
from bisect import bisect_right
import glob

import traj_panda as traj_panda

PARENT_DIRECTORY = 'exp/05-16'
NEW_DIRECTORY = '/root/jupyter-kernels/FPC2/data/exp'
FP_DIRECTORY = '/root/jupyter-kernels/FPC2/normal'

def load_goal_data(gravity_int_bits, gravity_frac_bits, fd_int_bits, fd_frac_bits):
    try:
        goal_data = pd.read_csv(f'{FP_DIRECTORY}/{gravity_int_bits}_{gravity_frac_bits}_{fd_int_bits}_{fd_frac_bits}/data.csv')
        time_array = goal_data['time'].values
        position_array = goal_data[['q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6']].values
        return time_array, position_array
    except Exception as e:
        print(f"Error reading goal data CSV file: {e}")
        return None, None

def calculate_goal(time,time_array, position_array):
    
    # Find the right index using binary search for efficiency
    index = bisect_right(time_array, time)
    
    # Handle edge cases where time is outside the known time range
    if index == 0:
        return np.array(position_array[0])
    if index >= len(time_array):
        return np.array(position_array[-1])

#     # Linear interpolation between index-1 and index
#     prev_pos = np.array(position_array[index-1])
#     next_pos = np.array(position_array[index])
#     prev_time = time_array[index-1]
#     next_time = time_array[index]
    goal = np.array(position_array[index - 1])
    
    # # Calculate the time ratio
    # time_diff = next_time - prev_time
    # time_ratio = (time - prev_time) / time_diff

    # # Interpolate the position
    # pos_diff = next_pos - prev_pos
    # goal = prev_pos + pos_diff * time_ratio
    
    return goal
    
        

def calculate_score(position, time, time_array, position_array):
    #time = row['time']
    goal = calculate_goal(time, time_array, position_array)
    #position = [row['q_1'], row['q_2'], row['q_3'], row['q_4'], row['q_5'], row['q_6']]

    print("time: ", time)
    print("goal: ", goal)
    print("position: ", position)

    # calculate the distance
    #print("goal: ", goal)
    #print("position: ", position)
    try:
        distance = np.linalg.norm(goal - position)
    except Exception as e:
        print(e)
        return float('inf')

    return distance

def calculate_score_from_folder_fp(gravity_int_bits, gravity_frac_bits, fd_int_bits, fd_frac_bits, matrix_index, flip_bit):
    folder = f'{NEW_DIRECTORY}/{gravity_int_bits}_{gravity_frac_bits}_{fd_int_bits}_{fd_frac_bits}_{matrix_index}_{flip_bit}/{gravity_int_bits}_{gravity_frac_bits}_{fd_int_bits}_{fd_frac_bits}'
    print("reading from ", folder)
    
    time_array, position_array = load_goal_data(gravity_int_bits, gravity_frac_bits, fd_int_bits, fd_frac_bits)
    
    try:
        data = pd.read_csv(f'{folder}/data.csv')
    except Exception as e:
        print(e)
        return float('inf') # there may be an error because the df is empty
    # is data empty
    if data.empty:
        return float('inf')
    print('data read')
    # calculate the score and print the sum
    last_row = data.iloc[-1]
    time = last_row['time']
    position = np.array([last_row['q_1'], last_row['q_2'], last_row['q_3'], last_row['q_4'], last_row['q_5'], last_row['q_6']])
    score = calculate_score(position, time, time_array, position_array)
    return score


if __name__ == "__main__":

    folders = glob.glob(f'{PARENT_DIRECTORY}/*')

    print(folders)

    # every folder has data.csv, which we will read and score here

    for folder in folders:
        data = pd.read_csv(f'{folder}/data.csv')
        # is data empty
        if data.empty:
            print(folder, "inf")
            continue

        # calculate the score and print the sum
        
        
        print(folder, data['score'].sum()/len(data))
