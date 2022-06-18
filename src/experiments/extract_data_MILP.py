import json
import os

path = "./out/Small"

instances = [
    (5,2,2,9),
    (5,2,3,10),
    (5,3,3,11),
    (5,3,4,12),
    (6,3,4,13)
]

algorithms = ["MILP-primal","GREEDY","LOCALSEARCH-LB","LOCALSEARCH-HC","LOCALSEARCH-BFSOPT"]

print("\n------------------------------------------------------")
out_file_name = f"{path}/results.csv"
with open(out_file_name, 'w') as fd:

    fd.write("nstations,ndeliveries,ndrones,seed,algorithm,completion_time,mean_schedule_time,mean_flight_time,mean_swap_time,mean_load_unload_time,mean_waiting_time,mean_delivery_time,mean_schedule_distance,mean_schedule_energy,mean_number_swaps,drone_utilization_time,drone_utilization,total_number_parcel_handover,mean_number_parcel_handover,execution_time\n")
    for ns, nd, nu, seed in instances:

        for algo in algorithms:
            in_file = f"{path}/S{ns}D{nd}U{nu}/{seed}/{algo}/metrics.json"
            if os.path.exists(in_file):
                with open(in_file) as jsondata:
                    data = json.load(jsondata)
                fd.write(f'{ns},{nd},{nu},{seed},{algo},{data["completion_time"]},{data["mean_schedule_time"]},{data["mean_flight_time"]},{data["mean_swap_time"]},{data["mean_load_unload_time"]},{data["mean_waiting_time"]}, {data["mean_delivery_time"]},{data["mean_schedule_distance"]},{data["mean_schedule_energy"]},{data["mean_number_swaps"]},{data["drone_utilization_time"]},{data["drone_utilization"]},{data["total_number_parcel_handover"]},{data["mean_number_parcel_handover"]},{data["execution_time"]}\n')
                #fd.write(f'{ns},{nd},{nu},{seed},{algo},{data["completion_time"]},{data["mean_delivery_time"]},{data["total_distance"]},{data["consumed_energy"]},{data["execution_time"]}\n')
                #print(f"{size},{algo},{completion_time},{mean_delivery_time},{total_distance},{consumed_energy},{execution_time}\n------------------------------------------------------")
print("----------------------------------------")