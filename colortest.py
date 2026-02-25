for codestoprnt in range(0, 256):
    print(f"\033[{codestoprnt}m{codestoprnt}\033[0m", end=" ")


class TextCodes:
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

    def color(text, color, style=None, bg=False, light=False):
        color_code = TextCodes.codes["colors"].get(color, None)
        if color_code:
            if bg:
                code = color_code["bg"][1] if light else color_code["bg"][0]
            else:
                code = color_code["text"][1] if light else color_code["text"][0]
            style_code = TextCodes.codes["styles"].get(style, "") if style else ""
            return f"{style_code}{code}{text}{TextCodes.codes['reset']}"
        return text
    
    def style(text, style, color=None, bg=False, light=False):
        style_code = TextCodes.codes["styles"].get(style, "")
        if color:
            color_code = TextCodes.codes["colors"].get(color, None)
            if color_code:
                if bg:
                    code = color_code["bg"][1] if light else color_code["bg"][0]
                else:
                    code = color_code["text"][1] if light else color_code["text"][0]
                return f"{style_code}{code}{text}{TextCodes.codes['reset']}"
        return f"{style_code}{text}{TextCodes.codes['reset']}"
    
    def reset(text):
        return f"{TextCodes.codes['reset']}{text}"


print(TextCodes.color(TextCodes.color("Hello, World!", "red", bg=True, style="blink", light=True), "red"))