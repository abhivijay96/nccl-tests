import matplotlib.pyplot as plt
import numpy as np
import sys

data_size = sys.argv[1]
data_size_mb = float(data_size)

def get_xs_ys():
    with open('latency_{}.log'.format(data_size)) as log_file:
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
                time_val = float(parts[5])
                current_y.append((data_size_mb / 1024) * 10**6 / time_val)

        if len(current_y) > 0:
            ys.append(current_y)

    return xs, ys

xs, ys = get_xs_ys()
print(xs)
print(ys)

for y in ys:
    y.sort()

# calculate the average and percentiles of ys
avg = [round(np.percentile(y, 50), 2) for y in ys]
p25 = [np.percentile(y, 25) for y in ys]
p75 = [np.percentile(y, 75) for y in ys]

print(xs)
print(avg)
print(p25)
print(p75)

# create a figure and an axes object
fig, ax = plt.subplots(figsize=(15.8, 4.8))

# plot the scatter plot with error bars on the axes object
ax.scatter(xs, avg)
ax.fill_between(xs, p25, p75, color='blue', alpha=0.2)
ax.set_xlabel('GPUs')
plt.xticks(rotation=270)
plt.ylim((100, 280))
ax.set_ylabel('BW (GB/s)')

plt.tight_layout()
plt.savefig('bw_{}MB.png'.format(data_size))