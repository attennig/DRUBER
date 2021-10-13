\ Model pathplanner
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  e_21 + e_13 + e_23 + e_34
Subject To
 c1: e_21 + e_23 = 1
 c4: e_34 = 1
 c6-1: e_13 <= 1
 c5-1: - e_21 + e_13 = 0
 c6-3: e_34 <= 1
 c5-3: - e_13 - e_23 + e_34 = 0
 c7: e_21 + e_13 + e_23 + e_34 <= 5
Bounds
Binaries
 e_21 e_13 e_23 e_34
End
