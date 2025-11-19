import numpy as np # type: ignore
import decimate
import sys
import matplotlib.pyplot as plt # type: ignore

def main():
    obj_name = 'bunny'

    iter_max_list = [i for i in range(1, 11)]
    # results = [29.599887079130305, 39.11094979558298, 45.40275950375311, 50.057720712409704, 53.04558676002803, 55.346853591034886, 56.543109054338125, 57.54528177285765, 57.962685701898984, 58.547958602402595]
    results = []
    print(obj_name)

    for iter_max in iter_max_list:
        np.seterr(invalid = 'raise')
        model = decimate.Decimater()
        model.parse_file(f'example/{obj_name}.obj')

        with open(f'progressive__{obj_name}.obja', 'w') as output:
            _, _, compression_ratio = model.contract(output, obj_name, iter_max)
            results.append(compression_ratio)
        print('results: ', results)
    
    print('results: ', results)

    plt.plot(iter_max_list, results)          # Trace une ligne reliant les points
    plt.scatter(iter_max_list, results)       # Ajoute les points si tu veux les voir clairement

    plt.xlabel("number of iterations")
    plt.ylabel("compression ratio (%)")
    plt.title("Compression ratio based on the number of iterations")

    plt.show()

if __name__ == '__main__':
    main()