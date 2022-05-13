for ns in "5";
do
  for nd in "1" "2" "3" "4";
  do
    for nu in "1" "2" "3" "4";
    do
      python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 11 -in ./in/MILP -out ./out -alg "MILP" -method "concurrent"&
    done;
  done;
done;
wait


