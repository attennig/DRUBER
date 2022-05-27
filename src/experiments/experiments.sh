for ns in "20";
do
  for nd in "15"; #"5" "10" "15" "20" "25";
  do
    for nu in "2" "4" "6" "8" "10" "12" "14" "16" "18" "20" "22" "24" "26" "28" "30";
    do
      #mkdir ./out/S${ns}D${nd}U${nu}
      #mkdir ./out/S${ns}D${nd}U${nu}/GREEDY
      python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 51 -in ./in/S${ns} -out ./out -alg "GREEDY">./out/S${ns}D${nd}U${nu}/GREEDY/out.txt 2>./out/S${ns}D${nd}U${nu}/GREEDY/err.txt &
      for method in "HC" "LB" "BFSOPT";
      do
        #mkdir ./out/S${ns}D${nd}U${nu}/LS${method}
        python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 51 -in ./in/S${ns}  -out ./out -alg "LOCALSEARCH" -method ${method}>./out/S${ns}D${nd}U${nu}/LS${method}/out.txt 2>./out/S${ns}D${nd}U${nu}/LS${method}/err.txt &
      done;
    done;
  done;
done;
wait


