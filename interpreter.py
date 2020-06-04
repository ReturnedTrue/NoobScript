from sys import *
version = "1.0"

def open_file(name):
    extension = name[-5:]
    if (not extension == ".noob"):
        raise NameError("Given file is not a .noob file!")

    
    return open(name, "r").read()

def getIndex(table, index):
    try:
        return table[index]
    except IndexError:
        return False
    return None

def lex(data):
    tokens = []
    current = ""
    inString = False
    string = ""

    for character in list(data):
        current += character

        if (current == " "):
            if (inString):
                current = " "
            else:
                current = ""

        elif (current == "noob"):
            tokens.append({
                "action": "PRINT"
            })
            current = ""
        
        elif (current == "NOOB"):
            tokens.append({
                "action": "UPPERCASE"
            })
            current = ""

        elif (current == "n00b"):
            tokens.append({
                "action": "LOWERCASE"
            })
            current = ""

        elif (character == "\""):
            if (inString):
                subtraction = 1

                while (True):
                    last = getIndex(tokens, len(tokens) - subtraction)
                    assignToLast = False
                    if (last and last["action"] == "UPPERCASE"):
                        string = string.upper()
                        assignToLast = True
                    elif (last and last["action"] == "LOWERCASE"):
                        string = string.lower()
                        assignToLast = True

                    info = {
                        "action": "STRING",
                        "content": string
                    }

                    if (assignToLast):
                        tokens[len(tokens) - subtraction] = info
                        subtraction = subtraction + 1
                    else:
                        tokens.append(info)
                        break

                string = ""
                inString = False
            else:
                current = ""
                inString = True

        elif (inString):
            string += current
            current = ""

        elif (current in "()"):
            current = ""
        
    return tokens

def parse(tokens):
    for index in range(len(tokens)):
        token = tokens[index]
        nextToken = getIndex(tokens, index + 1)

        if (token["action"] == "PRINT"):
            if (nextToken and nextToken["action"] == "STRING"):
                print(nextToken["content"])
            else:
                raise SyntaxError("NOOB! Expected string to print!")

if __name__ == "__main__":
    if (not getIndex(argv, 1) or argv[1] == " " or argv[1] == "-h"):
        print("NoobScript\nCall executable with file name to interpret\n-v to get version\n-h to display this help")
        
    elif (argv[1] == "-v"):
        print("NoobScript\nVersion: " + version)
    else:
        data = open_file(argv[1])
        if (data):
            tokens = lex(data)
            parse(tokens)
