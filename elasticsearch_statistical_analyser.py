import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

for i in range(5, 6):
    path = os.path.join('output', 'method_1_full.csv')
    df = pd.read_csv(path)
    df = df.loc[(df['Difficulty'] == i)]
    df = df.groupby(['Index', 'Asked for articles'])['Time in MS'].mean().reset_index()
    data_np = df.values  # converting to numpy
    unique_classes = np.unique(data_np[:, 0])
    data_dict = {}

    for u_class in unique_classes:
        class_data = data_np[data_np[:, 0] == u_class, :]  # masks out rows from class
        data_dict.update({u_class: {'x': class_data[:, 1], 'y': class_data[:, 2]}})
        plt.plot(data_dict[u_class]['x'], data_dict[u_class]['y'], label=u_class)
    plt.ylabel('Time in MS')
    plt.yscale('log')
    plt.xlabel('Asked for articles')
    plt.title('Simple query - English | method 1')
    plt.legend()
    save_path = os.path.join('output', 'method_1')
    plt.savefig(save_path)
    plt.show()


