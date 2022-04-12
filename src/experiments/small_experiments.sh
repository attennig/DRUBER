for n in "6" "8" "10" "12";
do
    echo "generate size: ${n} "
    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 4 -out ./out/smallC -alg NONE &
    wait
done;
wait

for n in "6" "8" "10" "12";
do
    for alg in "MILP" "GREEDY" "LOCALSEARCH-BFSOPT" "LOCALSEARCH-LB" "LOCALSEARCH-HC" ;
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 5 -out ./out/smallC -alg ${alg}
    done;
done;
wait

