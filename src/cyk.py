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

def cnf_list(dictcnf):
    listcnf = []

    for key in dictcnf:
        listoflist = []
        listoflist.append(key)
        listoflist.append(dictcnf[key])
        listcnf.append(listoflist)
    
    return listcnf

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
            elif(word != "string" and word != "variable" and cvn.CheckNumber(word)):
                new_word.append('number')
            else:
                new_word.append(word)
    return new_word

def cyk(dictG, code, dictUG):
    print()
    print(dictG)
    print()
    print(code)
    listG = cnf_list(dictG)
    print("\nini listG")
    print(listG)
    table = [[[] for j in range(i)] for i in range(len(code),0,-1)]
    for i in range(len(code)):
        if code[i] in dictG:
            table[0][i].extend(dictG[code[i]])
    for i in range(1,len(code)):
        for j in range(len(code)-i):
            for k in range(i):
                for el1 in table[i-k-1][j]:
                    for el2 in table[k][j+i-k]:
                        temp = str(el1) + str(" ") + str(el2)
                        if temp in dictG:
                            print("gabungan ada di dict", end="")
                            table[i][j].extend(dictG[temp])
                            print(table[i][j])
                        else:
                            # search di lhs listG apakah ada el1 dengan el2 lain, simpan rhs nya, ambil el2 lainnya
                            el2new = ""
                            found = False
                            for line in listG:
                                if line[0].split()[0] == el1 and len(line[0].split()) > 1:
                                    found = True
                                    rhs = line[1]
                                    print(line[0])
                                    el2new = line[0].split()[1]
                            # cari el2 lainnya di dictUG apakah kanannya itu ada el2 asli
                            # kalau ya berarti append rhs listG dimana el1 dengan el2 lain
                            if(found):
                                if el2new in dictUG:
                                    if dictUG[el2new][0] == el2:
                                        table[i][j].extend(rhs)
                                print("el2new : ",end="")
                                print(el2new)
                                print("table[i][j] : ", end="")
                                print(table[i][j])

    for i in range(len(code)):
        for j in range(len(code)-i):
            print(table[i][j], end="")
        print()

    if len(table[0][len(code)-1]) != 0:
        print("Accepted")
    else:
        print("Syntax Error")
    

v, t = read_cnf("out.txt")
# print()
# print("ini v")
# for i in range(len(v)):
#     print(v[i])
# print()
# print("ini t")
# for i in range(len(t)):
#     print(t[i])
# print()
dictGrammar = convert_cnf(v,t)
# print("\nini dict nya")
# print(dictGrammar)

dict_unswapped = unswap_convert_cnf(v,t)
# print("\n ini unswapped")
# print(dict_unswapped)

filename = input("Enter filename: ")
fc = read_inp(filename)
print(fc)
cyk(dictGrammar, fc, dict_unswapped)

# v,t = read_cnf('src\out.txt')
# dict = convert_cnf(v,t)
# fc = ['b', 'b']
# cyk(dict, fc)