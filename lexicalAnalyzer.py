import re


class token ():
    def __init__(self, value, line):
        self.type = "undefined"
        self.value = value
        self.line = line

    def displayToken(self):
        string = "\t(" + self.type + ", " + self.value + \
            ", " + str(self.line) + ")"
        return string


def intConst(word):
    pattern = "(^[+|-]?[0-9]+$)"
    success = re.match(pattern, word)
    if success:
        return True
    return False


def floatConst(word):
    pattern = "(^[+|-]?[0-9]*[.][0-9]+$)"
    success = re.match(pattern, word)
    if success:
        return True
    return False


def charConst(word):
    pattern = "(\'[\\sA-Za-z0-9-!@$#%^&*()+=;:<>,.?/{}[]|]\')"
    success = re.match(pattern, word)
    if success:
        return True
    return False


def stringConst(word):
    pattern = "(\"(.*)\")"
    success = re.match(pattern, word)
    if success:
        return True
    return False


def isIdentifier(word):
    pattern = "([A-Za-z]\\w*)"
    success = re.match(pattern, word)
    if success:
        return True
    return False


def generateToken(word, line, i):
    current_token = token(word, line)
    # string = str(line) + "\t" + word
    # print(string)
    i = i + 1
    return "", i, current_token


def breakWords(char):
    word = ""
    line = 1
    tokenlist = []
    single_breakers = [",",  ";", "(", ")", "{", "}", "[", "]",
                       "-", "+", "*", "/", "%", "=", ">", "<", "@", "!"]
    combo_breakers = ["||", "&&", ">=", "<=", "!=",
                      "++", "--", "+=", "-=", "*=", "/=", "=="]
    i = 0
    while (i < len(char)):
        checking = char[i]

        # Checking ASCII of New Line character
        if (char[i] == "\n"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
            else:
                i = i + 1
            line += 1
            continue

        # Checking ASCII of Space
        if (char[i] == " "):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
            else:
                i = i + 1
            continue

        # Checking for .
        if (char[i] == "."):
            if (word != ""):
                # If word contains only numbers then dot is a decimal
                if (word.isnumeric()):
                    word = word + char[i]
                    i = i + 1
                # If not then word and dot are separate
                else:
                    word, i, current_token = generateToken(word, line, i)
                    tokenlist.append(current_token)
                    i = i - 1

            if (i < len(char)):
                # If next character of dot is a number then dot is part of next and word continues
                checking = char[i+1]
                if (char[i+1].isnumeric()):
                    word = word + char[i]
                    i = i + 1
                # If next character of dot is not a number then dot is a separate word
                else:
                    word = word + char[i]
                    word, i, current_token = generateToken(word, line, i)
                    tokenlist.append(current_token)

            continue

        # Checking for Starting of a String (with double quote)
        if (char[i] == "\""):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
                i -= 1

            word = char[i]
            i = i + 1

            # String continues till File Ends, Next Double Quote or New Line Character
            while (i < len(char)):
                checking = char[i]
                if (i+1 < len(char)):
                    if (char[i] == "\\"):
                        checking = f"{char[i]}{char[i+1]}"
                        word = word + checking
                        i += 1
                        if (i+1 < len(char)):
                            i += 1
                            continue
                        else:
                            break

                if (char[i] != "\"" and char[i] != "\n"):
                    word = word + char[i]
                    i = i + 1
                else:
                    break

            if (char[i] == "\n"):
                line += 1

            # Breaking String if Double Quote Appear
            if (i < len(char) and char[i] == "\""):
                word = word + char[i]

            word, i, current_token = generateToken(word, line, i)
            tokenlist.append(current_token)
            continue

        # Checking for Starting of a Character (with single quote)
        if (char[i] == "\'"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
                i -= 1

            word = char[i]
            i = i + 1

            # Character continues till File Ends, New Line Character or Length (3 or 4)
            can_be = 3
            while (i < len(char) and char[i] != "\n" and len(word) < can_be):
                checking = char[i]
                word = word + char[i]
                if (word[1] == "\\"):
                    can_be = 4
                i = i + 1

            word, i, current_token = generateToken(word, line, i)
            tokenlist.append(current_token)
            i -= 1
            continue

        # Combo Breaking Word Appear
        if (i + 1 < len(char)):
            checking = f"{char[i]}{char[i+1]}"
        if (i + 1 < len(char) and f"{char[i]}{char[i+1]}" in combo_breakers):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
                i = i - 1

            word = f"{char[i]}{char[i+1]}"
            word, i, current_token = generateToken(word, line, i)
            tokenlist.append(current_token)
            i = i + 1
            continue

        # Single Character Breaking Word Appear
        if (char[i] in single_breakers):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
                i = i - 1

            word = char[i]
            word, i, current_token = generateToken(word, line, i)
            tokenlist.append(current_token)
            continue

        # Comment Character Appear
        if (char[i] == "$"):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenlist.append(current_token)
            else:
                i = i + 1

            if (i < len(char)):
                checking = char[i]
                # Multi Line Comment Characters Appear
                if (char[i] == "#"):
                    i = i + 1
                    # Itteration till the Ending Comment character Appear or File Ends
                    while (i < len(char)):
                        checking = char[i]
                        if (char[i] == "\n"):
                            line += 1
                        if (char[i] == "#" and char[i+1] == "$"):
                            i = i + 1
                            break
                        i = i + 1
                    i = i + 1
                    continue

                # Single Line Comment Character
                else:
                    # Itteration till the line ends or File Ends
                    while (i < len(char)):
                        checking = char[i]
                        if (char[i] == "\n"):
                            line += 1
                            break
                        i = i + 1
                    i = i + 1
                    continue

        # Character added to word if no breaking occurs
        word = word + char[i]
        i = i + 1

    # End of File with last word not Breaked
    if (word != ""):
        word, i, current_token = generateToken(word, line, i)
        tokenlist.append(current_token)

    # End Marker token... to ensure complete tree and complete input parsing
    tokenlist.append(token("~", line))

    return tokenlist


def classifyToken(tokenlist):
    keywords = {"~": "EOF", "true": "BOOL", "false": "BOOL", "if": "IF", "else": "ELSE", "do": "DO", "while": "WHILE",
                "for": "FOR", "switch": "SWITCH", "case": "CASE", "default": "DEFAULT", "continue": "CONTINUE",
                "break": "BREAK", "return": "RETURN", "void": "VOID", "class": "CLASS", "condensed": "CONDENSED",
                "symbol": "SYMBOL", "static": "STATIC", "function": "FUNCTION", "self": "CHAIN", "parent": "CHAIN",
                "public": "PUBLIC", "private": "PRIVATE", "preserved": "PRESERVED", "expands": "EXPANDS",
                "applies": "APPLIES", "concrete": "CONCRETE", "try": "TRY", "catch": "CATCH", "finally": "FINALLY",
                "throw": "THROW", "dict": "DICT", "int": "DT", "string": "DT", "exception": "EXCEPTION",
                "bool": "DT", "float": "DT", "char": "DT", "Main": "MAIN_METHOD", "new": "NEW"}
    operators = {"+": "P_M", "-": "P_M", "*": "M_D_M", "/": "M_D_M", "%": "M_D_M", "<": "R_OP", "<=": "R_OP", ">": "R_OP",
                 ">=": "R_OP", "!=": "R_OP", "==": "R_OP", "&&": "AND", "||": "OR", "!": "EXCLAIM", "=": "ASSIGN",
                 "++": "INC_DEC", "--": "INC_DEC", "+=": "COMP_ASSIGN", "-=": "COMP_ASSIGN", "*=": "COMP_ASSIGN",
                 "/=": "COMP_ASSIGN"}
    punctuators = {";": "SEMI_COL", ",": "COMMA", "(": "O_PARAN", ")": "C_PARAN", "{": "O_BRACE", "}": "C_BRACE",
                   "[": "O_BRACK", "]": "C_BRACK", ".": "TERMINATOR", ":": "COLON"}

    for i in range(len(tokenlist)):

        if (tokenlist[i].value in keywords.keys()):
            tokenlist[i].type = keywords[tokenlist[i].value]
            if (tokenlist[i].type == tokenlist[i].value.upper()):
                tokenlist[i].value = ""
            # print(tokenlist[i].displayToken())
            continue

        if (tokenlist[i].value in operators.keys()):
            tokenlist[i].type = operators[tokenlist[i].value]
            if (tokenlist[i].type == tokenlist[i].value.upper()):
                tokenlist[i].value = ""
            # print(tokenlist[i].displayToken())
            continue

        if (tokenlist[i].value in punctuators.keys()):
            tokenlist[i].type = punctuators[tokenlist[i].value]
            if (tokenlist[i].type == tokenlist[i].value.upper()):
                tokenlist[i].value = ""
            # print(tokenlist[i].displayToken())
            continue

        if (intConst(tokenlist[i].value)):
            tokenlist[i].type = "INT"
            # print(tokenlist[i].displayToken())
            continue

        if (floatConst(tokenlist[i].value)):
            tokenlist[i].type = "FLT"
            # print(tokenlist[i].displayToken())
            continue

        if (charConst(tokenlist[i].value)):
            tokenlist[i].type = "CHAR"
            tokenlist[i].value = tokenlist[i].value[1:-1]
            # print(tokenlist[i].displayToken())
            continue

        if (stringConst(tokenlist[i].value)):
            tokenlist[i].type = "STR"
            tokenlist[i].value = tokenlist[i].value[1:-1]
            # print(tokenlist[i].displayToken())
            continue

        if (isIdentifier(tokenlist[i].value)):
            tokenlist[i].type = "ID"
            # print(tokenlist[i].displayToken())
            continue

        tokenlist[i].type = "INVALID"
        # print(tokenlist[i].displayToken())

    return tokenlist


def generateOuput(tokens):
    output = "TOKENLIST:\n"
    for i in range(len(tokens)):
        if (i == len(tokens)-1):
            output = output + str(i) + "\t"
            output = output + tokens[i].displayToken()
            continue
        output = output + str(i) + "\t"
        output = output + tokens[i].displayToken() + "\n"
    return output


# with open("D:\\Uni Kaam\\3rd Year\\6th Semester\\CC\\MyProject\\inputFile.txt", "r") as inputfile:
#     input_text = inputfile.read()

# # generatedTokens = breakWords(input_text)
# # classifiedTokens = classifyToken(generatedTokens)
# # output_text = generateOuput(classifiedTokens)

# with open("D:\\Uni Kaam\\3rd Year\\6th Semester\\CC\\MyProject\\outputFile.txt", "w") as outputfile:
#     outputfile.write(generateOuput(classifyToken(breakWords(input_text))))
