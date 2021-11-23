import os
import helper
import CheckVarName as cvn
import re

def read_cnf(filename):
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

def unswap_convert_cnf(var_rules, terminal_rules):
    dict_unswap = {}
    for el in terminal_rules:
        if el[1] in dict_unswap:
            temp = []
            for els in el[1].split():
                temp.append(els)
            dict_unswap[el[0]].append(temp)
        else:
            temp = []
            temp2 = []
            for els in el[1].split():
                temp2.append(els)
            temp.append(temp2)
            dict_unswap[el[0]] = temp
    for el in var_rules:
        if el[0] in dict_unswap:
            temp = []
            for els in el[1].split():
                temp.append(els)
            dict_unswap[el[0]].append(temp)
        else:
            temp = []
            temp2 = []
            for els in el[1].split():
                temp2.append(els)
            temp.append(temp2)
            dict_unswap[el[0]] = temp
    return dict_unswap

def separator(lines):
    new_lines = []
    for line in lines:
        line = line.replace('+',' + ')
        line = line.replace('-',' - ')
        line = line.replace('*',' * ')
        line = line.replace('/',' / ')
        line = line.replace('%',' % ')
        line = line.replace('=',' = ')
        line = line.replace('>',' > ')
        line = line.replace('<',' < ')
        line = line.replace('!',' ! ')
        line = line.replace('[',' [ ')
        line = line.replace(']',' ] ')
        line = line.replace('(',' ( ')
        line = line.replace(')',' ) ')
        line = line.replace('\'',' \' ')
        line = line.replace('\"',' \" ')
        line = line.replace(':',' : ')
        line = line.replace(',',' , ')
        line = line.replace('^',' ^ ')
        line = line.replace('|',' | ')
        line = line.replace('&',' & ')
        line = line.replace('{',' { ')
        line = line.replace('}',' } ')
        for word in line.split():
            new_lines.append(word)
    
    return new_lines

def read_inp(filename):
    file = os.path.join(os.getcwd(), filename)
    file_content = []
    word_content = []
    reserved_words = ['False', 'class', 'is', 'return', 'None', 'continue', 'for', 'True', 'def', 'from', 'while', 'and', 'not', 'with', 'as', 'elif', 'if', 'or', 'else', 'import', 'pass', 'break', 'in', 'raise']

    with open(file) as fileinp:
        inp_line = fileinp.readlines()
        for i in range(len(inp_line)-1):
            file_content.append(inp_line[i][:-1])
        file_content.append(inp_line[len(inp_line)-1])
        word_content = separator(file_content)
    
    stack = []
    new_word = []
    for word in word_content:
        if (word == '\'' or word == '\"'):
            if (len(stack) > 0 and stack[len(stack)-1] == word):
                stack.pop()
            else:
                stack.append(word)
        if (len(stack) > 0 and word != '\'' and word != '\"'):
            new_word.append('string')
        else:
            if(cvn.CheckVariableName(word) and word not in reserved_words):
                new_word.append('variable')
            else:
                new_word.append(word)
    return new_word

def cyk(dict, code):
    table = [[set([]) for j in range(len(code)+1)] for i in range(len(code)+1)]
    #filling in the table
    for j in range(0,len(code)):
        #iterate over the dict
        for lhs, rule in dict.items():
            for rhs in rule:
                isNumber = cvn.CheckNumber(code[j])
                if(isNumber):
                    code[j] = 'number'
                # If a terminal is found
                if len(rhs) == 1 and rhs[0] == code[j]:
                    print("base : ", end="")
                    print(rhs)
                    table[j][j].add(lhs)
  
        for i in range(j, -1, -1):   
            # Iterate over the range i to j + 1   
            for k in range(i, j + 1):     
                # Iterate over the rules
                for lhs, rule in dict.items():
                    for rhs in rule:
                          
                        # If a terminal is found
                        if len(rhs) == 2 and \
                        rhs[0] in table[i][k] and \
                        rhs[1] in table[k + 1][j]:
                            print("recurrence : ", end="")
                            print(rhs)
                            table[i][j].add(lhs)

    for i in range(len(code)+1):
        for j in range(len(code)+1):
            print(table[i][j], end=' ')
        print()

    if(len(table[0][len(code)-2])!= 0):
        print("Accepted")
    else:
        print("Syntax Error")

v, t = read_cnf("src\out.txt")
print()
print("ini v")
for i in range(len(v)):
    print(v[i])
print()
print("ini t")
for i in range(len(t)):
    print(t[i])
print()
dict = convert_cnf(v,t)
print("\nini dict nya")
print(dict)

dict_unswapped = unswap_convert_cnf(v,t)
print("\n ini unswapped")
print(dict_unswapped)

fc = read_inp("src\inputAcc.py")
print(fc)
cyk(dict_unswapped, fc)

# v,t = read_cnf('src\out.txt')
# dict = convert_cnf(v,t)
# fc = ['b', 'b']
# cyk(dict, fc)