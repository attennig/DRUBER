from argparse import ArgumentParser
import os
import csv
import matplotlib.pyplot as plt
def plot_metric(out_path_plots, metric, data):
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
    S = 20

    out_path = "./out/S20 deliveryfixed"
    assert os.path.isfile(f'{out_path}/results.csv')
    #sizes = {"stations": [5], "deliveries": [2, 4, 6], "drones": [2, 4, 6]}
    #seeds = [1, 2]
    #algorithms = ["MILP-concurrent", "GREEDY", "LOCALSEARCH-LB", "LOCALSEARCH-HC", "LOCALSEARCH-BFSOPT"]
    for D in [25]:
        out_path_plots = f"{out_path}/plots/S{S}D{D}"
        if not os.path.exists(out_path_plots): os.mkdir(out_path_plots)

        points = []
        with open(f'{out_path}/results.csv', mode='r') as csv_file:
            csv_dict = csv.DictReader(csv_file)
            for row in csv_dict:
                points.append(row)
                features = list(row.keys())[4:]
        print(features)

        for feature in features:
            data = {}
            for point in points:
                nstations = int(point["nstations"])
                ndrones = int(point["ndrones"])
                ndeliveries = int(point["ndeliveries"])

                if nstations != S or ndeliveries != D: continue
                #if nstations != S or ndrones != U: continue

                alg = point["algorithm"]
                value = point[feature]
                if alg not in data.keys(): data[alg] = {}
                if value is not None: data[alg][ndrones] = float(value)
                #if value is not None: data[alg][ndeliveries] = float(value)

            print(f"{feature}\n{data}")
            plot_metric(out_path_plots, feature, data)