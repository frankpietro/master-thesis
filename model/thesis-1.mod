/*********************************************
 * OPL 22.1.1.0 Model
 * Author: frankp
 * Creation Date: May 13, 2023 at 9:51:04 PM
 *********************************************/

/****************************************************************
	CONSTANTS
****************************************************************/

int timeSlotDuration = ...;
int maxDailyTime  = ...;
int maxSkill = ...;
int minSkill = ...;
range Skills = minSkill..maxSkill;
float visitPercThreshold = ...;

/****************************************************************
	END CONSTANTS
****************************************************************/


/****************************************************************
	SETS AND PROPERTIES
****************************************************************/

// time slots
int numTimeSlots = ...;
range TimeSlots = 1..numTimeSlots;
range Days = 1..(numTimeSlots div 2);

// operators
int numOperators = ...;
range Operators = 1..numOperators;
int operatorSkill[Operators] = ...;
float operatorWage[Operators] = ...;
int operatorTime[Operators] = ...;
int operatorAvailability[Operators][TimeSlots] = ...;

// visits
int numVisits = ...;
range Visits = 1..numVisits;
int visitSkill[Visits] = ...;
int visitTime[Visits] = ...;

// patients
int numPatients = ...;
range Patients = 1..numPatients;

// single visits - useful for indexing them
tuple SingleVisitT {
	int id;
	int patient;
	int visit;
	int timeSlots[TimeSlots];
}

/****************************************************************
	END SETS AND PROPERTIES
****************************************************************/

/****************************************************************
	PARAMETERS
****************************************************************/

// requests
//int requests[Patients][TimeSlots][Visits] = ...;
{SingleVisitT} Requests = ...;

/****************************************************************
	END PARAMETERS
****************************************************************/


/****************************************************************
	PREPROCESSING PARAMETERS
****************************************************************/

int visitsPerPatient[Patients];
int patientRequiredTime[Patients];
int patientReqTimePerSkill[Patients][Skills];

int minGlobalContinuity[Patients];

int visitsPerVisitType[Visits];

/****************************************************************
	END PREPROCESSING PARAMETERS
****************************************************************/


/****************************************************************
	PREPROCESSING
****************************************************************/

execute PATIENT_STATS {	
	for(var r in Requests){
		visitsPerPatient[r.patient] += 1;
		patientRequiredTime[r.patient] += visitTime[r.visit];
		patientReqTimePerSkill[r.patient][visitSkill[r.visit]] += visitTime[r.visit];
	}
		
	for(var p in Patients){
		minGlobalContinuity[p] = minSkill;
		// computing minimum global continuity
		for(var s in Skills){
			// if visits of a certain skill level
			// are above the percentage threshold,
			// continuity is enforced for all visits
			if(
				minGlobalContinuity[p] < s && (
					(patientReqTimePerSkill[p][s] / patientRequiredTime[p]) > visitPercThreshold ||
					(patientReqTimePerSkill[p][s] == patientRequiredTime[p] && patientRequiredTime[p] != 0)
				)
			){				
				minGlobalContinuity[p] = s;
			}
		}
	}
	
	writeln("Visits per patient:", visitsPerPatient);
	writeln("Time required by patients:", patientRequiredTime);
	writeln("Time required by patients per skill:", patientReqTimePerSkill);
	writeln("Minimum global continuity:", minGlobalContinuity);
}	


execute VISIT_PRE_STATS {
	// Visits per visit type
	for(var r in Requests){
		visitsPerVisitType[r.visit] += 1;
	}
	writeln("Visits per type:", visitsPerVisitType);
}


execute TIME_STATS {
	// total required and available time
	var requiredTime = 0;
	for(var v in visitsPerVisitType){
		requiredTime += visitsPerVisitType[v] * visitTime[v];
	}
	writeln("Required time: ", requiredTime);
	
	var availableTime = 0;
	for(var o in Operators){
		var maxAvailability = 0;
		for(var t in TimeSlots){
			maxAvailability += operatorAvailability[o][t] * timeSlotDuration;
		}
		if(maxAvailability > operatorTime[o]){
			availableTime += operatorTime[o];
		}
		else {
			availableTime += maxAvailability;
		}
		
	}
	writeln("Available time: ", availableTime);
}

/****************************************************************
	END PREPROCESSING
****************************************************************/


/****************************************************************
	DECISION VARIABLES AND EXPRESSIONS
****************************************************************/

// decision variables
dvar boolean scheduling[Requests][TimeSlots][Operators];
//dvar boolean assignment[Patients][Operators];

