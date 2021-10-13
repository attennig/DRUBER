# DRUBER
Master Thesis: Simulator for parcel delivery via heterogeneous swarms of drones.

Work in prograss

Currently the simulation concerns only the path planning, which requires the following data as input:

- Mission info: customer ID (cID), way station of departure (src), destination of delivery (dst), budget, number of drons' commitments to the mission (n_commitments)
- Set of commitments for each of which we need: drone ID (dID), way station in which the drone take charge of the delivery (src), way station in which the drone take off the parcel (dst), cost
