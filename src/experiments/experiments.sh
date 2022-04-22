for ns in "5" "10";
do
  for nd in "2" "4" "6";
  do
    for nu in "2" "4" "6" ;
    do
      #python -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 3 -out ./out -alg "MILP" -method "concurrent"
      python -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 3 -out ./out -alg "GREEDY" -method ""&
      for method in "HC" "LB" "BFSOPT";
      do
        python -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 3 -out ./out -alg "LOCALSEARCH" -method ${method}&
      done;
    done;
  done;
done;
wait
