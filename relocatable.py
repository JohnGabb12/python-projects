import os
import copy

# base data
complete = False

# data
data = {
    # default data
    "": {"data" : False, "filled" : False},
    "color": [
        "\033[0m",    # 0: default
        "\033[91m",   # 1: red
        "\033[92m",   # 2: green
        "\033[93m",   # 3: orange
        "\033[94m",   # 4: blue
        "\033[95m",   # 5: magenta
        "\033[96m"    # 6: cyan
    ],

    # datas
    "osSize": {"data" : 0, "filled" : False},
    "memSize": {"data" : 0, "filled" : False},
    "jobN": {"data" : 0, "filled" : False},
    "jobSizes": {"data" : [], "filled" : 0},
    "jobTAT": {"data" : [], "filled" : 0},

    "sets": [], # default partition and job index
    "setI": 0,
    "TATdecr": {}, # {job index: remaining TAT}
    "jobsAvail": [], # Available jobs : [0, 1, 2, ... n-1] job indexes
    "setsAlloc": [], # sets that have allocated
    "setsDealloc": [], # sets that have deallocated jobs

    "availSpace": 180,
    "mode": 0 # 0: allocate, 1: deallocate, 2: rellocating, 3: compaction
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
    
    def colorText(text, colorCode):
        return f"{data['color'][colorCode]}{text}{data['color'][0]}"

    def pressEnter():
        print("Press enter to continue...", end="")
        input()
        
    def indent(data):
        return " "*4 + data
    
    def displayTable(table):
        if not table:
            return
        sanitized_table = copy.deepcopy(table)
        for i in range(len(sanitized_table)):
            for j in range(len(sanitized_table[i])):
                cell = str(sanitized_table[i][j])
                for code in data["color"]:
                    cell = cell.replace(code, "")
                sanitized_table[i][j] = cell
        
        max_cols = max(len(row) for row in table)
        col_widths = [max(len(str(row[i])) for row in sanitized_table if i < len(row)) for i in range(max_cols)]
        for irow in range(len(table)):
            padded_row = table[irow] + [""] * (max_cols - len(table[irow]))
            sanitized_padded_row = sanitized_table[irow] + [""] * (max_cols - len(sanitized_table[irow]))
            result = []
            for i, item in enumerate(padded_row):
                formatted_item = str(sanitized_padded_row[i]).ljust(col_widths[i])
                formatted_item = formatted_item.replace(str(sanitized_padded_row[i]), str(item))
                result.append(formatted_item)
                if i < len(padded_row) - 1:  # Not the last item
                    # Always add separator so empty cells still show column borders
                    result.append(" | ")
            print("".join(result))


def main():
    global data
    utils.clear()
    utils.topbar("ML-M3: ACT3 - Relocatable Dynamic Partition")

    # Memory Size
    memFallback = "Memory Size: " + utils.colorText(f"{data['memSize']['data']}M", 5)
    memSize_status = utils.getinp(
        prompt = "Enter Memory Size (M): ",
        name = "Memory Size",
        type = "int",
        variableName = "memSize",
        greaterThan = 0,
        fallback = memFallback
        )
    if memSize_status == "input":
        return False # input skip
    elif memSize_status != "Valid":
        print(memSize_status)
        utils.pressEnter()
        return False
    
    # OS Size
    osFallback = "OS Size: " + utils.colorText(f"{utils.rstrips(data['osSize']['data'])}M", 5)
    osSize_status = utils.getinp(
        prompt = "Enter OS Size (M): ",
        name = "OS Size",
        type = "float",
        variableName = "osSize",
        greaterThan = 0,
        lessThan = data["memSize"]["data"],
        fallback = osFallback
        )
    if osSize_status == "input":
        return False # input skip
    elif osSize_status != "Valid":
        print(osSize_status)
        utils.pressEnter()
        return False

    # Number of Jobs
    jobNFallback = "Number of Jobs: " + utils.colorText(f"{data['jobN']['data']}", 5)
    jobN_status = utils.getinp(
        prompt = "\nEnter Number of Jobs: ",
        name = "Number of Jobs",
        type = "int",
        variableName = "jobN",
        greaterThan = 0,
        fallback = jobNFallback
        )
    if jobN_status == "input":
        data["jobsAvail"] = [i for i in range(data["jobN"]["data"])]
        return False # input skip
    elif jobN_status != "Valid":
        print(jobN_status)
        utils.pressEnter()
        return False

    # Display table
    tableA = [[utils.colorText(i, 2) for i in ["Jobs", "Size", "TAT"]]]
    for i in range(data["jobSizes"]["filled"]):
        row = []

        jobcol = f"Job {i+1}"
        for o in data["setsDealloc"]:
            if i in o:
                jobcol = utils.colorText(jobcol, 1)
                break
        row.append(jobcol)

        row.append(f"{utils.rstrips(data['jobSizes']['data'][i])}M")
        if data["jobTAT"]["filled"] > i:
            row.append(f"{utils.rstrips(data['jobTAT']['data'][i])}")
        tableA.append(row)

    utils.displayTable(tableA)
    
    # Job Sizes
    if data["jobSizes"]["filled"] < data["jobN"]["data"]:
        jobSize_status = utils.getinp(
            prompt = f"\nEnter Job Size {data['jobSizes']['filled'] + 1}: ",
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
    
    if data["jobTAT"]["filled"] < data["jobN"]["data"]:
        jobTAT_status = utils.getinp(
            prompt = f"\nEnter Job TAT {data['jobTAT']['filled'] + 1}: ",
            name = f"Job TAT {data['jobTAT']['filled'] + 1}",
            type = "int",
            variableName = "jobTAT",
            greaterThan = 0,
            append = True,
            maxLength = data["jobN"]["data"]
            )
        if jobTAT_status == "input":
            data["TATdecr"][data["jobTAT"]["filled"] - 1] = data["jobTAT"]["data"][-1]
            return False # input skip
        elif jobTAT_status != "Valid":
            print(jobTAT_status)
            utils.pressEnter()
            return False



    def getAvailableSpace():
        return data["memSize"]["data"] - data["osSize"]["data"]

    # all data collected, perform FCFS
    print("\nRelocatable Dynamic Partition")
    table = []
    # table = [["Memory Size","Part Size","Job Allocation"]]
    # table.append(["OS", f"{utils.rstrips(data['osSize']['data'])}M", "OS"])


    if data["mode"] == 0: # allocating
        newSet = []
        additions = []
        if len(data["sets"]) > 0:
            newSet = data["sets"][-1].copy()
        for j in data["jobsAvail"]:
            js = data["jobSizes"]["data"][j]
            if js <= getAvailableSpace() - sum(data["jobSizes"]["data"][job] for job in newSet):
                newSet.append(j)
                additions.append(j)
        if len(data["sets"]) > 0:
            data["sets"][-1] = newSet
        else:
            data["sets"].append(newSet)
        data["setsAlloc"].append(additions)
        data["jobsAvail"] = [j for j in data["jobsAvail"] if j not in newSet]
    elif data["mode"] == 1: # deallocating
        torem = []
        for job, remaining in list(data.get("TATdecr", {}).items()):
            if remaining <= 1 and job in data["sets"][-1]:
                torem.append(job)
        data["setsDealloc"].append(torem)
    if data["mode"] == 2: # relocating
        newSet = data["sets"][-1].copy()
        for j in newSet.copy():
            if j in data["TATdecr"]:
                data["TATdecr"][j] -= 1
                if data["TATdecr"][j] <= 0:
                    newSet.remove(j)
                    del data["TATdecr"][j]
        data["sets"].append(newSet)

    num_sets = len(data["sets"])
    if num_sets == 0:
        table.append([ utils.colorText("OS", 4), utils.colorText(f"{utils.rstrips(data['osSize']['data'])}M", 6)])
    else:
        table.append([utils.colorText("OS", 4)] + [utils.colorText(f"{utils.rstrips(data['osSize']['data'])}M", 6) for _ in range(num_sets)])
        max_parts = max((len(s) for s in data["sets"]), default=0)
        rows_count = max_parts
        if getAvailableSpace() - sum(data["jobSizes"]["data"][j] for j in data["sets"][-1]) > 0:
            rows_count += 1  # for remaining space row
        for part_index in range(rows_count):
            row = [utils.colorText(f"Part {part_index+1}", 5)]
            for si in range(num_sets):
                sset = data["sets"][si]
                label = ""
                if part_index < len(sset):
                    job = sset[part_index]
                    label = f"Job {job+1}"
                    if si == data["setI"] and job in data["setsAlloc"][-1] and data["mode"] == 0:
                        label = utils.colorText(label, 2)
                    if job == -1:
                        label = ""
                    else:
                        if si < len(data.get("setsDealloc", [])) and job in data["setsDealloc"][si]:
                            if data["mode"] > 0 and data["setI"] == si:
                                label = utils.colorText(label, 1)
                            if data["setI"] != si:
                                label = utils.colorText(label, 1)
                elif part_index == len(sset):
                    used = sum(data["jobSizes"]["data"][j] for j in sset) if len(sset) > 0 else 0
                    rem = getAvailableSpace() - used
                    if si == data["setI"]+1:
                        label = utils.colorText(f"{utils.rstrips(rem)}M", 3) if data["mode"] == 3 else ""
                    else:
                        label = utils.colorText(f"{utils.rstrips(rem)}M", 3)
                else:
                    label = ""
                row.append(label)
            table.append(row)

        table.append([""] + [utils.colorText(f"Set {i+1}", 2) for i in range(num_sets)])

    utils.displayTable(table)
    print()
    mode = [
        utils.colorText("Allocating", 0),
        utils.colorText("Deallocating", 1),
        utils.colorText("Relocating", 2),
        utils.colorText("Compacting", 3)
    ]
    

    areAllJobsAllocated = len(data["jobsAvail"]) == 0
    allJobsFitInMemory = all(i <= data["memSize"]["data"] for i in data["jobSizes"]["data"])
    noItemsInSet = len(data["sets"][data["setI"]]) == 0
    

    if (areAllJobsAllocated and not allJobsFitInMemory) or noItemsInSet:
        print("\nConclusion:")
        print("All jobs have been allocated." if len(data["jobsAvail"]) == 0 else "Not all jobs were executed:")
        if all(o == -1 for o in data["sets"][data["setI"]]):
            data['sets'].pop() # remove last set if no allocations
        for o in data["jobsAvail"]:
            print(utils.indent(f"Job {o+1} ({utils.rstrips(data['jobSizes']['data'][o])}M)"))
        print(f"There are {len(data['sets'])} sets of allocations.")
        max_parts = max((len(s) for s in data["sets"]), default=0)
        # add 1 if the highest number of partitions when calculated has greater than 0 remaining space
        sds = sorted(data["sets"], key=lambda s: sum(data["jobSizes"]["data"][j] for j in s), reverse=True)
        if getAvailableSpace() - sum(data["jobSizes"]["data"][j] for j in sds[0]) > 0:
            max_parts += 1
        print(f"There are {max_parts} partitions.")
    else:
        print(f"Mode: {mode[data['mode']]}")
        data["mode"] = data["mode"]+1 if data["mode"] < 3 else 0
        if data["mode"]==3:
            data["setI"] += 1
        utils.pressEnter()
        return False

    return True
    
while not complete:
    complete = main()