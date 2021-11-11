\ Model pathplanner
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  delta_1 + delta_2
Subject To
 c1_1,1,1: x_1,1,1 = 1
 c2_1,2: x_1,1,2 = 1
 c3_1: x_1,1,1 + x_1,1,2 >= 1
 c4_1: delta_1 + x_1,1,1 >= 1
 c4_2: delta_2 + x_1,1,2 >= 1
 c5a_1,1: e_1,1,1,1 <= 1
 c5b_1,1: = 0
 c8_1,1: p_1,1,1 <= 1
 c9_1,1: p_1,1,1 <= 1
 c12_1,1,1: e_1,1,1,1 + p_1,1,1 <= 1
 c13_1,1init: e_1,1,1,1 <= 1
 c13_1,1: e_1,1,1,1 <= 1
 c14_1: soc_1,1 = 1
 c15_1,1: - e_1,1,1,1 + gamma_1,1 <= 0
 c16_1,2: 0.1 p_1,1,1 - soc_1,1 - 0.1 gamma_1,1 + soc_1,2 = 0
Bounds
 soc_1,1 <= 1
 soc_1,2 <= 1
Binaries
 delta_1 delta_2 e_1,1,1,1 x_1,1,1 x_1,1,2 p_1,1,1 gamma_1,1
End
