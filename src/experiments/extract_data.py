import json
import os

path = "./out"
sizes = {"stations":[20], "deliveries":[15], "drones":[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]}
#sizes = {"stations":[20], "drones":[5,10,15,20,25], "deliveries":[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]}
#sizes = {"stations":[5,10], "drones":[2,4,6], "deliveries":[2,4,6]}

seeds = range(1,51)
#seeds = [1,2]

algorithms = ["GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]
#algorithms = ["MILP-concurrent","GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]

print("\n------------------------------------------------------")
out_file_name = f"{path}/results.csv"
with open(out_file_name, 'w') as fd:

    fd.write("nstations,ndeliveries,ndrones,seed,algorithm,completion_time,mean_schedule_time,mean_flight_time,mean_swap_time,mean_load_unload_time,mean_waiting_time,mean_delivery_time,mean_schedule_distance,mean_schedule_energy,mean_number_swaps,drone_utilization_time,drone_utilization,total_number_parcel_handover,mean_number_parcel_handover,execution_time\n")
    for ns in sizes["stations"]:
        for nd in sizes["deliveries"]:
            for nu in sizes["drones"]:
                for seed in seeds:
                    for algo in algorithms:
                        in_file = f"{path}/S{ns}D{nd}U{nu}/{seed}/{algo}/metrics.json"
                        if os.path.exists(in_file):
                            with open(in_file) as jsondata:
                                data = json.load(jsondata)
                            fd.write(f'{ns},{nd},{nu},{seed},{algo},{data["completion_time"]},{data["mean_schedule_time"]},{data["mean_flight_time"]},{data["mean_swap_time"]},{data["mean_load_unload_time"]},{data["mean_waiting_time"]}, {data["mean_delivery_time"]},{data["mean_schedule_distance"]},{data["mean_schedule_energy"]},{data["mean_number_swaps"]},{data["drone_utilization_time"]},{data["drone_utilization"]},{data["total_number_parcel_handover"]},{data["mean_number_parcel_handover"]},{data["execution_time"]}\n')
                            #fd.write(f'{ns},{nd},{nu},{seed},{algo},{data["completion_time"]},{data["mean_delivery_time"]},{data["total_distance"]},{data["consumed_energy"]},{data["execution_time"]}\n')
                            #print(f"{size},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n------------------------------------------------------")
print("----------------------------------------")