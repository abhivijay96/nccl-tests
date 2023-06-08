import matplotlib.pyplot as plt
import random
import sys
import os

random.seed(1)

label_cache = {}
def get_label(data_size):
    if data_size in label_cache:
        return label_cache[data_size]
    x = '{} B'.format(data_size)
    label_cache[data_size] = x
    if data_size > 10 ** 3 and data_size < 10 ** 6:
        data_size_readable = data_size / 1024
        x = '{} KB'.format(float(data_size_readable))
        label_cache[data_size] = x 
    elif data_size > 10 ** 6:
        data_size_readable = data_size / 1024 / 1024
        x = '{} MB'.format(float(data_size_readable))
        label_cache[data_size] = x
    return x

def get_x_ys(exp_type, min_gpus, max_gpus):
    xs = []
    ys = []
    labels = []
    file_name_template = '{}_{}.log'
    for i in range(min_gpus, max_gpus + 1):
        file_name = file_name_template.format(exp_type, i)
        x_series = []
        y_series = []
        log_idx = 1
        if not os.path.exists(file_name):
            continue
        with open(file_name, 'r') as log_file:
            for line in log_file:
                line = line.strip()
                if 'float' not in line:
                    continue
                parts = line.split()
                # 0 - data size
                # 7 - bus bw out of order
                # 11 - bus bw in order
                data_size = int(parts[0])
                out_bw = float(parts[7])
                in_bw = float(parts[11])
                x_series.append(log_idx)
                log_idx += 1
                y_series.append(out_bw)
        xs.append(x_series)
        ys.append(y_series)
        label = '{} GPUs'.format(i)

        labels.append(label)
    return xs, ys, labels

# Define x and y values
x = [1, 2, 3]
y = x

# Define a list of possible linestyles
linestyles = ['-', '--', '-.', ':', (0, (5, 10)), (0, (10, 10)), (0, (15, 10)), (0, (20, 10)), (0, (25, 10)), (0, (30, 10)), (0, (35, 10)), (0, (40, 10)), (0, (45, 10)), (0, (50, 10))]
colors = [(0.5, 0.2, 0.8), # RGB tuple
          '#FF0000', # hex string
          '0.75', # grayscale value
          'c', # single character shorthand
          'mediumseagreen', # X11/CSS4 color name
          'xkcd:sky blue', # xkcd color name
          'tab:orange', # Tableau color
          'C2'] # CN color spec

exp_type = sys.argv[1]
xs, ys, labels = get_x_ys(exp_type, 2, 8)
print(xs, ys, labels)
plt.rcParams["font.size"] = 12
# Create a figure and an axis object
fig, ax = plt.subplots(figsize=(12.8, 4.8))

for i in range(len(xs)):
    # Generate a random linestyle from the list
    linestyle = 'solid'
    # Plot the line with the color and linestyle and label it with i
    ax.plot(xs[i], ys[i], color=colors[i], linestyle=linestyle, label=labels[i], lw=3)

# Add a legend and put it outside the plot
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=8)
ax.set_ylabel('BW (GB/s)')
x_ticks = []
x_tick_labels = []
i = 96
tick_idx = 1

while tick_idx < len(xs[0]) + 1:
    x_ticks.append(tick_idx)
    x_tick_labels.append(get_label(i))
    i = i * 2
    tick_idx += 1

ax.set_xticks(x_ticks)
ax.set_xticklabels(x_tick_labels)
plt.xticks(rotation=30)
plt.tight_layout()
# Show the plot
plt.savefig('{}.png'.format(exp_type))
