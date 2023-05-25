import matplotlib.pyplot as plt
import random
import sys

random.seed(1)

def get_x_ys(exp_type, max_gpus):
    xs = []
    ys = []
    labels = []
    file_name_template = '{}_{}.log'
    for i in range(2, max_gpus + 1):
        file_name = file_name_template.format(exp_type, i)
        x_series = []
        y_series = []
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
                x = '{} B'.format(data_size)
                if data_size > 10 ** 3 and data_size < 10 ** 6:
                    data_size_readable = data_size / 1024
                    x = '{} KB'.format(float(data_size_readable))
                elif data_size > 10 ** 6:
                    data_size_readable = data_size / 1024 / 1024
                    x = '{} MB'.format(float(data_size_readable))
                x_series.append(x)
                y_series.append(out_bw)
        xs.append(x_series)
        ys.append(y_series)
        label = '{} nghbr'.format(i - 1)

        labels.append(label)
    return xs, ys, labels

# Define x and y values
x = [1, 2, 3]
y = x

# Define a list of possible linestyles
linestyles = ['-', '--', '-.', ':', (0, (5, 10)), (0, (10, 10)), (0, (15, 10)), (0, (20, 10)), (0, (25, 10)), (0, (30, 10)), (0, (35, 10)), (0, (40, 10)), (0, (45, 10)), (0, (50, 10))]

exp_type = sys.argv[1]
xs, ys, labels = get_x_ys(exp_type, 2)
print(xs, ys, labels)
plt.rcParams["font.size"] = 12
# Create a figure and an axis object
fig, ax = plt.subplots(figsize=(12.8, 4.8))

for i in range(len(xs)):
    # Generate a random color based on blue
    color = (0, random.random(), random.random())
    # Generate a random linestyle from the list
    linestyle = 'solid'
    # Plot the line with the color and linestyle and label it with i
    ax.plot(xs[i], ys[i], color=color, linestyle=linestyle, label=labels[i], lw=3)

# Add a legend and put it outside the plot
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=5)
ax.set_ylabel('BW (MB/s)')
plt.xticks(rotation=30)
plt.tight_layout()
# Show the plot
plt.savefig('{}.png'.format(exp_type))
