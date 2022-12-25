import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = './output'

width = 300
height = 200

def main():
    camera = np.array([0, 0, 1])
    ratio = float(width) / height
    screen = {
        'LEFT': -1,
        'TOP': 1 / ratio,
        'RIGHT': 1,
        'BOTTOM': -1 / ratio,
    }

    image = np.zeros((height, width, 3))
    for i, y in enumerate(np.linspace(screen['TOP'], screen['BOTTOM'], height)):
        for j, x in enumerate(np.linspace(screen['LEFT'], screen['RIGHT'], width)):   
            pass
            # image[i, j] = ...

    plt.imsave(f'{OUTPUT_DIR}/image.png', image)

if __name__ == "__main__":
    main()

