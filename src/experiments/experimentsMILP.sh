for ns in "5";
do
  for nd in "2";
  do
    for nu in "2" "3" "4";
    do
      mkdir ./out/S${ns}D${nd}U${nu}

      mkdir ./out/S${ns}D${nd}U${nu}/MILP
      python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 5 -in ./in/S${ns} -out ./out -alg "MILP" -method "concurrent">./out/S${ns}D${nd}U${nu}/MILP/out.txt 2>./out/S${ns}D${nd}U${nu}/MILP/err.txt &

      mkdir ./out/S${ns}D${nd}U${nu}/GREEDY
      python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 5 -in ./in/S${ns} -out ./out -alg "GREEDY">./out/S${ns}D${nd}U${nu}/GREEDY/out.txt 2>./out/S${ns}D${nd}U${nu}/GREEDY/err.txt &

      for method in "HC" "LB" "BFSOPT";
      do
        mkdir ./out/S${ns}D${nd}U${nu}/LS${method}
        python3 -m src.experiments.simulate -ns ${ns} -nd ${nd} -nu ${nu} -i_s 1 -e_s 5 -in ./in/S${ns}  -out ./out -alg "LOCALSEARCH" -method ${method}>./out/S${ns}D${nd}U${nu}/LS${method}/out.txt 2>./out/S${ns}D${nd}U${nu}/LS${method}/err.txt &
      done;
    done;
  done;
done;
wait