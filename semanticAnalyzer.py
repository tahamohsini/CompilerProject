# import sys

from lexicalAnalyzer import token
from semanticFunctions import createScope, destroyScope, insertAttribute, insertFunctionTable, insertMainTable, lookupAttributeTable, lookupFunctionTable, lookupMainTable, scopeStack_, binTypeCompatible, uniTypeCompatible, mainTable_, functionTable_


i = 0
tokenList = []
# syntaxErr = True
error = ""

currentClass = ""
currentFunction = 0
currentScope = 0


def semanticAnalyzer(tokens):
    global i, tokenList
    i = 0
    tokenList = tokens
    result = structure()
    print(report())
    return result


def report():
    global currentClass, currentFunction, currentScope, scopeStack_, errorAt, mainTable_, functionTable_, error
    report = error + "\n"
    report += "\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\n"
    report += "\t\t\t\t\t\t  R\t  E\t  P\t  O\t  R\t  T\n"
    report += "\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\n\n"
    report += "\nLast Updated Class:\t" + currentClass + "\n"
    report += "Last Function Scope:\t" + str(currentFunction) + "\n"
    report += "Scope @ End:\t\t" + str(currentScope) + "\n\n"
    report += "###########################################################################\n"
    report += "Main Table:\n\n"
    for i in mainTable_:
        report += "Name:\t\t'" + i.name + "'\nType:\t\t'" + i.type + \
            "'\nTypeMod:\t'" + i.typeMod + "'\nParent:\t\t'" + i.parent + "'\n"
        report += "Attributes:\n"
        for j in i.attrTable:
            report += str(vars(j))
            report += "\n"
        report += "-------------------------\n"
    report += "\n"
    report += "###########################################################################\n"
    report += "Function Table:\n\n"
    for i in functionTable_:
        report += str(vars(i))
        report += "\n"
    return report


def syntaxError():
    global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_, errorAt
    return False


def reDeclarationError(name, detail):
    global i, error
    error += "\n\t***  Re-Declaration Error  ***\n\tID:\t\t" + name + "\n\tAs:\t\t" + \
        detail, "\n\tLine #:\t       ", str(tokenList[i].line) + "\n"
    return


def unDeclaredError(name, detail):
    global i, error
    error += "\n\t***  Un-Declared Error  ***\n\tID:\t\t" + name + "\n\tAs:\t\t" + \
        detail + "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def binTypeMismatchedError(left, right, op):
    global i, error
    error += "\n\t***  Type Mismatched Error  ***\n\t"+"Cant Apply:\t" + op + " on " + \
        left + " and " + right + \
        "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def uniTypeMismatchedError(operand, op):
    global i, error
    error += "\n\t***  Type Mismatched Error  ***\n\t"+"Cant Apply:\t" + op, " on " + \
        operand + "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def randomError(note):
    global i, error
    error += "\n\t***  Exception Unhandled  ***\n\t" + note + \
        "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def checkConstructor(check):
    length = len(check.attrTable)
    if (length == 0):
        return True
    count = 0
    for i in check.attrTable:
        if (i.name == check.name):
            if (i.params == ""):
                return True
            count += 1
    if (count > 0):
        randomError(
            check.name + " class doesn't contain no parameterized constructor.")
        return False
    return True


