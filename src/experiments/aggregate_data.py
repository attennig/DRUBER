import json


path = "./out"
sizes = {"stations":[5,10], "deliveries":[2,4,6], "drones":[2,4,6]}
seeds = [1,2]
algorithms = ["GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]

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
                    for seed in seeds:
                        in_file = f"{path}/S{ns}D{nd}U{nu}/{seed}/{algo}/metrics.json"
                        with open(in_file) as jsondata:
                            data = json.load(jsondata)
                            print(data)
                        completion_time += data["completion_time"]/len(seeds)
                        mean_delivery_time += data["mean_delivery_time"]/len(seeds)
                        total_distance += data["total_distance"]/len(seeds)
                        consumed_energy += data["consumed_energy"]/len(seeds)
                        execution_time += data["execution_time"]/len(seeds)

                    fd.write(f"{ns},{nd},{nu},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n")
                    # print(f"{size},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n------------------------------------------------------")
