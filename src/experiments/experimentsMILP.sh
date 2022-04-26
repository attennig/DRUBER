
for nd in "4" "6";
do
  for nu in "4" "6" ;
  do
    python3 -m src.experiments.simulate -ns 10 -nd ${nd} -nu ${nu} -i_s 1 -e_s 3 -out ./out -alg "MILP" -method "concurrent"&
  done;
done;
python3 -m src.experiments.simulate -ns 10 -nd 6 -nu 2 -i_s 1 -e_s 3 -out ./out -alg "MILP" -method "concurrent"&
wait

