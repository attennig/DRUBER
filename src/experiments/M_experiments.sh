#for n in "20" "30" "40" "50" "60" "70" "80" "90";
#do
#    echo "generate size: ${n} "
#    python3 -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 6 -out ./out/M -alg NONE &
#    wait
#done;
#wait

for n in "20" "30" "40" "50" "60" "70" "80" "90";
do
    for alg in "GREEDY" "LOCALSEARCH-BFSOPT" "LOCALSEARCH-LB" "LOCALSEARCH-HC" ; #
    do
        echo "run: ${alg} - size: ${n} "
        python3 -m src.experiments.experiment -n ${n} -i_s 1 -e_s 6 -out ./out/M -alg ${alg}
    done;
done;
wait

