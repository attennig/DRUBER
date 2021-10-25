\ Model pathplanner
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  delta_1 + delta_2
Subject To
 c1_1,1,1: x_1,1,1 = 1
 c1_1,2,1: x_1,2,1 = 0
 c2_1,2: x_1,1,2 + x_1,2,2 = 1
 c3_1: x_1,2,1 + x_1,2,2 >= 1
 c4_1: delta_1 + x_1,2,1 >= 1
 c4_2: delta_2 + x_1,2,2 >= 1
 c5a_1,1: e_1,1,1,1 + e_1,1,2,1 = 1
 c5b_1,1: e_1,2,1,1 + e_1,2,2,1 = 0
 c7_1,1: p_1,1,1 <= 1
 c8_1,1,2,1: x_1,1,1 + x_1,2,2 - p_1,1,1 <= 1
 c8_1,2,1,1: x_1,1,2 + x_1,2,1 - p_1,1,1 <= 1
 c9_1,1,1: x_1,1,1 + x_1,1,2 + p_1,1,1 <= 2
 c10_1,1,1,1,2: - e_1,1,2,1 + x_1,1,1 + x_1,2,2 + p_1,1,1 <= 2
 c10_1,1,1,2,1: - e_1,2,1,1 + x_1,1,2 + x_1,2,1 + p_1,1,1 <= 2
Bounds
Binaries
 delta_1 delta_2 e_1,1,1,1 e_1,1,2,1 e_1,2,1,1 e_1,2,2,1 x_1,1,1 x_1,1,2
 x_1,2,1 x_1,2,2 p_1,1,1
End
