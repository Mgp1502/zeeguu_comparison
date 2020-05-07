import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


path = os.path.join('output', 'test_1.csv')
df = pd.read_csv(path)
df = df.groupby(['Index', 'Asked for articles'])['Time in MS'].mean().reset_index()
data_np = df.values  # converting to numpy
unique_classes = np.unique(data_np[:, 0])
data_dict = {}

# mysql Fulltext: Red
# mysql: Green
# elastic: Blue
colors = ['red', 'green', 'blue', 'red', 'green', 'blue', 'red', 'green', 'blue']
# 1000K: '-'
# 100K: '-.'
# 10K: ':'
linestyles = ['-', '-', '-', '-.', '-.', '-.', ':', ':', ':']

i = 0
for u_class in unique_classes:
    class_data = data_np[data_np[:, 0] == u_class, :]  # masks out rows from class
    data_dict.update({u_class: {'x': class_data[:, 1], 'y': class_data[:, 2]}})
    plt.plot(data_dict[u_class]['x'], data_dict[u_class]['y'], label=u_class, linestyle=linestyles[i], color=colors[i])
    i = i+1
plt.ylabel('Time in MS')
plt.yscale('log')
plt.xlabel('Asked for articles')
plt.title('Simple query - English | Only Topics | Single user')
plt.legend(bbox_to_anchor=(1, 1))
save_path = os.path.join('output', 'topics')
plt.savefig(save_path, bbox_inches='tight')
plt.show()



