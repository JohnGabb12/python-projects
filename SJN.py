import os
import copy

# base data
complete = False

# data
data = {
    # default data
    "": {"data" : False, "filled" : False},

    # datas
    "processN": {"data" : 0, "filled" : False},
    "arrivalTimes": {"data" : [], "filled" : False},
    "burstTimes": {"data" : [], "filled" : False},

    # process data
    "processes": [],
    "timeCompleted": [],
    "currentTime": 0
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
        text = str(text)
        color_code = utils.codes["colors"].get(color, None)
        if color_code:
            if bg:
                code = color_code["bg"][1] if light else color_code["bg"][0]
            else:
                code = color_code["text"][1] if light else color_code["text"][0]
            style_code = utils.codes["styles"].get(style, "") if style else ""
            return f"{style_code}{code}{text}{utils.codes['reset'] if not utils.codes['reset'] in text else ''}"
        return text
    
    def style(text, style, color=None, bg=False, light=False):
        text = str(text)
        style_code = utils.codes["styles"].get(style, "")
        if color:
            color_code = utils.codes["colors"].get(color, None)
            if color_code:
                if bg:
                    code = color_code["bg"][1] if light else color_code["bg"][0]
                else:
                    code = color_code["text"][1] if light else color_code["text"][0]
                return f"{style_code}{code}{text}{utils.codes['reset']}"
        return f"{style_code}{text}{utils.codes['reset']}{utils.codes['reset'] if not utils.codes['reset'] in text else ''}"
    
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
    utils.topbar("FL-M5: ACT2 - SJN")

    # Number of Processes
    tempDataStatus = utils.getinp(
        prompt = "Enter Number of Processes: ",
        name = "Number of Processes",
        type = "int",
        variableName = "processN",
        greaterThan = 0,
        lessThan = 27
        )
    if tempDataStatus == "input":
        return False # input skip
    elif tempDataStatus != "Valid":
        print(tempDataStatus)
        utils.pressEnter()
        return False

    table = []
    table.append([utils.color("Process",'blue',light=True)] + [utils.color(f"P{i+1}",'blue',light=True) for i in range(data["processN"]["data"])])
    table.append([utils.color("Arrival Time",'green',light=True)] + [data["arrivalTimes"]["data"][i] if data["arrivalTimes"]["filled"] > i else utils.color("--",'red') for i in range(data["processN"]["data"])])
    table.append([utils.color("Burst Time",'yellow',light=True)] + [data["burstTimes"]["data"][i] if data["burstTimes"]["filled"] > i else utils.color("--",'red') for i in range(data["processN"]["data"])])

    utils.displayTable(table)

    if data["arrivalTimes"]["filled"] < data["processN"]["data"]:
        tempDataStatus = utils.getinp(
            prompt = f"\n{utils.color("ARRIVAL TIME",'green',light=True)}\nEnter {utils.color('Arrival','green',light=True)} time for {utils.color(f'P'+str(data['arrivalTimes']['filled'] + 1),'blue',light=True)}: ",
            name = f"Arrival Time for P{data['arrivalTimes']['filled'] + 1}",
            type = "int",
            variableName = "arrivalTimes",
            greaterThan = 0,
            append = True,
            )
        if tempDataStatus == "input":
            return False # input skip
        elif tempDataStatus != "Valid":
            print(tempDataStatus)
            utils.pressEnter()
            return False
        
    if data["burstTimes"]["filled"] < data["processN"]["data"]:
        tempDataStatus = utils.getinp(
            prompt = f"\n{utils.color("BURST TIME",'yellow',light=True)}\nEnter {utils.color('Burst','yellow',light=True)} time for {utils.color(f'P'+str(data['burstTimes']['filled'] + 1),'blue',light=True)}: ",
            name = f"Burst Time for P{data['burstTimes']['filled'] + 1}",
            type = "int",
            variableName = "burstTimes",
            greaterThan = 0,
            append = True,
            )
        if tempDataStatus == "input":
            return False # input skip
        elif tempDataStatus != "Valid":
            print(tempDataStatus)
            utils.pressEnter()
            return False

    print("Timeline starts at 0")
    table = []
    table.append([utils.color("Process",'blue',light=True)] + [data["processes"][i] if len(data["processes"]) > i else utils.color("--",'red') for i in range(data["processN"]["data"])])
    table.append([utils.color("Time Completed",'green',light=True)] + [data["timeCompleted"][i] if len(data["timeCompleted"]) > i else utils.color("--",'red') for i in range(data["processN"]["data"])])
    utils.displayTable(table)

    if len(data["processes"]) < data["processN"]["data"]:
        


        return False # skip ya
    
    return True
    
while not complete:
    complete = main()