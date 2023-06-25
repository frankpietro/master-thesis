# folders
DATA_FOLDER = 'data/'
MODEL_FOLDER = 'model/'
PYTHON_FOLDER = 'python/'
SCRIPTS_FOLDER = 'scripts/'

# data folder
OUTPUT_DATA = f'{DATA_FOLDER}output_data.py'
TMP_FILE = 'tmp.output'

OUTPUT_JSON = f'{DATA_FOLDER}output_data.json'
COMM_JSON = f'{DATA_FOLDER}commuting.json'
OPERATOR_JSON = f'{DATA_FOLDER}operators.json'
PATIENT_JSON = f'{DATA_FOLDER}patients.json'
VISIT_JSON = f'{DATA_FOLDER}visits.json'
HYPERPARAMS_JSON = f'{DATA_FOLDER}hyperparams.json'

INPUT_JSON_PATHS = [HYPERPARAMS_JSON, PATIENT_JSON, OPERATOR_JSON, VISIT_JSON, COMM_JSON]

# scripts folder
OUT_TO_PY = f'{SCRIPTS_FOLDER}out_to_py.sh'

# model folder
MOD_FILE = f'{MODEL_FOLDER}hcp.mod'
DAT_FILE = f'{MODEL_FOLDER}hcp.dat'
COMM_FILE = f'{MODEL_FOLDER}commuting.dat'

# OPL command
OPLRUN = '/home/frankp/ibm/ILOG/CPLEX_Studio2211/opl/bin/x86-64_linux/oplrun'
EXECUTION_COMMAND = f'{OPLRUN} {MOD_FILE} {DAT_FILE} >> {TMP_FILE}'

# indexes in daily schedule
PATIENT = 0
DAY = 1
SKILL = 2
START_TIME = 3
END_TIME = 4

# time granularity
TIME_UNIT = 5

# default values for insertion
DEF_OP_AV = 1
DEF_OP_START_TIME = 0
DEF_OP_END_TIME = 300


# --------------- PARAMETER NAMES --------------- #

# INPUT
# hyperparameters
C_WORKLOAD = 'Cw'
C_EXECUTION = 'Cx'
BIG_M = 'bigM'
COMM_COST = 'commutingCost'
N_DAYS = 'numDays'

# patients
N_PATIENTS = 'numPatients'
PAT_LATITUDE = 'patientLatitude'
PAT_LONGITUDE = 'patientLongitude'

PAT_PARAMS = [PAT_LATITUDE, PAT_LONGITUDE]

# operators
N_OPERATORS = 'numOperators'
OP_AVAILABILITY = 'operatorAvailability'
OP_END_TIME = 'operatorEndTime'
OP_LATITUDE = 'operatorLatitude'
OP_LONGITUDE = 'operatorLongitude'
OP_SKILL = 'operatorSkill'
OP_START_TIME = 'operatorStartTime'
OP_TIME = 'operatorTime'
OP_WAGE = 'operatorWage'

OP_PARAMS = [OP_LATITUDE, OP_LONGITUDE, OP_SKILL, OP_TIME, OP_WAGE]
OP_DAILY_PARAMS = [OP_AVAILABILITY, OP_END_TIME, OP_START_TIME]

# visits
VISIT_END_TIME = 'visitEndTime'
VISIT_PRIORITY = 'visitPriority'
VISIT_REQUEST = 'visitRequest'
VISIT_SKILL = 'visitSkill'
VISIT_START_TIME = 'visitStartTime'

VISIT_PARAMS = [VISIT_END_TIME, VISIT_PRIORITY, VISIT_SKILL, VISIT_START_TIME]

# commuting
COMM_TIME = 'commutingTime'

NUMERIC_PARAMS = [C_WORKLOAD, C_EXECUTION, BIG_M, COMM_COST, N_DAYS, N_PATIENTS, N_OPERATORS]

# DERIVED PARAMS
FEASIBLE_PATIENTS = 'feasiblePatients'

# OUTPUT
OBJECTIVE = 'objective'
ASSIGNMENT = 'assignment'
MOVEMENT = 'movement'
VISIT_EXEC = 'visitExecution'
WORKLOAD = 'workload' 