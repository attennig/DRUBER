\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  C_1,0 + C_1,1 + C_1,2 + C_1,3 + C
Subject To
 oneType_1,0: delta_1,0,move + delta_1,0,swap + delta_1,0,load
   + delta_1,0,unload + delta_1,0,idle = 1
 oneSLoc_1,0: x_1,0,1 + x_1,0,2 = 1
 oneELoc_1,0: y_1,0,1 + y_1,0,2 = 1
 oneType_1,1: delta_1,1,move + delta_1,1,swap + delta_1,1,load
   + delta_1,1,unload + delta_1,1,idle = 1
 oneSLoc_1,1: x_1,1,1 + x_1,1,2 = 1
 oneELoc_1,1: y_1,1,1 + y_1,1,2 = 1
 oneType_1,2: delta_1,2,move + delta_1,2,swap + delta_1,2,load
   + delta_1,2,unload + delta_1,2,idle = 1
 oneSLoc_1,2: x_1,2,1 + x_1,2,2 = 1
 oneELoc_1,2: y_1,2,1 + y_1,2,2 = 1
 oneType_1,3: delta_1,3,move + delta_1,3,swap + delta_1,3,load
   + delta_1,3,unload + delta_1,3,idle = 1
 oneSLoc_1,3: x_1,3,1 + x_1,3,2 = 1
 oneELoc_1,3: y_1,3,1 + y_1,3,2 = 1
 eachActionOneParcel_1,0: seq_1,0,1,0 + seq_1,0,1,1 + seq_1,0,1,2 <= 1
 eachActionOneParcel_1,1: seq_1,1,1,0 + seq_1,1,1,1 + seq_1,1,1,2 <= 1
 eachActionOneParcel_1,2: seq_1,2,1,0 + seq_1,2,1,1 + seq_1,2,1,2 <= 1
 eachActionOneParcel_1,3: seq_1,3,1,0 + seq_1,3,1,1 + seq_1,3,1,2 <= 1
 eachParcelOneAction_1,0: seq_1,0,1,0 + seq_1,1,1,0 + seq_1,2,1,0
   + seq_1,3,1,0 <= 1
 eachParcelOneAction_1,1: seq_1,0,1,1 + seq_1,1,1,1 + seq_1,2,1,1
   + seq_1,3,1,1 <= 1
 eachParcelOneAction_1,2: seq_1,0,1,2 + seq_1,1,1,2 + seq_1,2,1,2
   + seq_1,3,1,2 <= 1
 notMove_1,0,1: delta_1,0,swap + delta_1,0,load + delta_1,0,unload
   + delta_1,0,idle + x_1,0,1 - y_1,0,1 <= 1
 move_1,0,1: delta_1,0,move + x_1,0,1 + y_1,0,1 <= 2
 notMove_1,0,2: delta_1,0,swap + delta_1,0,load + delta_1,0,unload
   + delta_1,0,idle + x_1,0,2 - y_1,0,2 <= 1
 move_1,0,2: delta_1,0,move + x_1,0,2 + y_1,0,2 <= 2
 notMove_1,1,1: delta_1,1,swap + delta_1,1,load + delta_1,1,unload
   + delta_1,1,idle + x_1,1,1 - y_1,1,1 <= 1
 move_1,1,1: delta_1,1,move + x_1,1,1 + y_1,1,1 <= 2
 notMove_1,1,2: delta_1,1,swap + delta_1,1,load + delta_1,1,unload
   + delta_1,1,idle + x_1,1,2 - y_1,1,2 <= 1
 move_1,1,2: delta_1,1,move + x_1,1,2 + y_1,1,2 <= 2
 notMove_1,2,1: delta_1,2,swap + delta_1,2,load + delta_1,2,unload
   + delta_1,2,idle + x_1,2,1 - y_1,2,1 <= 1
 move_1,2,1: delta_1,2,move + x_1,2,1 + y_1,2,1 <= 2
 notMove_1,2,2: delta_1,2,swap + delta_1,2,load + delta_1,2,unload
   + delta_1,2,idle + x_1,2,2 - y_1,2,2 <= 1
 move_1,2,2: delta_1,2,move + x_1,2,2 + y_1,2,2 <= 2
 notMove_1,3,1: delta_1,3,swap + delta_1,3,load + delta_1,3,unload
   + delta_1,3,idle + x_1,3,1 - y_1,3,1 <= 1
 move_1,3,1: delta_1,3,move + x_1,3,1 + y_1,3,1 <= 2
 notMove_1,3,2: delta_1,3,swap + delta_1,3,load + delta_1,3,unload
   + delta_1,3,idle + x_1,3,2 - y_1,3,2 <= 1
 move_1,3,2: delta_1,3,move + x_1,3,2 + y_1,3,2 <= 2
 loadAssignment_1,0: delta_1,0,load - seq_1,0,1,0 - seq_1,0,1,1
   - seq_1,0,1,2 <= 0
 unloadAssignment_1,0: delta_1,0,unload - seq_1,0,1,0 - seq_1,0,1,1
   - seq_1,0,1,2 <= 0
 loadAssignment_1,1: delta_1,1,load - seq_1,1,1,0 - seq_1,1,1,1
   - seq_1,1,1,2 <= 0
 unloadAssignment_1,1: delta_1,1,unload - seq_1,1,1,0 - seq_1,1,1,1
   - seq_1,1,1,2 <= 0
 loadAssignment_1,2: delta_1,2,load - seq_1,2,1,0 - seq_1,2,1,1
   - seq_1,2,1,2 <= 0
 unloadAssignment_1,2: delta_1,2,unload - seq_1,2,1,0 - seq_1,2,1,1
   - seq_1,2,1,2 <= 0
 loadAssignment_1,3: delta_1,3,load - seq_1,3,1,0 - seq_1,3,1,1
   - seq_1,3,1,2 <= 0
 unloadAssignment_1,3: delta_1,3,unload - seq_1,3,1,0 - seq_1,3,1,1
   - seq_1,3,1,2 <= 0
 home_1: x_1,0,1 = 1
 movementConsistency_1,1,1: - y_1,0,1 + x_1,1,1 = 0
 movementConsistency_1,1,2: - y_1,0,2 + x_1,1,2 = 0
 movementConsistency_1,2,1: - y_1,1,1 + x_1,2,1 = 0
 movementConsistency_1,2,2: - y_1,1,2 + x_1,2,2 = 0
 movementConsistency_1,3,1: - y_1,2,1 + x_1,3,1 = 0
 movementConsistency_1,3,2: - y_1,2,2 + x_1,3,2 = 0
 eachParcelDeliveredOnce_1: delivered_1,0,1,0 + delivered_1,0,1,1
   + delivered_1,0,1,2 + delivered_1,1,1,0 + delivered_1,1,1,1
   + delivered_1,1,1,2 + delivered_1,2,1,0 + delivered_1,2,1,1
   + delivered_1,2,1,2 + delivered_1,3,1,0 + delivered_1,3,1,1
   + delivered_1,3,1,2 = 1
 deliveryDef<_1,1,0,0: delta_1,0,unload + y_1,0,2 + seq_1,0,1,0
   - delivered_1,0,1,0 <= 2
 deliveryDef>_1,1,0,0: - delta_1,0,unload - y_1,0,2 - seq_1,0,1,0
   + 3 delivered_1,0,1,0 <= 0
 deliveryDef<_1,1,0,1: delta_1,0,unload + y_1,0,2 + seq_1,0,1,1
   - delivered_1,0,1,1 <= 2
 deliveryDef>_1,1,0,1: - delta_1,0,unload - y_1,0,2 - seq_1,0,1,1
   + 3 delivered_1,0,1,1 <= 0
 deliveryDef<_1,1,0,2: delta_1,0,unload + y_1,0,2 + seq_1,0,1,2
   - delivered_1,0,1,2 <= 2
 deliveryDef>_1,1,0,2: - delta_1,0,unload - y_1,0,2 - seq_1,0,1,2
   + 3 delivered_1,0,1,2 <= 0
 deliveryDef<_1,1,1,0: delta_1,1,unload + y_1,1,2 + seq_1,1,1,0
   - delivered_1,1,1,0 <= 2
 deliveryDef>_1,1,1,0: - delta_1,1,unload - y_1,1,2 - seq_1,1,1,0
   + 3 delivered_1,1,1,0 <= 0
 deliveryDef<_1,1,1,1: delta_1,1,unload + y_1,1,2 + seq_1,1,1,1
   - delivered_1,1,1,1 <= 2
 deliveryDef>_1,1,1,1: - delta_1,1,unload - y_1,1,2 - seq_1,1,1,1
   + 3 delivered_1,1,1,1 <= 0
 deliveryDef<_1,1,1,2: delta_1,1,unload + y_1,1,2 + seq_1,1,1,2
   - delivered_1,1,1,2 <= 2
 deliveryDef>_1,1,1,2: - delta_1,1,unload - y_1,1,2 - seq_1,1,1,2
   + 3 delivered_1,1,1,2 <= 0
 deliveryDef<_1,1,2,0: delta_1,2,unload + y_1,2,2 + seq_1,2,1,0
   - delivered_1,2,1,0 <= 2
 deliveryDef>_1,1,2,0: - delta_1,2,unload - y_1,2,2 - seq_1,2,1,0
   + 3 delivered_1,2,1,0 <= 0
 deliveryDef<_1,1,2,1: delta_1,2,unload + y_1,2,2 + seq_1,2,1,1
   - delivered_1,2,1,1 <= 2
 deliveryDef>_1,1,2,1: - delta_1,2,unload - y_1,2,2 - seq_1,2,1,1
   + 3 delivered_1,2,1,1 <= 0
 deliveryDef<_1,1,2,2: delta_1,2,unload + y_1,2,2 + seq_1,2,1,2
   - delivered_1,2,1,2 <= 2
 deliveryDef>_1,1,2,2: - delta_1,2,unload - y_1,2,2 - seq_1,2,1,2
   + 3 delivered_1,2,1,2 <= 0
 deliveryDef<_1,1,3,0: delta_1,3,unload + y_1,3,2 + seq_1,3,1,0
   - delivered_1,3,1,0 <= 2
 deliveryDef>_1,1,3,0: - delta_1,3,unload - y_1,3,2 - seq_1,3,1,0
   + 3 delivered_1,3,1,0 <= 0
 deliveryDef<_1,1,3,1: delta_1,3,unload + y_1,3,2 + seq_1,3,1,1
   - delivered_1,3,1,1 <= 2
 deliveryDef>_1,1,3,1: - delta_1,3,unload - y_1,3,2 - seq_1,3,1,1
   + 3 delivered_1,3,1,1 <= 0
 deliveryDef<_1,1,3,2: delta_1,3,unload + y_1,3,2 + seq_1,3,1,2
   - delivered_1,3,1,2 <= 2
 deliveryDef>_1,1,3,2: - delta_1,3,unload - y_1,3,2 - seq_1,3,1,2
   + 3 delivered_1,3,1,2 <= 0
 firstLoad_1: seq_1,0,1,0 + seq_1,1,1,0 + seq_1,2,1,0 + seq_1,3,1,0 = 1
 firstLoad_1,1,0: - delta_1,0,load - x_1,0,1 + 2 seq_1,0,1,0 <= 0
 firstLoad_1,1,1: - delta_1,1,load - x_1,1,1 + 2 seq_1,1,1,0 <= 0
 firstLoad_1,1,2: - delta_1,2,load - x_1,2,1 + 2 seq_1,2,1,0 <= 0
 firstLoad_1,1,3: - delta_1,3,load - x_1,3,1 + 2 seq_1,3,1,0 <= 0
 nextAction_1,0,1,0: - delta_1,0,unload + seq_1,0,1,0 - seq_1,1,1,1 <= 0
 prevAction_1,0,1,0: - delta_1,0,load + seq_1,0,1,0 <= 0
 nextAction_1,0,1,1: - delta_1,0,unload + seq_1,0,1,1 - seq_1,1,1,2 <= 0
 prevAction_1,0,1,1: - delta_1,0,load + seq_1,0,1,1 <= 0
 nextAction_1,0,1,2: - delta_1,0,unload + seq_1,0,1,2 <= 0
 prevAction_1,0,1,2: - delta_1,0,load + seq_1,0,1,2 <= 0
 nextAction_1,1,1,0: - delta_1,1,unload + seq_1,1,1,0 - seq_1,2,1,1 <= 0
 prevAction_1,1,1,0: - delta_1,1,load + seq_1,1,1,0 <= 0
 nextAction_1,1,1,1: - delta_1,1,unload + seq_1,1,1,1 - seq_1,2,1,2 <= 0
 prevAction_1,1,1,1: - delta_1,1,load - seq_1,0,1,0 + seq_1,1,1,1 <= 0
 nextAction_1,1,1,2: - delta_1,1,unload + seq_1,1,1,2 <= 0
 prevAction_1,1,1,2: - delta_1,1,load - seq_1,0,1,1 + seq_1,1,1,2 <= 0
 nextAction_1,2,1,0: - delta_1,2,unload + seq_1,2,1,0 - seq_1,3,1,1 <= 0
 prevAction_1,2,1,0: - delta_1,2,load + seq_1,2,1,0 <= 0
 nextAction_1,2,1,1: - delta_1,2,unload + seq_1,2,1,1 - seq_1,3,1,2 <= 0
 prevAction_1,2,1,1: - delta_1,2,load - seq_1,1,1,0 + seq_1,2,1,1 <= 0
 nextAction_1,2,1,2: - delta_1,2,unload + seq_1,2,1,2 <= 0
 prevAction_1,2,1,2: - delta_1,2,load - seq_1,1,1,1 + seq_1,2,1,2 <= 0
 nextAction_1,3,1,0: - delta_1,3,unload + seq_1,3,1,0 <= 0
 prevAction_1,3,1,0: - delta_1,3,load + seq_1,3,1,0 <= 0
 nextAction_1,3,1,1: - delta_1,3,unload + seq_1,3,1,1 <= 0
 prevAction_1,3,1,1: - delta_1,3,load - seq_1,2,1,0 + seq_1,3,1,1 <= 0
 nextAction_1,3,1,2: - delta_1,3,unload + seq_1,3,1,2 <= 0
 prevAction_1,3,1,2: - delta_1,3,load - seq_1,2,1,1 + seq_1,3,1,2 <= 0
 1,0,1,0,1,0,1: - x_1,0,1 + y_1,0,1 + seq_1,0,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,0,1,0,1: x_1,0,1 - y_1,0,1 + seq_1,0,1,0 + seq_1,0,1,1 <= 2
 1,0,1,0,1,0,2: - x_1,0,2 + y_1,0,2 + seq_1,0,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,0,1,0,2: x_1,0,2 - y_1,0,2 + seq_1,0,1,0 + seq_1,0,1,1 <= 2
 1,0,1,0,1,1,1: y_1,0,1 - x_1,1,1 + seq_1,0,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,0,1,1,1: - y_1,0,1 + x_1,1,1 + seq_1,0,1,0 + seq_1,1,1,1 <= 2
 1,0,1,0,1,1,2: y_1,0,2 - x_1,1,2 + seq_1,0,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,0,1,1,2: - y_1,0,2 + x_1,1,2 + seq_1,0,1,0 + seq_1,1,1,1 <= 2
 1,0,1,0,1,2,1: y_1,0,1 - x_1,2,1 + seq_1,0,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,0,1,2,1: - y_1,0,1 + x_1,2,1 + seq_1,0,1,0 + seq_1,2,1,1 <= 2
 1,0,1,0,1,2,2: y_1,0,2 - x_1,2,2 + seq_1,0,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,0,1,2,2: - y_1,0,2 + x_1,2,2 + seq_1,0,1,0 + seq_1,2,1,1 <= 2
 1,0,1,0,1,3,1: y_1,0,1 - x_1,3,1 + seq_1,0,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,0,1,3,1: - y_1,0,1 + x_1,3,1 + seq_1,0,1,0 + seq_1,3,1,1 <= 2
 1,0,1,0,1,3,2: y_1,0,2 - x_1,3,2 + seq_1,0,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,0,1,3,2: - y_1,0,2 + x_1,3,2 + seq_1,0,1,0 + seq_1,3,1,1 <= 2
 1,0,1,1,1,0,1: - x_1,0,1 + y_1,1,1 + seq_1,1,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,1,1,0,1: x_1,0,1 - y_1,1,1 + seq_1,1,1,0 + seq_1,0,1,1 <= 2
 1,0,1,1,1,0,2: - x_1,0,2 + y_1,1,2 + seq_1,1,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,1,1,0,2: x_1,0,2 - y_1,1,2 + seq_1,1,1,0 + seq_1,0,1,1 <= 2
 1,0,1,1,1,1,1: - x_1,1,1 + y_1,1,1 + seq_1,1,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,1,1,1,1: x_1,1,1 - y_1,1,1 + seq_1,1,1,0 + seq_1,1,1,1 <= 2
 1,0,1,1,1,1,2: - x_1,1,2 + y_1,1,2 + seq_1,1,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,1,1,1,2: x_1,1,2 - y_1,1,2 + seq_1,1,1,0 + seq_1,1,1,1 <= 2
 1,0,1,1,1,2,1: y_1,1,1 - x_1,2,1 + seq_1,1,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,1,1,2,1: - y_1,1,1 + x_1,2,1 + seq_1,1,1,0 + seq_1,2,1,1 <= 2
 1,0,1,1,1,2,2: y_1,1,2 - x_1,2,2 + seq_1,1,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,1,1,2,2: - y_1,1,2 + x_1,2,2 + seq_1,1,1,0 + seq_1,2,1,1 <= 2
 1,0,1,1,1,3,1: y_1,1,1 - x_1,3,1 + seq_1,1,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,1,1,3,1: - y_1,1,1 + x_1,3,1 + seq_1,1,1,0 + seq_1,3,1,1 <= 2
 1,0,1,1,1,3,2: y_1,1,2 - x_1,3,2 + seq_1,1,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,1,1,3,2: - y_1,1,2 + x_1,3,2 + seq_1,1,1,0 + seq_1,3,1,1 <= 2
 1,0,1,2,1,0,1: - x_1,0,1 + y_1,2,1 + seq_1,2,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,2,1,0,1: x_1,0,1 - y_1,2,1 + seq_1,2,1,0 + seq_1,0,1,1 <= 2
 1,0,1,2,1,0,2: - x_1,0,2 + y_1,2,2 + seq_1,2,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,2,1,0,2: x_1,0,2 - y_1,2,2 + seq_1,2,1,0 + seq_1,0,1,1 <= 2
 1,0,1,2,1,1,1: - x_1,1,1 + y_1,2,1 + seq_1,2,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,2,1,1,1: x_1,1,1 - y_1,2,1 + seq_1,2,1,0 + seq_1,1,1,1 <= 2
 1,0,1,2,1,1,2: - x_1,1,2 + y_1,2,2 + seq_1,2,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,2,1,1,2: x_1,1,2 - y_1,2,2 + seq_1,2,1,0 + seq_1,1,1,1 <= 2
 1,0,1,2,1,2,1: - x_1,2,1 + y_1,2,1 + seq_1,2,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,2,1,2,1: x_1,2,1 - y_1,2,1 + seq_1,2,1,0 + seq_1,2,1,1 <= 2
 1,0,1,2,1,2,2: - x_1,2,2 + y_1,2,2 + seq_1,2,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,2,1,2,2: x_1,2,2 - y_1,2,2 + seq_1,2,1,0 + seq_1,2,1,1 <= 2
 1,0,1,2,1,3,1: y_1,2,1 - x_1,3,1 + seq_1,2,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,2,1,3,1: - y_1,2,1 + x_1,3,1 + seq_1,2,1,0 + seq_1,3,1,1 <= 2
 1,0,1,2,1,3,2: y_1,2,2 - x_1,3,2 + seq_1,2,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,2,1,3,2: - y_1,2,2 + x_1,3,2 + seq_1,2,1,0 + seq_1,3,1,1 <= 2
 1,0,1,3,1,0,1: - x_1,0,1 + y_1,3,1 + seq_1,3,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,3,1,0,1: x_1,0,1 - y_1,3,1 + seq_1,3,1,0 + seq_1,0,1,1 <= 2
 1,0,1,3,1,0,2: - x_1,0,2 + y_1,3,2 + seq_1,3,1,0 + seq_1,0,1,1 <= 2
 bis1,0,1,3,1,0,2: x_1,0,2 - y_1,3,2 + seq_1,3,1,0 + seq_1,0,1,1 <= 2
 1,0,1,3,1,1,1: - x_1,1,1 + y_1,3,1 + seq_1,3,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,3,1,1,1: x_1,1,1 - y_1,3,1 + seq_1,3,1,0 + seq_1,1,1,1 <= 2
 1,0,1,3,1,1,2: - x_1,1,2 + y_1,3,2 + seq_1,3,1,0 + seq_1,1,1,1 <= 2
 bis1,0,1,3,1,1,2: x_1,1,2 - y_1,3,2 + seq_1,3,1,0 + seq_1,1,1,1 <= 2
 1,0,1,3,1,2,1: - x_1,2,1 + y_1,3,1 + seq_1,3,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,3,1,2,1: x_1,2,1 - y_1,3,1 + seq_1,3,1,0 + seq_1,2,1,1 <= 2
 1,0,1,3,1,2,2: - x_1,2,2 + y_1,3,2 + seq_1,3,1,0 + seq_1,2,1,1 <= 2
 bis1,0,1,3,1,2,2: x_1,2,2 - y_1,3,2 + seq_1,3,1,0 + seq_1,2,1,1 <= 2
 1,0,1,3,1,3,1: - x_1,3,1 + y_1,3,1 + seq_1,3,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,3,1,3,1: x_1,3,1 - y_1,3,1 + seq_1,3,1,0 + seq_1,3,1,1 <= 2
 1,0,1,3,1,3,2: - x_1,3,2 + y_1,3,2 + seq_1,3,1,0 + seq_1,3,1,1 <= 2
 bis1,0,1,3,1,3,2: x_1,3,2 - y_1,3,2 + seq_1,3,1,0 + seq_1,3,1,1 <= 2
 1,1,1,0,1,0,1: - x_1,0,1 + y_1,0,1 + seq_1,0,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,0,1,0,1: x_1,0,1 - y_1,0,1 + seq_1,0,1,1 + seq_1,0,1,2 <= 2
 1,1,1,0,1,0,2: - x_1,0,2 + y_1,0,2 + seq_1,0,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,0,1,0,2: x_1,0,2 - y_1,0,2 + seq_1,0,1,1 + seq_1,0,1,2 <= 2
 1,1,1,0,1,1,1: y_1,0,1 - x_1,1,1 + seq_1,0,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,0,1,1,1: - y_1,0,1 + x_1,1,1 + seq_1,0,1,1 + seq_1,1,1,2 <= 2
 1,1,1,0,1,1,2: y_1,0,2 - x_1,1,2 + seq_1,0,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,0,1,1,2: - y_1,0,2 + x_1,1,2 + seq_1,0,1,1 + seq_1,1,1,2 <= 2
 1,1,1,0,1,2,1: y_1,0,1 - x_1,2,1 + seq_1,0,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,0,1,2,1: - y_1,0,1 + x_1,2,1 + seq_1,0,1,1 + seq_1,2,1,2 <= 2
 1,1,1,0,1,2,2: y_1,0,2 - x_1,2,2 + seq_1,0,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,0,1,2,2: - y_1,0,2 + x_1,2,2 + seq_1,0,1,1 + seq_1,2,1,2 <= 2
 1,1,1,0,1,3,1: y_1,0,1 - x_1,3,1 + seq_1,0,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,0,1,3,1: - y_1,0,1 + x_1,3,1 + seq_1,0,1,1 + seq_1,3,1,2 <= 2
 1,1,1,0,1,3,2: y_1,0,2 - x_1,3,2 + seq_1,0,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,0,1,3,2: - y_1,0,2 + x_1,3,2 + seq_1,0,1,1 + seq_1,3,1,2 <= 2
 1,1,1,1,1,0,1: - x_1,0,1 + y_1,1,1 + seq_1,1,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,1,1,0,1: x_1,0,1 - y_1,1,1 + seq_1,1,1,1 + seq_1,0,1,2 <= 2
 1,1,1,1,1,0,2: - x_1,0,2 + y_1,1,2 + seq_1,1,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,1,1,0,2: x_1,0,2 - y_1,1,2 + seq_1,1,1,1 + seq_1,0,1,2 <= 2
 1,1,1,1,1,1,1: - x_1,1,1 + y_1,1,1 + seq_1,1,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,1,1,1,1: x_1,1,1 - y_1,1,1 + seq_1,1,1,1 + seq_1,1,1,2 <= 2
 1,1,1,1,1,1,2: - x_1,1,2 + y_1,1,2 + seq_1,1,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,1,1,1,2: x_1,1,2 - y_1,1,2 + seq_1,1,1,1 + seq_1,1,1,2 <= 2
 1,1,1,1,1,2,1: y_1,1,1 - x_1,2,1 + seq_1,1,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,1,1,2,1: - y_1,1,1 + x_1,2,1 + seq_1,1,1,1 + seq_1,2,1,2 <= 2
 1,1,1,1,1,2,2: y_1,1,2 - x_1,2,2 + seq_1,1,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,1,1,2,2: - y_1,1,2 + x_1,2,2 + seq_1,1,1,1 + seq_1,2,1,2 <= 2
 1,1,1,1,1,3,1: y_1,1,1 - x_1,3,1 + seq_1,1,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,1,1,3,1: - y_1,1,1 + x_1,3,1 + seq_1,1,1,1 + seq_1,3,1,2 <= 2
 1,1,1,1,1,3,2: y_1,1,2 - x_1,3,2 + seq_1,1,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,1,1,3,2: - y_1,1,2 + x_1,3,2 + seq_1,1,1,1 + seq_1,3,1,2 <= 2
 1,1,1,2,1,0,1: - x_1,0,1 + y_1,2,1 + seq_1,2,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,2,1,0,1: x_1,0,1 - y_1,2,1 + seq_1,2,1,1 + seq_1,0,1,2 <= 2
 1,1,1,2,1,0,2: - x_1,0,2 + y_1,2,2 + seq_1,2,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,2,1,0,2: x_1,0,2 - y_1,2,2 + seq_1,2,1,1 + seq_1,0,1,2 <= 2
 1,1,1,2,1,1,1: - x_1,1,1 + y_1,2,1 + seq_1,2,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,2,1,1,1: x_1,1,1 - y_1,2,1 + seq_1,2,1,1 + seq_1,1,1,2 <= 2
 1,1,1,2,1,1,2: - x_1,1,2 + y_1,2,2 + seq_1,2,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,2,1,1,2: x_1,1,2 - y_1,2,2 + seq_1,2,1,1 + seq_1,1,1,2 <= 2
 1,1,1,2,1,2,1: - x_1,2,1 + y_1,2,1 + seq_1,2,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,2,1,2,1: x_1,2,1 - y_1,2,1 + seq_1,2,1,1 + seq_1,2,1,2 <= 2
 1,1,1,2,1,2,2: - x_1,2,2 + y_1,2,2 + seq_1,2,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,2,1,2,2: x_1,2,2 - y_1,2,2 + seq_1,2,1,1 + seq_1,2,1,2 <= 2
 1,1,1,2,1,3,1: y_1,2,1 - x_1,3,1 + seq_1,2,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,2,1,3,1: - y_1,2,1 + x_1,3,1 + seq_1,2,1,1 + seq_1,3,1,2 <= 2
 1,1,1,2,1,3,2: y_1,2,2 - x_1,3,2 + seq_1,2,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,2,1,3,2: - y_1,2,2 + x_1,3,2 + seq_1,2,1,1 + seq_1,3,1,2 <= 2
 1,1,1,3,1,0,1: - x_1,0,1 + y_1,3,1 + seq_1,3,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,3,1,0,1: x_1,0,1 - y_1,3,1 + seq_1,3,1,1 + seq_1,0,1,2 <= 2
 1,1,1,3,1,0,2: - x_1,0,2 + y_1,3,2 + seq_1,3,1,1 + seq_1,0,1,2 <= 2
 bis1,1,1,3,1,0,2: x_1,0,2 - y_1,3,2 + seq_1,3,1,1 + seq_1,0,1,2 <= 2
 1,1,1,3,1,1,1: - x_1,1,1 + y_1,3,1 + seq_1,3,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,3,1,1,1: x_1,1,1 - y_1,3,1 + seq_1,3,1,1 + seq_1,1,1,2 <= 2
 1,1,1,3,1,1,2: - x_1,1,2 + y_1,3,2 + seq_1,3,1,1 + seq_1,1,1,2 <= 2
 bis1,1,1,3,1,1,2: x_1,1,2 - y_1,3,2 + seq_1,3,1,1 + seq_1,1,1,2 <= 2
 1,1,1,3,1,2,1: - x_1,2,1 + y_1,3,1 + seq_1,3,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,3,1,2,1: x_1,2,1 - y_1,3,1 + seq_1,3,1,1 + seq_1,2,1,2 <= 2
 1,1,1,3,1,2,2: - x_1,2,2 + y_1,3,2 + seq_1,3,1,1 + seq_1,2,1,2 <= 2
 bis1,1,1,3,1,2,2: x_1,2,2 - y_1,3,2 + seq_1,3,1,1 + seq_1,2,1,2 <= 2
 1,1,1,3,1,3,1: - x_1,3,1 + y_1,3,1 + seq_1,3,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,3,1,3,1: x_1,3,1 - y_1,3,1 + seq_1,3,1,1 + seq_1,3,1,2 <= 2
 1,1,1,3,1,3,2: - x_1,3,2 + y_1,3,2 + seq_1,3,1,1 + seq_1,3,1,2 <= 2
 bis1,1,1,3,1,3,2: x_1,3,2 - y_1,3,2 + seq_1,3,1,1 + seq_1,3,1,2 <= 2
 nogaps_1,1: - seq_1,0,1,0 - seq_1,1,1,0 - seq_1,2,1,0 - seq_1,3,1,0
   + seq_1,0,1,1 + seq_1,1,1,1 + seq_1,2,1,1 + seq_1,3,1,1 <= 0
 nogaps_1,2: - seq_1,0,1,1 - seq_1,1,1,1 - seq_1,2,1,1 - seq_1,3,1,1
   + seq_1,0,1,2 + seq_1,1,1,2 + seq_1,2,1,2 + seq_1,3,1,2 <= 0
 loadTime_1,0: - 50 delta_1,0,load + C_1,0 >= 0
 unloadTime_1,0: - 40 delta_1,0,unload + C_1,0 >= 0
 swapTime_1,0: - 60 delta_1,0,swap + C_1,0 >= 0
 moveTime_1,0,1,2: - 715.7142857142857 delta_1,0,move - 20000 x_1,0,1
   - 20000 y_1,0,2 + C_1,0 >= -40000
 moveTime_1,0,2,1: - 715.7142857142857 delta_1,0,move - 20000 y_1,0,1
   - 20000 x_1,0,2 + C_1,0 >= -40000
 loadTime_1,1: - 50 delta_1,1,load - C_1,0 + C_1,1 >= 0
 unloadTime_1,1: - 40 delta_1,1,unload - C_1,0 + C_1,1 >= 0
 swapTime_1,1: - 60 delta_1,1,swap - C_1,0 + C_1,1 >= 0
 moveTime_1,1,1,2: - 715.7142857142857 delta_1,1,move - 20000 x_1,1,1
   - 20000 y_1,1,2 - C_1,0 + C_1,1 >= -40000
 moveTime_1,1,2,1: - 715.7142857142857 delta_1,1,move - 20000 y_1,1,1
   - 20000 x_1,1,2 - C_1,0 + C_1,1 >= -40000
 loadTime_1,2: - 50 delta_1,2,load - C_1,1 + C_1,2 >= 0
 unloadTime_1,2: - 40 delta_1,2,unload - C_1,1 + C_1,2 >= 0
 swapTime_1,2: - 60 delta_1,2,swap - C_1,1 + C_1,2 >= 0
 moveTime_1,2,1,2: - 715.7142857142857 delta_1,2,move - 20000 x_1,2,1
   - 20000 y_1,2,2 - C_1,1 + C_1,2 >= -40000
 moveTime_1,2,2,1: - 715.7142857142857 delta_1,2,move - 20000 y_1,2,1
   - 20000 x_1,2,2 - C_1,1 + C_1,2 >= -40000
 loadTime_1,3: - 50 delta_1,3,load - C_1,2 + C_1,3 >= 0
 unloadTime_1,3: - 40 delta_1,3,unload - C_1,2 + C_1,3 >= 0
 swapTime_1,3: - 60 delta_1,3,swap - C_1,2 + C_1,3 >= 0
 moveTime_1,3,1,2: - 715.7142857142857 delta_1,3,move - 20000 x_1,3,1
   - 20000 y_1,3,2 - C_1,2 + C_1,3 >= -40000
 moveTime_1,3,2,1: - 715.7142857142857 delta_1,3,move - 20000 y_1,3,1
   - 20000 x_1,3,2 - C_1,2 + C_1,3 >= -40000
 deliveryPred_1,1,1,0,1,0: - 20000 seq_1,0,1,0 - 20000 seq_1,0,1,1
   >= -40000
 deliveryPred_1,1,1,0,1,1: - 20000 seq_1,1,1,0 - 20000 seq_1,0,1,1 + C_1,0
   - C_1,1 >= -40000
 deliveryPred_1,1,1,0,1,2: - 20000 seq_1,2,1,0 - 20000 seq_1,0,1,1 + C_1,0
   - C_1,2 >= -40000
 deliveryPred_1,1,1,0,1,3: - 20000 seq_1,3,1,0 - 20000 seq_1,0,1,1 + C_1,0
   - C_1,3 >= -40000
 deliveryPred_1,1,1,1,1,0: - 20000 seq_1,0,1,0 - 20000 seq_1,1,1,1 - C_1,0
   + C_1,1 >= -40000
 deliveryPred_1,1,1,1,1,1: - 20000 seq_1,1,1,0 - 20000 seq_1,1,1,1
   >= -40000
 deliveryPred_1,1,1,1,1,2: - 20000 seq_1,2,1,0 - 20000 seq_1,1,1,1 + C_1,1
   - C_1,2 >= -40000
 deliveryPred_1,1,1,1,1,3: - 20000 seq_1,3,1,0 - 20000 seq_1,1,1,1 + C_1,1
   - C_1,3 >= -40000
 deliveryPred_1,1,1,2,1,0: - 20000 seq_1,0,1,0 - 20000 seq_1,2,1,1 - C_1,0
   + C_1,2 >= -40000
 deliveryPred_1,1,1,2,1,1: - 20000 seq_1,1,1,0 - 20000 seq_1,2,1,1 - C_1,1
   + C_1,2 >= -40000
 deliveryPred_1,1,1,2,1,2: - 20000 seq_1,2,1,0 - 20000 seq_1,2,1,1
   >= -40000
 deliveryPred_1,1,1,2,1,3: - 20000 seq_1,3,1,0 - 20000 seq_1,2,1,1 + C_1,2
   - C_1,3 >= -40000
 deliveryPred_1,1,1,3,1,0: - 20000 seq_1,0,1,0 - 20000 seq_1,3,1,1 - C_1,0
   + C_1,3 >= -40000
 deliveryPred_1,1,1,3,1,1: - 20000 seq_1,1,1,0 - 20000 seq_1,3,1,1 - C_1,1
   + C_1,3 >= -40000
 deliveryPred_1,1,1,3,1,2: - 20000 seq_1,2,1,0 - 20000 seq_1,3,1,1 - C_1,2
   + C_1,3 >= -40000
 deliveryPred_1,1,1,3,1,3: - 20000 seq_1,3,1,0 - 20000 seq_1,3,1,1
   >= -40000
 deliveryPred_1,2,1,0,1,0: - 20000 seq_1,0,1,1 - 20000 seq_1,0,1,2
   >= -40000
 deliveryPred_1,2,1,0,1,1: - 20000 seq_1,1,1,1 - 20000 seq_1,0,1,2 + C_1,0
   - C_1,1 >= -40000
 deliveryPred_1,2,1,0,1,2: - 20000 seq_1,2,1,1 - 20000 seq_1,0,1,2 + C_1,0
   - C_1,2 >= -40000
 deliveryPred_1,2,1,0,1,3: - 20000 seq_1,3,1,1 - 20000 seq_1,0,1,2 + C_1,0
   - C_1,3 >= -40000
 deliveryPred_1,2,1,1,1,0: - 20000 seq_1,0,1,1 - 20000 seq_1,1,1,2 - C_1,0
   + C_1,1 >= -40000
 deliveryPred_1,2,1,1,1,1: - 20000 seq_1,1,1,1 - 20000 seq_1,1,1,2
   >= -40000
 deliveryPred_1,2,1,1,1,2: - 20000 seq_1,2,1,1 - 20000 seq_1,1,1,2 + C_1,1
   - C_1,2 >= -40000
 deliveryPred_1,2,1,1,1,3: - 20000 seq_1,3,1,1 - 20000 seq_1,1,1,2 + C_1,1
   - C_1,3 >= -40000
 deliveryPred_1,2,1,2,1,0: - 20000 seq_1,0,1,1 - 20000 seq_1,2,1,2 - C_1,0
   + C_1,2 >= -40000
 deliveryPred_1,2,1,2,1,1: - 20000 seq_1,1,1,1 - 20000 seq_1,2,1,2 - C_1,1
   + C_1,2 >= -40000
 deliveryPred_1,2,1,2,1,2: - 20000 seq_1,2,1,1 - 20000 seq_1,2,1,2
   >= -40000
 deliveryPred_1,2,1,2,1,3: - 20000 seq_1,3,1,1 - 20000 seq_1,2,1,2 + C_1,2
   - C_1,3 >= -40000
 deliveryPred_1,2,1,3,1,0: - 20000 seq_1,0,1,1 - 20000 seq_1,3,1,2 - C_1,0
   + C_1,3 >= -40000
 deliveryPred_1,2,1,3,1,1: - 20000 seq_1,1,1,1 - 20000 seq_1,3,1,2 - C_1,1
   + C_1,3 >= -40000
 deliveryPred_1,2,1,3,1,2: - 20000 seq_1,2,1,1 - 20000 seq_1,3,1,2 - C_1,2
   + C_1,3 >= -40000
 deliveryPred_1,2,1,3,1,3: - 20000 seq_1,3,1,1 - 20000 seq_1,3,1,2
   >= -40000
 completionTimeDef_1,0: - C_1,0 + C >= 0
 completionTimeDef_1,1: - C_1,1 + C >= 0
 completionTimeDef_1,2: - C_1,2 + C >= 0
 completionTimeDef_1,3: - C_1,3 + C >= 0
 socInit_1: B_1,-1 = 1
 batterySwap_1,0: - delta_1,0,swap + B_1,0 >= 0
 batterySwap_1,1: - delta_1,1,swap + B_1,1 >= 0
 batterySwap_1,2: - delta_1,2,swap + B_1,2 >= 0
 batterySwap_1,3: - delta_1,3,swap + B_1,3 >= 0
 noConsumption_1,0: 100 delta_1,0,load + 100 delta_1,0,unload
   + 100 delta_1,0,idle - B_1,-1 + B_1,0 <= 100
 noConsumption_1,1: 100 delta_1,1,load + 100 delta_1,1,unload
   + 100 delta_1,1,idle - B_1,0 + B_1,1 <= 100
 noConsumption_1,2: 100 delta_1,2,load + 100 delta_1,2,unload
   + 100 delta_1,2,idle - B_1,1 + B_1,2 <= 100
 noConsumption_1,3: 100 delta_1,3,load + 100 delta_1,3,unload
   + 100 delta_1,3,idle - B_1,2 + B_1,3 <= 100
 batteryConsumptionNoPayload_1,0,1,2: 0.0660684804287143 delta_1,0,move
   + 100 x_1,0,1 + 100 y_1,0,2 - 100 seq_1,0,1,0 - 100 seq_1,0,1,1
   - 100 seq_1,0,1,2 - B_1,-1 + B_1,0 <= 200
 batteryConsumptionNoPayload_1,0,2,1: 0.0660684804287143 delta_1,0,move
   + 100 y_1,0,1 + 100 x_1,0,2 - 100 seq_1,0,1,0 - 100 seq_1,0,1,1
   - 100 seq_1,0,1,2 - B_1,-1 + B_1,0 <= 200
 batteryConsumptionNoPayload_1,1,1,2: 0.0660684804287143 delta_1,1,move
   + 100 x_1,1,1 + 100 y_1,1,2 - 100 seq_1,1,1,0 - 100 seq_1,1,1,1
   - 100 seq_1,1,1,2 - B_1,0 + B_1,1 <= 200
 batteryConsumptionNoPayload_1,1,2,1: 0.0660684804287143 delta_1,1,move
   + 100 y_1,1,1 + 100 x_1,1,2 - 100 seq_1,1,1,0 - 100 seq_1,1,1,1
   - 100 seq_1,1,1,2 - B_1,0 + B_1,1 <= 200
 batteryConsumptionNoPayload_1,2,1,2: 0.0660684804287143 delta_1,2,move
   + 100 x_1,2,1 + 100 y_1,2,2 - 100 seq_1,2,1,0 - 100 seq_1,2,1,1
   - 100 seq_1,2,1,2 - B_1,1 + B_1,2 <= 200
 batteryConsumptionNoPayload_1,2,2,1: 0.0660684804287143 delta_1,2,move
   + 100 y_1,2,1 + 100 x_1,2,2 - 100 seq_1,2,1,0 - 100 seq_1,2,1,1
   - 100 seq_1,2,1,2 - B_1,1 + B_1,2 <= 200
 batteryConsumptionNoPayload_1,3,1,2: 0.0660684804287143 delta_1,3,move
   + 100 x_1,3,1 + 100 y_1,3,2 - 100 seq_1,3,1,0 - 100 seq_1,3,1,1
   - 100 seq_1,3,1,2 - B_1,2 + B_1,3 <= 200
 batteryConsumptionNoPayload_1,3,2,1: 0.0660684804287143 delta_1,3,move
   + 100 y_1,3,1 + 100 x_1,3,2 - 100 seq_1,3,1,0 - 100 seq_1,3,1,1
   - 100 seq_1,3,1,2 - B_1,2 + B_1,3 <= 200
 batteryConsumptionWPayload_1,0,1,1,1:
   7.2283254431384125e-04 delta_1,0,move + 100 x_1,0,1 + 100 y_1,0,1
   + 100 seq_1,0,1,0 + 100 seq_1,0,1,1 + 100 seq_1,0,1,2 - B_1,-1 + B_1,0
   <= 300
 batteryConsumptionWPayload_1,0,1,2,1: 0.3621391047012344 delta_1,0,move
   + 100 x_1,0,1 + 100 y_1,0,2 + 100 seq_1,0,1,0 + 100 seq_1,0,1,1
   + 100 seq_1,0,1,2 - B_1,-1 + B_1,0 <= 300
 batteryConsumptionWPayload_1,0,2,1,1: 0.3621391047012344 delta_1,0,move
   + 100 y_1,0,1 + 100 x_1,0,2 + 100 seq_1,0,1,0 + 100 seq_1,0,1,1
   + 100 seq_1,0,1,2 - B_1,-1 + B_1,0 <= 300
 batteryConsumptionWPayload_1,0,2,2,1:
   7.2283254431384125e-04 delta_1,0,move + 100 x_1,0,2 + 100 y_1,0,2
   + 100 seq_1,0,1,0 + 100 seq_1,0,1,1 + 100 seq_1,0,1,2 - B_1,-1 + B_1,0
   <= 300
 batteryConsumptionWPayload_1,1,1,1,1:
   7.2283254431384125e-04 delta_1,1,move + 100 x_1,1,1 + 100 y_1,1,1
   + 100 seq_1,1,1,0 + 100 seq_1,1,1,1 + 100 seq_1,1,1,2 - B_1,0 + B_1,1
   <= 300
 batteryConsumptionWPayload_1,1,1,2,1: 0.3621391047012344 delta_1,1,move
   + 100 x_1,1,1 + 100 y_1,1,2 + 100 seq_1,1,1,0 + 100 seq_1,1,1,1
   + 100 seq_1,1,1,2 - B_1,0 + B_1,1 <= 300
 batteryConsumptionWPayload_1,1,2,1,1: 0.3621391047012344 delta_1,1,move
   + 100 y_1,1,1 + 100 x_1,1,2 + 100 seq_1,1,1,0 + 100 seq_1,1,1,1
   + 100 seq_1,1,1,2 - B_1,0 + B_1,1 <= 300
 batteryConsumptionWPayload_1,1,2,2,1:
   7.2283254431384125e-04 delta_1,1,move + 100 x_1,1,2 + 100 y_1,1,2
   + 100 seq_1,1,1,0 + 100 seq_1,1,1,1 + 100 seq_1,1,1,2 - B_1,0 + B_1,1
   <= 300
 batteryConsumptionWPayload_1,2,1,1,1:
   7.2283254431384125e-04 delta_1,2,move + 100 x_1,2,1 + 100 y_1,2,1
   + 100 seq_1,2,1,0 + 100 seq_1,2,1,1 + 100 seq_1,2,1,2 - B_1,1 + B_1,2
   <= 300
 batteryConsumptionWPayload_1,2,1,2,1: 0.3621391047012344 delta_1,2,move
   + 100 x_1,2,1 + 100 y_1,2,2 + 100 seq_1,2,1,0 + 100 seq_1,2,1,1
   + 100 seq_1,2,1,2 - B_1,1 + B_1,2 <= 300
 batteryConsumptionWPayload_1,2,2,1,1: 0.3621391047012344 delta_1,2,move
   + 100 y_1,2,1 + 100 x_1,2,2 + 100 seq_1,2,1,0 + 100 seq_1,2,1,1
   + 100 seq_1,2,1,2 - B_1,1 + B_1,2 <= 300
 batteryConsumptionWPayload_1,2,2,2,1:
   7.2283254431384125e-04 delta_1,2,move + 100 x_1,2,2 + 100 y_1,2,2
   + 100 seq_1,2,1,0 + 100 seq_1,2,1,1 + 100 seq_1,2,1,2 - B_1,1 + B_1,2
   <= 300
 batteryConsumptionWPayload_1,3,1,1,1:
   7.2283254431384125e-04 delta_1,3,move + 100 x_1,3,1 + 100 y_1,3,1
   + 100 seq_1,3,1,0 + 100 seq_1,3,1,1 + 100 seq_1,3,1,2 - B_1,2 + B_1,3
   <= 300
 batteryConsumptionWPayload_1,3,1,2,1: 0.3621391047012344 delta_1,3,move
   + 100 x_1,3,1 + 100 y_1,3,2 + 100 seq_1,3,1,0 + 100 seq_1,3,1,1
   + 100 seq_1,3,1,2 - B_1,2 + B_1,3 <= 300
 batteryConsumptionWPayload_1,3,2,1,1: 0.3621391047012344 delta_1,3,move
   + 100 y_1,3,1 + 100 x_1,3,2 + 100 seq_1,3,1,0 + 100 seq_1,3,1,1
   + 100 seq_1,3,1,2 - B_1,2 + B_1,3 <= 300
 batteryConsumptionWPayload_1,3,2,2,1:
   7.2283254431384125e-04 delta_1,3,move + 100 x_1,3,2 + 100 y_1,3,2
   + 100 seq_1,3,1,0 + 100 seq_1,3,1,1 + 100 seq_1,3,1,2 - B_1,2 + B_1,3
   <= 300
