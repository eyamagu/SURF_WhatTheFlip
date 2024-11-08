#!/bin/bash

#put in mujoco_simulation

FD_INT=10;
FD_FRAC=10;
path='/root/jupyter-kernels/FPC2';

#matrix index
for n in {0..5};
do
  #flipbit index
	for m in {0..19};
	do
		#config change value in config to set where to bit flip and which value in the matrix
    		sed -i '15s/.*/const int INT_BITS_FD = '$FD_INT';/' include/config.hpp
    		sed -i '16s/.*/const int FRAC_BITS_FD = '$FD_FRAC';/' include/config.hp
    		sed -i '20s/.*/const int BIT_FLIP = '$m';/' include/config.hpp
		sed -i '21s/.*/const int MATRIX_VAL = '$n';/' include/config.hpp
		./scripts.sh panda
		#save data
		mkdir ${path}/data/exp/15_15_${FD_INT}_${FD_FRAC}_${n}_${m}
		cp -r ./exp/05-16/15_15_${FD_INT}_${FD_FRAC} ${path}/data/exp/15_15_${FD_INT}_${FD_FRAC}_${n}_${m}
	done
done
python3 scripts/heatmap_new.py
cp -r ./test.png ${path}

./scripts.sh panda
cp -r ./exp/05-16/15_15_${FD_INT}_${FD_FRAC} ${path}/normal
python3 scripts/heatmap_fp.py
cp -r ./test.png ${path}/normal
