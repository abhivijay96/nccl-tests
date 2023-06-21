import matplotlib.pyplot as plt

# GPU 5/rx, link 8, 63626086 KB

def get_x_ys(file_name, gpu_id, direction):
    xs = []
    ys = []
    labels = []
    with open(file_name, 'r') as log_file:
        for line in log_file:
            if 'GPU {}'.format(gpu_id) in line and direction in line:
                line = line.strip()
                parts = line.split()
                parts[3] = parts[3].replace(',', '')
                link_id = int(parts[3])
                data_size = int(parts[4]) / 1024
                if len(xs) < link_id + 1:
                    print('Link: {}'.format(link_id))
                    xs.insert(link_id, [])
                    ys.insert(link_id, [])
                    labels.insert(link_id, 'Link: {}'.format(link_id))
                ys[link_id].append(data_size)
                xs[link_id].append(len(xs[link_id]) + 1)
    return xs, ys, labels

gpus = [i for i in range(8)]
directions = ['tx', 'rx']

for gpu in gpus:
    for direction in directions:
        xs, ys, labels = get_x_ys('gpu_bandwidth.log', gpu, 'tx')

        fig, ax = plt.subplots(figsize=(12.8, 4.8))

        for i in range(len(xs)):
            # Generate a random linestyle from the list
            linestyle = 'solid'
            # Plot the line with the color and linestyle and label it with i
            ax.plot(xs[i], ys[i], linestyle=linestyle, label=labels[i], lw=2)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=6)
        ax.set_ylabel('Data (MB)')
        plt.tight_layout()
        plt.savefig('nvlink_GPU{}_{}.png'.format(gpu, direction))
