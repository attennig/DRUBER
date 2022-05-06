for ns in "20";
do
  for nd in "5" "10" "15" "20" "25";
  do
    for nu in "2" "4" "6" "8" "10" "12" "14" "16" "18" "20" "22" "24" "26" "28" "30";
    do
      python -m src.experiments.update_metrics -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 21 -out ./out -alg "GREEDY" -method "">>out.txt
      for method in "HC" "LB" "BFSOPT";
      do
        python -m src.experiments.update_metrics -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 21 -out ./out -alg "LOCALSEARCH" -method ${method}>>out.txt
      done;
    done;
  done;
done;
wait
