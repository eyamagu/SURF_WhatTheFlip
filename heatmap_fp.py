import glob
import sys
import os

EXPERIMENT_DIRECTORY = "/root/jupyter-kernels/FPC2/data/exp/"

folders = glob.glob(f'{EXPERIMENT_DIRECTORY}/*')

print("folders: ", folders)

# remove the {EXPERIMENT_DIRECTORY} part
folders = [folder[len(EXPERIMENT_DIRECTORY):] for folder in folders]

print(folders)
# separate the int_bits and frac_bits
folders = [folder.split('_') for folder in folders]

GRAVITY_INT = '15'
GRAVITY_FRAC = '15'
FD_INT = '10'
FD_FRAC = '10'

# convert all to ints

# filter the list so that only the ones with two 8's are left
folders = [[int(x) for x in folder] for folder in folders if folder[0] == GRAVITY_INT and folder[1] == GRAVITY_FRAC]

print(folders)

# now remove the first two elements from each folder
folders = [folder[4:] for folder in folders]

folders = sorted(folders)

print(folders)

min_matrix_bits = folders[0][0] #int
max_matrix_bits = folders[-1][0]
min_flip_bits = folders[0][1] # frac
max_flip_bits = folders[-1][1]

print(min_matrix_bits)
print(max_matrix_bits)
print(min_flip_bits)
print(max_flip_bits)

# now read all and calculate the scores, then heatmap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from score_fp import calculate_score_from_folder_fp
  
#total_scores = [[calculate_score_from_folder(int_bits, frac_bits) for frac_bits in range(min_frac_bits, max_frac_bits+1)] for int_bits in range(min_int_bits, max_int_bits+1)]
print("total scores")
total_scores = np.array([[calculate_score_from_folder_fp(GRAVITY_INT, GRAVITY_FRAC, FD_INT, FD_FRAC, matrix_index, flip_bit) for flip_bit in range(min_flip_bits, max_flip_bits+1)] for matrix_index in range(min_matrix_bits, max_matrix_bits+1)])
print('end')
fig, ax = plt.subplots(figsize = (15,8))

colors = ["#d0d0f0", "#b3a0c6", "#8a5b8a", "#6a2c6c"]  # Light to dark purples
n_bins = [3]  # Discretizes the interpolation into bins
cmap_name = "soft_purple"
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

# fig, ax = plt.subplots()
cax = ax.matshow(total_scores, cmap=custom_cmap)

# Add colorbar
fig.colorbar(cax, orientation='horizontal', pad=0.05, fraction=0.09)

# We want to show all ticks...
ax.set_xticks(np.arange(len(range(min_flip_bits, max_flip_bits+1))))
ax.set_yticks(np.arange(len(range(min_matrix_bits, max_matrix_bits+1))))

# ... and label them with the respective list entries
ax.set_xticklabels(range(min_flip_bits, max_flip_bits+1))
ax.set_yticklabels(range(min_matrix_bits, max_matrix_bits+1))

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor", fontsize=10)

# Loop over data dimensions and create text annotations, but write the score with 3 decimal points
for i in range(len(range(min_matrix_bits, max_matrix_bits+1))):
    for j in range(len(range(min_flip_bits, max_flip_bits+1))):
        text = ax.text(j, i, f'{total_scores[i, j]:.6f}',
                       ha="center", va="center", color="w", fontsize=10)

# name the x and y axis
ax.set_xlabel("Number of Bit Flips", fontsize=18)
ax.set_ylabel("qpos_fd Matrix Index", fontsize=18)

ax.set_title(f"Difference in Final Joint Positions with Multiple Bit Flips for 15_15_10_10", fontsize=20)
fig.tight_layout()

plt.show()

plt.savefig('test.png',bbox_inches='tight')