Bounds
 B_1,-1 <= 1
 B_1,0 <= 1
 B_1,1 <= 1
 B_1,2 <= 1
 B_1,3 <= 1
Binaries
 delta_1,0,move delta_1,0,swap delta_1,0,load delta_1,0,unload
 delta_1,0,idle delta_1,1,move delta_1,1,swap delta_1,1,load
 delta_1,1,unload delta_1,1,idle delta_1,2,move delta_1,2,swap
 delta_1,2,load delta_1,2,unload delta_1,2,idle delta_1,3,move
 delta_1,3,swap delta_1,3,load delta_1,3,unload delta_1,3,idle x_1,0,1
 y_1,0,1 x_1,0,2 y_1,0,2 x_1,1,1 y_1,1,1 x_1,1,2 y_1,1,2 x_1,2,1 y_1,2,1
 x_1,2,2 y_1,2,2 x_1,3,1 y_1,3,1 x_1,3,2 y_1,3,2 seq_1,0,1,0 seq_1,1,1,0
 seq_1,2,1,0 seq_1,3,1,0 seq_1,0,1,1 seq_1,1,1,1 seq_1,2,1,1 seq_1,3,1,1
 seq_1,0,1,2 seq_1,1,1,2 seq_1,2,1,2 seq_1,3,1,2 delivered_1,0,1,0
 delivered_1,0,1,1 delivered_1,0,1,2 delivered_1,1,1,0 delivered_1,1,1,1
 delivered_1,1,1,2 delivered_1,2,1,0 delivered_1,2,1,1 delivered_1,2,1,2
 delivered_1,3,1,0 delivered_1,3,1,1 delivered_1,3,1,2
End
