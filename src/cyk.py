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
    table = [[[] for j in range(i)] for i in range(len(code),0,-1)]
    for i in range(len(code)):
        isNumber = cvn.CheckNumber(code[i])
        if(isNumber):
            code[i] = 'number'
        if code[i] in dict:
            table[0][i].append(dict[code[i]])
    for i in range(1,len(code)):
        for j in range(len(code)-i):
            for k in range(i):
                for el1 in table[i-k-1][j]:
                    for el2 in table[k][j+i-k]:
                        try:
                            table[i][j]=dict[str(el1) + " " + str(el2)]
                        except KeyError:
                            continue
                        # temp = str(el1) + " " + str(el2)
                        # if temp in dict:
                        #     print("gabungan ada di dict")
                        #     table[i][j].append(dict[temp])
    for i in range(1, len(code)):
        for j in range(len(code)-i):
            print(table[i][j])

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
cyk(dict, fc)

# v,t = read_cnf('src\out.txt')
# dict = convert_cnf(v,t)
# fc = ['b', 'b']
# cyk(dict, fc)