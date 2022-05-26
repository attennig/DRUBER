######## SIMULATION PARAMETERS ###########
AoI_SIZE = 25*10**3 #[m] = 25 km^2
HORIZON = 20*10**4
SWAP_TIME = 60 #[s]
LOAD_TIME = 20 #[s]
UNLOAD_TIME = 20 #[s]
ALTITUDE = 5 #[m]
DRONE_SPEED = 7 #[m/s]
DRONE_MAX_PAYLOAD = 2 #[kg]
MIN_DISTANCE = 5*10**3 #[m] = 5 km
# matrice 600 dji battery TB48S
UNIT_CONSUMPTION = 9.23112501 * 10**(-5)  #[SoC/sec] (SoC percentage consumed with no payload flying 1 sec)
ALPHA = 0.00041367153091968886 #[SoC/(sec*kg)]
CONSUMPTION_UPPER_BOUND = 100


############ ARGUMENT PARSER ###################
ALGORITHMS = ["MILP", "GREEDY", "LOCALSEARCH"]
MILP_METHODS = {"primal": 0, "dual": 1, "barrier": 2, "concurrent": 4}
LOCAL_SEARCH_METHODS = ["HC", "LB", "BFSOPT"]
DESCRIPTION_STR = "This framework has been designed to simulate drone parcel delivery."

############# GUROBI OPT PARAMETERS #############
OPT_TIME_LIMIT = 8*60 # [minutes]
OPT_MEM_LIMIT = 16 # [GB]




MAP_FLAG = False