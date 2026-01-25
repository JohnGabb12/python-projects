import os

# base data
complete = False

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
        
    def getinp(prompt, name, type, greaterThan=-float('inf'), lessThan=float('inf'), flag=False, fallback=""):
        if flag:
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
        return "input"
    
    def pressEnter():
        print("Press enter to continue...", end="")
        input()
        
    def indent(data):
        return " "*4 + data

# data
data = {
    "osFilled": False,
    "osSize": 0,
    "memFilled": False,
    "memSize": 0,
    "jobNFilled": False,
    "jobN": 0,
    "partN": 0,
    "partData": []
}


def main():
    global data
    utils.clear()
    utils.topbar("ML-M3: Act1 Fixed Partition - First Fit")

    memSize_status = utils.getinp(
        "Enter Memory Size (k): ",
        "Memory Size",
        "int",
        greaterThan = 0,
        flag = data["memFilled"],
        fallback = f"Memory Size: {data['memSize']}k"
        )
    if memSize_status == "input":
        return False # input skip
    elif memSize_status != "Valid":
        print(memSize_status)
        utils.pressEnter()
        return False
    else:
        data["memFilled"] = True
        data["memSize"] = float(data["memSize"])
    


    return True
    
while not complete:
    complete = main()