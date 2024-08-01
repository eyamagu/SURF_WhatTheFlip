#!/bin/bash
#script to run inside the container and fix everything

CURR_PATH='/root/jupyter-kernels/FPC2'
FD_INT=5;
FD_FRAC=8;


git pull
cd scripts
touch __init__.py
sed -i '9a #include <filesystem>' whole_test.py
sed -i "84a plt.savefig('test_nm.png')" heatmap_var.py
sed -i '50s/.*/fig, ax = plt.subplots(figsize = (8,8))/' heatmap_var.py
sed -i '85a def calculate_score_from_folder(gravity_int_bits, gravity_frac_bits, fd_int_bits, fd_frac_bits, matrix_index, flip_bit):\
\    folder = f'\''{NEW_DIRECTORY}/{gravity_int_bits}_{gravity_frac_bits}_{fd_int_bits}_{fd_frac_bits}_{matrix_index}_{flip_bit}/{gravity_int_bits}_{gravity_frac_bits}_{fd_int_bits}_{fd_frac_bits}'\''\
\    print("reading from ", folder)\
\    try:\
\        data = pd.read_csv(f'\''{folder}/data.csv'\'')\
\    except Exception as e:\
\        print(e)\
\        return float('\''inf'\'') # there may be an error because the df is empty\
\    # is data empty\
\    if data.empty:\
\        return float('\''inf'\'')\
\    print('\''data read'\'')\
\    # calculate the score and print the sum\
\    data['\''score'\''] = data.apply(calculate_score, axis=1)\
\    return data['\''score'\''].sum()/len(data)' score.py
sed -i "9a NEW_DIRECTORY = '${CURR_PATH}/data/exp'" score.py

cp -r ${CURR_PATH}/heatmap_new.py ./
cp -r ${CURR_PATH}//heatmap_fp.py ./
cp -r ${CURR_PATH}//score_fp.py ./
cp -r ${CURR_PATH}//score_byM.py ./

cd ..

#add include <filesystem>
cd include
sed -i '672i\
void bitflip(int bitPosition) {\
    std::cout << "Raw value before bit flip: " << raw_ << std::endl;\
    if (bitPosition >= 0 && bitPosition < (INT_BITS+FRAC_BITS)) {\
        raw_ ^= (1 << bitPosition);\
        std::cout << "Raw value after bit flip: " << raw_ << std::endl;\
    } else {\
        std::cerr << "Bit position out of range" << std::endl;\
    }\
}\
' FixedPoint/fixed_point.hpp
sed -i '3a #include <filesystem>' config.hpp
sed -i '6a #include <filesystem>' pinocchio_plus/aba.hxx

#add values to config
sed -i '19a const int BIT_FLIP = 0;\' config.hpp
sed -i '20a const int MATRIX_VAL = 0;\' config.hpp

cd ..

#add lines to trajectory_tracking.cc
cd src
#The line specification 177 can be changed to 175 to flip bits for qpos_gravity, qvel_gravity, qacc_gravity

#flips one bit at index BIT_FLIP
# sed -i '177i\
#     if(count == 0){\
#         for(int i = 0; i < BIT_FLIP; ++i) {\
#             std::cout << "Value before flipbit: " << qpos_fd(MATRIX_VAL,0);\
#             qpos_fd(MATRIX_VAL,0).bitflip(i);\
#             std::cout << "Value after flipbit: " << qpos_fd(MATRIX_VAL,0);\
#         }\
#         count++;\
#     }\
# ' trajectory_tracking.cc


#randomly flips BIT_FLIP number of bits at the beginning
sed -i '177i\
if(count == 0){\
    std::cout << "Value before flipbit: " << qpos_fd(MATRIX_VAL,0);\
    std::vector<int> bitPositions('$FD_INT' + '$FD_FRAC');\
    std::iota(bitPositions.begin(), bitPositions.end(), 0); // Fill with 0, 1, 2, ..., 19\
\
    // Randomly shuffle the list\
    std::random_device rd;  // Seed for the random number engine\
    std::mt19937 g(rd());   // Mersenne Twister pseudo-random generator\
    std::shuffle(bitPositions.begin(), bitPositions.end(), g);\
\
    // Flip the first BIT_FLIP bits\
    for (int i = 0; i < BIT_FLIP; ++i) {\
        int pos = bitPositions[i];\
        qpos_fd(MATRIX_VAL, 0).bitflip(pos);\
    }\
    std::cout << "Value after flipbit: " << qpos_fd(MATRIX_VAL,0);\
    count++;\
}' trajectory_tracking.cc
sed -i '9i\ int count = 0;' trajectory_tracking.cc
sed -i '2i \ 
        #include <algorithm>\
        #include <iostream>\
        #include <random>\
        #include <vector>\
' trajectory_tracking.cc
cd ..
