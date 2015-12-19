__author__ = 'Pramod'
import sys

def getClauses (givenlist):
    #Fetch Clauses from the Given List
    if isinstance(givenlist , str):
        return givenlist
    else:
        if (givenlist[0] == "and"):
            return givenlist[1:]
        else:
            return [givenlist]

def getLiterals (givenClause):
    #Get Literals from the given clause
    for i in range(1, len(givenClause)):
        if isinstance(givenClause[i], str):
            literalList.append(givenClause[i])
        else:
            getLiterals(givenClause[i])
    uniqueliterals = list(set(literalList))
    return uniqueliterals

def find(lit, clause):
    #Find literals in the clause
        if isinstance(clause, list):
            if clause[0] == "not":
                if isinstance(lit, list):
                    if clause[1] == lit[1]:
                        return True
            else:
                 for k in range(0,len(clause)):
                    if isinstance(clause[k], list):
                        if clause[k][0] == "not":
                            if isinstance(lit,list):
                                if clause[k][1] == lit[1]:
                                    return True
                    else:
                        if clause[k] == lit:
                            return True
        elif isinstance(clause, str):
            if lit == clause:
                return True
        return False

def updateModel (model, puresymbolslist):
    #Utility method to update the model values
    temp_model = model
    temp_model[puresymbolslist[0]] = puresymbolslist[1]
    return temp_model

def findPureSymbols(literalresult, clausesnotknown):
    #Function to find pure symbols
    for l in literalresult:
        lf = False
        not_lf = False
        for c in clausesnotknown:
            if find(l,c) and not lf:
                lf = True
            if isinstance(l,list):
                var = l[1]
            else:
                var = []
                var = ["not", l[0]]
            if find(var,c) and not not_lf:
                not_lf = True
        if not_lf != lf:
            return l, lf
    return None, None

def updateLiterals (literalresult, puresymbolslist):
    #Utility method to change literals
    temp_literal = literalresult
    literalresult.remove(puresymbolslist[0])
    return literalresult


def dpllAlogorithm (clauseslist, model, literalresult):
    #DPLL algorithm
    clausesnotknown = []
    for i in range(0, len(clauseslist)):
        var1 = callTruthTable(clauseslist[i], model)
        if var1 is False:
            return False
        elif var1 != True:
            clausesnotknown.append(clauseslist[i])
    if not clausesnotknown:
        if literalresult:
            for lit in literalresult:
                model[lit] = True
        return model
    puresymbolslist = findPureSymbols(literalresult, clausesnotknown)
    if puresymbolslist[0]:
        return dpllAlogorithm(clauseslist, updateModel(model, puresymbolslist), updateLiterals(literalresult, puresymbolslist))
    unitclauseslist = findUnitClauses(clauseslist, model)
    if unitclauseslist:
        return dpllAlogorithm(clauseslist, updateModel(model, unitclauseslist), updateLiterals(literalresult, unitclauseslist))
    lit = literalresult.pop()
    #recursively call dpll algorithm
    return (dpllAlogorithm(clauseslist, updateModel(model, [lit,True]), literalresult) or
    dpllAlogorithm(clauseslist, updateModel(model, [lit,False]), literalresult))



def findUnitClauses (clauseslist, model):
    #Utility Function to find Unit Clauses
    for c in clauseslist:
        cnt = 0
        negate_literal = False
        for sub in c:
            if sub == "not":
                negate_literal = True
                continue
            """if negate_literal == True:
                sub = ["not", sub]"""
            if  sub not in model:
                cnt += 1
                unitclause = []
                unitclause.append(sub)
                unitclause.append((sub[0] != "not"))
        if cnt == 1:
            return unitclause
    return None, None


args=[];
def disjuncts(s):
    """Return a list of the disjuncts in the sentence s."""
    if isinstance(s, list) and s[0] == "or":
        for i in range(1,len(s)):
            args.append(s[i]);
        return args;
    else:
        return [s]

















def callTruthTable (list1, model):
    #Gives truth values to the sent list
    if isinstance(list1, list):
        if(list1[0] == "or"):
            var_or = False
            for j in range(1, len(list1)):
                var_or = callTruthTable(list1[j],model)
                if var_or is None:
                    var_or = None
                elif var_or:
                    return True
            return var_or
        elif(list1[0] == "and"):
            value=False
            for k in range(1, len(list1)):
                var_and = callTruthTable(list1[k],model)
                if var_and is None:
                    value = None
                elif var_and is False:
                    return False
            return value
        elif(list1[0] == "not"):
             var_not = callTruthTable(list1[1], model)
             if var_not is None:
                 return None
             else:
                 return not var_not
    else:
        if isinstance(list1,str):
            return model.get(list1)

#Old Comments
#myString = '["and", "R", ["not", "B"], "W"]'
#myString = '["or", "R", ["not", "B"], "W"]'
#myString = '["not", "P"]'
#myString = '["and", ["or", "P", ["not", "R"]], ["or", ["not", "Q"], ["not", "R"], "P"]]'
#myString = '["and", "A", ["or", "B", "C"], ["or", "B", "D"]]'
#myList = '["and", ["not", "A"], "B"]'
#myString = '[["or", ["not", "A"], "B"],["or", "C", "D"]]'
#myString = '["and", "A", ["not", "A"]]'




myString = '["and", ["not", "P"], "P"]'
myList = eval(myString)
literalList = []
print "myList:",(myList)
clauseresult = getClauses(myList)
literalresult = getLiterals(myList)
model = {}
print "clauseresult:",clauseresult
literalresult = getLiterals(myList)
print "literalresult:",literalresult
model = {}
print "model:",model
dpllresult = dpllAlogorithm(clauseresult, model, literalresult)
print "dpllresult:",dpllresult

"""
myString = '["and", "A", ["or", "B", "C"], ["or", "B", "D"]]'
myList = eval(myString)
literalList = []
clauseresult = getClauses(myList)
literalresult = getLiterals(myList)
model = {}
dpllresult = dpllAlogorithm(clauseresult, model, literalresult)
outputlist = []
if dpllresult:
    outputlist.append('True')
    for key,value in model.items():
        outputfile = str(key) + "=" + str(value).lower()
        outputlist.append(outputfile)
    else:
        outputlist.append('False')
        print "dpllresult:",outputlist
"""
"""
filename = sys.argv[2]
fo = open(filename, "r")
fb = open("CNF_satisfiability.txt", "w")
with open(filename) as fp:
    content = fp.read().splitlines()
    for i in range(1,len(content)):
            myString = content[i]
            myList = eval(myString)
            literalList = []
            clauseresult = getClauses(myList)
            literalresult = getLiterals(myList)
            model = {}
            dpllresult = dpllAlogorithm(clauseresult, model, literalresult)
            outputlist = []
            if dpllresult:
                outputlist.append('True')
                for key,value in model.items():
                    outputfile = str(key) + "=" + str(value).lower()
                    outputlist.append(outputfile)
            else:
                outputlist.append('False')
            #print "myString:",myString
            #print "myList:",(myList)
            #print "clauseresult:",clauseresult
            #print "literalresult:",literalresult
            #print "model:",model
            print "dpllresult:",outputlist
            fb.write(str(outputlist)+ '\n')
    fo.close()
    fb.close()

"""
#if __name__ == "__main__":
#    main(sys.argv)

