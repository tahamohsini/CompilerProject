# import sys

i = 0
tokenList = []
# syntaxErr = True
errorAt = 0
synError = ""


def syntaxAnalyzer(tokens):
    global i, tokenList, errorAt, synError
    i = 0
    errorAt = 0
    tokenList = tokens
    result = structure()
    if (not result):
        synError += "\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type + \
              "\n\tFile:\t\'.\\input.txt\' [@ " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt) + "\n\n\n"
        print("\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type +
              "\n\tFile:\t\'.\\input.txt\' [@ " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt))
    return synError, result


def syntaxError():
    global i, tokenList, errorAt
    if (i > errorAt):
        errorAt = i
    return False


try:

    def structure():
        global i, tokenList
        if (tokenList[i].type == "STATIC"):
            i += 1
            if (tokenList[i].type == "CLASS"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (inherit()):
                        if (tokenList[i].type == "O_BRACE"):
                            i += 1
                            if (sCst()):
                                if (tokenList[i].type == "EOF"):
                                    return True
        elif (tokenList[i].type == "CONDENSED"):
            i += 1
            if (tokenList[i].type == "CLASS"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (inherit()):
                        if (tokenList[i].type == "O_BRACE"):
                            i += 1
                            if (cCst()):
                                if (tokenList[i].type == "EOF"):
                                    return True
        elif (concrete_() and tokenList[i].type == "CLASS"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (inherit()):
                    if (tokenList[i].type == "O_BRACE"):
                        i += 1
                        if (gCst()):
                            if (tokenList[i].type == "EOF"):
                                return True
        elif (tokenList[i].type == "SYMBOL"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_BRACE"):
                    i += 1
                    if (intSt()):
                        if (tokenList[i].type == "C_BRACE"):
                            i += 1
                            if (structure()):
                                if (tokenList[i].type == "EOF"):
                                    return True
        return syntaxError()

    def sCst():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            i += 1
            return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            if (pubPriv_()):
                if (tokenList[i].type == "STATIC"):
                    i += 1
                    if (functionSig()):
                        return sCst()
        elif (tokenList[i].type == "PRIVATE"):
            i += 1
            if (tokenList[i].type == "STATIC"):
                i += 1
            if (classVars()):
                return sCst()
        elif (public_() and tokenList[i].type == "STATIC"):
            i += 1
            return sCst_()
        return syntaxError()

    def public_():
        global i, tokenList
        if (tokenList[i].type == "PUBLIC"):
            i += 1
            return True
        elif (tokenList[i].type == "STATIC" or tokenList[i].type == "CONCRETE" or tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "VOID" or tokenList[i].type == "DICT"):
            return True
        return syntaxError()

    def inherit():
        global i, tokenList
        if (expands() and applies()):
            return True
        return syntaxError()

    def expands():
        global i, tokenList
        if (tokenList[i].type == "EXPANDS"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return True
        elif (tokenList[i].type == "APPLIES" or "O_BRACE"):
            return True
        return syntaxError()

    def applies():
        global i, tokenList
        if (tokenList[i].type == "APPLIES"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return applies_()
        elif (tokenList[i].type == "O_BRACE"):
            return True
        return syntaxError()

    def applies_():
        global i, tokenList
        if (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return applies_()
        elif (tokenList[i].type == "O_BRACE"):
            return True
        return syntaxError()

    def pubPriv_():
        global i, tokenList
        if (tokenList[i].type == "PUBLIC" or tokenList[i].type == "PRIVATE"):
            i += 1
            return True
        elif (tokenList[i].type == "STATIC"):
            return True
        return syntaxError()

    def functionSig():
        global i, tokenList
        if (returnType() and tokenList[i].type == "ID"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if(argumentList() and tokenList[i].type == "C_PARAN"):
                    i += 1
                    if(bodyMST()):
                        return True
        return syntaxError()

    def returnType():
        global i, tokenList
        if (tokenList[i].type == "DT" or tokenList[i].type == "ID"):
            i += 1
            return returnType_()
        elif (tokenList[i].type == "VOID"):
            i += 1
            return True
        elif (tokenList[i].type == "DICT"):
            i += 1
            if (tokenList[i].type == "O_BRACK"):
                i += 1
                if (tokenList[i].type == "C_BRACK"):
                    i += 1
                    return True
        return syntaxError()

    def returnType_():
        global i, tokenList
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        elif (tokenList[i].type == "ID"):
            return True
        return syntaxError()

    def argumentList():
        global i, tokenList
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT"):
            return argumentList_()
        return syntaxError()

    def argumentList_():
        global i, tokenList
        if (tokenList[i].type == "DT" or tokenList[i].type == "ID"):
            i += 1
            if(argumentList___() and tokenList[i].type == "ID"):
                i += 1
                return argumentList__()
        if (tokenList[i].type == "DICT"):
            i += 1
            if (tokenList[i].type == "O_BRACK"):
                i += 1
                if (tokenList[i].type == "C_BRACK"):
                    i += 1
                    if (tokenList[i].type == "ID"):
                        i += 1
                        return argumentList__()
        return syntaxError()

    def argumentList__():
        global i, tokenList
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            return argumentList_()
        return syntaxError()

    def argumentList___():
        global i, tokenList
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return True
        elif (tokenList[i].type == "ID"):
            return True
        return syntaxError()

    def bodyMST():
        global i, tokenList
        if (tokenList[i].type == "O_BRACE"):
            i += 1
            if (mst()):
                tokenList[i].type == "C_BRACE"
                i += 1
                return True
        return syntaxError()

    def mst():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE" or tokenList[i].type == "CASE" or tokenList[i].type == "DEFAULT"):
            return True
        if (tokenList[i].type == "SWITCH" or tokenList[i].type == "IF" or tokenList[i].type == "FOR" or tokenList[i].type == "WHILE" or tokenList[i].type == "DO" or tokenList[i].type == "RETURN" or tokenList[i].type == "CONTINUE" or tokenList[i].type == "BREAK" or tokenList[i].type == "TRY" or tokenList[i].type == "INC_DEC" or tokenList[i].type == "CHAIN" or tokenList[i].type == "DT" or tokenList[i].type == "DICT" or tokenList[i].type == "ID" or tokenList[i].type == "THROW"):
            if (sst()):
                return mst()
        return syntaxError()

    def sst():
        global i, tokenList
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
            if (sp_() and tokenList[i].type == "ID"):
                return ref()
        elif (tokenList[i].type == "CHAIN"):
            i += 1
            if (tokenList[i].type == "TERMINATOR"):
                i += 1
                if (tokenList[i].type == "ID"):
                    check = ref()
                    if (check):
                        check = assignOp()
                        if (check):
                            check = expression()
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
            if (throw_() and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def throw_():
        global i, tokenList
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
                        if (throw__() and tokenList[i].type == "C_PARAN"):
                            return True
        return syntaxError()

    def throw__():
        global i, tokenList
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "STR"):
            i += 1
            return True
        return syntaxError()

    def switchSt():
        global i, tokenList
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
                            if (switchBody() and tokenList[i].type == "C_BRACE"):
                                i += 1
                                return True
        return syntaxError()

    def switchBody():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "CASE" or tokenList[i].type == "DEFAULT"):
            if (case() and default()):
                return True
        return syntaxError()

    def case():
        global i, tokenList
        if (tokenList[i].type == "case"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if(const() and tokenList[i].type == "C_PARAN"):
                    i += 1
                    if (tokenList[i].type == "COLON"):
                        i += 2
                        if(mst()):
                            return case()
        elif (tokenList[i].type == "DEFAULT" or tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def default():
        global i, tokenList
        if (tokenList[i].type == "DEFAULT"):
            i += 1
            if (tokenList[i].type == "COLON"):
                i += 1
                if (mst()):
                    return case()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def const():
        global i, tokenList
        if (tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "CHAR" or tokenList[i].type == "BOOL"):
            i += 1
            return True
        return syntaxError()

    def ifSt():
        global i, tokenList
        if (tokenList[i].type == "IF"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if (expression()):
                    if (tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (bodyMST() and oElse()):
                            return True
        return syntaxError()

    def oElse():
        global i, tokenList
        if (tokenList[i].type == "else"):
            i += 1
            return oElse_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def oElse_():
        global i, tokenList
        if (tokenList[i].type == "IF"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if (expression()):
                    if (tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (bodyMST()):
                            return oElse()
        elif (bodyMST()):
            return True
        return syntaxError()

    def expression():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (b() and a_()):
                return True
        return syntaxError()

    def a_():
        global i, tokenList
        if (tokenList[i].type == "OR"):
            i += 1
            if (b() and a_()):
                return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def b():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (c() and b_()):
                return True
        return syntaxError()

    def b_():
        global i, tokenList
        if (tokenList[i].type == "AND"):
            i += 1
            if (c() and b_()):
                return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def c():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (e() and c_()):
                return True
        return syntaxError()

    def c_():
        global i, tokenList
        if (tokenList[i].type == "R_OP"):
            i += 1
            if (e() and c_()):
                return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def e():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (t() and e_()):
                return True
        return syntaxError()

    def e_():
        global i, tokenList
        if (tokenList[i].type == "P_M"):
            i += 1
            if (t() and e_()):
                return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def t():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (f() and t_()):
                return True
        return syntaxError()

    def t_():
        global i, tokenList
        if (tokenList[i].type == "M_D_M"):
            i += 1
            if (f() and t_()):
                return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def f():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN"):
            i += 1
            if (expression() and tokenList[i].type == "C_PARAN"):
                return True
        elif (const()):
            return True
        elif (tokenList[i].type == "EXCLAIM"):
            i += 1
            return f()
        elif (sp_() and tokenList[i].type == "ID"):
            i += 1
            return optF()
        return syntaxError()

    def sp_():
        global i, tokenList
        if (tokenList[i].type == "CHAIN"):
            i += 1
            if (tokenList[i].type == "TERMINATOR"):
                i += 1
                return True
        elif (tokenList[i].type == "ID"):
            return True
        return syntaxError()

    def optF():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return optF()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                i += 1
                return optF1()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (pl() and tokenList[i].type == "C_PARAN"):
                i += 1
                return optF_()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return True
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def optF1():
        global i, tokenList
        if (tokenList[i].type == "INC_DEC"):
            i += 1
            return True
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return optF()
        return syntaxError()

    def optF_():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return optF()
        elif (tokenList[i].type == "SEMI_COL" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID" or tokenList[i].type == "COMMA" or tokenList[i].type == "C_BRACK" or tokenList[i].type == "C_PARAN" or tokenList[i].type == "C_BRACE" or tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "INT" or tokenList[i].type == "FLT" or tokenList[i].type == "CHAR" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL"):
            return True
        return syntaxError()

    def pl():
        global i, tokenList
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "O_PARAN" or tokenList[i].type == "EXCLAIM" or tokenList[i].type == "INT" or tokenList[i].type == "CHAR" or tokenList[i].type == "FLT" or tokenList[i].type == "STR" or tokenList[i].type == "BOOL" or tokenList[i].type == "CHAIN" or tokenList[i].type == "ID"):
            if (expression()):
                return pl_()
        return syntaxError()

    def pl_():
        global i, tokenList
        if (tokenList[i].type == "COMMA"):
            i += 1
            if (expression()):
                return pl_()
        elif (tokenList[i].type == "C_PARAN"):
            return True
        return syntaxError()

    def forSt():
        global i, tokenList
        if (tokenList[i].type == "FOR"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
                if(st1() and expression() and tokenList[i].type == "SEMI_COL"):
                    i += 1
                    if (st3() and tokenList[i].type == "C_PARAN"):
                        return body()
        return syntaxError()

    def body():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "O_BRACE"):
            return bodyMST()
        return syntaxError()

    def st1():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return declare_()
        elif (sp_() and tokenList[i].type == "ID"):
            i += 1
            if (ref() and assignOp() and expression() and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def ref():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                i += 1
                return ref_()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (pl() and tokenList[i].type == "C_PARAN"):
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
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                i += 1
                return ref_()
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            return True
        return syntaxError()

    def assignOp():
        global i, tokenList
        if (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            i += 1
            return True
        return syntaxError()

    def st3():
        global i, tokenList
        if (tokenList[i].type == "INC_DEC"):
            i += 1
            if (sp_() and tokenList[i].type == "ID"):
                i += 1
                return ref()
        elif (tokenList[i].type == "ID"):
            i += 1
            return forOpt()
        elif (tokenList[i].type == "C_PARAN"):
            return True
        return syntaxError()

    def forOpt():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                return forOpt1()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (pl() and tokenList[i].type == "C_PARAN"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return forOpt()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return forOpt_()
        elif (assignOp() and expression()):
            return forOpt_()
        return syntaxError()

    def forOpt1():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return forOpt_()
        elif (assignOp() and expression()):
            return forOpt_()
        return syntaxError()

    def forOpt_():
        global i, tokenList
        if (tokenList[i].type == "C_PARAN"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return forOpt()
        return syntaxError()

    def whileSt():
        global i, tokenList
        if (tokenList[i].type == "WHILE"):
            i += 1
            if (tokenList[i].type == "O_PARAN"):
                i += 1
            if (expression() and tokenList[i].type == "C_PARAN"):
                i += 1
                return body()
        return syntaxError()

    def doWhileSt():
        global i, tokenList
        if (tokenList[i].type == "DO"):
            i += 1
            if (bodyMST() and tokenList[i].type == "WHILE"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    if (expression() and tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (tokenList[i].type == "SEMI_COL"):
                            i += 1
                            return True
        return syntaxError()

    def returnSt():
        global i, tokenList
        if (tokenList[i].type == "RETURN"):
            i += 1
            if (return_() and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def return_():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            return True
        elif (expression()):
            return True
        return syntaxError()

    def continueSt():
        global i, tokenList
        if (tokenList[i].type == "CONTNIUE"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def breakSt():
        global i, tokenList
        if (tokenList[i].type == "BREAK"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def trySt():
        global i, tokenList
        if (tokenList[i].type == "TRY"):
            i += 1
            if (bodyMST() and catchFinally()):
                return True
        return syntaxError()

    def catchFinally():
        global i, tokenList
        if (tokenList[i].type == "FINALLY"):
            return finallyC()
        elif (tokenList[i].type == "CATCH"):
            if (catch() and finallyC_()):
                return True
        return syntaxError()

    def finallyC():
        global i, tokenList
        if (tokenList[i].type == "FINALLY"):
            i += 1
            return bodyMST()
        return syntaxError()

    def catch():
        global i, tokenList
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
                            if (bodyMST()):
                                return catch_()
        return syntaxError()

    def catch_():
        global i, tokenList
        if (tokenList[i].type == "FINALLY" or tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "CATCH"):
            return catch()
        return syntaxError()

    def finallyC_():
        global i, tokenList
        if (tokenList[i].type == "FINALLY"):
            i += 1
            return bodyMST()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def classVars():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            return nDec()
        elif (tokenList[i].type == "ID"):
            i += 1
            return oDec()
        elif (tokenList[i].type == "dict"):
            i += 1
            return multiArr()
        return syntaxError()

    def consVar():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            return nDec()
        elif (tokenList[i].type == "ID"):
            i += 1
            return consVar_()
        elif (tokenList[i].type == "dict"):
            i += 1
            return multiArr()
        return syntaxError()

    def consVar_():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN"):
            i += 1
            if (argumentList() and tokenList[i].type == "C_PARAN"):
                i += 1
                return bodyMST()
        elif (tokenList[i].type == "ID"):
            i += 1
            return object_()
        elif (tokenList[i].type == "O_BRACE"):
            i += 1
            if (tokenList[i].type == "C_BRACE"):
                i += 1
                return oArr_()
        return syntaxError()

    def nDec():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            return declare_()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return gArr_()
        return syntaxError()

    def declare_():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return declare_()
        elif (tokenList[i].type == "ASSIGN"):
            i += 1
            return initList()
        return syntaxError()

    def initList():
        global i, tokenList
        if (sp_() and tokenList[i].type == "ID"):
            i += 1
            return list1()
        elif (const()):
            return list2()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (expression() and tokenList[i].type == "C_PARAN"):
                return list2()
        elif (tokenList[i].type == "EXCLAIM"):
            i += 1
            if (f()):
                return initList_()
        return syntaxError()

    def initList_():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return declare_()
        return syntaxError()

    def list1():
        global i, tokenList
        if (tokenList[i].type == "ASSIGN"):
            i += 1
            return initList()
        elif (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return list1()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                i += 1
                return list3()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (pl() and tokenList[i].type == "C_PARAN"):
                i += 1
                return list2()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            return list2()
        elif (list2()):
            return True
        return syntaxError()

    def list2():
        global i, tokenList
        if (tokenList[i].type == "M_D_M" or tokenList[i].type == "P_M" or tokenList[i].type == "R_OP" or tokenList[i].type == "AND" or tokenList[i].type == "OR" or tokenList[i].type == "SEMI_COL" or tokenList[i].type == "COMMA"):
            if (t_() and e_() and c_() and b_() and a_() and initList_()):
                return True
        return syntaxError()

    def list3():
        global i, tokenList
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
        elif (list2()):
            return True
        return syntaxError()

    def gArr_():
        global i, tokenList
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
            if (initGArr() and gArr_()):
                return True
        return syntaxError()

    def initGArr():
        global i, tokenList
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

    def initGArr_():
        global i, tokenList
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                if (valGArr() and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        elif (expression() and tokenList[i].type == "C_BRACK"):
            i += 1
            return True
        return syntaxError()

    def valGArr():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (const() and valGArr_()):
            return True
        return syntaxError()

    def valGArr_():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (const() and valGArr_()):
                return True
        return syntaxError()

    def oDec():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            return object_()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return oArr_()
        return syntaxError()

    def object_():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return object_()
        elif (tokenList[i].type == "ASSIGN"):
            i += 1
            if (initObject()):
                return object_()
        return syntaxError()

    def initObject():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            return True
        elif (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    if (pl() and tokenList[i].type == "C_PARAN"):
                        i += 1
                        return True
        return syntaxError()

    def oArr_():
        global i, tokenList
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
            if (initOArr()):
                return oArr_()
        return syntaxError()

    def initOArr():
        global i, tokenList
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

    def initOArr_():
        global i, tokenList
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                if (valOArr() and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        elif (expression() and tokenList[i].type == "C_BRACK"):
            i += 1
            return True
        return syntaxError()

    def valOArr():
        global i, tokenList
        if (tokenList[i].type == "NEW"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    if (pl() and tokenList[i].type == "C_PARAN"):
                        i += 1
                        return valOArr_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def valOArr_():
        global i, tokenList
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
                        if (pl() and tokenList[i].type == "C_PARAN"):
                            i += 1
                            return valOArr_()
        return syntaxError()

    def multiArr():
        global i, tokenList
        if (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    return multiArr_()
        return syntaxError()

    def multiArr_():
        global i, tokenList
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
            if (initMultidim()):
                return multiArr_()
        return syntaxError()

    def initMultidim():
        global i, tokenList
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

    def initMultidim_():
        global i, tokenList
        if (tokenList[i].type == "C_BRACK"):
            i += 1
            if (tokenList[i].type == "O_BRACE"):
                i += 1
                if (valMultidim() and tokenList[i].type == "C_BRACE"):
                    i += 1
                    return True
        elif (expression() and tokenList[i].type == "C_BRACK"):
            i += 1
            return True
        return syntaxError()

    def valMultidim():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            return valMultidim_()
        elif (tokenList[i].type == "C_BRACE"):
            return True
        return syntaxError()

    def valMultidim_():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            return True
        elif (tokenList[i].type == "COMMA"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return valMultidim_()
        return syntaxError()

    def sstID():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            return object_()
        elif (tokenList[i].type == "TERMINATOR" or tokenList[i].type == "O_BRACK" or tokenList[i].type == "O_PARAN" or tokenList[i].type == "INC_DEC" or tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            return sstID_()
        return syntaxError()

    def sstID_():
        global i, tokenList
        if (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return sstID_()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (expression() and tokenList[i].type == "C_BRACK"):
                i += 1
                return sst1()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (pl() and tokenList[i].type == "C_PARAN"):
                i += 1
                return sst2()
        elif (tokenList[i].type == "INC_DEC"):
            i += 1
            if (tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        elif (tokenList[i].type == "ASSIGN" or tokenList[i].type == "COMP_ASSIGN"):
            i += 1
            if (expression() and tokenList[i].type == "SEMI_COL"):
                i += 1
                return True
        return syntaxError()

    def sst1():
        global i, tokenList
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
            if (expression() and tokenList[i].type == "SEMI_COL"):
                return True
        elif (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        return syntaxError()

    def sst2():
        global i, tokenList
        if (tokenList[i].type == "SEMI_COL"):
            i += 1
            return True
        elif (tokenList[i].type == "TERMINATOR"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                return sstID_()

    def intSt():
        global i, tokenList
        if (public_() and returnType()):
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    if (argumentList() and tokenList[i].type == "C_PARAN"):
                        i += 1
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

    def sCst_():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            return sStDT()
        elif (tokenList[i].type == "ID"):
            i += 1
            return sStID()
        elif (tokenList[i].type == "DICT"):
            i += 1
            if (multiArr()):
                return sCst()
        elif (tokenList[i].type == "VOID"):
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                i += 1
                return sMain()
        return syntaxError()

    def sStDT():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (declare_()):
                return sCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return sStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        return syntaxError()

    def sStDT_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (gArr_()):
                return sCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        return syntaxError()

    def sStID():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (object_()):
                return sCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return sStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (tokenList[i].type == "C_PARAN"):
                i += 1
                if (bodyMST):
                    return sCst()
        return syntaxError()

    def sStID_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (oArr_()):
                return sCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return sMain()
        return syntaxError()

    def sMain():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN"):
            i += 1
            if (argumentList() and tokenList[i].type == "C_PARAN"):
                i += 1
                if (bodyMST()):
                    return sCstNM()
        return syntaxError()

    def sCstNM():
        global i, tokenList
        if (tokenList[i].type == "FUNCTION"):
            i += 1
            if (pubPriv_() and tokenList[i].type == "STATIC"):
                i += 1
                if (functionSig()):
                    return sCstNM()
        elif (tokenList[i].type == "PRIVATE"):
            i += 1
            if (tokenList[i].type == "STATIC"):
                i += 1
                if (classVars()):
                    return sCstNM()
        elif (public_()):
            if (tokenList[i].type == "STATIC"):
                i += 1
                if (consVar()):
                    return sCstNM()
        # elif (pubPriv_() and tokenList[i].type == "STATIC"):
        #     i += 1
        #     if (classVars()):
        #         return sCstNM()
        elif (tokenList[i].type == "C_BRACE"):
            i += 1
            return mainDone()
        return syntaxError()

    def mainDone():
        global i, tokenList
        if (tokenList[i].type == "EOF"):
            return True
        elif (tokenList[i].type == "STATIC"):
            i += 1
            if (tokenList[i].type == "CLASS"):
                i += 1
                if (tokenList[i].type == "ID"):
                    i += 1
                    if (inherit() and tokenList[i].type == "O_BRACE"):
                        i += 1
                        if (sCstNM()):
                            return mainDone()
        elif (tokenList[i].type == "SYMBOL"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_BRACE"):
                    i += 1
                    if (intSt() and tokenList[i].type == "C_BRACE"):
                        i += 1
                        return mainDone()
        elif (concCond_() and tokenList[i].type == "CLASS"):
            i += 1
            if (tokenList[i].type == "ID"):
                i += 1
                if (inherit() and tokenList[i].type == "O_BRACE"):
                    i += 1
                    if (gcCstNM()):
                        return mainDone()
        return syntaxError()

    def concCond_():
        global i, tokenList
        if (tokenList[i].type == "CONCRETE"):
            i += 1
            return True
        elif (tokenList[i].type == "CONDENSED"):
            i += 1
            return True
        elif (tokenList[i].type == "CLASS"):
            return True
        return syntaxError()

    def concrete_():
        global i, tokenList
        if (tokenList[i].type == "CONCRETE"):
            i += 1
            return True
        elif (tokenList[i].type == "CLASS"):
            return True
        return syntaxError()

    def cCst():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            i += 1
            return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            if (access() and types()):
                return cCst()
        elif (presPriv() and statConc()):
            if (classVars()):
                return cCst()
        elif (classVars()):
            return cCst()
        elif (public_()):
            return cCst_()
        return syntaxError()

    def access():
        global i, tokenList
        if (tokenList[i].type == "PUBLIC"):
            i += 1
            return True
        elif (tokenList[i].type == "PRIVATE"):
            i += 1
            return True
        elif (tokenList[i].type == "PRESERVED"):
            i += 1
            return True
        elif (tokenList[i].type == "CONDENSED" or tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID" or tokenList[i].type == "STATIC" or tokenList[i].type == "CONCRETE"):
            return True
        return syntaxError()

    def types():
        global i, tokenList
        if (tokenList[i].type == "CONDENSED"):
            i += 1
            if (returnType() and tokenList[i].type == "ID"):
                i += 1
                if (tokenList[i].type == "O_PARAN"):
                    i += 1
                    if (argumentList() and tokenList[i].type == "C_PARAN"):
                        i += 1
                        if (tokenList[i].type == "SEMI_COL"):
                            i += 1
                            return True
        elif (statConc() and functionSig()):
            return True
        return syntaxError()

    def statConc():
        global i, tokenList
        if (tokenList[i].type == "STATIC"):
            i += 1
            return True
        elif (tokenList[i].type == "CONCRETE"):
            i += 1
            return True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID"):
            return True
        return syntaxError()

    def presPriv():
        global i, tokenList
        if (tokenList[i].type == "PRIVATE"):
            i += 1
            return True
        elif (tokenList[i].type == "PRESERVED"):
            i += 1
            return True
        return syntaxError()

    def cCst_():
        global i, tokenList
        if (tokenList[i].type == "STATIC"):
            i += 1
            return cCst__()
        elif (tokenList[i].type == "CONCRETE"):
            i += 1
            if (classVars()):
                return cCst()
        return syntaxError()

    def cCst__():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            return cStDT()
        elif (tokenList[i].type == "ID"):
            i += 1
            return cStID()
        elif (tokenList[i].type == "DICT"):
            i += 1
            if (multiArr()):
                return cCst()
        elif (tokenList[i].type == "VOID"):
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                i += 1
                return gcMain()
        return syntaxError()

    def cStDT():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (declare_()):
                return cCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return cStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def cStDT_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (gArr_()):
                return cCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def cStID():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (object_()):
                return cCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return cStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (argumentList() and tokenList[i].type == "C_PARAN"):
                i += 1
                if (bodyMST()):
                    return cCst()
        return syntaxError()

    def cStID_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (oArr_()):
                return cCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def gcMain():
        global i, tokenList
        if (tokenList[i].type == "O_PARAN"):
            i += 1
            if (argumentList() and tokenList[i].type == "C_PARAN"):
                i += 1
                if (bodyMST()):
                    return gcCstNM()
        return syntaxError()

    def gcCstNM():
        global i, tokenList
        if (tokenList[i].type == "FUNCTION"):
            i += 1
            if (access() and types()):
                return gcCstNM()
        elif (tokenList[i].type == "C_BRACE"):
            i += 1
            return mainDone()
        elif (presPriv() and statConc()):
            if (classVars()):
                return gcCstNM()
        elif (public_()):
            if (gcConsVar()):
                return gcCstNM()
        return syntaxError()

    def gcConsVar():
        global i, tokenList
        if (tokenList[i].type == "CONCRETE"):
            return classVars()
        elif (static_()):
            return consVar()
        return syntaxError()

    def gCst():
        global i, tokenList
        if (tokenList[i].type == "C_BRACE"):
            i += 1
            return structure()
        elif (tokenList[i].type == "FUNCTION"):
            i += 1
            if (access() and types()):
                return gCst()
        elif (presPriv() and statConc()):
            if (classVars()):
                return gCst()
        elif (public_()):
            return gCst_()
        return syntaxError()

    def gCst_():
        global i, tokenList
        if (tokenList[i].type == "CONCRETE"):
            i += 1
            if (classVars()):
                return gCst()
        elif (static_()):
            return gCst__()
        return syntaxError()

    def static_():
        global i, tokenList
        if (tokenList[i].type == "STATIC"):
            i += 1
            return True
        elif (tokenList[i].type == "DT" or tokenList[i].type == "ID" or tokenList[i].type == "DICT" or tokenList[i].type == "VOID"):
            return True
        return syntaxError()

    def gCst__():
        global i, tokenList
        if (tokenList[i].type == "DT"):
            i += 1
            return gStDT()
        elif (tokenList[i].type == "ID"):
            i += 1
            return gStID()
        elif (tokenList[i].type == "DICT"):
            i += 1
            if (multiArr()):
                return gCst()
        elif (tokenList[i].type == "VOID"):
            i += 1
            if (tokenList[i].type == "MAIN_METHOD"):
                i += 1
                return gcMain()
        return syntaxError()

    def gStDT():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (declare_()):
                return gCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return gStDT_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def gStDT_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (gArr_()):
                return gCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def gStID():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (object_()):
                return gCst()
        elif (tokenList[i].type == "O_BRACK"):
            i += 1
            if (tokenList[i].type == "C_BRACK"):
                i += 1
                return gStID_()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        elif (tokenList[i].type == "O_PARAN"):
            i += 1
            if (argumentList() and tokenList[i].type == "C_PARAN"):
                i += 1
                if (bodyMST()):
                    return gCst()
        return syntaxError()

    def gStID_():
        global i, tokenList
        if (tokenList[i].type == "ID"):
            i += 1
            if (oArr_()):
                return gCst()
        elif (tokenList[i].type == "MAIN_METHOD"):
            i += 1
            return gcMain()
        return syntaxError()

    def z():
        global i, tokenList
        return syntaxError()


except LookupError:
    print("Tree Incomplete... Input Completely Parsed")
