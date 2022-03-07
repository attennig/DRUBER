for n in "5" "6" "7" "8" "9" "10";
do
    echo "generate size: ${n} "
    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 6 -out ./out/small -alg NONE &
    wait
done;
wait

for n in "5" "6" "7" "8" "9" "10";
do
    for alg in "MILP" "GREEDY";
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 6 -out ./out/small -alg ${alg} &
    done;
done;
wait

python3 -m src.experiments.plots -out ./out/small &
