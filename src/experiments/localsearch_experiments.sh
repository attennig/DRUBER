for n in "15" "20" "25" "30" "35" "40" "45" "50";
do
    echo "generate size: ${n}"
    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 5 -out ./out/localsearch -alg NONE &
    wait
done;
wait

for n in "15" "20" "25" "30" "35" "40" "45" "50";
do
    for alg in "GREEDY" "LOCALSEARCH-BFSOPT" "LOCALSEARCH-LB" "LOCALSEARCH-HC" ;
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 5 -out ./out/localsearch -alg ${alg}
    done;
done;
wait
