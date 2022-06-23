

with open('results.csv', mode='r') as in_file:
    content = in_file.read().splitlines()
CT_gr = 0
with open('results_out.csv', mode='w') as out_file:
    # completion time
    # CT reduction perc
    # mean numbero of parcel handover
    # drone utilization
    # drone utilization time
    # UT increase perc
    # exec time
    # mean drone energy consumption
    # mean number of battery replecement
    # ,,mean_schedule_time 6 ,mean_flight_time 7 ,mean_swap_time 8,mean_load_unload_time9,mean_waiting_time10,mean_delivery_time11,mean_schedule_distance12,,,total_number_parcel_handover17,mean_number_parcel_handover,execution_time,perc_flight_time,perc_swap_time,perc_load_unload_time,perc_waiting_time,diff_demand-cons

    out_file.write(f"nstations,ndeliveries,ndrones,seed,algorithm,completion_time,mean_schedule_energy,mean_number_swaps,drone_utilization_time,drone_utilization,mean_number_parcel_handover,execution_time,CT_reduction_perc,UT_increase_perc\n")
    #                 0         1            2      3      4            5         13                    14                 15                      16              18                               19


    #line = content[0].split(",")
    #print(f"{','.join(map(str,line[:6]))},{','.join(map(str,line[13:17]))},{','.join(map(str,line[18:20]))}")
    for line_str in content[1:]:

        line = line_str.split(",")
        if line[4] == "GREEDY":
            CT_gr = float(line[5])
            UT_gr = float(line[15])
            print(f"{CT_gr}, {UT_gr}")
        CT_alg = float(line[5])
        UT_alg = float(line[15])

        new_line = f"{','.join(map(str,line[:6]))},{','.join(map(str,line[13:17]))},{','.join(map(str,line[18:20]))},{100*(CT_alg-CT_gr)/CT_gr},{100*(UT_alg-UT_gr)/UT_gr}\n"
        out_file.write(new_line)

'''

        line = in_file.readline()
        out_file.write(line)
        while line != "":
            line = in_file.readline()
            print(line.split(","))

        #if row["algorithm"] == "GREEDY": CT_gr = row['completion_time']
        #new_row['comletion_time'] = row['completion_time']/CT_gr
        #new_row['mean_flight_time'] = row['mean_flight_time']/CT_gr
        #new_row['mean_swap_time'] = row['mean_swap_time']/CT_gr
        #new_row['mean_load_unload_time'] = row['mean_load_unload_time']/CT_gr
        #new_row['mean_waiting_time'] = row['mean_waiting_time']/CT_gr
        #csv_writer.writerow(new_row)'''
