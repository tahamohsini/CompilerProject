mainTable_ = []
functionTable_ = []
scopeStack_ = [0]
highestScope = 0
typeCompatibility = {
    "intint+": "int",
    "intint-": "int",
    "intint*": "int",
    "intint/": "int",
    "intint%": "int",
    "intint=": "int",
    "intint==": " bool",
    "intint!=": "bool",
    "intint<=": "bool",
    "intint<": "bool",
    "intint>": "bool",
    "intint>=": "bool",
    "intfloat+": "float",
    "intfloat-": "float",
    "intfloat*": "float",
    "intfloat/": "float",
    "intfloat=": "int",
    "intfloat==": "bool",
    "intfloat!=": "bool",
    "intfloat<=": "bool",
    "intfloat<": "bool",
    "intfloat>": "bool",
    "intfloat>=": "bool",
    "intchar+": "int",
    "intchar-": "int",
    "intchar*": "int",
    "intchar/": "int",
    "intchar%": "int",
    "intchar=": "int",
    "intchar==": "bool",
    "intchar!=": "bool",
    "intchar<=": "bool",
    "intchar<": "bool",
    "intchar>": "bool",
    "intchar>=": "bool",
    "intbool+": "int",
    "intbool-": "int",
    "intbool*": "int",
    "intbool/": "int",
    "intbool%": "int",
    "intbool=": "int",
    "intbool==":  "bool",
    "intbool!=": "bool",
    "intbool<=": "bool",
    "intbool<": "bool",
    "intbool>": "bool",
    "intbool>=": "bool",
    "floatfloat+": "float",
    "floatfloat-": "float",
    "floatfloat*": "float",
    "floatfloat/": "float",
    "floatfloat=": "float",
    "floatfloat==": "bool",
    "floatfloat!=": "bool",
    "floatfloat<=": "bool",
    "floatfloat<": "bool",
    "floatfloat>": "bool",
    "floatfloat>=": "bool",
    "floatchar+": "float",
    "floatchar-": "float",
    "floatchar*": "float",
    "floatchar/": "float",
    "floatchar%": "float",
    "floatchar=": "float",
    "floatchar==": "bool",
    "floatchar!=": "bool",
    "floatchar<=": "bool",
    "floatchar<": "bool",
    "floatchar>": "bool",
    "floatchar>=": "bool",
    "floatbool+": "float",
    "floatbool-": "float",
    "floatbool*": "float",
    "floatbool/": "float",
    "floatbool=": "bool",
    "floatbool==": "bool",
    "floatbool!=": "bool",
    "floatbool<=": "bool",
    "floatbool<": "bool",
    "floatbool>": "bool",
    "floatbool>=": "bool",
    "stringstring+": "string",
    "stringstring=":  "string",
    "stringstring==": "bool",
    "stringstring!=": "bool",
    "stringstring<=": "bool",
    "stringstring<": "bool",
    "stringstring>": "bool",
    "stringstring>=": "bool",
    "stringint=": "int",
    "stringfloat=": "int",
    "stringchar+": "string",
    "stringchar=": "string",
    "stringbool=": "string",
    "charchar+": "int",
    "charchar-": "int",
    "charchar*": "int",
    "charchar/": "int",
    "charchar%": "int",
    "charchar=": "char",
    "charchar==": "bool",
    "charchar!=": "bool",
    "charchar<=": "bool",
    "charchar<": "bool",
    "charchar>": "bool",
    "charchar>=": "bool",
    "charint+": "char",
    "charint-": "char",
    "charint*": "char",
    "charint/": "char",
    "charint%": "int",
    "charint=": "char",
    "charint==": "bool",
    "charint!=": "bool",
    "charint<=": "bool",
    "charint<": "bool",
    "charint>": "bool",
    "charint>=": "bool",
    "charfloat+": "float",
    "charfloat-": "float",
    "charfloat*": "float",
    "charfloat/": "float",
    "charfloat=": "char",
    "charfloat==": "bool",
    "charfloat!=": "bool",
    "charfloat<=": "bool",
    "charfloat<": "bool",
    "charfloat>": "bool",
    "charfloat>=": "bool",
    "charstring+": "string",
    "charbool+":  "int",
    "charbool-": "int",
    "charbool*": "int",
    "charbool/": "int",
    "charbool%": "int",
    "charbool=": "char",
    "charbool==": "bool",
    "charbool!=": "bool",
    "charbool<=": "bool",
    "charbool<": "bool",
    "charbool>": "bool",
    "charbool>=": "bool",
    "boolbool+": "bool",
    "boolbool-": "bool",
    "boolbool*": "bool",
    "boolbool/": "bool",
    "boolbool%": "bool",
    "boolbool=": "bool",
    "boolbool==": "bool",
    "boolbool!=": "bool",
    "boolbool<=": "bool",
    "boolbool<": "bool",
    "boolbool>": "bool",
    "boolbool>=": "bool",
    "boolbool&&": "bool",
    "boolbool||": "bool",
    "boolint+": "int",
    "boolint-": "int",
    "boolint*": "int",
    "boolint/": "int",
    "boolint%": "int",
    "boolint=": "bool",
    "boolint==": "bool",
    "boolint!=": "bool",
    "boolint<=": "bool",
    "boolint<": "bool",
    "boolint>": "bool",
    "boolint>=": "bool",
    "boolfloat-": "float",
    "boolfloat*": "float",
    "boolfloat/": "float",
    "boolfloat%": "float",
    "boolfloat=": "bool",
    "boolfloat==": "bool",
    "boolfloat!=": "bool",
    "boolfloat<=": "bool",
    "boolfloat<": "bool",
    "boolfloat>": "bool",
    "boolfloat>=": "bool",
    "boolchar+": "int",
    "boolchar-": "int",
    "boolchar*": "int",
    "boolchar/": "int",
    "boolchar%": "int",
    "boolchar=": "bool",
    "boolchar==": "bool",
    "boolchar!=": "bool",
    "boolchar<=": "bool",
    "boolchar<": "bool",
    "boolchar>": "bool",
    "boolchar>=": "bool",
    "char!": "bool",
    "int!": "bool",
    "int++": "int",
    "int--": "int",
    "float!": "bool",
    # "bool!": "bool",
    # "bool++": "bool",
    # "bool--": "bool",
    # "char++": "char",
    # "char--": "char",
    # "float++": "float",
    # "float--": "float"
}


