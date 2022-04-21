#for n in "100" "150" "200" "250" "300" "400" "500";
#do
#    echo "generate size: ${n} "
#    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 2 -out ./out/L -alg NONE &
#    wait
#done;
#wait

for n in "100" "150" "200" "250" "300" "400" "500";
do
    for alg in "GREEDY" "LOCALSEARCH-LB" "LOCALSEARCH-HC" ; #"LOCALSEARCH-BFSOPT"
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 2 -out ./out/L -alg ${alg}
    done;
done;
wait

