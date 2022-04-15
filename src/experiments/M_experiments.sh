for n in "10" "12" "14" "16" "18" "20";
do
    echo "generate size: ${n} "
    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 6 -out ./out/M -alg NONE &
    wait
done;
wait

for n in "10" "12" "14" "16" "18" "20";
do
    for alg in "MILP" "GREEDY" "LOCALSEARCH-BFSOPT" "LOCALSEARCH-LB" "LOCALSEARCH-HC" ; #
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 6 -out ./out/M -alg ${alg}
    done;
done;
wait

