#!/bin/bash
#script to run the container and copy the script above to inside the scripts

#dont know if I need this?
#cd /home/eyamaguchi26/root/jupyter-kernels/FPC6
folder='FPC2'

module load apptainer


apptainer exec --fakeroot --writable-tmpfs fpc.sif bash -c "

  cd /mujoco_simulation &&
  cp -r /root/jupyter-kernels/$folder/fix.sh ./ &&
  ./fix.sh 
  cp -r /root/jupyter-kernels/$folder/flipbit.sh ./ &&
  ./flipbit.sh
"
