mkdir ./out/Small/S5D2U2
python3 -m src.experiments.simulate -ns 5 -nd 2 -nu 2 -i_s 9 -e_s 10 -in ./in/MILPexp -out ./out/Small -alg "MILP" -method "concurrent">./out/Small/S5D2U2MILPout.txt 2>./out/Small/S5D2U2MILPerr.txt &
python3 -m src.experiments.simulate -ns 5 -nd 2 -nu 2 -i_s 9 -e_s 10 -in ./in/MILPexp -out ./out/Small -alg "GREEDY" >./out/Small/S5D2U2GREEDYout.txt 2>./out/Small/S5D2U2GREEDYerr.txt &
for method in "HC" "LB" "BFSOPT";
    do
      python3 -m src.experiments.simulate  -ns 5 -nd 2 -nu 2 -i_s 9 -e_s 10 -in ./in/MILPexp -out ./out/Small -alg "LOCALSEARCH" -method ${method}>./out/Small/S5D2U2LOCALSEARCH${method}out.txt 2>./out/Small/S5D2U2LOCALSEARCH${method}err.txt &
    done;


mkdir ./out/Small/S5D2U3
python3 -m src.experiments.simulate -ns 5 -nd 2 -nu 3 -i_s 10 -e_s 11 -in ./in/MILPexp -out ./out/Small -alg "MILP" -method "concurrent">./out/Small/S5D2U3MILPout.txt 2>./out/Small/S5D2U3MILPerr.txt &
python3 -m src.experiments.simulate -ns 5 -nd 2 -nu 3 -i_s 10 -e_s 11 -in ./in/MILPexp -out ./out/Small -alg "GREEDY">./out/Small/S5D2U3GREEDYout.txt 2>./out/Small/S5D2U3GREEDYerr.txt &
for method in "HC" "LB" "BFSOPT";
    do
      python3 -m src.experiments.simulate -ns 5 -nd 2 -nu 3 -i_s 10 -e_s 11  -in ./in/MILPexp -out ./out/Small -alg "LOCALSEARCH" -method ${method}>./out/Small/S5D2U3LOCALSEARCH${method}out.txt 2>./out/Small/S5D2U3LOCALSEARCH${method}err.txt &
    done;


mkdir ./out/Small/S5D3U3
python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 3 -i_s 11 -e_s 12 -in ./in/MILPexp -out ./out/Small -alg "MILP" -method "concurrent">./out/Small/S5D3U3MILPout.txt 2>./out/Small/S5D3U3MILPerr.txt &
python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 3 -i_s 11 -e_s 12 -in ./in/MILPexp -out ./out/Small -alg "GREEDY">./out/Small/S5D3U3GREEDYout.txt 2>./out/Small/S5D3U3GREEDYerr.txt &
for method in "HC" "LB" "BFSOPT";
    do
      python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 3 -i_s 11 -e_s 12  -in ./in/MILPexp -out ./out/Small -alg "LOCALSEARCH" -method ${method}>./out/Small/S5D3U3LOCALSEARCH${method}out.txt 2>./out/Small/S5D3U3LOCALSEARCH${method}err.txt &
    done;



mkdir ./out/Small/S5D3U4
python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 4 -i_s 12 -e_s 13 -in ./in/MILPexp -out ./out/Small -alg "MILP" -method "concurrent">./out/Small/S5D3U4MILPout.txt 2>./out/Small/S5D3U4MILPerr.txt &
python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 4 -i_s 12 -e_s 13 -in ./in/MILPexp -out ./out/Small -alg "GREEDY">./out/Small/S5D3U4GREEDYout.txt 2>./out/Small/S5D3U4GREEDYerr.txt &
for method in "HC" "LB" "BFSOPT";
    do
      python3 -m src.experiments.simulate -ns 5 -nd 3 -nu 4 -i_s 12 -e_s 13 -in ./in/MILPexp -out ./out/Small -alg "LOCALSEARCH" -method ${method}>./out/Small/S5D3U4LOCALSEARCH${method}out.txt 2>./out/Small/S5D3U4LOCALSEARCH${method}err.txt &
    done;


mkdir ./out/Small/S6D3U4
python3 -m src.experiments.simulate -ns 6 -nd 3 -nu 4 -i_s 13 -e_s 14 -in ./in/MILPexp -out ./out/Small -alg "MILP" -method "concurrent">./out/Small/S6D3U4MILPout.txt 2>./out/Small/S6D3U4MILPerr.txt &
python3 -m src.experiments.simulate -ns 6 -nd 3 -nu 4 -i_s 13 -e_s 14 -in ./in/MILPexp -out ./out/Small -alg "GREEDY">./out/Small/S6D3U4GREEDYout.txt 2>./out/Small/S6D3U4GREEDYerr.txt &
for method in "HC" "LB" "BFSOPT";
    do
      python3 -m src.experiments.simulate -ns 6 -nd 3 -nu 4 -i_s 13 -e_s 14 -in ./in/MILPexp -out ./out/Small -alg "LOCALSEARCH" -method ${method}>./out/Small/S6D3U4LOCALSEARCH${method}out.txt 2>./out/Small/S6D3U4LOCALSEARCH${method}err.txt &
    done;
wait