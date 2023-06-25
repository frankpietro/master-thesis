import src.constants as c
import src.utilities as u


# --------------- GETS --------------- #

# INPUT
def get_numeric_param(parameter):
    input_data = u.merge_JSON_files(c.INPUT_JSON_PATHS)
    if parameter in c.NUMERIC_PARAMS:
        return input_data[parameter]


def get_patient_param(patient, parameter):
    patient_data = u.retrieve_JSON(c.PATIENT_JSON)
    
    if parameter in c.PAT_PARAMS:
        return patient_data[parameter][patient]


def get_operator_param(operator, parameter):
    operator_data = u.retrieve_JSON(c.OPERATOR_JSON)
    
    if parameter in c.OP_PARAMS:
        return operator_data[parameter][operator]


def get_operator_daily_param(operator, parameter, day):
    operator_data = u.retrieve_JSON(c.OPERATOR_JSON)
    
    if parameter in c.OP_DAILY_PARAMS:
        return operator_data[parameter][operator][day]
    

def get_visit_param(patient, day, parameter):
    visit_data = u.retrieve_JSON(c.VISIT_JSON)
    
    if parameter in c.VISIT_PARAMS:
        return visit_data[parameter][patient][day]


# OUTPUT
def get_objective():
    output_data = u.retrieve_JSON(c.OUTPUT_JSON)
    return output_data[c.OBJECTIVE]


def get_movement(node_1, node_2, operator=None, day=None):
    output_data = u.retrieve_JSON(c.OUTPUT_JSON)
    if not operator:
        return output_data[c.MOVEMENT][node_1][node_2]
    elif not day:
        return output_data[c.MOVEMENT][node_1][node_2][operator]
    else:
        return output_data[c.MOVEMENT][node_1][node_2][operator][day]


def get_assignment(patient, operator):
    output_data = u.retrieve_JSON(c.OUTPUT_JSON)
    return output_data[c.ASSIGNMENT][patient][operator]


def get_feasibility(operator, patient):
    output_data = u.retrieve_JSON(c.OUTPUT_JSON)
    return output_data[c.FEASIBLE_PATIENTS][operator][patient]


def get_visit_execution(operator, patient, day):
    output_data = u.retrieve_JSON(c.OUTPUT_JSON)
    return output_data[c.VISIT_EXECUTION][operator][patient][day]

# --------------- END GETS --------------- #

# --------------- OPERATORS --------------- #

def add_operator(lat, lon, wage, skill, time):
    operator_data = u.retrieve_JSON(c.OPERATOR_JSON)

    operator_data[c.OP_LATITUDE].append(lat)
    operator_data[c.OP_LONGITUDE].append(lon)
    operator_data[c.OP_WAGE].append(wage)
    operator_data[c.OP_SKILL].append(skill)
    operator_data[c.OP_TIME].append(time)

    operator_data[c.N_OPERATORS] += 1

    # any parameter indexed also by days can provide the number of days
    n_days = len(operator_data[c.OP_AVAILABILITY][0])

    # defalut: always available for max time
    operator_data[c.OP_AVAILABILITY].append([c.DEF_OP_AV]*n_days)
    operator_data[c.OP_START_TIME].append([c.DEF_OP_START_TIME]*n_days)
    operator_data[c.OP_END_TIME].append([c.DEF_OP_END_TIME]*n_days)

    u.save_JSON(operator_data, c.OPERATOR_JSON)

    # change commuting matrix
    u.generate_commuting_matrix()


def remove_operator(operator):
    operator_data = u.retrieve_JSON(c.OPERATOR_JSON)
    
    for param in c.OP_PARAMS + c.OP_DAILY_PARAMS:
        operator_data[param].pop(operator)
    
    operator_data['numOperators'] -= 1

    u.save_JSON(operator_data, c.OPERATOR_JSON)

    # change commuting matrix
    u.generate_commuting_matrix()


