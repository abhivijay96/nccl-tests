import matplotlib.pyplot as plt
import numpy as np

def get_xs_ys():
    with open('latency.log') as log_file:
        xs = []
        ys = []
        current_y = []
        for line in log_file:
            line = line.strip()
            # [PAIR]: 1 0
            if '[PAIR]' in line:
                print(line)
                parts = line.split()
                sender = parts[-2]
                receiver = parts[-1]
                pair_id = '{}->{}'.format(sender, receiver)
                xs.append(pair_id)
                if len(current_y) > 0:
                    ys.append(current_y)
                current_y = []
            if '[STAT]' in line:
                print(line)
                parts = line.split()
                time_val = float(parts[6])
                current_y.append(time_val)

        if len(current_y) > 0:
            ys.append(current_y)

    return xs, ys

xs, ys = get_xs_ys()
print(xs)
print(ys)

# calculate the average and percentiles of ys
avg = [np.mean(y) for y in ys]
p25 = [np.percentile(y, 25) for y in ys]
p75 = [np.percentile(y, 75) for y in ys]

# create a figure and an axes object
fig, ax = plt.subplots()

# plot the scatter plot with error bars on the axes object
ax.scatter(xs, avg)
ax.errorbar(xs, avg, yerr=[p25, p75], fmt='o')
ax.set_xlabel('GPUs')
ax.set_ylabel('Latency (us)')

plt.tight_layout()
plt.savefig('latency.png')