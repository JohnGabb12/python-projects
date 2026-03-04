import os
import copy

# base data
complete = False

# data
data = {
    # default data
    "": {"data" : False, "filled" : False},

    # datas
    "framesN": {"data": 0, "filled": False},
    "pagesN": {"data": 0, "filled": False},
    "reqPagesN": {"data": 0, "filled": False},
    "reqPages": {"data": [], "filled": 0},
    
    # process data
    "sets": [],
    "faults": [],
    "oldFaultData": [],
    "setIndex": 0,
    "freq": [], # for LFU: {page: frequency}
    "previousFaults": {},
    "previousFaults2": {},
    
    "mode": 0 # 0: new/clone set, 1: deallocate, 2: allocate
}

class utils:
    codes = {
        "colors": {
            "red": {# 0: dark, 1: light
                "text": ["\033[31m","\033[91m"],
                "bg": ["\033[41m","\033[101m"]
            },
            "green": {
                "text": ["\033[32m","\033[92m"],
                "bg": ["\033[42m","\033[102m"]
            },
            "yellow": {
                "text": ["\033[33m","\033[93m"],
                "bg": ["\033[43m","\033[103m"]
            },
            "blue": {
                "text": ["\033[34m","\033[94m"],
                "bg": ["\033[44m","\033[104m"]
            },
            "magenta": {
                "text": ["\033[35m","\033[95m"],
                "bg": ["\033[45m","\033[105m"]
            },
            "cyan": {
                "text": ["\033[36m","\033[96m"],
                "bg": ["\033[46m","\033[106m"]
            },
            "white": {
                "text": ["\033[37m","\033[97m"],
                "bg": ["\033[47m","\033[107m"]
            }
        },
        "styles": {
            "bold": "\033[1m",
            "dim": "\033[2m",
            "italic": "\033[3m",
            "underline": "\033[4m",
            "blink": "\033[5m",
            "reverse": "\033[7m",
            "hidden": "\033[8m",
            "strikethrough": "\033[9m",
            "overline": "\033[53m"
        },
        "reset": "\033[0m"
    }

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
    
    def color(text, color, style=None, bg=False, light=False):
        color_code = utils.codes["colors"].get(color, None)
        if color_code:
            if bg:
                code = color_code["bg"][1] if light else color_code["bg"][0]
            else:
                code = color_code["text"][1] if light else color_code["text"][0]
            style_code = utils.codes["styles"].get(style, "") if style else ""
            return f"{style_code}{code}{text}{utils.codes['reset']}"
        return text
    
    def style(text, style, color=None, bg=False, light=False):
        style_code = utils.codes["styles"].get(style, "")
        if color:
            color_code = utils.codes["colors"].get(color, None)
            if color_code:
                if bg:
                    code = color_code["bg"][1] if light else color_code["bg"][0]
                else:
                    code = color_code["text"][1] if light else color_code["text"][0]
                return f"{style_code}{code}{text}{utils.codes['reset']}"
        return f"{style_code}{text}{utils.codes['reset']}"
    
    def resetText(text):
        return f"{utils.codes['reset']}{text}"

    def getinp(
            prompt,                 # input prompt
            name,                   # name of the variable for error messages
            type,                   # type of input: "int", "float", "textonly", "any"
            variableName="",        # variable name in data dictionary
            greaterThan=-float('inf'), lessThan=float('inf'), # INT | FLOAT : range limits for numbers
            fallback="",            # fallback message if data is already filled and append is False
            append=False,           # whether to append to list or not
            maxLength=50,           # INT | FLOAT : maximum length of the list if append is True
            lessThanEqual=False,    # INT | FLOAT : whether the lessThan limit is inclusive or not
            canBeEmpty=False,       # whether the input can be empty or not
            maxChars=100,           # maximum characters allowed in the input
            minAlpha="A", maxAlpha="Z", # TEXTONLY : range limits for characters
            caseSensitive=False     # TEXTONLY : whether the character limits are case sensitive or not
            ):
        global data

        # Fallback Handler
        if not append:
            if data[variableName]["filled"]:
                if len(fallback) > 0:
                    print(fallback)
                return "Valid"
        else:
            if len(data[variableName]["data"]) >= maxLength:
                return "Valid"
            
        # Get input
        s = input(prompt)
        finalData = None # processed data

        # Input Validation
        if len(s) > maxChars:
            return f"{name} must be less than {maxChars} {'digits' if type in ['int', 'float'] else 'characters'}."
    
        if not canBeEmpty and len(s) == 0:
            return f"{name} cannot be empty."

        if type == "textonly":
            if not caseSensitive:
                s = s.upper()
            for o in s:
                if o in "\n\r":
                    return "Newlines are not allowed."
            for o in s:
                if o in "0123456789-.,;:!?@#$%^&*()_+=/\\|\"' " or not o.isalpha():
                    return "Invalid input."
                if o.upper() < minAlpha.upper() or o.upper() > maxAlpha.upper():
                    return f"{name} must be between {minAlpha} and {maxAlpha}."
            finalData = s
        
        if type == "any":
            for o in s:
                if o in "\n\r":
                    return "Newlines are not allowed."
            finalData = s
        
        if type in ["int", "float"]:
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
            if lessThanEqual:
                if float(s) > lessThan:
                    return f"{name} must be less than or equal to {utils.rstrips(lessThan)}."
            else:
                if float(s) >= lessThan:
                    return f"{name} must be less than {utils.rstrips(lessThan)}."
            finalData = int(s) if type == "int" else float(s)
        
        if not append:
            data[variableName]["data"] = finalData
            data[variableName]["filled"] = True
        else:
            data[variableName]["data"].append(finalData)
            data[variableName]["filled"] += 1
        return "input"

    def pressEnter():
        print("Press enter to continue...", end="")
        input()
        
    def indent(data):
        return " "*4 + data
    
    def displayTable(table, noBorder=[]):
        if not table:
            return
        santable = copy.deepcopy(table)
        for i in range(len(santable)):
            for j in range(len(santable[i])):
                cell = str(santable[i][j])
                for code in utils.codes["reset"], *[code for color in utils.codes["colors"].values() for codes in color.values() for code in codes], *utils.codes["styles"].values():
                    cell = cell.replace(code, "")
                santable[i][j] = cell
        
        mcols = max(len(row) for row in table)
        colwidths = [max(len(str(row[i])) for row in santable if i < len(row)) for i in range(mcols)]
        for irow in range(len(table)):
            padrow = table[irow] + [""] * (mcols - len(table[irow]))
            santable_padrow = santable[irow] + [""] * (mcols - len(santable[irow]))
            result = []
            for i, item in enumerate(padrow):
                hasBGColor = None
                for color in utils.codes["colors"].values():
                    for code in color["bg"]:
                        if code in str(item):
                            hasBGColor = code
                            break
                    if hasBGColor:
                        break
                formitem = str(santable_padrow[i]).ljust(colwidths[i])
                formitem = formitem.replace(str(santable_padrow[i]), str(item)).replace(utils.codes["reset"], (" " if hasBGColor else "") + utils.codes["reset"]).replace(code, code + (" " if hasBGColor else ""))
                result.append(formitem)
                if i < len(padrow) - 1:
                    if right_cell := (str(padrow[i+1]) if i+1 < len(padrow) else ""):
                        right_cell_has_bg = any(code in right_cell for color in utils.codes["colors"].values() for code in color["bg"])
                        result.append(utils.style(f"{'' if hasBGColor else ' '}{'|' if irow not in noBorder else ' '}{'' if right_cell_has_bg else ' '}", "dim"))
            print("".join(result))
            


