import matplotlib.pyplot as plt

# GPU 5/rx, link 8, 63626086 KB

def get_x_ys(file_name):
    xs = []
    ys = []
    txs = []
    rxs = []
    labels = []
    num_links_on_switch = 16

    with open(file_name, 'r') as log_file:
        for line in log_file:
            if 'link' in line:
                line = line.strip()
                parts = line.split()
                parts[3] = parts[3].replace(',', '')
                link_id = int(parts[3])
                switch_id = int(link_id / 2)
                data_size = int(parts[4]) / 1024
                if len(xs) < switch_id + 1:
                    print('Switch: {}'.format(switch_id))
                    xs.insert(switch_id, [])
                    ys.insert(switch_id, [])
                    txs.insert(switch_id, [])
                    rxs.insert(switch_id, [])
                    labels.insert(switch_id, 'Switch: {}'.format(switch_id + 1))
                if 'tx' in line:
                    txs[switch_id].append(data_size)
                if 'rx' in line:
                    rxs[switch_id].append(data_size)
     
    for switch_id in range(len(txs)):
        prev_tx_sum = 0
        prev_rx_sum = 0
        for idx in range(int(len(txs[switch_id]) / num_links_on_switch)):
            offset = idx * num_links_on_switch
            total_tx = sum(txs[switch_id][offset: offset + num_links_on_switch]) - prev_tx_sum
            total_rx = sum(rxs[switch_id][offset: offset + num_links_on_switch]) - prev_rx_sum
            if total_tx == 0:
                # continue
                total_tx = 1
                total_rx = 0
            ys[switch_id].append(total_rx / total_tx)
            # ys[switch_id].append(total_tx)
            xs[switch_id].append(len(xs[switch_id]) + 1)
            prev_tx_sum = total_tx + prev_tx_sum
            prev_rx_sum = total_rx + prev_rx_sum
    return xs, ys, labels


xs, ys, labels = get_x_ys('gpu_bandwidth.log')
fig, ax = plt.subplots(figsize=(12.8, 4.8))

for i in range(len(xs)):
    # Generate a random linestyle from the list
    linestyle = 'solid'
    # Plot the line with the color and linestyle and label it with i
    ax.plot(xs[i], ys[i], linestyle=linestyle, label=labels[i], lw=2)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=6)
ax.set_ylabel('Rx / Tx')
# ax.set_ylim((0.8, 1.2))
plt.tight_layout()
plt.savefig('nvswitch.png')
