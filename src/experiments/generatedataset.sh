for ns in "5" "10";
do
  for nd in "2" "4" "6";
  do
    for nu in "2" "4" "6" ;
    do
      python -m src.experiments.instancegenerator -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 3 -out ./out &
      wait
    done;
  done;
done;
wait
