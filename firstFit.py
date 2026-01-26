import os

# base data
complete = False

# data
data = {
    "": {"data" : False, "filled" : False},

    "osSize": {"data" : 0, "filled" : False},
    "memSize": {"data" : 0, "filled" : False},
    "jobN": {"data" : 0, "filled" : False},
    "partN": {"data" : 0, "filled" : False},
    "partSizes": {"data" : [], "filled" : 0},
    "jobSizes": {"data" : [], "filled" : 0},

    "sets": [[{"P": 0, "J": 0}]], # default partition and job index
    "setI": 0,
    "jobI": 0,

}

class utils:
    def clear():
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')
            
    def topbar(act):
        print(f"VALENCERINA, JOHN GABRIELLE N.\n{act}\n")
        
    def rstrips(number):
        s = str(number)
        if '.' in s:
            s = s.rstrip('0')
            if s.endswith('.'):
                s = s.rstrip('.')
        return s
        
    def getinp(prompt, name, type, variableName="", greaterThan=-float('inf'), lessThan=float('inf'), fallback="", append=False, maxLength=50):
        global data
        if not append:
            if data[variableName]["filled"]:
                print(fallback)
                return "Valid"
        else:
            if len(data[variableName]["data"]) >= maxLength:
                return "Valid"
        s = input(prompt)
        for o in s:
            if not o in "0123465789-.":
                return "Invalid input."
        if len(s) <= 0:
            return "Invalid input."
        if sum(1 if o == "." else 0 for o in s) > 1:
            return "Invalid input."
        if "." in s and type == "int":
            return "Only integers allowed."
        try:
            if type == "int":
                int(s)
            else:
                float(s)
        except Exception as e:
            return f"An error has occured: {e}."
        if float(s) <= greaterThan:
            return f"{name} must be greater than {utils.rstrips(greaterThan)}."
        if float(s) >= lessThan:
            return f"{name} must be less than {utils.rstrips(lessThan)}."
        if not append:
            data[variableName]["data"] = float(s) if type == "float" else int(s)
            data[variableName]["filled"] = True
        else:
            data[variableName]["data"].append(float(s) if type == "float" else int(s))
            data[variableName]["filled"] += 1
        return "input"
    
    def pressEnter():
        print("Press enter to continue...", end="")
        input()
        
    def indent(data):
        return " "*4 + data


def main():
    global data
    utils.clear()
    utils.topbar("ML-M3: Act1 Fixed Partition - First Fit")

    # Memory Size
    memSize_status = utils.getinp(
        prompt = "Enter Memory Size (k): ",
        name = "Memory Size",
        type = "int",
        variableName = "memSize",
        greaterThan = 0,
        fallback = f"Memory Size: {data['memSize']['data']}k"
        )
    if memSize_status == "input":
        return False # input skip
    elif memSize_status != "Valid":
        print(memSize_status)
        utils.pressEnter()
        return False
    
    # OS Size
    osSize_status = utils.getinp(
        prompt = "Enter OS Size (k): ",
        name = "OS Size",
        type = "float",
        variableName = "osSize",
        greaterThan = 0,
        lessThan = data["memSize"]["data"],
        fallback = f"OS Size: {utils.rstrips(data['osSize']['data'])}k"
        )
    if osSize_status == "input":
        return False # input skip
    elif osSize_status != "Valid":
        print(osSize_status)
        utils.pressEnter()
        return False
    
    # Number of Partitions
    partN_status = utils.getinp(
        prompt = "\nEnter Number of Partitions: ",
        name = "Number of Partitions",
        type = "int",
        variableName = "partN",
        greaterThan = 0,
        fallback = f"\nCurrent Partitions ({data['partN']['data']}): {'(Unused Memory ' + str(data['memSize']['data'] - data["osSize"]["data"] - sum(o for o in data['partSizes']['data'])) + 'k)' if data['partSizes']['filled'] < data['partN']['data'] else ''}"
        )
    if partN_status == "input":
        return False # input skip
    elif partN_status != "Valid":
        print(partN_status)
        utils.pressEnter()
        return False
    
    # Partition Sizes
    for i in range(data["partSizes"]["filled"]):
        print(utils.indent(f"Partition {i+1}: {utils.rstrips(data['partSizes']['data'][i])}k"))
    if data["partSizes"]["filled"] < data["partN"]["data"]:
        partSize_status = utils.getinp(
            prompt = utils.indent(f"Enter Partition Size {data['partSizes']['filled'] + 1}: "),
            name = f"Partition Size {data['partSizes']['filled'] + 1}",
            type = "float",
            variableName = "partSizes",
            greaterThan = 0,
            append = True,
            lessThan = data["memSize"]["data"] - data["osSize"]["data"] - sum(o for o in data["partSizes"]["data"]) + 0.001,
            maxLength = data["partN"]["data"]
            )
        if partSize_status == "input":
            return False # input skip
        elif partSize_status != "Valid":
            print(partSize_status)
            utils.pressEnter()
            return False

    # Number of Jobs
    jobN_status = utils.getinp(
        prompt = "\nEnter Number of Jobs: ",
        name = "Number of Jobs",
        type = "int",
        variableName = "jobN",
        greaterThan = 0,
        fallback = f"\nCurrent Jobs ({data['jobN']['data']}):"
        )
    if jobN_status == "input":
        return False # input skip
    elif jobN_status != "Valid":
        print(jobN_status)
        utils.pressEnter()
        return False

    # Job Sizes
    for i in range(data["jobSizes"]["filled"]):
        print(utils.indent(f"Job {i+1}: {utils.rstrips(data['jobSizes']['data'][i])}k"))
    if data["jobSizes"]["filled"] < data["jobN"]["data"]:
        jobSize_status = utils.getinp(
            prompt = utils.indent(f"Enter Job Size {data['jobSizes']['filled'] + 1}: "),
            name = f"Job Size {data['jobSizes']['filled'] + 1}",
            type = "float",
            variableName = "jobSizes",
            greaterThan = 0,
            append = True,
            maxLength = data["jobN"]["data"]
            )
        if jobSize_status == "input":
            return False # input skip
        elif jobSize_status != "Valid":
            print(jobSize_status)
            utils.pressEnter()
            return False

    # All data collected, perform First Fit
    print("\nFirst Fit")
    print("Memory\t| Partition Size\t| Job Allocation")
    print(f"OS\t| {utils.rstrips(data['osSize']['data'])}k\t\t{'\t| OS'*len(data['sets'])}")
    
    if data["setI"] < data[""]:
        data["setI"] += 1
        utils.pressEnter()
        return False

    print(f"\t| \t\t\t| {'\t| '.join('Set '+ str(i+1) for i in range(len(data['sets'])))}")



    return True
    
while not complete:
    complete = main()