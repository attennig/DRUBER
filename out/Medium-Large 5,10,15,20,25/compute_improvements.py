

with open('aggregate_results10.csv', mode='r') as in_file:
    content = in_file.read().splitlines()
CT_gr = 0
with open('aggregate_res_10d_out.csv', mode='w') as out_file:

    out_file.write(f"{content[0]},CT_reduction_perc,UT_increase_perc\n")

    for line_str in content[1:]:
        print(line_str)
        line = line_str.split(",")

        if line[1] == "GREEDY":
            CT_gr = float(line[2])
            UT_gr = float(line[3])
        CT_alg = float(line[2])
        UT_alg = float(line[3])
        new_line = f"{line_str},{100*(CT_gr-CT_alg)/CT_alg},{100*(UT_alg-UT_gr)/UT_gr}\n"
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
