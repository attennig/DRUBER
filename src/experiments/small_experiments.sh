#for n in "6" "8" "10" "12";
#do
#    echo "generate size: ${n} "
#    python -m src.experiments.experiment -g -n ${n} -i_s 1 -e_s 4 -out ./out/small2 -alg NONE &
#    wait
#done;
#wait

for n in "6" "8" "10";
do
    for alg in "MILP" "GREEDY" "LOCALSEARCH";# "MILP" "GREEDY"
    do
        echo "run: ${alg} - size: ${n} "
        python -m src.experiments.experiment -n ${n} -i_s 1 -e_s 4 -out ./out/small2 -alg ${alg} >> ./out/small2/sollog.txt 2>>./out/small2/sollog.txt
    done;
done;
wait

#python -m src.experiments.plots -out ./out/small2 &
