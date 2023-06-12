import os
from . import constants as c


def compute_commuting_matrix():
    import data.input_data as id
    import numpy as np
    from scipy.spatial import distance_matrix

    lats = id.patientLatitude + id.operatorLatitude
    lons = id.patientLongitude + id.operatorLongitude

    # generate matrix with euclidean distances
    return distance_matrix(np.array([lats, lons]).T, np.array([lats, lons]).T)


def write_commuting_matrix(matrix):
    with open(c.COMM_FILE, 'w') as f:
        f.write('commutingTime = [\n')
        for i in range(len(matrix)):
            f.write('\t[' + ','.join([str(round(x,2)) for x in matrix[i]]))
            
            if i != len(matrix) - 1:
                f.write('],\n')
            else:
                f.write(']\n')

        f.write('];\n')


def preprocess():
    # retrieve input data and create a file in the data folder
    os.system(f'{c.DAT_TO_PY} {c.DAT_FILE} {c.INPUT_DATA}')

    # compute commuting matrix
    matrix = compute_commuting_matrix()
    write_commuting_matrix(matrix)

    # run the model
    os.system(c.EXECUTION_COMMAND)

    # retrieve output data and create a file in the data folder
    os.system(f'{c.OUT_TO_PY} {c.TMP_FILE} {c.OUTPUT_DATA}')