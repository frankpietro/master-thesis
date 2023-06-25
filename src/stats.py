import src.constants as c
import src.utilities as u


# --------------- OPERATORS --------------- #

def operator_assignment(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} assignment --")

    assigned_patients = []
    for p in range(input_data['numPatients']):
        if output_data['assignment'][p][operator] == 1:
            assigned_patients.append(p)
    
    if verbose:
        # no patients assigned
        if len(assigned_patients) == 0:
            print(f"No patients assigned to operator {operator}")
        # one patient assigned
        elif len(assigned_patients) == 1:
            print(f"Patient {assigned_patients[0]}")
        # more than one patient assigned
        else:
            print(f"Patients {assigned_patients[0]}", end='')
            for p in assigned_patients[1:]:
                print(f", {p}", end='')
        
        print()

    return assigned_patients


def operator_schedule(input_data, output_data, operator, verbose=False, condensed=True):
    if verbose:
        print(f"-- Operator {operator} schedule --")

    schedule = []

    for d in range(input_data['numDays']):
        for p in range(input_data['numPatients']):
            if output_data['visitExecution'][operator][p][d] == 1:
                # order of info: patient, day, skill, start time, end time
                visit_info = (p, d, input_data['visitSkill'][p][d], input_data['visitStartTime'][p][d], input_data['visitEndTime'][p][d])
                
                schedule.append(visit_info)
    
    schedule.sort(key=lambda x: (x[1], x[2]))

    if verbose:
        for d in range(input_data['numDays']):
            print(f"Day {d}: ", end='')

            # daily schedule
            ds = [x for x in schedule if x[1] == d]
            if condensed:
                print("[", end='')
                for i in range(len(ds)):
                    if i == len(ds) - 1:
                        print(f"{ds[i][3]} - {ds[i][4]}", end='')
                    else:
                        print(f"{ds[i][3]} - {ds[i][4]}", end=' --> ')
                print("]")
            
            else:
                # cases
                if len(ds) == 0:
                    print("No visits")
                else:
                    for i in range(len(ds)):
                        if i == len(ds) - 1:
                            print(f"Patient {ds[i][0]} with skill {ds[i][2]} from {ds[i][3]} to {ds[i][4]}")
                        else:
                            print(f"Patient {ds[i][0]} with skill {ds[i][2]} from {ds[i][3]} to {ds[i][4]}", end=', ')

        print()        

    return schedule


def operator_utilization(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} utilization --")

    utilization = output_data['workload'][operator] / input_data['operatorTime'][operator]
    utilization = round(utilization*100, 2)

    if verbose:
        print(f"Utilization: {utilization}%")

    return utilization


def operator_total_wage(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} total wage --")

    w = output_data['workload'][operator] * input_data['operatorWage'][operator]
    # pad with zeros if not enough decimals
    w = round(w, 2)
    w_str = f"{w:.2f}"

    if verbose:
        print(f"Total wage: {w_str}€")

    return w


def operator_total_visits(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} total visits --")

    total_visits = len(operator_schedule(input_data, output_data, operator, False))

    if verbose:
        print(f"Total visits: {total_visits}")

    return total_visits


def operator_overskill(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} overskill --")

    # for each day and patient, check if visitSkill < operatorSkill
    overskill = 0
    for d in range(input_data['numDays']):
        for p in range(input_data['numPatients']):
            if output_data['visitExecution'][operator][p][d] == 1:
                if input_data['visitSkill'][p][d] < input_data['operatorSkill'][operator]:
                    overskill += 1

    overskill = overskill / operator_total_visits(input_data, output_data, operator, False)

    if verbose:
        print(f"Overskill: {(overskill * 100):.2f}%")

    return overskill


def operator_availability(input_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} availability --")

    availability = input_data['operatorAvailability'][operator]
        
    if verbose:
        print(f"Availability: {availability}")

    return availability


def operator_times(input_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} times --")
    
    start_times = [input_data['operatorStartTime'][operator][d] for d in range(input_data['numDays'])]
    end_times = [input_data['operatorEndTime'][operator][d] for d in range(input_data['numDays'])]

    if verbose:
        print(f"Start times: {start_times}")
        print(f"End times: {end_times}")

    return start_times, end_times

# --------------- END OPERATORS --------------- #


# --------------- PATIENTS --------------- #

