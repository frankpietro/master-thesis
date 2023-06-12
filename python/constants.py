VERSION = 4

# folders
DATA_FOLDER = 'data/'
MODEL_FOLDER = 'model/'
PYTHON_FOLDER = 'python/'
SCRIPTS_FOLDER = 'scripts/'

# scripts paths
DAT_TO_PY = f'{SCRIPTS_FOLDER}dat_to_py.sh'
OUT_TO_PY = f'{SCRIPTS_FOLDER}out_to_py.sh'

# model data
INPUT_DATA = f'{DATA_FOLDER}input_data.py'
OUTPUT_DATA = f'{DATA_FOLDER}output_data.py'
TMP_FILE = 'tmp.output'

# model files
MOD_FILE = f'{MODEL_FOLDER}thesis-{VERSION}.mod'
DAT_FILE = f'{MODEL_FOLDER}thesis-{VERSION}.dat'
COMM_FILE = f'{MODEL_FOLDER}commuting.dat'

# OPL command
OPLRUN = '/home/frankp/ibm/ILOG/CPLEX_Studio2211/opl/bin/x86-64_linux/oplrun'
EXECUTION_COMMAND = f'{OPLRUN} {MOD_FILE} {DAT_FILE} {COMM_FILE} >> {TMP_FILE}'