def change_operator_param(operator, parameter, new_value):
    if parameter in c.OP_PARAMS:
        operator_data = u.retrieve_JSON(c.OPERATOR_JSON)
        operator_data[parameter][operator] = new_value
        u.save_JSON(operator_data, c.OPERATOR_JSON)

        # change commuting matrix
        if parameter in [c.OP_LATITUDE, c.OP_LONGITUDE]:
            u.generate_commuting_matrix()
    
    else:
        raise Exception(f'Parameter {parameter} not valid')


def change_operator_daily_param(operator, parameter, day, new_value):
    if parameter in c.OP_DAILY_PARAMS:
        operator_data = u.retrieve_JSON(c.OPERATOR_JSON)
        operator_data[parameter][operator][day] = new_value
        u.save_JSON(operator_data, c.OPERATOR_JSON)

    else:
        raise Exception(f'Parameter {parameter} not valid')

# --------------- END OPERATORS --------------- #

# --------------- PATIENTS --------------- #

def add_patient(lat, lon):
    patient_data = u.retrieve_JSON(c.PATIENT_JSON)
    
    patient_data[c.PAT_LATITUDE].append(lat)
    patient_data[c.PAT_LONGITUDE].append(lon)
    patient_data[c.N_PATIENTS] += 1

    u.save_JSON(patient_data, c.PATIENT_JSON)

    # change commuting matrix
    u.generate_commuting_matrix()

    # change visits data
    visit_data = u.retrieve_JSON(c.VISIT_JSON)
    
    n_days = len(visit_data[c.VISIT_REQUEST][0])

    for param in visit_data:
        # default: no visits
        visit_data[param].append([0]*n_days)
    
    u.save_JSON(visit_data, c.VISIT_JSON)


def remove_patient(patient):
    patient_data = u.retrieve_JSON(c.PATIENT_JSON)
    
    for field in c.PAT_PARAMS:
        patient_data[field].pop(patient)

    patient_data[c.N_PATIENTS] -= 1
    
    u.save_JSON(patient_data, c.PATIENT_JSON)

    # change commuting matrix
    u.generate_commuting_matrix()

    # change visits data
    visit_data = u.retrieve_JSON(c.VISIT_JSON)
    for field in visit_data:
        visit_data[field].pop(patient)
    u.save_JSON(visit_data, c.VISIT_JSON)


def change_patient_param(patient, parameter, new_value):
    if parameter in c.PAT_PARAMS:
        patient_data = u.retrieve_JSON(c.PATIENT_JSON)
        patient_data[parameter][patient] = new_value
        u.save_JSON(patient_data, c.PATIENT_JSON)

        # change commuting matrix
        # always do it because only lat and lon can change at the moment
        u.generate_commuting_matrix()

# --------------- END PATIENTS --------------- #

# --------------- VISITS --------------- #

def add_visit_request(patient, day, skill, start_time, end_time):
    visit_data = u.retrieve_JSON(c.VISIT_JSON)
    
    visit_data[c.VISIT_REQUEST][patient][day] = 1

    visit_data[c.VISIT_SKILL][patient][day] = skill
    visit_data[c.VISIT_START_TIME][patient][day] = start_time
    visit_data[c.VISIT_END_TIME][patient][day] = end_time
    
    visit_data[c.VISIT_PRIORITY][patient][day] = 0

    u.save_JSON(visit_data, c.VISIT_JSON)


def remove_visit_request(patient, day):
    visit_data = u.retrieve_JSON(c.VISIT_JSON)
    
    visit_data[c.VISIT_REQUEST][patient][day] = 0

    # reset other fields (not mandatory, but more elegant)
    for param in c.VISIT_PARAMS:
        visit_data[param][patient][day] = 0

    u.save_JSON(visit_data, c.VISIT_JSON)


def change_visit_param(patient, day, parameter, new_value):
    if parameter in c.VISIT_PARAMS:
        visit_data = u.retrieve_JSON(c.VISIT_JSON)
        visit_data[parameter][patient][day] = new_value
        u.save_JSON(visit_data, c.VISIT_JSON)
    
    else:
        raise Exception(f'Parameter {parameter} not valid')

# --------------- END VISITS --------------- #