// objective function: cost
dexpr float totalWage = sum(r in Requests, t in TimeSlots, o in Operators) scheduling[r][t][o] * visitTime[r.visit] * operatorWage[o];

/****************************************************************
	END DECISION VARIABLES AND EXPRESSIONS
****************************************************************/


/****************************************************************
	COMPUTATION
****************************************************************/

minimize totalWage;

subject to {
	// each visit must be done
	forall (r in Requests) {
        sum(t in TimeSlots, o in Operators) scheduling[r][t][o] == 1;
    }
    
    // the time slot of each visit must be feasible
    forall (r in Requests, t in TimeSlots, o in Operators){
    	scheduling[r][t][o] == 1 => r.timeSlots[t] == 1;
    }
    
    // the operator must be available when handling the request
    forall (r in Requests, t in TimeSlots, o in Operators){
    	scheduling[r][t][o] == 1 => operatorAvailability[o][t] == 1;
    }
    
    // the skill of the operator must be g.e. than the skill required for the visit
    forall (r in Requests, t in TimeSlots, o in Operators) {
        scheduling[r][t][o] == 1 => operatorSkill[o] >= visitSkill[r.visit];
    }
    
    // sum of visit times for all patients, visits, and operators should be l.e. than the time slot duration
	forall (t in TimeSlots, o in Operators)	{
	    sum(r in Requests) scheduling[r][t][o] * visitTime[r.visit] <= timeSlotDuration;
	}
	
	// sum of visit times for all patients, time slots, and visits should be less than or equal to the available working time of the operator.
	forall (o in Operators)	{
	    sum(r in Requests, t in TimeSlots) scheduling[r][t][o] * visitTime[r.visit] <= operatorTime[o];
	}
	
	// no operator works more than its daily time
	forall (o in Operators, d in Days) {
		sum(r in Requests, t in (2*d-1)..(2*d))(scheduling[r][t][o] * visitTime[r.visit]) <= maxDailyTime;
	}

	// minimum global continuity
	forall (r in Requests, t in TimeSlots, o in Operators){
		scheduling[r][t][o] * operatorSkill[o] >= scheduling[r][t][o] * minGlobalContinuity[r.patient];
	}
	
	// care continuity constraint for same skill level visits
	forall (p in Patients){
		sum(
			r1 in Requests,
			r2 in Requests : visitSkill[r1.visit] == visitSkill[r2.visit] || (minGlobalContinuity[p] > visitSkill[r1.visit] || minGlobalContinuity[p] > visitSkill[r2.visit]),
			t1 in TimeSlots,
			t2 in TimeSlots : t1 != t2,
			o1 in Operators,
			o2 in Operators : o1 != o2)(scheduling[r1][t1][o1] * scheduling[r2][t2][o2]) <= 0;
	}
};

/****************************************************************
	END COMPUTATION
****************************************************************/


/****************************************************************
	POSTPROCESSING PARAMETERS
****************************************************************/

int shifts[Operators][TimeSlots];
int operatorCount[Patients][Operators];
int visitedOperators[Patients];

int visitsPerTimeSlot[TimeSlots];

/****************************************************************
	END POSTPROCESSING PARAMETERS
****************************************************************/


/****************************************************************
	POSTPROCESSING
****************************************************************/



execute VISIT_POST_STATS {
	// Visits per time slot
	for(var t in TimeSlots){
		var vpts = 0;
		for(var r in Requests){
			for(var o in Operators){
				vpts += scheduling[r][t][o];
			}
		}
		visitsPerTimeSlot[t] = vpts;
	}
	writeln("Visits per time slot:", visitsPerTimeSlot);
}

execute OP_STATS {
	for(var o in Operators){
		for(var t in TimeSlots){
			var shift = 0;
			for(var r in Requests){
				shift += scheduling[r][t][o] * visitTime[r.visit];
			}
		shifts[o][t] = shift;
		}
	}
	
	writeln("Total shifts per operator:");
	for(var o in Operators){
		writeln(shifts[o]);
	}
}


execute OP_COUNT {
	for (var r in Requests) {
		for (var t in TimeSlots) {
			for (var o in Operators) {
				if (scheduling[r][t][o] == 1) {
					operatorCount[r.patient][o] = 1;
				}
			}
		}
	}
	
	writeln("Number of operators that visited each patient:");
	for(var p in Patients){
		for(var o in Operators){
			visitedOperators[p] += operatorCount[p][o];
		}
	}
	writeln(visitedOperators);	
}

/****************************************************************
	END POSTPROCESSING
****************************************************************/
