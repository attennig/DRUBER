from argparse import ArgumentParser
import os
import csv
import matplotlib.pyplot as plt
def plot_metric(metric, data):
    plt.clf()
    for alg in data.keys():
        N, V = [], []
        for key, value in sorted(data[alg].items()):
            N.append(key)
            V.append(value)
        print(f"{N},{V}")
        plt.plot(N,V)

    plt.gca().legend(tuple(data.keys()))
    plt.title(metric)
    plt.savefig(f"{out_path_plots}/{metric}.png")


if __name__ == "__main__":

    parser = ArgumentParser()

    # MANDATORY
    parser.add_argument("-out", dest='out_path', action="store", type=str,
                        help="path to output folder")

    args = parser.parse_args()

    out_path = args.out_path

    assert os.path.isfile(f'{out_path}/results.csv')
    out_path_plots = f"{out_path}/plots"
    if not os.path.exists(out_path_plots): os.mkdir(out_path_plots)

    points = []
    with open(f'{out_path}/results.csv', mode='r') as csv_file:
        csv_dict = csv.DictReader(csv_file)
        for row in csv_dict:
            points.append(row)

            features = list(row.keys())[2:]
    print(features)

    for feature in features:
        data = {}
        for point in points:
            n = int(point["size"])
            alg = point["algorithm"]
            value = point[feature]
            if alg not in data.keys(): data[alg] = {}
            data[alg][n] = float(value)

        plot_metric(feature, data)
