# Code for creating a progressive obja file for different iteration values
# and saving a figure that shows the compression ratio per iteration

import numpy as np
import decimate
import sys
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) == 2:
        obj_name = sys.argv[1]
    else :
        # Choose the model here
        obj_name = 'bunny'

    iter_max_list = [i for i in range(1, 11)]
    results = []
    cpt = 1
    for iter_max in iter_max_list:
        print(f'Computing the compression ratio n°{cpt} out of 10:')
        cpt += 1
        np.seterr(invalid = 'raise')
        model = decimate.Decimater()
        model.parse_file(f'example/{obj_name}.obj')

        with open(f'progressive_models/progressive__{obj_name}.obja', 'w') as output:
            _, _, compression_ratio = model.contract(output, obj_name, iter_max)
            results.append(compression_ratio)
    

    plt.plot(iter_max_list, results)         
    plt.scatter(iter_max_list, results)       

    plt.xlabel("number of iterations")
    plt.ylabel("compression ratio (%)")
    plt.title("Compression ratio based on the number of iterations")

    plt.show()

if __name__ == '__main__':
    main()