def main():
    global data
    utils.clear()
    utils.topbar("ML-M4: ACT5 - Least Frequently Used")

    def getindex(pageIndex):
        if pageIndex <= 0:
            return ""
        if pageIndex > 26:
            return ""
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[pageIndex-1]

    table = [
        [utils.style("Frames","bold"), utils.color(data["framesN"]["data"], "cyan") if data["framesN"]["filled"] else utils.color("Not set", "red")],
        [utils.style("Pages","bold"), f"{utils.color(data['pagesN']['data'], 'cyan')} {utils.color('(A - ', 'green')}{utils.color(getindex(data['pagesN']['data']), 'green')}{utils.color(')', 'green')}" if data["pagesN"]["filled"] else utils.color("Not set", "red")],
        [utils.style("Requested Pages","bold"), utils.color(data["reqPagesN"]["data"], "cyan") if data["reqPagesN"]["filled"] else utils.color("Not set", "red")],
        [utils.style("Requested Pages List","bold"), f"{utils.style(', ', 'dim')}".join([utils.color(str(i), "yellow", light=True) for i in data["reqPages"]["data"]]) if data["reqPages"]["filled"] > 0 else utils.color("Not set", "red")]
    ]


    utils.displayTable(table)
    print() # empty line

    # Number of Frames
    tempDataStatus = utils.getinp(
        prompt = "Enter Number of Frames: ",
        name = "Number of Frames",
        type = "int",
        variableName = "framesN",
        greaterThan = 0,
        )
    if tempDataStatus == "input":
        return False # input skip
    elif tempDataStatus != "Valid":
        print(tempDataStatus)
        utils.pressEnter()
        return False
    
    # Number of Pages
    tempDataStatus = utils.getinp(
        prompt = "Enter Number of Pages: ",
        name = "Number of Pages",
        type = "int",
        variableName = "pagesN",
        greaterThan = 0,
        lessThan = 27
        )
    if tempDataStatus == "input":
        return False # input skip
    elif tempDataStatus != "Valid":
        print(tempDataStatus)
        utils.pressEnter()
        return False
    
    # Number of Requested Pages
    tempDataStatus = utils.getinp(
        prompt = "Enter Number of Requested Pages: ",
        name = "Number of Requested Pages",
        type = "int",
        variableName = "reqPagesN",
        greaterThan = 0,
        )
    if tempDataStatus == "input":
        return False # input skip
    elif tempDataStatus != "Valid":
        print(tempDataStatus)
        utils.pressEnter()
        return False
    

    if data["reqPages"]["filled"] < data["reqPagesN"]["data"]:
        reqPage_status = utils.getinp(
            prompt = f"\nEnter Requested Page {data['reqPages']['filled'] + 1}: ",
            name = f"Requested Page {data['reqPages']['filled'] + 1}",
            type = "textonly",
            variableName = "reqPages",
            greaterThan = 0,
            append = True,
            maxLength = data["reqPagesN"]["data"],
            maxChars = 1,
            maxAlpha=getindex(data["pagesN"]["data"])
            )
        if reqPage_status == "input":
            data["reqPages"]["data"][-1] = data["reqPages"]["data"][-1].upper()
            return False # input skip
        elif reqPage_status != "Valid":
            print(reqPage_status)
            utils.pressEnter()
            return False
        
    # functions
    def getCurrentRequestedPage():
        return data["reqPages"]["data"][data["setIndex"]]
    
    data["previousFaults"] = {page: -1 for page in data["reqPages"]["data"][:data["setIndex"]+1]}

    # new/clone set
    if data["mode"] == 0:
        data["sets"].append([] if len(data["sets"]) == 0 else copy.deepcopy(data["sets"][-1]))
        data["faults"].append(-1)
        data["oldFaultData"].append(-1)
        data["freq"].append(-1)
    
    # deallocate
    if data["mode"] == 1:
        if len(data["sets"][-1]) == data["framesN"]["data"]:
            # get least recently used page

            count = {page: 0 for page in data["sets"][-1]}
            p = []
            
            for page in data["sets"][-1]:
                for o in range(data["previousFaults"][page], data["setIndex"]):
                    if data["reqPages"]["data"][o+1] == page:
                        count[page] += 1
                        data["previousFaults"][page] = o if data["previousFaults"][page] not in p else -1
                        p.append(o)
            lfu = min(count, key=count.get)

            if not getCurrentRequestedPage() in data["sets"][-1]:
                pgs = {}
                for page in data["sets"][-1]:
                    for o in range(data["setIndex"]-1, -1, -1):
                        if data["reqPages"]["data"][o] == page and count[page] == count[lfu]:
                            pgs[page] = data["setIndex"] - o
                            break
                data["faults"][-1] = max(pgs, key=pgs.get)
        elif not getCurrentRequestedPage() in data["sets"][-1]:
            data["faults"][-1] = getCurrentRequestedPage()
    
    # allocate
    if data["mode"] == 2:
        cur = getCurrentRequestedPage()
        if len(data["sets"][-1]) < data["framesN"]["data"]:
            if not cur in data["sets"][-1]:
                data["sets"][-1].append(cur)
        else:
            if not cur in data["sets"][-1]:
                # replace least recently used page with current requested page
                lru = data["faults"][-1]
                for i in range(len(data["sets"][-1])):
                    if data["sets"][-1][i] == lru:
                        data["sets"][-1][i] = cur
                        break

        # Display freq
        data["freq"] = [-1]*(data["setIndex"]+1)
        count = {page: 0 for page in data["sets"][-1]}
        p = []

        for page in data["sets"][-1]:
            for o in range(data["previousFaults"][page], data["setIndex"]):
                if data["reqPages"]["data"][o+1] == page:
                    count[page] += 1
                    data["previousFaults"][page] = o if data["previousFaults"][page] not in p else -1
                    p.append(o)
        
        p = []
        for o in range(data["setIndex"], -1, -1):
            if data["reqPages"]["data"][o] in count and data["reqPages"]["data"][o] not in p:
                data["freq"][o] = count[data["reqPages"]["data"][o]]
                p.append(data["reqPages"]["data"][o])

    
    print("Legend:\n",utils.color("Green", "green"), ": Requested Page\n", utils.color("Red", "red", light=True), ": Page Fault\n", utils.color(utils.style("Blinking Red", "blink"),"red"), ": To be Deallocated\n", utils.color("Red Background", "red", bg=True), ": Deallocated Page\n", utils.style("Dimmed", "dim"), ": Frequency\n")
    
    frameTable = []+[[" "]+[utils.style(i, "dim") if i != -1 else " " for i in data["freq"]]]
    frameTable += [["LFU"]+[utils.color(data["reqPages"]["data"][i], "yellow", light=True) for i in range(data["setIndex"]+1)]]
    # Frame1 | Set1 | Set2 | ...
    for i in range(data["framesN"]["data"]):
        row = [utils.color(f"Frame {i+1}", "cyan", style="bold")]
        for seti in range(len(data["sets"])):
            cell = data["sets"][seti][i] if i < len(data["sets"][seti]) else " "
            notEmpty = cell != " "
            isLatest = seti == data["setIndex"]
            isRequested = cell == data["reqPages"]["data"][seti]
            isFault = False
            deallocMode = data["mode"] == 1
            allocMode = data["mode"] == 2
            if len(data["faults"]) > seti:
                isFault = cell == data["faults"][seti]
            if deallocMode and isLatest and isFault:
                cell = utils.color(cell, "red", style="blink")
            if isRequested:
                cell = utils.color(cell, "green")
            if not isLatest:
                if len(data["sets"][seti+1]) > i and notEmpty:
                    if data["sets"][seti+1][i] == data["reqPages"]["data"][seti+1] and not data["faults"][seti+1] == -1:
                        cell = utils.color(cell, "red", bg=True)
            row.append(cell)
        frameTable.append(row)
    frameTable.append([utils.color("PF", "red", light=True)]+[utils.color("*", "red", light=True) if data["faults"][i] != -1 and (data["setIndex"] != i or data["mode"] == 2) else " " for i in range(len(data["sets"]))])

    utils.displayTable(frameTable, noBorder=[0])
    
    setIndexPast = data["setIndex"] >= data["reqPagesN"]["data"] - 1

    if setIndexPast and data["mode"] >= 2:
        print(f"\n{utils.color('Conclusion: ', 'red', light=True)}")
        table = [
            [utils.style("Page Faults", "bold"), utils.color(str(sum(1 for f in data["faults"] if f != -1)), "red")],
            [utils.style("Page Hits", "bold"), utils.color(str(sum(1 for f in data["faults"] if f == -1)), "green")],
        ]
        utils.displayTable(table)
        return True

    print("Mode: ", utils.color("New/Next", "yellow") if data["mode"] == 0 else utils.color("Deallocate", "red", light=True) if data["mode"] == 1 else utils.color("Allocate", "green"))
    if data["setIndex"] > 0:
        utils.pressEnter()
    else:
        if data["mode"] > 0:
            utils.pressEnter()
    data["mode"] += 1
    if data["mode"] >= 3:
        data["setIndex"] += 1
        data["mode"] = 0
    return False
    
while not complete:
    complete = main()