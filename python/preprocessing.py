import os
from . import constants as c
import json
import numpy as np

from scipy.spatial import distance_matrix


def compute_commuting_matrix():
    input_data = retrieve_JSON(c.INPUT_JSON)
    lats = input_data['patientLatitude'] + input_data['operatorLatitude']
    lons = input_data['patientLongitude'] + input_data['operatorLongitude']

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

    json_to_save = {"commutingTime": matrix.tolist()}
    save_JSON(json_to_save, c.COMM_JSON)


def generate_JSON(dir_name):
    data = {}

    for var in dir(dir_name):
        if not var.startswith('__'):
            data[var] = getattr(dir_name, var)

    return data


def save_JSON(data, file_name):
    # save it in a .json file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
    

def retrieve_JSON(file_name):
    # retrieve it from the .json file
    with open(file_name, 'r') as f:
        return json.load(f)
    

def json_to_dat(dat_file, json_file=None, json_data=None):    
    def write_value(val, tabs=0, comma=False):
        write_str = ''
        if isinstance(val, list):
            write_str += '\t'*tabs
            write_str += '[\n' + '\t'*(tabs+1)
            for i, item in enumerate(val):
                comma = True if i != len(val) - 1 else False
                write_str += write_value(item, tabs+1, comma)
                
            write_str += '\n' + '\t'*tabs + '],\n'
        else:
            write_str += f"{val}"
            write_str += ',' if comma else ' '

        return write_str

    if json_file:
        with open(json_file, 'r') as file:
            data = json.load(file)
    else:
        data = json_data

    with open(dat_file, 'w') as file:
        for key, value in data.items():
            file.write(f'{key} = ')
            write_str = write_value(value)
            # delete one char before the semicolon
            if write_str[-2] == ',':
                write_str = write_str[:-2]
            else:
                write_str = write_str[:-1]

            # convert every "],\n\n]" to "]\n]"
            write_str = write_str.replace('],\n\n]', ']\n]')
            # convert every "[\n\t\t[" to "[\n\t["
            write_str = write_str.replace('[\n\t\t[', '[\n\t[')

            file.write(write_str)
            file.write(";\n\n")


def preprocess():
    # compute commuting matrix
    matrix = compute_commuting_matrix()
    # save both as a .dat and a .json file
    write_commuting_matrix(matrix)

    # save input data as .dat file
    json_to_dat(c.DAT_FILE, json_file=c.INPUT_JSON)
    
    # run the model
    os.system(c.EXECUTION_COMMAND)

    # retrieve output data and create a file in the data folder
    os.system(f'{c.OUT_TO_PY} {c.TMP_FILE} {c.OUTPUT_DATA}')

    # save the output data in a .json file
    import data.output_data as out_d
    data = generate_JSON(out_d)
    save_JSON(data, c.OUTPUT_JSON)

    # remove the python file
    os.remove(c.OUTPUT_DATA)
    os.system(f"touch {c.OUTPUT_DATA}")

