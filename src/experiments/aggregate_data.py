import json
import os

path = "./out"
#sizes = {"stations":[20], "deliveries":[5,10,15,20,25], "drones":[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]}
sizes = {"stations":[20], "drones":[5,10,15,20,25], "deliveries":[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]}
#sizes = {"stations":[5,10], "drones":[2,4,6], "deliveries":[2,4,6]}

seeds = [1,2,3,4,5]
#seeds = [1,2]

algorithms = ["GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]
#algorithms = ["MILP-concurrent","GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]

print("\n------------------------------------------------------")
out_file_name = f"{path}/results.csv"
with open(out_file_name, 'w') as fd:
    fd.write("nstations,ndeliveries,ndrones,algorithm,completion_time,mean_delivery_time,total_distance,consumed_energy,execution_time\n")

    for ns in sizes["stations"]:
        for nd in sizes["deliveries"]:
            for nu in sizes["drones"]:
                for algo in algorithms:
                    completion_time = 0
                    mean_delivery_time = 0
                    total_distance = 0
                    consumed_energy = 0
                    execution_time = 0
                    N = 0
                    for seed in seeds:
                        in_file = f"{path}/S{ns}D{nd}U{nu}/{seed}/{algo}/metrics.json"
                        if os.path.exists(in_file):
                            N += 1
                            with open(in_file) as jsondata:
                                data = json.load(jsondata)
                                print(data)
                            completion_time += data["completion_time"]
                            mean_delivery_time += data["mean_delivery_time"]
                            total_distance += data["total_distance"]
                            consumed_energy += data["consumed_energy"]
                            execution_time += data["execution_time"]

                    if N > 0:
                        completion_time = completion_time / N
                        mean_delivery_time = mean_delivery_time / N
                        total_distance = total_distance / N
                        consumed_energy = consumed_energy / N
                        execution_time = execution_time / N

                        fd.write(f"{ns},{nd},{nu},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n")
                        # print(f"{size},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n------------------------------------------------------")