def patient_assignment(input_data, output_data, patient, verbose=False):
    if verbose:
        print(f"-- Patient {patient} assignment --")

    assigned_operators = []
    for o in range(input_data['numOperators']):
        if output_data['assignment'][patient][o] == 1:
            assigned_operators.append(o)
    
    if verbose:
        # no operators assigned
        if len(assigned_operators) == 0:
            print(f"No operators assigned to patient {patient}")
        # one operator assigned
        elif len(assigned_operators) == 1:
            print(f"Operator {assigned_operators[0]}")
        # more than one operator assigned
        else:
            print(f"Operators {assigned_operators[0]}", end='')
            for o in assigned_operators[1:]:
                print(f", {o}", end='')
        
        print()

    return assigned_operators


def patient_expense(input_data, output_data, patient, verbose=False):
    if verbose:
        print(f"-- Patient {patient} expense --")

    expense = 0
    for d in range(input_data['numDays']):
        for o in range(input_data['numOperators']):
            if output_data['visitExecution'][o][patient][d] == 1:
                expense += visit_duration(input_data, patient, d) * input_data['operatorWage'][o]
    
    expense = round(expense, 2)
    expense_str = f"{expense:.2f}"

    if verbose:
        print(f"Total expense: {expense_str}€")

    return expense


def patient_visits_per_skill(input_data, output_data, patient, verbose=False):
    if verbose:
        print(f"-- Patient {patient} visits per skill --")

    visits_per_skill = {}
    for d in range(input_data['numDays']):
        for o in range(input_data['numOperators']):
            if output_data['visitExecution'][o][patient][d] == 1:
                skill = input_data['visitSkill'][patient][d]
                if skill in visits_per_skill:
                    visits_per_skill[skill] += 1
                else:
                    visits_per_skill[skill] = 1
    
    if verbose:
        for skill, visits in visits_per_skill.items():
            print(f"Skill {skill}: {visits} visits")

    return visits_per_skill

# --------------- END PATIENTS --------------- #


# --------------- VISITS --------------- #

def operator_travel_time(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} movement --")

    schedule = operator_schedule(input_data, output_data, operator, False)
    movement = 0
    for i in range(len(schedule)):
        if i == 0:
            movement += input_data['commutingTime'][input_data['numPatients'] + operator][schedule[i][0]]
        elif i == len(schedule) - 1:
            movement += input_data['commutingTime'][schedule[i][0]][input_data['numPatients'] + operator]
        else:
            movement += input_data['commutingTime'][schedule[i][0]][schedule[i+1][0]]
    
    mov_cost = movement * input_data['commutingCost']
    
    if verbose:
        print(f"Total movement: {movement:.2f} minutes")
        print(f"Movement cost: {mov_cost:.2f}€")

    return movement


# efficiency = workload / (workload + travel time)
def operator_efficiency(input_data, output_data, operator, verbose=False):
    if verbose:
        print(f"-- Operator {operator} efficiency --")

    efficiency = output_data['workload'][operator] / (output_data['workload'][operator] + operator_travel_time(input_data, output_data, operator, False))

    if verbose:
        print(f"Efficiency: {(100*efficiency):.2f}%")

    return efficiency


def visit_duration(input_data, patient, day, verbose=False):
    if verbose:
        print(f"-- Duration of visit for patient {patient} on day {day} --")

    duration = input_data['visitEndTime'][patient][day] - input_data['visitStartTime'][patient][day]

    if verbose:
        print(f"Duration: {duration} minutes")

    return duration


def not_executed_visits(input_data, output_data, verbose=False):
    if verbose:
        print("-- Not executed visits --")

    not_executed = []
    for p in range(input_data['numPatients']):
        for d in range(input_data['numDays']):
            # sum over operators of output_data['visitExecution'][:, p, d] < input_data['visitRequest'][p][d] --> visit not executed
            executed = sum([output_data['visitExecution'][o][p][d] for o in range(input_data['numOperators'])])
            if executed < input_data['visitRequest'][p][d]:
                not_executed.append((p, d, input_data['visitSkill'][p][d], input_data['visitStartTime'][p][d], input_data['visitEndTime'][p][d]))

    if verbose:
        print(f"Number of not executed visits: {len(not_executed)}")
        print(f"Not executed visits: {not_executed}")

    return not_executed

# --------------- END VISITS --------------- #
