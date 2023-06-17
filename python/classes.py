class VisitRequest:
    def __init__(self, patient, day, start, end, skill, priority):
        self.patient = patient
        self.day = day
        self.start = start
        self.end = end
        self.skill = skill
        self.priority = priority

    def __str__(self):
        return f'VisitRequest(patient={self.patient}, day={self.day}, start={self.start}, end={self.end}, skill={self.skill}, priority={self.priority})'
    
    def __repr__(self):
        return self.__str__()


class Visit(VisitRequest):
    def __init__(self, patient, day, start, end, skill, priority, operator):
        super().__init__(patient, day, start, end, skill, priority)
        self.operator = operator

    def __str__(self):
        return f'Visit(patient={self.patient}, day={self.day}, start={self.start}, end={self.end}, skill={self.skill}, priority={self.priority}, operator={self.operator})'
    
    def __repr__(self):
        return self.__str__()