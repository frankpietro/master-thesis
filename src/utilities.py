import os
import json
import numpy as np

import src.constants as c

from scipy.spatial import distance_matrix


# save a JSON to a location
def save_JSON(data, file_name):
    # save it in a .json file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
    
# retrieve a JSON from a location - if it does not exist, create it
def retrieve_JSON(file_name):
    # if file_name does not exist, create it
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('{}')

    with open(file_name, 'r') as f:
        return json.load(f)
    
# read values from a JSON file
def read_values(json_file, var_names):
    json_data = retrieve_JSON(json_file)
    if isinstance(var_names, str):
        return json_data[var_names]
    else:
        return [json_data[var_name] for var_name in var_names]
    
# write values to a JSON file
def write_values(json_file, var_names, values):
    json_data = retrieve_JSON(json_file)
    if isinstance(var_names, str):
        json_data[var_names] = values
    else:
        for var_name, value in zip(var_names, values):
            json_data[var_name] = value

    save_JSON(json_data, json_file)

# merge a list of JSON files
def merge_JSON_files(json_paths):
    merged_json = {}
    for json_file in json_paths:
        json_data = retrieve_JSON(json_file)
        merged_json = {**merged_json, **json_data}

    return merged_json

# generate commuting matrix
def generate_commuting_matrix():
    patient_data = retrieve_JSON(c.PATIENT_JSON)
    operator_data = retrieve_JSON(c.OPERATOR_JSON)
    lats = patient_data['patientLatitude'] + operator_data['operatorLatitude']
    lons = patient_data['patientLongitude'] + operator_data['operatorLongitude']

    # generate matrix with euclidean distances
    dm = distance_matrix(np.array([lats, lons]).T, np.array([lats, lons]).T)

    json_to_save = {"commutingTime": dm.tolist()}
    save_JSON(json_to_save, c.COMM_JSON)