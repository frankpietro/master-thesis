import os
import json

import python.constants as c
import python.utilities as u
import python.stats as s


def generate_JSON(dir_name):
    data = {}

    for var in dir(dir_name):
        if not var.startswith('__'):
            data[var] = getattr(dir_name, var)

    return data


def JSON_to_dat(dat_file, json_file=None, json_data=None):    
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


def preprocess(verbose=False):
    if verbose:
        print("Start preprocessing...")
    
    # compute commuting matrix and save as a .json file
    u.generate_commuting_matrix()

    if verbose:
        print("Generated commuting matrix")

    # save all data in a .dat file
    input_data = u.merge_JSON_files(c.INPUT_JSON_PATHS)
    JSON_to_dat(c.DAT_FILE, json_data=input_data)

    if verbose:
        print("Generated .dat file")
    

def run_solver(verbose=False):
    if verbose:
        print("Start running solver...")
    
    # run the IBM solver
    os.system(c.EXECUTION_COMMAND)

    if verbose:
        print("Run ended")


def postprocess(verbose=False):
    if verbose:
        print("Start postprocessing...")
    
    # retrieve output data and create a file in the data folder
    os.system(f'{c.OUT_TO_PY} {c.TMP_FILE} {c.OUTPUT_DATA}')

    # save the output data in a .json file
    import data.output_data as out_d
    data = generate_JSON(out_d)
    u.save_JSON(data, c.OUTPUT_JSON)

    if verbose:
        print("Output data saved")

    # remove the python file
    os.remove(c.TMP_FILE)
    os.remove(c.OUTPUT_DATA)
    os.system(f"touch {c.OUTPUT_DATA}")

    if verbose:
        print("Cleaning completed")
        print("Postprocessing completed")


def run(verbose=False):
    preprocess(verbose)
    run_solver(verbose)
    postprocess(verbose)
    s.get_objective(verbose)
