import os
import helper
import re

def read_cnf(filename="src\cnf.txt"):
    file = os.path.join(os.getcwd(), filename)
    with open(file) as cnf:
        rules = cnf.readlines()
        var_rules = []
        terminal_rules = []

        for rule in rules:
            lhs, rhs = rule.split(" -> ")
            rhs = rhs[:-1].split(" | ")
            for r in rhs:
                if (str.islower(r)):
                    terminal_rules.append([lhs, r])
                else:
                    var_rules.append([lhs, r])

        return var_rules, terminal_rules

def convert_cnf(var_rules, terminal_rules):
    dict = {}

    for el in terminal_rules:
        if el[1] in dict:
            dict[el[1]].append(el[0])
        else:
            temp = []
            temp.append(el[0])
            dict[el[1]] = temp
    for el in var_rules:
        if el[1] in dict:
            dict[el[1]].append(el[0])
        else:
            temp = []
            temp.append(el[0])
            dict[el[1]] = temp

    return dict

def read_inp(filename):
    # Read from file
    f = open(filename, "r")
    contents = f.read()
    contents = contents.split()
    f.close()

    result = contents

    operators = [':', ',', '=', '<', '>', '>=', '<=', '==', '!=', r'\+', '-', r'\*', '/', r'\*\*', r'\(', r'\)',r'\'\'\'', r'\'', r'\"']

    # For each operator..
    for operator in operators:
        temporaryResult = []
        # For each statement..
        for statement in result:
            format = r"[A..z]*(" + operator +r")[A..z]*"
            x = re.split(format, statement)
            
            # Append 
            for splitStatement in x:
                temporaryResult.append(splitStatement) 
        file_content = temporaryResult

    # Strip space
    temporaryResult = []
    for statement in result:
        stripped = statement.split()
        for splitStatement in stripped: 
            temporaryResult.append(splitStatement)

    file_content = temporaryResult

    # Strip empty string
    file_content = [string for string in result if string!='']

    return file_content

def map_proc(piece):
    mapping = {
        r'[A-z0-9]*' : "string",
        r'[0-9]*' : "number",
        r'[A-Za-z_][A-Za-z_0-9]*' : "variable",
    }

def cyk(dict, code):
    table = [[set([]) for j in range(len(code))] for i in range(len(code))]

    #filling in the table
    for j in range(0,len(code)):
        #iterate over the dict
        for key,item in dict.items():
            if(len(key.split()) == 1 and key[0] == code[j]):
                table[j][j].add(item)
        for i in range(j,-1,-1):
            for k in range(i,j+1):
                for key,item in dict.items():
                    if(len(key.split)==2 and key[0] in table[i][k] and key[1] in table[k+1][j]):
                        table[i][j].add(item)

    if(len(table[0][len(code)-1])!= 0):
        print("true")
    else:
        print("false")

    
    

    
    # base case where code is translated to regex then mapped to lhs that has converted to the key of dict
    #for i in range(len(code)):
        # res = map_proc(code[i])
        # table[0][i] = dict[res]

# fc = read_inp("src\inputAcc.py")
# print(fc)

# v, t = read_cnf()
# print()
# print("ini v")
# for i in range(len(v)):
#     print(v[i])
# print()
# print("ini t")
# for i in range(len(t)):
#     print(t[i])
# print()
# dict = convert_cnf(v,t)
# print("\nini dict nya")
# print(dict)