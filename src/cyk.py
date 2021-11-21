import os
import helper

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
    for i in range(len(terminal_rules)):
        for el in terminal_rules[i][1].split():
            if el in dict:
                dict[el].append(terminal_rules[i][0])
            else:
                temp = []
                temp.append(terminal_rules[i][0])
                dict[el] = temp
    for i in range(len(var_rules)):
        for el in var_rules[i][1].split():
            if el in dict:
                dict[el].append(var_rules[i][0])
            else:
                temp = []
                temp.append(var_rules[i][0])
                dict[el] = temp
    return dict

def read_inp(filename):
    file = os.path.join(os.getcwd(), filename)
    file_content = []
    
    with open(file) as fileinp:
        inp_line = fileinp.readlines()
        for line in inp_line:
            line.replace("    ", "")
            file_content.append(line[:-1])
    
    return file_content

def map_proc(piece):
    mapping = {
        r'[A-z0-9]*' : "string",
        r'[0-9]*' : "number",
        r'[A-Za-z_][A-Za-z_0-9]*' : "variable",
    }

def cyk(dict, code):
    # triangular array of set
    table = [[set([]) for j in range(len(code)-i)] for i in range(len(code))]
    
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
# print("coba")
# print(v[0][1].split())
# dict_test = convert_cnf(v,t)
# print("\nini dict nya")
# print(dict_test)