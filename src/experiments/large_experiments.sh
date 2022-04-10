for n in "15" "20" "25" "30" "35" "40" "45" "50";
do
    echo "generate size: ${n} "
    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 10 -out ./out/large -alg NONE &
    wait
done;
wait

for n in "15" "20" "25" "30" "35" "40" "45" "50";
do
    for alg in "GREEDY" "LOCALSEARCH";
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 10 -out ./out/large -alg ${alg}
    done;
done;
wait