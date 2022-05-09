for ns in "20";
do
  for nd in "15"; #"5" "10" "15" "20" "25";
  do
    for nu in "2" "4" "6" "8" "10" "12" "14" "16" "18" "20" "22" "24" "26" "28" "30";
    do
      python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 11 -in ./in/S${ns} -out ./out -alg "GREEDY"&
      for method in "HC" "LB" "BFSOPT";
      do
        python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 11 -in ./in/S${ns}  -out ./out -alg "LOCALSEARCH" -method ${method}&
      done;
    done;
  done;
done;
wait