#for n in "15" "20" "25" "30"; # "35" "40" "45" "50";
#do
#    echo "generate size: ${n}"
#    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 4 -out ./out/largeLOCAL -alg NONE &
#    wait
#done;
#wait

for n in "15" "20" "25" "30"; # "35" "40" "45" "50";
do
    for alg in "LOCALSEARCH-BFSOPT";# "GREEDY" "LOCALSEARCH-HC" ;
    do
        echo "run: ${alg} - size: ${n} "
        python -m src.experiments.experiment -n ${n} -i_s 1 -e_s 4 -out ./out/largeLOCAL -alg ${alg}
    done;
done;
wait