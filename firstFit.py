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
        
    def getinp(prompt, name, type, variableName="", greaterThan=-float('inf'), lessThan=float('inf'), fallback="", noDataInsert=False):
        global data
        if data[variableName]["filled"]:
            print(fallback)
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
        if not noDataInsert:
            data[variableName]["data"] = float(s) if type == "float" else int(s)
            data[variableName]["filled"] = True
        return "input"
    
    def getlistinp(prompt, name, type, count, variableName="", greaterThan=-float('inf'), lessThan=float('inf')):
        global data
        if data[variableName]["filled"] >= count:
            print(f"{name}s: {', '.join([utils.rstrips(o) for o in data[variableName]['data']])}")
            return "Valid"
        while data[variableName]["filled"] < count:
            ind_status = utils.getinp(
                prompt = f"{prompt} {data[variableName]['filled'] + 1}: ",
                name = name + str(data[variableName]['filled'] + 1),
                type = type,
                variableName = f"{variableName}_{data[variableName]['filled']}",
                greaterThan = greaterThan,
                lessThan = lessThan,
                noDataInsert = True,
                fallback = f"{name} {data[variableName]['filled'] + 1}: {utils.rstrips(data[variableName]['data'][data[variableName]['filled']])}"
                )
            if ind_status == "input":
                data[variableName]["data"].append(float(data[variableName]['data'][data[variableName]['filled']]))
                data[variableName]["filled"] += 1
            elif ind_status != "Valid":
                return ind_status

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
        prompt = "Enter Number of Partitions: ",
        name = "Number of Partitions",
        type = "int",
        variableName = "partN",
        greaterThan = 0,
        fallback = f"Number of Partitions: {data['partN']['data']}"
        )
    if partN_status == "input":
        return False # input skip
    elif partN_status != "Valid":
        print(partN_status)
        utils.pressEnter()
        return False
    
    # Partition Sizes
    partSizes_status = utils.getlistinp(
        prompt = "Enter Size of Partition",
        name = "Partition Size",
        type = "float",
        count = data["partN"]["data"],
        variableName = "partSizes",
        greaterThan = 0,
        lessThan = data["memSize"]["data"] - data["osSize"]["data"]
        )
    if partSizes_status == "input":
        return False # input skip
    elif partSizes_status != "Valid":
        print(partSizes_status)
        utils.pressEnter()
        return False

    # Number of Jobs
    jobN_status = utils.getinp(
        prompt = "Enter Number of Jobs: ",
        name = "Number of Jobs",
        type = "int",
        variableName = "jobN",
        greaterThan = 0,
        fallback = f"Number of Jobs: {data['jobN']['data']}"
        )
    if jobN_status == "input":
        return False # input skip
    elif jobN_status != "Valid":
        print(jobN_status)
        utils.pressEnter()
        return False


    return True
    
while not complete:
    complete = main()