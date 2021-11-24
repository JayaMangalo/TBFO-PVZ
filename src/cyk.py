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
    reserved_words = ['+', '-' , '*', '/', '%', '=', '>', '<', '!', '[' ,']', '(' ,')', '\'', '\"', ':', ',', '&', '^', 'variable', 'number', 'string', 'str', 'int', 'float', 'chr', 'double', 'true', 'false', 'none', 'and', 'or', 'not', 'as', 'break', 'continue', 'class', 'def', 'if', 'elif', 'else', 'raise', 'for', 'in', 'from', 'import', 'is', 'pass', 'return', 'while','with','input','print','range']

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
        if (len(stack) > 0 and word != '\'' and word != '\"' and word not in reserved_words):
            new_word.append('string')
        else:
            if(cvn.CheckVariableName(word) and word not in reserved_words):
                new_word.append('variable')
            elif(word != "string" and word != "variable" and cvn.CheckNumber(word)):
                new_word.append('number')
            else: #reserved words
                new_word.append(word)
    return new_word

def cyk(dictG, code):
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
                            table[i][j] = dictG[temp]
    if ('ALGORITHM' in table[-1][-1]):
        print("Accepted")
    else:
        print("Syntax Error")
    

if __name__ == '__main__':
    v, t = read_cnf("out.txt")
    dictGrammar = convert_cnf(v,t)
    fc = read_inp("inputAcc.py")
    cyk(dictGrammar, fc)
