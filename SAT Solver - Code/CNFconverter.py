__author__ = 'Pramod'
#!/usr/bin/python
import sys

def biconditionalElimination( myList1, myList2 ):
    #Apply Biconditional Elimination
    newList1 = []
    subList1 = []
    subList2 = []
    subList1.append("implies")
    subList1.append(myList1)
    subList1.append(myList2)
    subList2.append("implies")
    subList2.append(myList2)
    subList2.append(myList1)
    newList1.append("and")
    newList1.append(subList1)
    newList1.append(subList2)
    return newList1

def implicationElimination( myList1, myList2 ):
    #Apply Implication Elimination
    newList2 = []
    sublist1 = []
    sublist1.append("not")
    sublist1.append(myList1)
    newList2.append("or")
    newList2.append(sublist1)
    newList2.append(myList2)
    return newList2

def removeNegation ( list ):
    #Remove Negation associated with Literals
    negationList = []
    if list[0] == "and":
        subList1 = removeNegation(list[1])
        subList2 = removeNegation(list[2])
        negationList.append("or")
        negationList.append(subList1)
        negationList.append(subList2)
    elif list[0] == "or":
        subList3 = removeNegation(list[1])
        subList4 = removeNegation(list[2])
        negationList.append("and")
        negationList.append(subList3)
        negationList.append(subList4)
    elif list[0] == "not":
        negationList.append(list[1])
    else:
        negationList.append("not")
        negationList.append(list[0])
    return negationList

def function ( myList ):
    #Utility function which make calls to methods to remove iff and implication
    newResult = []
    if isinstance(myList,str):
        return myList
    elif myList[0] == "iff":
        result = biconditionalElimination(myList[1], myList[2])
        myList = []
        myList.append("dummy")
        myList.append(result[1])
        myList.append(result[2])
        newResult.append("and")
    elif myList[0] == "implies":
        result = implicationElimination(myList[1], myList[2])
        myList = []
        myList.append("dummy")
        myList.append(result[1])
        myList.append(result[2])
        newResult.append("or")
    elif myList[0] == "not":
        newResult.append("not")
    elif myList[0] == "and":
        newResult.append("and")
    elif myList[0] == "or":
        newResult.append("or")
    for i in range(len(myList) - 1):
            newResult.append(function(myList[i+1]))
    return newResult

def demorgans (exp):
    #Apply demorgans
    if isinstance(exp,str):
        return exp
    if exp[0] == "not":
       arr = []
       if isinstance(exp[1],str):
           return exp
       elif exp[1][0] == "and":
           op = "or"
       elif exp[1][0] == "or":
           op = "and"
       elif exp[1][0] == "not":
           op = ""
       if op != "":
          arr.append(op)
       for i in range(len(exp[1])-1):
           if op != "":
               arr.append(demorgans(["not",exp[1][i+1]]))
           else:
               return demorgans(exp[1][i+1])
       return arr
    if exp[0] != "not":
        arr = []
        arr.append(exp[0])
        for i in range(len(exp)-1):
            arr.append(demorgans(exp[i+1]))
        return arr


def getBinaryOperands(proposition):
    #Wrapper function to convert more than two operands to two operands before applying distributive property
    if isinstance(proposition, str):
        return proposition
    elif len(proposition) == 2:
        return [proposition[0], getBinaryOperands(proposition[1])]
    elif len(proposition) == 3:
        return [proposition[0], getBinaryOperands(proposition[1]), getBinaryOperands(proposition[2])]
    else:
        return [proposition[0], getBinaryOperands(proposition[1]), getBinaryOperands([proposition[0]] + proposition[2:])]

def applyDistributive (prop) :
    #Apply Distributive Property
    if isinstance(prop, list) :
        if prop[0] == "not":
            answer = prop
        else :
            op = prop[0]
            operand1 =  applyDistributive(prop[1])
            operand2 =  applyDistributive(prop[2])
            if op == "or" :
                answer = pushdistributive(operand1, operand2)
            else :
                answer = ["and", operand1, operand2]
    else:
        answer = prop
    return answer

def pushdistributive ( p1, p2 ):
    #Push OR's inside
    if isinstance(p1, list) and p1[0] == "and" :
        finalanswer = ["and", pushdistributive(p1[1],p2), pushdistributive(p1[2],p2)]
    elif  isinstance(p2, list) and p2[0] == "and" :
        finalanswer = ["and", pushdistributive(p1,p2[1]), pushdistributive(p1,p2[2])]
    else :
        finalanswer = ["or", p1, p2]
    return finalanswer

"""def applyassociativeproperty(exp):
    #Apply Associative property
    resultlist = []
    if isinstance(exp,str) or exp[0] == "not" :
        return exp
    if exp[0] == "or":
        resultlist.append("or")
        for j in range(len(exp)-1):
            result = applyassociativeproperty(exp[j+1])
            if not isinstance(result,str) and result[0] == "or":
                for i in range(len(result)-1):
                    resultlist.append(result[i+1])
            else:
                resultlist.append(result)
        return resultlist
    if exp[0] == "and":
        resultlist.append("and")
        for k in range(len(exp)-1):
            result = applyassociativeproperty(exp[k+1])
            if not isinstance(result,str) and result[0] == "and":
                for i in range(len(result)-1):
                    resultlist.append(result[i+1])
            else:
                resultlist.append(result)
        return resultlist"""

