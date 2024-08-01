#!/bin/bash
#script to run the container and copy the script above to inside the scripts

#path to where you are storing the other files
path='/root/jupyter-kernels/FPC2';

module load apptainer


apptainer exec --fakeroot --writable-tmpfs fpc.sif bash -c "
  cd /mujoco_simulation &&
  cp -r ${path}/fix.sh ./ &&
  ./fix.sh 
  cp -r ${path}/flipbit.sh ./ &&
  ./flipbit.sh
"
