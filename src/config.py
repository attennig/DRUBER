######## SIMULATION PARAMETERS ###########
AoI_SIZE = 50*10**3 #[m] = 50 km
HORIZON = 8*60**2
SWAP_TIME = 60 #[s]
DRONE_SPEED = 14 #[m/s]
DRONE_MAX_PAYLOAD = 2 #[kg]
MIN_DISTANCE = 5*10**3 #[m] = 5 km
UNIT_CONSUMPTION = 0.00006 #[SoC/m] (SoC percentage consumed with no weight flying 1 meter)
ALPHA = 0.00003 #[SoC/(m*kg)]
CONSUMPTION_UPPER_BOUND = 100

STATIONS_RATE  = 0.5
DRONES_RATE = 0.35
DELIVERIES_RATE = 0.15



############ ARGUMENT PARSER ###################
ALGORITHMS = ["MILP", "GREEDY", "GREEDYSWAPS", "LOCALSEARCH", "NONE"]
MILP_METHODS = {"primal": 0, "dual": 1, "barrier": 2, "concurrent": 4}
DESCRIPTION_STR = "This framework has been designed to simulate drone parcel delivery."

############# GUROBI OPT PARAMETERS #############
OPT_TIME_LIMIT = 2*60 # [minutes]
OPT_MEM_LIMIT = 8 # [GB]