def assoc(exp,final):
    if isinstance(exp,str) or exp[0] == "not" :
        return exp


    if exp[0] == "and":
        final.append("and")
        for j in range(len(exp)-1):
            result = assoc(exp[j+1],[])
            if not isinstance(result,str) and result[0] == "and":
                for i in range(len(result)-1):
                    final.append(result[i+1])
            else:
                final.append(result)

        return final

    if exp[0] == "or":
        final.append("or")
        for j in range(len(exp)-1):
            result = assoc(exp[j+1],[])
            if not isinstance(result,str) and result[0] == "or":
                for i in range(len(result)-1):
                    final.append(result[i+1])
            else:
                final.append(result)
        return final


"""def removedup(exp):
    if isinstance(exp,str):
        return exp
    arr = []
    for j in range(len(exp)-1):
        op = exp[j+1]
        if not isinstance(exp,str):
            op = exp[0]+"-"+exp[1]
        arr.append(op)
    arr = list(set(arr))
    arr = arr.sort()
    arr = [exp[0]]+arr
    return str(",",arr)


def redo(exp):
    for j in range(len(exp)):
        if not isinstance(exp,str):
            for j in range(len(exp[j])):
                if str.find(exp,"not-") != -1:
                    arr.append()


def removefinaldup(exp):
    if isinstance(exp,str):
        return exp
    if len(exp) == 2:
        return exp
    arr = []
    for i in range(len(exp)-1):
        a = removedup(exp[i+1])
        arr.append(a)

    arr = list(set(arr))
    arr = [exp[0]]+ arr
    arr = redo(arr)
    return arr
"""

def remove_duplicates(old_list):
    new_list = []
    if old_list == []:
        new_list = []
    else:
        if (old_list[0] not in old_list[1:]):
            new_list = [old_list[0]] + remove_duplicates(old_list[1:])
        else:
            new_list = remove_duplicates(old_list[1:])
    return new_list

#iterate through list and removes duplicates from list.
def duplicate_parser(old_list):
    unique_list=[];
    old_list=remove_duplicates(old_list);
    for i in range(0,len(old_list)):
        #unique_list.append(old_list[i]);
        if isinstance(old_list[i],list):
            unique_list.append(remove_duplicates(old_list[i]));
        else:
            unique_list.append(old_list[i]);
    return  unique_list;





#old Comments
#myString = '["iff", ["and", ["not", "R"], "B"], ["or", "N", "M"]]'
#myString  = '["not", ["and", "A", "B", "C"]]'
#myString = '["not",["or","a","b"]]'
#myString = '["or","A","B","C"]'
#myString = '["or", ["and", ["not", "p"], "q"],"r"]'
#myString = '["and", ["or", ["and", ["not","P"], "Q"], "R"], ["or", ["not", "P"], ["not", "R"]]]'
#newList1  = biconditionalElimination(myList)
#newList2 = implicationElimination(myList)
#print(newList1)
#print(newList2)
#myString = '["and", ["or", ["and", ["not","P"], "Q", "S"], "R"], ["or", ["not","P"], ["not","R"]]]'
#myString = '["or", ["and", "A", "B"], ["and", "C", "D"]]'
#myString = '["or", ["and", "A","B","C"], ["and", "B", "D"]]'

#working comments
"""
myString = '["or","a","b","c",["and","d","e","f"],["not","k"],"l"]'
myList = eval(myString)
listbeforedemorgans =  function(myList)
listafterdemorgans = demorgans(listbeforedemorgans)
covert3to2 = getBinaryOperands(listafterdemorgans)
resultafterdistributive = applyDistributive(covert3to2)
resultassociative = applyassociativeproperty(resultafterdistributive)
print  resultassociative
"""

#old comments
"""print "myString:",myString
print "myList:",myList
print "listbeforedemorgans:",listbeforedemorgans
print "listafterdemorgans:",listafterdemorgans
print "covert3to2",covert3to2
#print "resultafterdistributive:",resultafterdistributive
#print "resultassociative",resultassociative"""

def main(argv):
    #Main function
    filename = sys.argv[2]
    fo = open(filename, "r")
    fb = open("sentences_CNF.txt", "w")
    with open(filename) as fp:
        content = fp.read().splitlines()
        for i in range(1,len(content)):
            myString = content[i]
            myList = eval(myString)
            listbeforedemorgans =  function(myList)
            listafterdemorgans = demorgans(listbeforedemorgans)
            covert3to2 = getBinaryOperands(listafterdemorgans)
            resultafterdistributive = applyDistributive(covert3to2)
            resultassociative = assoc(resultafterdistributive,[])
            removeduplicatesliterals = duplicate_parser(resultassociative)
            fb.write(repr(removeduplicatesliterals)+ '\n')
            print "myString:",myString
            print "myList:",myList
            print "listbeforedemorgans:",listbeforedemorgans
            print "listafterdemorgans:",listafterdemorgans
            print "covert3to2:",covert3to2
            print "resultafterdistributive:",resultafterdistributive
            print "resultassociative",resultassociative
            print "removeduplicatesliterals",removeduplicatesliterals
        fo.close()
        fb.close()
    return

if __name__ == "__main__":
    main(sys.argv)