class mainTable:
    def __init__(self, name, ofType, typeMod, parent):
        self.name = name
        self.type = ofType
        self.typeMod = typeMod
        self.parent = parent
        self.attrTable = []


class attributeTable:
    def __init__(self, name, params, ofType, accessMod, stat, concCond):
        self.name = name
        self.params = params
        self.type = ofType
        self.accessMod = accessMod
        self.stat = stat
        self.concCond = concCond


class functionTable:
    def __init__(self, name, ofType, scope):
        self.name = name
        self.type = ofType
        self.scope = scope


def lookupMainTable(name):
    x = next((j for j in mainTable_ if j.name == name), "")
    if (x == ""):
        return False
    # print("\tLookUp Main Table")
    # print(vars(x))
    return x


def insertMainTable(name, ofType, typeMod, parent):
    if (lookupMainTable(name) == False):
        obj = mainTable(name, ofType, typeMod, parent)
        mainTable_.append(obj)
        # print("\tMain Table")
        # for t in mainTable_:
        #     print(vars(t))
        return True
    return False


def lookupAttributeTable(name, paramList, ofName):
    x = lookupMainTable(ofName)
    if (x != False):
        if (paramList == "~"):
            y = next((j for j in x.attrTable if j.name == name), "")
            if (y == ""):
                return False
            # print("\tLookUp Attr Table")
            # print(vars(y))
            return y
        else:
            y = next((j for j in x.attrTable if j.name ==
                     name and j.params == paramList), "")
            if (y == ""):
                return False
            # print("\tLookUp Attr Table")
            # print(vars(y))
            return y
    return False


def insertAttribute(name, params, ofType, accessMod, stat, concCond, ofName):
    if(lookupAttributeTable(name, params, ofName) == False):
        for i in mainTable_:
            if i.name == ofName:
                obj = attributeTable(name, params, ofType,
                                     accessMod, stat, concCond)
                i.attrTable.append(obj)
                # print("\tAttr Table")
                # for t in i.attrTable:
                #     print(vars(t))
                return True
    return False


def lookupFunctionTable(name):
    for i in scopeStack_:
        x = next((j for j in functionTable_ if j.scope ==
                 i and j.name == name), "")
        if (x != ""):
            # print("\tLookUp Func Table")
            # print(vars(x))
            return x.type
    return False


def insertFunctionTable(name, ofType, scope):
    if(lookupFunctionTable(name) == False):
        obj = functionTable(name, ofType, scope)
        functionTable_.append(obj)
        # print("\tFunction Table")
        # for t in functionTable_:
        #     print(vars(t))
        return True
    return False


def createScope():
    global highestScope
    highestScope += 1
    x = highestScope
    # print("createdScope:\t", x)
    scopeStack_.insert(0, x)
    return scopeStack_[0]


def destroyScope():
    x = scopeStack_.pop(0)
    # print("destroyedScope:\t", x)
    return scopeStack_[0]


def binTypeCompatible(left, right, op):
    check = left + right + op
    if check in typeCompatibility.keys():
        return typeCompatibility[check]
    check = right + left + op
    if check in typeCompatibility.keys():
        return typeCompatibility[check]
    return False


def uniTypeCompatible(left, op):
    check = left + op
    if check in typeCompatibility.keys():
        return typeCompatibility[check]
    return False
