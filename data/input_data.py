
bigM = 999999
Cw = 10
Cx = 1000

numDays = 10

numPatients = 20
patientLatitude = [5, 19, 6, 7, 9, 2, 14, 6, 16, 11, 7, 8, 14, 7, 0, 17, 8, 13, 4, 11]
patientLongitude = [6, 2, 24, 18, 9, 29, 27, 39, 33, 0, 37, 11, 11, 35, 28, 22, 23, 28, 37, 7]

numOperators = 7
operatorSkill = [1,1,1,1,2,2,2]
operatorTime = [1800,1800,1800,1200,1800,1800,1200]
operatorWage = [1,1,1,1,1.5,1.5,1.5]
operatorAvailability = [
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
	[1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
	[1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
]

operatorStartTime = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 120, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[60, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 120, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 60]
]

operatorEndTime = [
	[300, 0, 300, 300, 300, 300, 0, 300, 300, 180],
	[0, 300, 300, 300, 300, 300, 300, 300, 300, 300],
	[0, 300, 300, 300, 0, 300, 300, 240, 0, 300],
	[300, 300, 300, 300, 300, 0, 300, 300, 300, 300],
	[300, 0, 300, 300, 300, 300, 0, 300, 300, 300],
	[300, 300, 300, 210, 300, 300, 300, 0, 300, 300],
	[300, 180, 300, 300, 300, 300, 0, 300, 300, 300]
]

operatorLatitude = [0, 6, 11, 6, 6, 2, 7]
operatorLongitude = [2, 10, 3, 12, 14, 6, 18]

visitRequest = [
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
	[0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
	[0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
]

visitSkill = [
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 1, 0, 0, 2, 1, 1, 0, 0, 1],
	[0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 2, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
	[0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 2, 0, 0, 0]
]

visitStartTime = [
	[150,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,  35,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0, 225,   0,   0,   0,   0,   0,   0],
	[  0, 190, 210,  45,   0, 120,   0,  30, 125,   0],
	[  0,   0,   0,   0,   0,  45,   0,   0,   0,   0],
	[  0,   0,   0,   0,   0, 175,   0,   0,   0,   0],
	[  0, 195,   0,   0,   0, 160,   0,   0,   0,  35],
	[105,   0,   0,   0,   0,   0,   0,   0,   0, 210],
	[  0, 230,   0,   0, 110, 110,  45,   0,   0,  90],
	[  0,   0,   0, 175,   0,   0, 160,   0,   0,   0],
	[  0, 235,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0, 160, 200,   0,   0,   0,   0,  60],
	[  0,   0,   0,   0,   0, 150, 110,  30,   0,   0],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 220],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 105],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 210],
	[  0,   0, 195,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0,   0,   0,   0,   0, 165,   0, 170],
	[  0,   0,   0, 175,   0,   0, 165,  80,   0,   0],
	[  0,   0,   0,   0,   0,   0, 145,   0,   0,   0]
]

visitEndTime = [
	[180,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,  55,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0, 265,   0,   0,   0,   0,   0,   0],
	[  0, 210, 250,  90,   0, 140,   0,  50, 165,   0],
	[  0,   0,   0,   0,   0,  85,   0,   0,   0,   0],
	[  0,   0,   0,   0,   0, 215,   0,   0,   0,   0],
	[  0, 225,   0,   0,   0, 180,   0,   0,   0,  70],
	[135,   0,   0,   0,   0,   0,   0,   0,   0, 250],
	[  0, 270,   0,   0, 130, 140,  90,   0,   0, 120],
	[  0,   0,   0, 195,   0,   0, 190,   0,   0,   0],
	[  0, 255,   0,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0, 190, 240,   0,   0,   0,   0,  80],
	[  0,   0,   0,   0,   0, 175, 140,  90,   0,   0],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 270],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 155],
	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 230],
	[  0,   0, 230,   0,   0,   0,   0,   0,   0,   0],
	[  0,   0,   0,   0,   0,   0,   0, 175,   0, 210],
	[  0,   0,   0, 200,   0,   0, 185, 120,   0,   0],
	[  0,   0,   0,   0,   0,   0, 175,   0,   0,   0]
]

visitPriority = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
































commutingCost = 0.2