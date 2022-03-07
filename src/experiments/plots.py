from argparse import ArgumentParser
import os
import csv
import matplotlib.pyplot as plt

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

    print(points)

    ct_MILP = {}
    ct_GREEDY = {}
    et_MILP = {}
    et_GREEDY = {}
    for point in points:
        n = point["size"]
        alg = point["algorithm"]
        mct = point["mean completion time"]
        met = point["mean execution time"]
        if alg == "MILP":
            ct_MILP[n] = float(mct)
            et_MILP[n] = float(met)
        if alg == "GREEDY":
            ct_GREEDY[n] = float(mct)
            et_GREEDY[n] = float(met)



    # blue squares and green triangles
    plt.plot(list(ct_MILP.keys()), list(ct_MILP.values()), 'gs', list(ct_GREEDY.keys()), list(ct_GREEDY.values()), 'r^')
    plt.gca().legend(('MILP', 'GREEDY'))
    plt.title("Mean Completion Time")
    plt.savefig(f"{out_path_plots}/mct.png")
    plt.show()

    plt.plot(list(et_MILP.keys()), list(et_MILP.values()), 'gs', list(et_GREEDY.keys()), list(et_GREEDY.values()), 'r^')
    plt.gca().legend(('MILP', 'GREEDY'))
    plt.title("Mean Execution Time")
    plt.savefig(f"{out_path_plots}/met.png")
    plt.show()

