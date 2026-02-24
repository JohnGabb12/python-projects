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
    "reqPages": {"data": [], "filled": False},
    
    # process data
    "faults": [],
    
    "mode": 0 # 0: allocate, 1: deallocate
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

    def getinp(prompt, name, type, variableName="", greaterThan=-float('inf'), lessThan=float('inf'), fallback="", append=False, maxLength=50, lessThatEqual=False):
        global data
        if not append:
            if data[variableName]["filled"]:
                if len(fallback) > 0:
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
        sanitized_table = copy.deepcopy(table)
        for i in range(len(sanitized_table)):
            for j in range(len(sanitized_table[i])):
                cell = str(sanitized_table[i][j])
                for code in utils.codes["reset"], *[code for color in utils.codes["colors"].values() for codes in color.values() for code in codes], *utils.codes["styles"].values():
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
    utils.topbar("ML-M4: ACT4 - Least Recently Used")

    table = [
        [utils.style("Frames","bold"), utils.color(data["framesN"]["data"], "cyan") if data["framesN"]["filled"] else utils.color("Not set", "red")],
        [utils.style("Pages","bold"), utils.color(data["pagesN"]["data"], "cyan") if data["pagesN"]["filled"] else utils.color("Not set", "red")],
        [utils.style("Requested Pages","bold"), utils.color(data["reqPages"]["data"], "cyan") if data["reqPages"]["filled"] else utils.color("Not set", "red")],
    ]


    utils.displayTable(table)

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
        variableName = "reqPages",
        greaterThan = 0,
        )
    if tempDataStatus == "input":
        return False # input skip
    elif tempDataStatus != "Valid":
        print(tempDataStatus)
        utils.pressEnter()
        return False

    return True
    
while not complete:
    complete = main()