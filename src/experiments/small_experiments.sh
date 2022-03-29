for n in "5" "6" "7";
do
    echo "generate size: ${n} "
    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 2 -out ./out/small2 -alg NONE &
    wait
done;
wait

for n in "5" "6" "7";
do
    for alg in "MILP" "GREEDY" "LOCALSEARCH";
    do
        echo "run: ${alg} - size: ${n} "
        python -m src.experiments.experiment -n ${n} -i_s 1 -e_s 2 -out ./out/small2 -alg ${alg} &
    done;
done;
wait

python -m src.experiments.plots -out ./out/small2 &
