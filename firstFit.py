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

    "sets": [], # default partition and job index
    "setI": 0,
    "jobsAvail": [], # Available jobs : [0, 1, 2, ... n-1] job indexes
    "setsDealloc": [], # sets that have deallocated jobs
    "defaultPart": [] # default partition

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
        
    def getinp(prompt, name, type, variableName="", greaterThan=-float('inf'), lessThan=float('inf'), fallback="", append=False, maxLength=50, lessThatEqual=False):
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
        if lessThatEqual:
            if float(s) > lessThan:
                return f"{name} must be less than or equal to {utils.rstrips(lessThan)}."
        else:
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
    
    def displayTable(table):
        if not table:
            return
        max_cols = max(len(row) for row in table)
        col_widths = [max(len(str(row[i])) for row in table if i < len(row)) for i in range(max_cols)]
        for row in table:
            padded_row = row + [""] * (max_cols - len(row))
            result = []
            for i, item in enumerate(padded_row):
                formatted_item = str(item).ljust(col_widths[i])
                result.append(formatted_item)
                if i < len(padded_row) - 1:  # Not the last item
                    # Add separator only if next item is non-empty
                    if str(padded_row[i + 1]).strip() != "":
                        result.append(" | ")
            print("".join(result))


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
        fallback = f"\nCurrent Partitions ({data['partN']['data']}): {'(Unused Memory ' + str(data['memSize']['data'] - data['osSize']['data'] - sum(o for o in data['partSizes']['data'])) + 'k)' if data['partSizes']['filled'] < data['partN']['data'] else ''}"
        )
    if partN_status == "input":
        data["defaultPart"] = [-1 for _ in range(data["partN"]["data"])]
        return False # input skip
    elif partN_status != "Valid":
        print(partN_status)
        utils.pressEnter()
        return False
    
    # Partition Sizes
    for i in range(data["partSizes"]["filled"]):
        print(utils.indent(f"Partition {i+1}: {utils.rstrips(data['partSizes']['data'][i])}k"))
    if data["partSizes"]["filled"] < data["partN"]["data"]:
        unused_mem = data["memSize"]["data"] - data["osSize"]["data"] - sum(o for o in data["partSizes"]["data"])
        partSize_status = utils.getinp(
            prompt = utils.indent(f"Enter Partition Size {data['partSizes']['filled'] + 1}: "),
            name = f"Partition Size {data['partSizes']['filled'] + 1}",
            type = "float",
            variableName = "partSizes",
            greaterThan = 0,
            append = True,
            lessThan = unused_mem,
            maxLength = data["partN"]["data"],
            lessThatEqual = True
            )
        if partSize_status == "input":
            if unused_mem - data["partSizes"]["data"][-1] == 0 and data["partSizes"]["filled"] < data["partN"]["data"]:
                # remove last partition added
                data["partSizes"]["data"].pop()
                data["partSizes"]["filled"] -= 1
                print(f"No unused memory left to allocate remaining partitions.")
                utils.pressEnter()
                return False
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
        data["jobsAvail"] = [i for i in range(data["jobN"]["data"])]
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
    table = []

    # print("Memory\t| Part Size\t| Job Allocation")
    table.append(["Memory", "Part Size", "Job Allocation"])
    
    # print(f"OS\t| {utils.rstrips(data['osSize']['data'])}k\t{'\t| OS'*len(data['sets'])}")
    table.append(["OS", f"{utils.rstrips(data['osSize']['data'])}k"] + ["OS"] + ["OS" for _ in range(len(data["sets"]))])

    # calculate set
    if len(data["sets"]) == 0:
        data["sets"].append(data["defaultPart"].copy()) # add new set
    else:
        data["sets"].append(data["sets"][-1].copy()) # add new set from previous set with the deallocations applied
        prev_set = data["sets"][data["setI"]]
        allocated_jobs = [job for job in prev_set if job != -1]
        allocated_jobs.sort(key=lambda x: data["jobSizes"]["data"][x])
        jobs_to_deallocate = allocated_jobs[:2] # 2 smallest jobs
        for job in jobs_to_deallocate:
            for p in range(data["partN"]["data"]):
                if data["sets"][data["setI"]][p] == job:
                    data["sets"][data["setI"]][p] = -1

    # allocating jobs
    toremove = []
    for i in data["jobsAvail"]:
        for p in range(data["partN"]["data"]):
            if data["sets"][data["setI"]][p] == -1 and data["jobSizes"]["data"][i] <= data["partSizes"]["data"][p]:
                data["sets"][data["setI"]][p] = i
                toremove.append(i)
                break
    for i in toremove:
        data["jobsAvail"].remove(i)

    # deallocating jobs
    prev_set = data["sets"][data["setI"]]
    allocated_jobs = [job for job in prev_set if job != -1]
    allocated_jobs.sort(key=lambda x: data["jobSizes"]["data"][x])
    deallocated_jobs = allocated_jobs[:2] # 2 smallest jobs
    data["setsDealloc"].append(deallocated_jobs)

    # display partitions
    for i in range(data["partN"]["data"]):
        row = [f"Part {i+1}", f"{utils.rstrips(data['partSizes']['data'][i])}k"]
        for s in range(len(data["sets"])):
            if data["sets"][s][i] == -1:
                row.append("Free")
            else:
                ji = data['sets'][s][i]
                if not ji in data['setsDealloc'][s]:
                    row.append(f"Job {ji+1} ({utils.rstrips(data['jobSizes']['data'][ji])}k)")
                else:
                    row.append(f"Job {ji+1} ({utils.rstrips(data['jobSizes']['data'][ji])}k)*")
        table.append(row)
    
    table.append([" ", f"{utils.rstrips(data['memSize']['data'])}k"] + [f"Set {i+1}" for i in range(len(data["sets"]))])

    utils.displayTable(table)

    if all(o == -1 for o in data["sets"][data["setI"]]) or len(data["jobsAvail"]) == 0:
        print("\nConclusion:")
        print("All jobs have been allocated." if len(data["jobsAvail"]) == 0 else "Not all jobs were executed:")
        for o in data["jobsAvail"]:
            print(utils.indent(f"Job {o+1} ({utils.rstrips(data['jobSizes']['data'][o])}k)"))
        print(f"There are {len(data['sets']) - 1} sets of allocations.")
    else:
        data["setI"] += 1
        utils.pressEnter()
        return False



    return True
    
while not complete:
    complete = main()