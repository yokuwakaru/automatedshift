# Prefer to represent string constants as class variables (in python).
# This is to prevent bugs due to spelling errors.
# If you type in "Unasigned" instead of "Unassigned" when checking for equality somewhere,
# Python won't complain and this could lead to errors
# If you type in EmployeeGrade.UNASIGNED instead of EmployeeGrade.UNASSIGNED
# Python will complain.


class EmployeeGrade:
    UNASSIGNED = "Unassigned"
    M = "Manager",
    PT = "Part Time",
    FT = "Full Time"


# Another class for the same reason even though it's hard to have errors typing A, B, C, D...
# You don't want errors in ANY, NONE, or DAYOFF
class Shift:
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    G = "G"
    NONE = "None"
    DAYOFF = "DayOff"


# Self explanatory?
class Employee:
    def __init__(self, name, employeeGrade):
        self.name = name
        self.employeeGrade = employeeGrade
        # A list of N shifts where N is the number of days in a month like so [A, B, ANY, D, ANY...]
        self.requestedShifts = []
        # A list of N shifts where N is the number of days in a month like so [A, B, A, NONE, D...]
        # Notice we track the assigned shift both in the rota and within the employee data model cause it allows us to
        # do different checks
        self.assignedShifts = []


    # https://www.pythonforbeginners.com/basics/__str__-vs-__repr
    # https://stackoverflow.com/questions/1436703/difference-between-str-and-repr
    
    def __repr__(self):
        # One way of converting an Employee object into a string representation.
        # We can customize this. I chose to use the name and the shifts.
        # This is useful when you want to output the shifts for each employee.
        return "%s: %s" % (self.name, ', '.join(self.assignedShifts))

    def __str__(self):
        # Another way of converting an Employee object into a string representation.
        # I use just the name. This is useful when you want to output the shift assignments in the Rota.
        return self.name


class Rota:
    # A list of N RotaDays where N is the number of days in a month
    def __init__(self):
        # We initialize the list here to an empty list
        # example_assignedShifts = [
        #   {A:employee1, B:employee2}, # <-- this is day 0
        #   {A:employee2, B:employee3}, # <-- this is day 1
        # ]
        self.assignedShifts = []

    def assign(self, day, shift, employee):
        # If we don't have a dictionary for the current day
        if len(self.assignedShifts) <= day:
            # Stuff the assignedShifts list with empty dictionaries until its size is the same as the days.
            # We use dictionaries cause it's easier to say shifts['G'] = Employee('Alan') instead of assuming
            # array position 4 is for G or some such. You could even create a class with A, B, C, D.. variables
            # and assign to it but I've used a dictionary for now. Chose your data structures for maximum efficiency!
            while len(self.assignedShifts) <= day:
                self.assignedShifts.append({})
        # We have a dictionary for the current day. But do we already have someone assigned to the shift?
        # If we didn't assign to a shift it would not exist in the dictionary.
        elif shift in self.assignedShifts[day]:
            raise Exception('Failed to assign %s to shift %s on day %d. Already assigned to %s.' % (
                employee.name, shift, day, self.assignedShifts[day][shift].name))
        # Everything was cool. Go ahead and add this employee to the shift
        self.assignedShifts[day][shift] = employee

        # Now stuff the employee's assigned shifts with this shift
        if len(employee.assignedShifts) <= day:
            while len(employee.assignedShifts) <= day:
                employee.assignedShifts.append(Shift.NONE)
        employee.assignedShifts[day] = shift

    def __repr__(self):
        # This function is python's way of converting an object into a string
        # I use this to print the rota (you can change the output by simply changing this function)
        s = ""  # The final string representation will end up in this variable
        # Go through all the assigned s
        hifts
        
        # https://dbader.org/blog/python-enumerate
        
        for index, day in enumerate(self.assignedShifts):
            # Make sure the day has some shifts assigned.
            if day is not None and len(day.keys()) > 0:
                shifts = []  # I'm going to stuff a string representation of each shift into this array
                # and later join each element with a comma using a convenient join function
                # I sort the shift keys so they always come out as A, B, C, D, E, ...
                for key in sorted(day.keys()):
                    # day[key] is the employee. Python will automatically use the __str__() function to determine
                    # how to convert the employee to its string representation.
                    shifts.append("%s: %s" % (key, day[key]))
                s += "Day %s // %s\n" % (index, ', '.join(shifts))

                # The following is a one line way of doing the same thing above using functional programming paradigm
                # Functional programmers jerk off to this stuff calling it more elegant.
                #
                # s += "Day %s // %s\n" % (index, ', '.join(map(lambda key: "%s: %s" % (key, day[key]), sorted(day.keys()))))
            else:  # No shifts assigned on this day? Just print the day with '--' to represent no schedules
                s += "Day %s // --\n" % (index)
        return s


# Presumably the following data will come from the command line but prefer an input file so you don't have to enter names and grades all the time
e1 = Employee('小林', EmployeeGrade.M)
e2 = Employee('リチャード', EmployeeGrade.FT)
e3 = Employee('前井', EmployeeGrade.FT)
e4 = Employee('前川', EmployeeGrade.FT)
e5 = Employee('ホヨン', EmployeeGrade.FT)
e6 = Employee('坂田', EmployeeGrade.PT)

rota = Rota()

# we use Shift.G and not "G" even though technically it's the same thing
rota.assign(0, Shift.A, e1)
rota.assign(0, Shift.B, e2)
rota.assign(0, Shift.DAYOFF, e3)
# rota.assign(1, Shift.D, e1)  # This will throw an error
print(rota)

# Now print employee shifts
for e in [e1, e2, e3, e4, e5, e6]:
    # We are specifically asking for the string representation __repr__ with the shift assignments
    # as opposed to the __str__ representation which just has the name.
    print(repr(e))

"""
rota.assignedShifts[0]["A"]

this will get 小林: A


logic:

"C" in rota.assignedShifts[0]

returns False as,

"B" in rota.assignedShifts[0]

returns True

"""
