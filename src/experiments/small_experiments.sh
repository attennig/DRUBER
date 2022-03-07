for n in "5" "6" "7" "8" "9";
do
    echo "generate size: ${n} "
    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 6 -out ./out/small -alg NONE
    wait
done;
wait

for n in "5" "6" "7" "8" "9";
do
    for alg in "MILP" "GREEDY";
    do
        echo "run: ${alg} - size: ${n} "
        python -m src.experiments.experiment -n ${n} -i_s 1 -e_s 6 -out ./out/small -alg ${alg}
    done;
done;
wait

python -m src.experiments.plots -out ./out/small
