for n in "6" "8" "10" "12" "14" "16";
do
    echo "generate size: ${n} "
    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 6 -out ./out/milpexp -alg NONE &
    wait
done;
wait
for n in "6" "8" "10" "12" "14" "16";
do
    for method in "primal" "dual" "barrier" "concurrent";
    do
        echo "run: ${alg} - size: ${n} "
        python -m src.experiments.experiment -n ${n} -i_s 1 -e_s 6 -out ./out/milpexp -alg MILP -method ${method} &
    done;
done;
wait

python -m src.experiments.plots -out ./out/milpexp &