try:

    def structure():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "STATIC"):
            typeMod = tokenList[i].type
            i += 1
            if (tokenList[i].type == "CLASS"):
                entryOf = tokenList[i].type
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    parent, check = inherit()
                    if (check):
                        check = insertMainTable(name, entryOf, typeMod, parent)
                        if (check == False):
                            reDeclarationError(name, "Static Class")
                            return False
                        currentClass = name
                        if (tokenList[i].type == "O_BRACE"):
                            currentScope = createScope()
                            i += 1
                            check = sCst()
                            if (check):
                                if (tokenList[i].type == "EOF"):
                                    return True
        elif (tokenList[i].type == "CONDENSED"):
            typeMod = tokenList[i].type
            i += 1
            if (tokenList[i].type == "CLASS"):
                entryOf = tokenList[i].type
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    parent, check = inherit()
                    if (check):
                        check = insertMainTable(name, entryOf, typeMod, parent)
                        if (check == False):
                            reDeclarationError(name, "Condensed Class")
                            return False
                        currentClass = name
                        if (tokenList[i].type == "O_BRACE"):
                            currentScope = createScope()
                            i += 1
                            check = cCst()
                            if (check):
                                if (tokenList[i].type == "EOF"):
                                    return True
        else:
            typeMod, check = concrete_()
            if (check and tokenList[i].type == "CLASS"):
                entryOf = tokenList[i].type
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    parent, check = inherit()
                    if (check):
                        check = insertMainTable(name, entryOf, typeMod, parent)
                        if (check == False):
                            reDeclarationError(name, "General Class")
                            return False
                        currentClass = name
                        if (tokenList[i].type == "O_BRACE"):
                            currentScope = createScope()
                            i += 1
                            check = gCst()
                            if (check):
                                if (tokenList[i].type == "EOF"):
                                    return True
            elif (tokenList[i].type == "SYMBOL"):
                entryOf = tokenList[i].type
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    check = insertMainTable(name, entryOf, "", "")
                    if (check == False):
                        reDeclarationError(name, "Symbol")
                        return False
                    currentClass = name
                    if (tokenList[i].type == "O_BRACE"):
                        currentScope = createScope()
                        i += 1
                        check = intSt()
                        if (check):
                            if (tokenList[i].type == "C_BRACE"):
                                currentScope = destroyScope()
                                i += 1
                                check = structure()
                                if (check):
                                    if (tokenList[i].type == "EOF"):
                                        return True
        return syntaxError()

    def sCst():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            currentScope = destroyScope()
            i += 1
            check = lookupMainTable(currentClass)
            check = checkConstructor(check)
            if (check):
                return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            accessMod, check = pubPriv_()
            if (check):
                if (tokenList[i].type == "STATIC"):
                    static = 1
                    i += 1
                    check = functionSig(accessMod, static, "")
                    if (check):
                        return sCst()
        elif (tokenList[i].type == "PRIVATE"):
            accessMod = tokenList[i].type
            i += 1
            if (tokenList[i].type == "STATIC"):
                stat = tokenList[i].type
                i += 1
            check = classVars(accessMod, stat, "")
            if (check):
                return sCst()
        else:
            accessMod, check = public_()
            if (check and tokenList[i].type == "STATIC"):
                static = tokenList[i].type
                i += 1
                return sCst_(accessMod, static)
        return syntaxError()

    def public_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        accessMod = "PUBLIC"
        if (tokenList[i].type == "PUBLIC"):
            i += 1
            return accessMod, True
        elif (tokenList[i].type == "STATIC" or tokenList[i].type == "CONCRETE" or tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "VOID" or tokenList[i].type == "DICT"):
            return accessMod, True
        return accessMod, syntaxError()

    def inherit():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        parent = ""
        parClass, check = expands()
        if (check):
            parSymbol, check = applies()
            if (check):
                if (parClass != "" and parSymbol != ""):
                    parent = parClass + "," + parSymbol
                else:
                    parent = parClass + parSymbol
                return parent, True
        return parent, syntaxError()

    def expands():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        parClass = ""
        if (tokenList[i].type == "EXPANDS"):
            i += 1
            if (tokenList[i].type == "ID"):
                id = tokenList[i].value
                check = lookupMainTable(id)
                if (check == False):
                    unDeclaredError(id, "Parent Class")
                    return parClass, False
                if (check.type != "CLASS"):
                    randomError(
                        "Class should be inherited from a class.")
                    return parClass, False
                if (check.typeMod == "CONCRETE" or check.typeMod == "STATIC"):
                    randomError("class can't be inherited from " +
                                check.typeMod.lower() + " class.")
                    return parClass, False
                parClass = parClass + id
                i += 1
                return parClass, True
        elif (tokenList[i].type == "APPLIES" or "O_BRACE"):
            return parClass, True
        return parClass, syntaxError()

    def applies():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        parSymbol = ""
        if (tokenList[i].type == "APPLIES"):
            i += 1
            if (tokenList[i].type == "ID"):
                id = tokenList[i].value
                check = lookupMainTable(id)
                if (check == False):
                    unDeclaredError(id, "Parent Symbol")
                    return parSymbol, False
                if (check.type != "SYMBOL"):
                    randomError(
                        "APPLIES should be followed by a SYMBOL Identifier")
                    return parSymbol, False
                if (parSymbol != ""):
                    parSymbol += ","
                parSymbol = parSymbol + id
                i += 1
                return applies_(parSymbol)
        elif (tokenList[i].type == "O_BRACE"):
            return parSymbol, True
        return parSymbol, syntaxError()

    def applies_(parSymbol):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                id = tokenList[i].value
                check = lookupMainTable(id)
                if (check == False):
                    unDeclaredError(id, "Parent Symbol")
                    return parSymbol, False
                parSymbol = parSymbol + "," + id
                i += 1
                return applies_(parSymbol)
        elif (tokenList[i].type == "O_BRACE"):
            return parSymbol, True
        return syntaxError()

    def pubPriv_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        accessMod = ""
        if (tokenList[i].type == "PUBLIC" or tokenList[i].type == "PRIVATE"):
            accessMod = tokenList[i].type
            i += 1
            return accessMod, True
        elif (tokenList[i].type == "STATIC"):
            accessMod = "PUBLIC"
            return accessMod, True
        return accessMod, syntaxError()

    def functionSig(accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        ofType, check = returnType()
        if (check and tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                currentScope = createScope()
                currentFunction = currentScope
                i += 1
                paramList, check = argumentList()
                if(check and tokenList[i].type == "C_PARAN"):
                    i += 1
                    check = insertAttribute(
                        name, paramList, ofType, accessMod, static, concCond, currentClass)
                    if (check == False):
                        reDeclarationError(
                            name, "Method in '" + currentClass + "'")
                        return False
                    check = bodyMST()
                    if(check):
                        return True
        return syntaxError()

    def returnType():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "DT" or tokenList[i].type == "ID"):
            retType = tokenList[i].value
            if (tokenList[i].type == "ID"):
                check = lookupMainTable(retType)
                if (check == False):
                    unDeclaredError(
                        retType, "Can't return object of this type.")
                    return "", False
                if (check.type == "STATIC" or check.type == "CONDENSED"):
                    randomError("Can't return object of " +
                                check.type+" class.")
                    return "", False
            i += 1
            return returnType_(retType)
        elif (tokenList[i].type == "VOID"):
            retType = tokenList[i].type
            i += 1
            return retType, True
        elif (tokenList[i].type == "DICT"):
            i += 1
            if (tokenList[i].type == "O_BRACK"):
                i += 1
                if (tokenList[i].type == "C_BRACK"):
                    i += 1
                    return retType, True
        return retType, syntaxError()

    def returnType_(retType):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                retType += "[]"
                i += 1
                return retType, True
        elif (tokenList[i].type == "ID"):
            return retType, True
        return retType, syntaxError()

    def argumentList():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        paramList = ""
        if (tokenList[i].type == "C_PARAN"):
            return paramList, True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT"):
            return argumentList_(paramList)
        return paramList, syntaxError()

    def argumentList_(paramList):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT" or tokenList[i].type == "ID"):
            if (tokenList[i].type == "ID"):
                check = lookupMainTable(tokenList[i].value)
                if (check == False):
                    unDeclaredError(
                        tokenList[i].value, "Can't receive object of this type as argument.")
                    return "", False
                if (check.type == "STATIC" or check.type == "CONDENSED"):
                    randomError(check.type + " class can't be instantiated.")
                    return "", False
            varType = tokenList[i].value
            paramList += tokenList[i].value
            i += 1
            check = argumentList___()
            if(check and tokenList[i].type == "ID"):
                name = tokenList[i].value
                check = insertFunctionTable(name, varType, currentScope)
                if (check == False):
                    reDeclarationError(name, "In Function Parameter List")
                    return paramList, False
                i += 1
                return argumentList__(paramList)
        if (tokenList[i].type == "DICT"):
            i += 1
            if (tokenList[i].type == "O_BRACK"):
                i += 1
                if (tokenList[i].type == "C_BRACK"):
                    i += 1
                    if (tokenList[i].type == "ID"):
                        i += 1
                        return argumentList__(paramList)
        return paramList, syntaxError()

    def argumentList__(paramList):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_PARAN"):
            return paramList, True
        elif (tokenList[i].type == "COMMA"):
            paramList += ","
            i += 1
            return argumentList_(paramList)
        return paramList, syntaxError()

    def argumentList___():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        elif (tokenList[i].type == "ID"):
            return True
        return syntaxError()

    def bodyMST():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_BRACE"):
            i += 1
            check = mst()
            if (check):
                tokenList[i].type == "C_BRACE"
                if (currentFunction == scopeStack_[0]):
                    # print("\tMethod Scope:\t", currentFunction)
                    currentFunction == 0
                # else:
                #     print("\tMethod Scope:\t", currentFunction)
                currentScope = destroyScope()
                i += 1
                return True
        return syntaxError()

    def mst():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE" or tokenList[i].type == "CASE" or tokenList[i].type == "DEFAULT"):
            return True
        if (tokenList[i].type == "SWITCH" or tokenList[i].type == "IF" or tokenList[i].type == "FOR" or tokenList[i].type == "WHILE" or tokenList[i].type == "DO" or tokenList[i].type == "RETURN" or tokenList[i].type == "CONTINUE" or tokenList[i].type == "BREAK" or tokenList[i].type == "TRY" or tokenList[i].type == "INC_DEC" or tokenList[i].type == "CHAIN" or tokenList[i].type == "DT" or tokenList[i].type == "DICT" or tokenList[i].type == "ID" or tokenList[i].type == "THROW"):
            check = sst()
            if (check):
                return mst()
        return syntaxError()

    def sst():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SWITCH"):
            return switchSt()
        elif (tokenList[i].type == "IF"):
            return ifSt()
        elif (tokenList[i].type == "FOR"):
            return forSt()
        elif (tokenList[i].type == "WHILE"):
            return whileSt()
        elif (tokenList[i].type == "DO"):
            return doWhileSt()
        elif (tokenList[i].type == "RETURN"):
            return returnSt()
        elif (tokenList[i].type == "CONTNIUE"):
            return continueSt()
        elif (tokenList[i].type == "BREAK"):
            return breakSt()
        elif (tokenList[i].type == "TRY"):
            return trySt()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            searchIn, check = sp_()
            if (check and tokenList[i].type == "ID"):
                return ref()
        elif (tokenList[i].type == "CHAIN"):
            i += 1
            if (tokenList[i].type == "TERMINATOR"):
                i += 1
                if (tokenList[i].type == "ID"):
                    check = ref()
                    if (check):
                        op, check = assignOp()
                        if (check):
                            type_, check = expression()
                            if (check and tokenList[i].type == "SEMI_COL"):
                                i += 1
                                return True
        elif (tokenList[i].type == "DT"):
            i += 1
            return nDec()
        elif (tokenList[i].type == "DICT"):
            i += 1
            return multiArr()
        elif (tokenList[i].type == "ID"):
            i += 1
            return sstID()
        elif (tokenList[i].type == "THROW"):
            i += 1
            check = throw_()
            if (check and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def throw_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "EXCEPTION"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (tokenList[i].type == "O_PARAN"):
                        i += 1
                        check = throw__()
                        if (check and tokenList[i].type == "C_PARAN"):
                            return True
        return syntaxError()

    def throw__():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "STR"):
            i += 1
            return True
        return syntaxError()

    def switchSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SWITCH"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (tokenList[i].type == "O_BRACE"):
                            i += 1
                            check = switchBody()
                            if (check and tokenList[i].type == "C_BRACE"):
                                i += 1
                                return True
        return syntaxError()

    def switchBody():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "CASE" or tokenList[i].type == "DEFAULT"):
            check = case()
            if (check):
                check = default()
                if (check):
                    return True
        return syntaxError()

    def case():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "case"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                constType, check = const()
                if(check and tokenList[i].type == "C_PARAN"):
                    i += 1
                    if (tokenList[i].type == "COLON"):
                        i += 2
                        check = mst()
                        if(check):
                            return case()
        elif (tokenList[i].type == "DEFAULT" or tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def default():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DEFAULT"):
            i += 1
            if (tokenList[i].type == "COLON"):
                i += 1
                check = mst()
                if (check):
                    return case()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def const():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        ofType = ""
        if (tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "CHAR" or tokenList[i].type == "BOOL"):
            if (tokenList[i].type == "INT"):
                ofType = "int"
            if (tokenList[i].type == "FLT"):
                ofType = "float"
            if (tokenList[i].type == "CHAR"):
                ofType = "char"
            if (tokenList[i].type == "STR"):
                ofType = "string"
            if (tokenList[i].type == "BOOL"):
                ofType = "bool"
            i += 1
            return ofType, True
        return ofType, syntaxError()

    def ifSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "IF"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                type_, check = expression()
                if (check):
                    if (tokenList[i].type == "C_PARAN"):
                        i += 1
                        check = bodyMST()
                        if (check):
                            check = oElse()
                            if (check):
                                return True
        return syntaxError()

    def oElse():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "else"):
            i += 1
            return oElse_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def oElse_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "IF"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                type_, check = expression()
                if (check):
                    if (tokenList[i].type == "C_PARAN"):
                        i += 1
                        check = bodyMST()
                        if (check):
                            return oElse()
        else:
            check = bodyMST()
            if (check):
                return True
        return syntaxError()

    def expression():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = b()
            if (check):
                retType, check = a_(type_)
                if (check):
                    return retType, True
        return retType, syntaxError()

    def a_(typeIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "OR"):
            op = tokenList[i].value
            i += 1
            type_, check = b()
            typeOut = binTypeCompatible(typeIn, type_, op)
            if (typeOut == False):
                binTypeMismatchedError(typeIn, type_, op)
                return "", False
            if (check):
                typeIn, check = a_(typeOut)
                if (check):
                    return typeIn, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return typeIn, True
        return typeIn, syntaxError()

    def b():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = c()
            if (check):
                retType, check = b_(type_)
                if (check):
                    return retType, True
        return retType, syntaxError()

    def b_(typeIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "AND"):
            op = tokenList[i].value
            i += 1
            type_, check = c()
            typeOut = binTypeCompatible(typeIn, type_, op)
            if (typeOut == False):
                binTypeMismatchedError(typeIn, type_, op)
                return "", False
            if (check):
                typeIn, check = b_(typeOut)
                if (check):
                    return typeIn, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return typeIn, True
        return typeIn, syntaxError()

    def c():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = e()
            if (check):
                retType, check = c_(type_)
                if (check):
                    return retType, True
        return retType, syntaxError()

    def c_(typeIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "R_OP"):
            op = tokenList[i].value
            i += 1
            type_, check = e()
            typeOut = binTypeCompatible(typeIn, type_, op)
            if (typeOut == False):
                binTypeMismatchedError(typeIn, type_, op)
                return "", False
            if (check):
                typeIn, check = c_(typeOut)
                if (check):
                    return typeIn, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return typeIn, True
        return typeIn, syntaxError()

    def e():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = t()
            if (check):
                retType, check = e_(type_)
                if (check):
                    return retType, True
        return retType, syntaxError()

    def e_(typeIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "P_M"):
            op = tokenList[i].value
            i += 1
            type_, check = t()
            typeOut = binTypeCompatible(typeIn, type_, op)
            if (typeOut == False):
                binTypeMismatchedError(typeIn, type_, op)
                return "", False
            if (check):
                typeIn, check = e_(typeOut)
                if (check):
                    return typeIn, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return typeIn, True
        return typeIn, syntaxError()

    def t():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        retType = ""
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = f()
            if (check):
                retType, check = t_(type_)
                if (check):
                    return retType, True
        return retType, syntaxError()

    def t_(typeIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "M_D_M"):
            op = tokenList[i].value
            i += 1
            type_, check = f()
            typeOut = binTypeCompatible(typeIn, type_, op)
            if (typeOut == False):
                binTypeMismatchedError(typeIn, type_, op)
                return "", False
            if (check):
                typeIn, check = t_(typeOut)
                if (check):
                    return typeIn, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return typeIn, True
        return typeIn, syntaxError()

    def f():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        type_ = ""
        if (tokenList[i].type == "O_PARAN"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_PARAN"):
                return type_, True
        else:
            type_, check = const()
            if (check):
                return type_, True
            elif (tokenList[i].type == "EXCLAIM"):
                op = tokenList[i].value
                i += 1
                type_, check = f()
                typeOut = uniTypeCompatible(type_, op)
                if (typeOut == False):
                    uniTypeMismatchedError(type_, op)
                return "", False
            else:
                searchIn, check = sp_()
                if (check and tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return optF(name, searchIn)
        return type_, syntaxError()

    def sp_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        searchIn = ""
        if (tokenList[i].type == "CHAIN"):
            searchIn = tokenList[i].value
            if (searchIn == "parent"):
                check = lookupMainTable(currentClass)
                if (check == False):
                    randomError(currentClass, " isnt inherited from any Class")
                    return "", False
                searchIn = check
            else:
                searchIn = currentClass
            i += 1
            if (tokenList[i].type == "TERMINATOR"):
                i += 1
                return searchIn, True
        elif (tokenList[i].type == "ID"):
            return searchIn, True
        return searchIn, syntaxError()

    def optF(name, searchIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        type_ = ""
        if (tokenList[i].type == "TERMINATOR"):
            if (searchIn == ""):
                check = lookupFunctionTable(name)
                if (check == False):
                    unDeclaredError(name, "Not accessible in current Scope")
                    return "", False
                if (check == "int" or check == "float" or check == "char" or check == "string" or check == "bool"):
                    randomError(
                        name, " is of Primitive Data Type, can't Refer")
                    return "", False
                searchIn = check
            else:
                check = lookupAttributeTable(name, "~", searchIn)
                if (check == False):
                    unDeclaredError(name, "un Declared in ", searchIn)
                    return "", False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                type_ = check.type
                if (type_ == "int" or type_ == "float" or type_ == "char" or type_ == "string" or type_ == "bool"):
                    randomError(
                        name, " is of Primitive Data Type, can't Refer in ", searchIn)
                    return "", False
                searchIn = type_
            i += 1
            if (tokenList[i].type == "ID"):
                name = tokenList[i].value
                i += 1
                return optF(name, searchIn)
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return optF1(name, searchIn)
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            param, check = pl()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                return optF_(name, searchIn, param)
        elif (tokenList[i].type == "INC_DEC"):
            op = tokenList[i].value
            if (searchIn == ""):
                check = lookupFunctionTable(name)
                if (check == False):
                    unDeclaredError(name, "Not accessible in current Scope")
                    return "", False
                type_ = uniTypeCompatible(check, op)
                if (type_ == False):
                    uniTypeMismatchedError(type_, op)
                    return "", False
            else:
                check = lookupAttributeTable(name, "~", searchIn)
                if (check == False):
                    unDeclaredError(name, "un Declared in ", searchIn)
                    return "", False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                check = check.type
                type_ = uniTypeCompatible(check, op)
                if (type_ == False):
                    uniTypeMismatchedError(check, op)
                    return "", False
            i += 1
            return type_, True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            if (searchIn == ""):
                check = lookupFunctionTable(name)
                if (check == False):
                    unDeclaredError(name, "Not accessible in current Scope")
                    return type_, False
                type_ = check
            else:
                check = lookupAttributeTable(name, "~", searchIn)
                if (check == False):
                    unDeclaredError(name, "un Declared in ", searchIn)
                    return type_, False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                type_ = check.type
            return type_, True
        return type_, syntaxError()

    def optF1(name, searchIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        type_ = ""
        if (tokenList[i].type == "INC_DEC"):
            i += 1
            return type_, True
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return optF(name, searchIn)
        return type_, syntaxError()

    def optF_(name, searchIn, param):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        type_ = ""
        if (searchIn == ""):
            searchIn = currentClass
        check = lookupAttributeTable(name, param, searchIn)
        if (check == False):
            unDeclaredError(name, "un Declared in ", searchIn)
            return type_, False
        if (searchIn != currentClass):
            if (check.accessMod == "PRIVATE"):
                randomError("Can't access 'private' Modified variable")
                return "", False
        type_ = check.type
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (type_ == "int" or type_ == "float" or type_ == "char" or type_ == "string" or type_ == "bool"):
                randomError(
                    name, " is of Primitive Data Type, can't Refer in ", searchIn)
                return "", False
            searchIn = type_
            if (tokenList[i].type == "ID"):
                name = tokenList[i].value
                i += 1
                return optF(name, searchIn)
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return type_, True
        return type_, syntaxError()

    def pl():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        paramList = ""
        if (tokenList[i].type == "C_PARAN"):
            return paramList, True
        elif (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            type_, check = expression()
            paramList += type_
            if (check):
                return pl_(paramList)
        return paramList, syntaxError()

    def pl_(paramList):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "COMMA"):
            paramList += ","
            i += 1
            type_, check = expression()
            paramList += type_
            if (check):
                return pl_(paramList)
        elif (tokenList[i].type == "C_PARAN"):
            return paramList, True
        return paramList, syntaxError()

    def forSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FOR"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                check = st1()
                if(check):
                    type_, check = expression()
                    if (check and tokenList[i].type == "SEMI_COL"):
                        i += 1
                        check = st3()
                        if (check and tokenList[i].type == "C_PARAN"):
                            return body()
        return syntaxError()

    def body():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "O_BRACE"):
            return bodyMST()
        return syntaxError()

    def st1():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return declare_()
        else:
            searchIn, check = sp_()
            if (check and tokenList[i].type == "ID"):
                i += 1
                check = ref()
                if (check):
                    op, check = assignOp()
                    if (check):
                        type_, check = expression()
                        if (check and tokenList[i].type == "SEMI_COL"):
                            i += 1
                            return True
        return syntaxError()

    def ref():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return ref_()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            param, check = pl()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (tokenList[i].type == "TERMINATOR"):
                    i += 1
                    if (tokenList[i].type == "ID"):
                        i += 1
                        return ref()
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            return True
        return syntaxError()

    def ref_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return ref_()
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            return True
        return syntaxError()

    def assignOp():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        op = ""
        if (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            op = tokenList[i].value
            i += 1
            return op, True
        return op, syntaxError()

    def st3():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "INC_DEC"):
            i += 1
            searchIn, check = sp_()
            if (check and tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "ID"):
            i += 1
            return forOpt()
        elif (tokenList[i].type == "C_PARAN"):
            return True
        return syntaxError()

    def forOpt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                return forOpt1()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            param, check = pl()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return forOpt()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return forOpt_()
        else:
            op, check = assignOp()
            if (check):
                type_, check = expression()
                if (check):
                    return forOpt_()
        return syntaxError()

    def forOpt1():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return forOpt_()
        else:
            op, check = assignOp()
            if (check):
                type_, check = expression()
                if (check):
                    return forOpt_()
        return syntaxError()

    def forOpt_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        return syntaxError()

    def whileSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "WHILE"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                return body()
        return syntaxError()

    def doWhileSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DO"):
            i += 1
            check = bodyMST()
            if (check and tokenList[i].type == "WHILE"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    type_, check = expression()
                    if (check and tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (tokenList[i].type == "SEMI_COL"):
                            i += 1
                            return True
        return syntaxError()

    def returnSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "RETURN"):
            i += 1
            check = return_()
            if (check and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def return_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            return True
        else:
            type_, check = expression()
            if (check):
                return True
        return syntaxError()

    def continueSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "CONTNIUE"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def breakSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "BREAK"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def trySt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TRY"):
            i += 1
            check = bodyMST()
            if (check):
                check = catchFinally()
                if (check):
                    return True
        return syntaxError()

    def catchFinally():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FINALLY"):
            return finallyC()
        elif (tokenList[i].type == "CATCH"):
            check = catch()
            if (check):
                check = finallyC_()
                if (check):
                    return True
        return syntaxError()

    def finallyC():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FINALLY"):
            i += 1
            return bodyMST()
        return syntaxError()

    def catch():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "CATCH"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if (tokenList[i].type == "EXCEPTION"):
                    i += 1
                    if (tokenList[i].type == "ID"):
                        i += 1
                        if (tokenList[i].type == "C_PARAN"):
                            i += 1
                            check = bodyMST()
                            if (check):
                                return catch_()
        return syntaxError()

    def catch_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FINALLY" or tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "CATCH"):
            return catch()
        return syntaxError()

    def finallyC_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FINALLY"):
            i += 1
            return bodyMST()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def classVars(accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            ofType = tokenList[i].value
            i += 1
            return nDec(ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "ID"):
            ofType = tokenList[i].value
            check = lookupMainTable(ofType)
            if (check == False):
                unDeclaredError(ofType, "Can't create object.")
                return False
            if (check.type != "CLASS"):
                randomError("Can't create object of 'symbol'")
                return False
            if (check.typeMod == "CONDENSED" or check.typeMod == "STATIC"):
                randomError("Can't create object of '" +
                            check.typeMod.lower() + " class'")
                return False
            i += 1
            return oDec(check.name, accessMod, static, concCond)
        elif (tokenList[i].type == "dict"):
            i += 1
            return multiArr()
        return syntaxError()

    def consVar(accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            ofType = tokenList[i].value
            i += 1
            return nDec(ofType, accessMod, static, "")
        elif (tokenList[i].type == "ID"):
            ofType = tokenList[i].value
            i += 1
            return consVar_(ofType, accessMod, static)
        elif (tokenList[i].type == "dict"):
            i += 1
            return multiArr()
        return syntaxError()

    def consVar_(ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            param, check = argumentList()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (currentClass != ofType):
                    randomError(
                        "constructor and class name should be same.")
                    return False
                if (static != "" and param != ""):
                    randomError(
                        "class could not have parameterized static constructor")
                    return False
                check = insertAttribute(
                    ofType, param, ofType, accessMod, static, "", currentClass)
                if (check == False):
                    reDeclarationError(
                        ofType, "Constructor of class "+currentClass)
                    return False
                return bodyMST()
        elif (tokenList[i].type == "ID"):
            name = tokenList[i].value
            check = lookupMainTable(ofType)
            if (check == False):
                unDeclaredError(ofType, "Can't create object.")
                return False
            if (check.type != "CLASS"):
                randomError("Can't create object of 'symbol'")
                return False
            if (check.typeMod == "CONDENSED"):
                randomError("Can't create object of 'condensed class'")
                return False
            i += 1
            return object_(name, ofType, accessMod, static, "")
        elif (tokenList[i].type == "O_BRACE"):
            i += 1
            if (tokenList[i].type == "C_BRACE"):
                i += 1
                return oArr_()
        return syntaxError()

    def nDec(ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            return declare_(name, ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return gArr_()
        return syntaxError()

    def declare_(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (accessMod == ""):
            if (tokenList[i].type == "SEMI_COL"):
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, "Inside Scope No# ", currentScope)
                    return False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, "Inside Scope No# ", currentScope)
                    return False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return declare_(name, ofType, accessMod, static, concCond)
            elif (tokenList[i].type == "ASSIGN"):
                i += 1
                return initList(name, ofType, accessMod, static, concCond)
        else:
            if (tokenList[i].type == "SEMI_COL"):
                check = insertAttribute(
                    name, "~", ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Variable Declaration in '" + currentClass + "'")
                    return False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                check = insertAttribute(
                    name, "~", ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Variable Declaration in '" + currentClass + "'")
                    return False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return declare_(name, ofType, accessMod, static, concCond)
            elif (tokenList[i].type == "ASSIGN"):
                i += 1
                return initList(name, ofType, accessMod, static, concCond)
        return syntaxError()

    def initList(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        searchIn, check = sp_()
        if (check and tokenList[i].type == "ID"):
            idName = tokenList[i].value
            i += 1
            return list1(name, ofType, accessMod, static, concCond, idName, searchIn)
        else:
            constType, check = const()
            if (check):
                return list2(name, ofType, accessMod, static, concCond, constType)
            elif (tokenList[i].type == "O_PARAN"):
                i += 1
                type_, check = expression()
                if (check and tokenList[i].type == "C_PARAN"):
                    return list2(name, ofType, accessMod, static, concCond, type_)
            elif (tokenList[i].type == "EXCLAIM"):
                i += 1
                type_, check = f()
                if (check):
                    check = binTypeCompatible(ofType, type_, "=")
                    if (check == False):
                        binTypeMismatchedError(ofType, type_, "=")
                        return False
                    return initList_(name, ofType, accessMod, static, concCond)
        return syntaxError()

    def initList_(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (accessMod == ""):
            if (tokenList[i].type == "SEMI_COL"):
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, "Inside Scope No# ", currentScope)
                    return False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, "Inside Scope No# ", currentScope)
                    return False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return declare_(name, ofType, accessMod, static, concCond)
        else:
            if (tokenList[i].type == "SEMI_COL"):
                check = insertAttribute(
                    name, "~", ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Variable Declaration in '" + currentClass + "'")
                    return "", False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                check = insertAttribute(
                    name, "~", ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Variable Declaration in '" + currentClass + "'")
                    return "", False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return declare_(name, ofType, accessMod, static, concCond)
        return syntaxError()

    def list1(name, ofType, accessMod, static, concCond, idName, searchIn):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ASSIGN"):
            op = tokenList[i].value
            if (searchIn == ""):
                check = lookupFunctionTable(idName)
                if (check == False):
                    unDeclaredError(idName, "Not accessible in current Scope")
                    return False
            else:
                check = lookupAttributeTable(idName, "~", searchIn)
                if (check == False):
                    unDeclaredError(idName, "un Declared in ", searchIn)
                    return False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                check = check.type
            type_ = binTypeCompatible(ofType, check, op)
            if (type_ == False):
                binTypeMismatchedError(ofType, check, op)
                return False
            i += 1
            return initList(name, ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "TERMINATOR"):
            if (searchIn == ""):
                check = lookupFunctionTable(idName)
                if (check == False):
                    unDeclaredError(idName, "Not accessible in current Scope")
                    return False
            else:
                check = lookupAttributeTable(idName, "~", searchIn)
                if (check == False):
                    unDeclaredError(idName, "un Declared in ", searchIn)
                    return False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                check = check.type
            if (check == "int" or check == "float" or check == "char" or check == "string" or check == "bool"):
                randomError(
                    idName, " is of Primitive Data Type, can't Refer")
                return False
            searchIn = check
            i += 1
            if (tokenList[i].type == "ID"):
                idName = tokenList[i].value
                i += 1
                return list1(name, ofType, accessMod, static, concCond, idName, searchIn)
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return list3()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            param, check = pl()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (searchIn == ""):
                    searchIn = currentClass
                check = lookupAttributeTable(idName, param, searchIn)
                if (check == False):
                    unDeclaredError(idName, "un Declared in ", searchIn)
                    return False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                type_ = check.type
                return list2(name, ofType, accessMod, static, concCond, type_)
        elif (tokenList[i].type == "INC_DEC"):
            op = tokenList[i].value
            if (searchIn == ""):
                check = lookupFunctionTable(idName)
                if (check == False):
                    unDeclaredError(idName, "Not accessible in current Scope")
                    return False
            else:
                check = lookupAttributeTable(idName, "~", searchIn)
                if (check == False):
                    unDeclaredError(idName, "un Declared in ", searchIn)
                    return False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                check = check.type
            type_ = uniTypeCompatible(check, op)
            if (type_ == False):
                uniTypeMismatchedError(check, op)
                return False
            i += 1
            return list2(name, ofType, accessMod, static, concCond, type_)
        else:
            if (searchIn == ""):
                check = lookupFunctionTable(idName)
                if (check == False):
                    unDeclaredError(idName, "Not accessible in current Scope")
                    return False
            else:
                check = lookupAttributeTable(idName, "~", searchIn)
                if (check == False):
                    unDeclaredError(idName, "un Declared in ", searchIn)
                    return False
                if (searchIn != currentClass):
                    if (check.accessMod == "PRIVATE"):
                        randomError("Can't access 'private' Modified variable")
                        return "", False
                check = check.type
            type_ = check
            check = list2(name, ofType, accessMod, static, concCond, type_)
            if (check):
                return True
        return syntaxError()

    def list2(name, ofType, accessMod, static, concCond, type_):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "SEMI_COL" or tokenList[i].type == "COMMA"):
            type_, check = t_(type_)
            if (check):
                type_, check = e_(type_)
                if (check):
                    type_, check = c_(type_)
                    if (check):
                        type_, check = b_(type_)
                        if (check):
                            type_, check = a_(type_)
                            if (check):
                                check = binTypeCompatible(ofType, type_, "=")
                                if (check == False):
                                    binTypeMismatchedError(ofType, type_, "=")
                                    return False
                                check = initList_(
                                    name, ofType, accessMod, static, concCond)
                                if (check):
                                    return True
        return syntaxError()

    # Array Implementation
    def list3():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ASSIGN"):
            i += 1
            return initList()
        elif (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return list1()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return list2()
        else:
            check = list2()
            if (check):
                return True
        return syntaxError()

    # Array Implementation
    def gArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 2
                return gArr_()
        elif (tokenList[i].type == "ASSIGN"):
            i += 1
            check = initGArr()
            if (check):
                check = gArr_()
                if (check):
                    return True
        return syntaxError()

    # Array Implementation
    def initGArr():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "DT"):
                i += 1
                if (tokenList[i].type == "O_BRACK"):
                    i += 1
                    return initGArr_()
        return syntaxError()

    # Array Implementation
    def initGArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                check = valGArr()
                if (check and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        else:
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        return syntaxError()

    # Array Implementation
    def valGArr():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            return True
        else:
            constType, check = const()
            if (check):
                check = valGArr_()
                if (check):
                    return True
        return syntaxError()

    # Array Implementation
    def valGArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            constType, check = const()
            if (check):
                check = valGArr_()
                if (check):
                    return True
        return syntaxError()

    def oDec(ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            return object_(name, ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return oArr_()
        return syntaxError()

    def object_(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (accessMod == ""):
            if (tokenList[i].type == "SEMI_COL"):
                if (name != ""):
                    check = insertFunctionTable(name, ofType, currentScope)
                    if (check == False):
                        reDeclarationError(
                            name, "Inside Scope No# ", currentScope)
                        return False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                if (name != ""):
                    check = insertFunctionTable(name, ofType, currentScope)
                    if (check == False):
                        reDeclarationError(
                            name, "Inside Scope No# ", currentScope)
                        return False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return object_(name, ofType, accessMod, static, concCond)
            elif (tokenList[i].type == "ASSIGN"):
                i += 1
                check = initObject(name, ofType, accessMod, static, concCond)
                if (check):
                    return object_("", ofType, accessMod, static, concCond)
        else:
            if (tokenList[i].type == "SEMI_COL"):
                if (name != ""):
                    check = insertAttribute(
                        name, "~", ofType, accessMod, static, concCond, currentClass)
                    if (check == False):
                        reDeclarationError(
                            name, "Object decalaration in " + currentClass)
                        return False
                i += 1
                return True
            elif (tokenList[i].type == "COMMA"):
                if (name != ""):
                    check = insertAttribute(
                        name, "~", ofType, accessMod, static, concCond)
                    if (check == False):
                        reDeclarationError(
                            name, "Object decalaration in " + currentClass)
                        return False
                i += 1
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    return object_(name, ofType, accessMod, static, concCond)
            elif (tokenList[i].type == "ASSIGN"):
                i += 1
                check = initObject(name, ofType, accessMod, static, concCond)
                if (check):
                    return object_("", ofType, accessMod, static, concCond)
        return syntaxError()

    def initObject(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            idName = tokenList[i].value
            if (accessMod == ""):
                check = lookupFunctionTable(idName)
                if (check == False):
                    unDeclaredError(
                        idName, "Can't create another reference of it")
                    return False
                y = check
                while(True):
                    if (ofType == y):
                        break
                    else:
                        check = lookupMainTable(y)
                        check = lookupMainTable(check.parent.split(',')[0])
                        if (check == False):
                            randomError("Can't implicitly convert " +
                                        idName + " into " + name)
                            return False
                        if (check.type != "CLASS"):
                            randomError("Can't implicitly convert " +
                                        idName + " into " + name)
                            return False
                        y = check
                # Object of Child Class
                check = insertFunctionTable(name, y, currentScope)
                if (check == False):
                    reDeclarationError(name, "Inside Scope No# ", currentScope)
                    return False
            else:
                check = lookupAttributeTable(idName, "~", currentClass)
                if (check == False):
                    unDeclaredError(
                        idName, "Can't create another reference of it")
                    return False
                y = check
                while(True):
                    if (ofType == y.type):
                        break
                    else:
                        check = lookupMainTable(y.name)
                        check = lookupMainTable(check.parent.split(',')[0])
                        if (check == False):
                            randomError("Can't implicitly convert " +
                                        idName + " into " + name)
                            return False
                        if (check.type != "CLASS"):
                            randomError("Can't implicitly convert " +
                                        idName + " into " + name)
                            return False
                        y = check
                check = insertAttribute(
                    name, "~", y, accessMod, static, concCond, currentClass)
            i += 1
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "ID"):
                idName = tokenList[i].value
                check = lookupMainTable(idName)
                if (check == False):
                    unDeclaredError(
                        idName, "can't create object of this class.")
                    return False
                if (check.type != "CLASS"):
                    randomError("Object can't be of " + check.type + " type.")
                    return False
                if (check.typeMod == "STATIC" or check.typeMod == "CONDENSED"):
                    randomError("Object can't be of " +
                                check.typeMod + " class.")
                    return False
                if (ofType != idName):
                    y = check.parent.split(',')[0]
                    while (True):
                        check = lookupMainTable(y)
                        if (check == False):
                            randomError("Can't implicitly convert " +
                                        ofType + " into " + idName)
                            return False
                        if (check.type != "CLASS"):
                            randomError("Can't implicitly convert " +
                                        ofType + " into " + idName)
                            return False
                        if (check.typeMod == "STATIC" or check.typeMod == "CONDENSED"):
                            randomError("Object can't be of " +
                                        check.typeMod + " class.")
                            return False
                        if (check.name == ofType):
                            break
                        else:
                            y = check.parent.split(',')[0]
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    param, check = pl()
                    if (check and tokenList[i].type == "C_PARAN"):
                        i += 1
                        check = lookupAttributeTable(idName, param, idName)
                        if (check == False):
                            unDeclaredError(
                                idName, "Don't have same signature constructor.")
                            return False
                        if (accessMod == ""):
                            check = insertFunctionTable(
                                name, idName, currentScope)
                            if (check == False):
                                reDeclarationError(
                                    name, "Inside Scope No# ", currentScope)
                                return False
                        else:
                            check = insertAttribute(
                                name, "~", idName, accessMod, static, concCond, currentClass)
                            if (check == False):
                                reDeclarationError(
                                    name, "Object Declaration in '" + currentClass + "'")
                        return True
        return syntaxError()

    # Array Implementation
    def oArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return oArr_()
        elif (tokenList[i].type == "ASSIGN"):
            i += 1
            check = initOArr()
            if (check):
                return oArr_()
        return syntaxError()

    # Array Implementation
    def initOArr():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_BRACK"):
                    i += 1
                    return initOArr_()
        return syntaxError()

    # Array Implementation
    def initOArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                check = valOArr()
                if (check and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        else:
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        return syntaxError()

    # Array Implementation
    def valOArr():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    param, check = pl()
                    if (check and tokenList[i].type == "C_PARAN"):
                        i += 1
                        return valOArr_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    # Array Implementation
    def valOArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "NEW"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (tokenList[i].type == "O_PARAN"):
                        i += 1
                        param, check = pl()
                        if (check and tokenList[i].type == "C_PARAN"):
                            i += 1
                            return valOArr_()
        return syntaxError()

    # Array Implementation
    def multiArr():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return multiArr_()
        return syntaxError()

    # Array Implementation
    def multiArr_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return multiArr_()
        elif (tokenList[i].type == "ASSIGN"):
            i += 1
            check = initMultidim()
            if (check):
                return multiArr_()
        return syntaxError()

    # Array Implementation
    def initMultidim():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "DICT"):
                i += 1
                if (tokenList[i].type == "O_BRACK"):
                    i += 1
                    return initMultidim_()
        return syntaxError()

    # Array Implementation
    def initMultidim_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                check = valMultidim()
                if (check and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        else:
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        return syntaxError()

    # Array Implementation
    def valMultidim():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            return valMultidim_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    # Array Implementation
    def valMultidim_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return valMultidim_()
        return syntaxError()

    def sstID():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            return object_()
        elif (tokenList[i].type == "TERMINATOR" or tokenList[i].type == "O_BRACK" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "INC_DEC" or tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            return sstID_()
        return syntaxError()

    def sstID_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return sstID_()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "C_BRACK"):
                i += 1
                return sst1()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            param, check = pl()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                return sst2()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def sst1():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return sstID_()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            i += 1
            type_, check = expression()
            if (check and tokenList[i].type == "SEMI_COL"):
                return True
        elif (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        return syntaxError()

    def sst2():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return sstID_()

    def intSt():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        accessMod, check = public_()
        if (check):
            ofType, check = returnType()
            if (check):
                if (tokenList[i].type == "ID"):
                    name = tokenList[i].value
                    i += 1
                    if (tokenList[i].type == "O_PARAN"):
                        currentScope = createScope()
                        currentFunction = currentScope
                        i += 1
                        paramList, check = argumentList()
                        if (check and tokenList[i].type == "C_PARAN"):
                            i += 1
                            check = insertAttribute(
                                name, paramList, ofType, accessMod, "STATIC", "", currentClass)
                            if (check == False):
                                reDeclarationError(
                                    name, "Method in '" + currentClass + "'")
                                return False
                            if (tokenList[i].type == "O_BRACE"):
                                i += 1
                                if (tokenList[i].type == "C_BRACE"):
                                    i += 1
                                    if (tokenList[i].type == "SEMI_COL"):
                                        i += 1
                                        return intSt()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def sCst_(accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            ofType = tokenList[i].value
            i += 1
            return sStDT(ofType, accessMod, static)
        elif (tokenList[i].type == "ID"):
            ofType = tokenList[i].value
            check = lookupMainTable(ofType)
            if (check == False):
                unDeclaredError(ofType, "Can't create object.")
                return False
            if (check.type != "CLASS"):
                randomError("Can't create object of 'symbol'")
                return False
            if (check.typeMod == "CONDENSED"):
                randomError("Can't create object of 'condensed class'")
                return False
            i += 1
            return sStID(ofType, accessMod, static)
        elif (tokenList[i].type == "DICT"):
            i += 1
            check = multiArr()
            if (check):
                return sCst()
        elif (tokenList[i].type == "VOID"):
            ofType = tokenList[i].value
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                name = tokenList[i].value
                i += 1
                return sMain(name, ofType, accessMod, static)
        return syntaxError()

    def sStDT(ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = declare_(name, ofType, accessMod, static, "")
            if (check):
                return sCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return sStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return sMain(name, ofType, accessMod, static)
        return syntaxError()

    # Array Implementation
    def sStDT_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = gArr_()
            if (check):
                return sCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        return syntaxError()

    def sStID(ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = object_(name, ofType, accessMod, static, "")
            if (check):
                return sCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return sStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return sMain(name, ofType, accessMod, static)
        elif (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            if (tokenList[i].type == "C_PARAN"):
                i += 1
                if (currentClass != ofType):
                    randomError(
                        "constructor and class name should be same.")
                    return False
                if (static != ""):
                    randomError(
                        "class could not have parameterized static constructor")
                    return False
                check = insertAttribute(
                    ofType, "", ofType, accessMod, static, "", currentClass)
                if (check == False):
                    reDeclarationError(
                        ofType, "Constructor of class " + currentClass)
                    return False
                check = bodyMST()
                if (check):
                    return sCst()
        return syntaxError()

    # Array Implementation
    def sStID_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = oArr_()
            if (check):
                return sCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        return syntaxError()

    def sMain(name, ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            paramList, check = argumentList()
            if (check and tokenList[i].type == "C_PARAN"):
                check = insertAttribute(
                    name, paramList, ofType, accessMod, static, "", currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Method in '" + currentClass + "'")
                    return False
                i += 1
                check = bodyMST()
                if (check):
                    return sCstNM()
        return syntaxError()

    def sCstNM():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FUNCTION"):
            i += 1
            accessMod, check = pubPriv_()
            if (check and tokenList[i].type == "STATIC"):
                i += 1
                check = functionSig(accessMod, "", "")
                if (check):
                    return sCstNM()
        elif (tokenList[i].type == "PRIVATE"):
            accessMod = tokenList[i].type
            i += 1
            if (tokenList[i].type == "STATIC"):
                static = tokenList[i].type
                i += 1
                check = classVars(accessMod, static, "")
                if (check):
                    return sCstNM()
        elif (tokenList[i].type == "C_BRACE"):
            currentScope = destroyScope()
            i += 1
            check = lookupMainTable(currentClass)
            check = checkConstructor(check)
            if (check):
                return mainDone()
        else:
            accessMod, check = public_()
            if (check and tokenList[i].type == "STATIC"):
                static = tokenList[i].type
                i += 1
                check = consVar(accessMod, static)
                if (check):
                    return sCstNM()
        return syntaxError()

    def mainDone():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "EOF"):
            return True
        elif (tokenList[i].type == "STATIC"):
            i += 1
            if (tokenList[i].type == "CLASS"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    parent, check = inherit()
                    if (check and tokenList[i].type == "O_BRACE"):
                        i += 1
                        check = sCstNM()
                        if (check):
                            return mainDone()
        elif (tokenList[i].type == "SYMBOL"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_BRACE"):
                    i += 1
                    check = intSt()
                    if (check and tokenList[i].type == "C_BRACE"):
                        i += 1
                        return mainDone()
        else:
            check = concCond_()
            if (check and tokenList[i].type == "CLASS"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    parent, check = inherit()
                    if (check and tokenList[i].type == "O_BRACE"):
                        i += 1
                        check = gcCstNM()
                        if (check):
                            return mainDone()
        return syntaxError()

    def concCond_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        concCond = ""
        if (tokenList[i].type == "CONCRETE"):
            concCond = tokenList[i].type
            i += 1
            return concCond, True
        elif (tokenList[i].type == "CONDENSED"):
            concCond = tokenList[i].type
            i += 1
            return concCond, True
        elif (tokenList[i].type == "CLASS"):
            return concCond, True
        return concCond, syntaxError()

    def concrete_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        typeMod = ""
        if (tokenList[i].type == "CONCRETE"):
            typeMod = tokenList[i].type
            i += 1
            return typeMod, True
        elif (tokenList[i].type == "CLASS"):
            return typeMod, True
        return typeMod, syntaxError()

    def cCst():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            currentScope = destroyScope()
            i += 1
            check = lookupMainTable(currentClass)
            check = checkConstructor(check)
            if (check):
                return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            accessMod, check = access()
            if (check):
                check = types(accessMod)
                if (check):
                    return cCst()
        else:
            accessMod, check = presPriv()
            if (check):
                static, concCond, check = statConc()
                if (check):
                    check = classVars(accessMod, static, concCond)
                    if (check):
                        return cCst()
            else:
                check = classVars("PUBLIC", "", "")
                if (check):
                    return cCst()
                else:
                    accessMod, check = public_()
                    if (check):
                        return cCst_(accessMod)
        return syntaxError()

    def access():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        accessMod = ""
        if (tokenList[i].type == "PUBLIC"):
            accessMod = tokenList[i].type
            i += 1
            return accessMod, True
        elif (tokenList[i].type == "PRIVATE"):
            accessMod = tokenList[i].type
            i += 1
            return accessMod, True
        elif (tokenList[i].type == "PRESERVED"):
            accessMod = tokenList[i].type
            i += 1
            return accessMod, True
        elif (tokenList[i].type == "CONDENSED" or tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID" or tokenList[i].type == "STATIC" or tokenList[i].type == "CONCRETE"):
            accessMod = "PUBLIC"
            return accessMod, True
        return accessMod, syntaxError()

    def types(accessMod):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "CONDENSED"):
            concCond = tokenList[i].type
            i += 1
            ofType, check = returnType()
            if (check and tokenList[i].type == "ID"):
                name = tokenList[i].value
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    currentScope = createScope()
                    currentFunction = currentScope
                    i += 1
                    paramList, check = argumentList()
                    if (check and tokenList[i].type == "C_PARAN"):
                        check = insertAttribute(
                            name, paramList, ofType, accessMod, "", concCond, currentClass)
                        if (check == False):
                            reDeclarationError(
                                name, "Method in '" + currentClass + "'")
                            return False
                        i += 1
                        if (tokenList[i].type == "SEMI_COL"):
                            i += 1
                            return True
        else:
            static, concCond, check = statConc()
            if (check):
                check = functionSig(accessMod, static, concCond)
                if (check):
                    return True
        return syntaxError()

    def statConc():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        static = ""
        concCond = ""
        if (tokenList[i].type == "STATIC"):
            static = tokenList[i].type
            i += 1
            return static, concCond, True
        elif (tokenList[i].type == "CONCRETE"):
            concCond = tokenList[i].type
            i += 1
            return static, concCond, True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID"):
            return static, concCond, True
        return static, concCond, syntaxError()

    def presPriv():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        accessMod = ""
        if (tokenList[i].type == "PRIVATE" or tokenList[i].type == "PRESERVED"):
            accessMod = tokenList[i].type
            i += 1
            return accessMod, True
        return accessMod, syntaxError()

    def cCst_(accessMod):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        static = ""
        concCond = ""
        if (tokenList[i].type == "STATIC"):
            static = tokenList[i].type
            i += 1
            return cCst__(accessMod, static)
        elif (tokenList[i].type == "CONCRETE"):
            concCond = tokenList[i].type
            i += 1
            check = classVars(accessMod, static, concCond)
            if (check):
                return cCst()
        return syntaxError()

    def cCst__(accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            ofType = tokenList[i].value
            i += 1
            return cStDT(ofType, accessMod, static)
        elif (tokenList[i].type == "ID"):
            ofType = tokenList[i].value
            check = lookupMainTable(ofType)
            if (check == False):
                unDeclaredError(ofType, "Can't create object.")
                return False
            if (check.type != "CLASS"):
                randomError("Can't create object of 'symbol'")
                return False
            if (check.typeMod == "CONDENSED"):
                randomError("Can't create object of 'condensed class'")
                return False
            i += 1
            return cStID(ofType, accessMod, static)
        elif (tokenList[i].type == "DICT"):
            i += 1
            check = multiArr()
            if (check):
                return cCst()
        elif (tokenList[i].type == "VOID"):
            ofType = tokenList[i].value
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                name = tokenList[i].value
                i += 1
                return gcMain(name, ofType, accessMod, static, "")
        return syntaxError()

    def cStDT(ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = declare_(name, ofType, accessMod, static, "")
            if (check):
                return cCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return cStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return gcMain(name, ofType, accessMod, static, "")
        return syntaxError()

    # Array Implementation
    def cStDT_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = gArr_()
            if (check):
                return cCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def cStID(ofType, accessMod, static):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = object_(name, ofType, accessMod, static, "")
            if (check):
                return cCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return cStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return gcMain(name, ofType, accessMod, static, "")
        elif (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            param, check = argumentList()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (currentClass != ofType):
                    randomError(
                        "constructor and class name should be same.")
                    return False
                if (static != "" and param != ""):
                    randomError(
                        "class could not have parameterized static constructor")
                    return False
                check = insertAttribute(
                    ofType, param, ofType, accessMod, static, "", currentClass)
                if (check == False):
                    reDeclarationError(
                        ofType, "Constructor of class " + currentClass)
                    return False
                check = bodyMST()
                if (check):
                    return cCst()
        return syntaxError()

    # Array Implementation
    def cStID_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = oArr_()
            if (check):
                return cCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def gcMain(name, ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            paramList, check = argumentList()
            if (check and tokenList[i].type == "C_PARAN"):
                check = insertAttribute(
                    name, paramList, ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        name, "Method in '" + currentClass + "'")
                    return False
                i += 1
                check = bodyMST()
                if (check):
                    return gcCstNM()
        return syntaxError()

    def gcCstNM():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "FUNCTION"):
            i += 1
            accessMod, check = access()
            if (check):
                check = types(accessMod)
                if (check):
                    return gcCstNM()
        elif (tokenList[i].type == "C_BRACE"):
            currentScope = destroyScope()
            i += 1
            check = lookupMainTable(currentClass)
            check = checkConstructor(check)
            if (check):
                return mainDone()
        else:
            accessMod, check = presPriv()
            if (check):
                static, concCond, check = statConc()
                if (check):
                    check = classVars(accessMod, static, concCond)
                    if (check):
                        return gcCstNM()
            else:
                accessMod, check = public_()
                if (check):
                    check = gcConsVar(accessMod)
                    if (check):
                        return gcCstNM()
        return syntaxError()

    def gcConsVar(accessMod):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "CONCRETE"):
            concCond = tokenList[i].type
            return classVars(accessMod, "", concCond)
        else:
            static, check = static_()
            if (check):
                return consVar(accessMod, static)
        return syntaxError()

    def gCst():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "C_BRACE"):
            currentScope = destroyScope()
            i += 1
            check = lookupMainTable(currentClass)
            check = checkConstructor(check)
            if (check):
                return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            accessMod, check = access()
            if (check):
                check = types(accessMod)
                if (check):
                    return gCst()
        else:
            accessMod, check = presPriv()
            if (check):
                static, concCond, check = statConc()
                if (check):
                    check = classVars(accessMod, static, concCond)
                    if (check):
                        return gCst()
            else:
                accessMod, check = public_()
                if (check):
                    return gCst_(accessMod)
        return syntaxError()

    def gCst_(accessMod):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        static = ""
        concCond = ""
        if (tokenList[i].type == "CONCRETE"):
            concCond = ""
            i += 1
            check = classVars(accessMod, static, concCond)
            if (check):
                return gCst()
        else:
            static, check = static_()
            if (check):
                return gCst__(accessMod, static, concCond)
        return syntaxError()

    def static_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        static = ""
        if (tokenList[i].type == "STATIC"):
            static = tokenList[i].type
            i += 1
            return static, True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID"):
            return static, True
        return static, syntaxError()

    def gCst__(accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "DT"):
            ofType = tokenList[i].value
            i += 1
            return gStDT(ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "ID"):
            ofType = tokenList[i].value
            check = lookupMainTable(ofType)
            if (check == False):
                unDeclaredError(ofType, "Can't create object.")
                return False
            if (check.type != "CLASS"):
                randomError("Can't create object of 'symbol'")
                return False
            if (check.typeMod == "CONDENSED"):
                randomError("Can't create object of 'condensed class'")
                return False
            i += 1
            return gStID(ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "DICT"):
            i += 1
            check = multiArr()
            if (check):
                return gCst()
        elif (tokenList[i].type == "VOID"):
            ofType = tokenList[i].type
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                name = tokenList[i].value
                i += 1
                return gcMain(name, ofType, accessMod, static, concCond)
        return syntaxError()

    def gStDT(ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = declare_(name, ofType, accessMod, static, concCond)
            if (check):
                return gCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return gStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return gcMain(name, ofType, accessMod, static, concCond)
        return syntaxError()

    # Array Implementation
    def gStDT_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = gArr_()
            if (check):
                return gCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def gStID(ofType, accessMod, static, concCond):
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            name = tokenList[i].value
            i += 1
            check = object_(name, ofType, accessMod, static, concCond)
            if (check):
                return gCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return gStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            name = tokenList[i].value
            i += 1
            return gcMain(name, ofType, accessMod, static, concCond)
        elif (tokenList[i].type == "O_PARAN"):
            currentScope = createScope()
            currentFunction = currentScope
            i += 1
            param, check = argumentList()
            if (check and tokenList[i].type == "C_PARAN"):
                i += 1
                if (currentClass != ofType):
                    randomError(
                        "constructor and class name should be same.")
                    return False
                if (static != "" and param != ""):
                    randomError(
                        "class could not have parameterized static constructor")
                    return False
                if (concCond != ""):
                    randomError(
                        "constructor can't be modified by concrete or condensed")
                    return False
                check = insertAttribute(
                    ofType, param, ofType, accessMod, static, concCond, currentClass)
                if (check == False):
                    reDeclarationError(
                        ofType, "Constructor of class "+currentClass)
                    return False
                check = bodyMST()
                if (check):
                    return gCst()
        return syntaxError()

    # Array Implementation
    def gStID_():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        if (tokenList[i].type == "ID"):
            i += 1
            check = oArr_()
            if (check):
                return gCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def z():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_
        return syntaxError()


except LookupError:
    print("Tree Incomplete... Input Completely Parsed")
