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
    dict_var = {}
    dict_term = {}

    for el in terminal_rules:
        if el[1] in dict_term:
            dict_term[el[1]].append(el[0])
        else:
            temp = []
            temp.append(el[0])
            dict_term[el[1]] = temp
    for el in var_rules:
        if el[1] in dict_var:
            dict_var[el[1]].append(el[0])
        else:
            temp = []
            temp.append(el[0])
            dict_var[el[1]] = temp

    return dict_term, dict_var

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

fc = read_inp("src\inputAcc.py")
print(fc)

v, t = read_cnf()
print()
print("ini v")
for i in range(len(v)):
    print(v[i])
print()
print("ini t")
for i in range(len(t)):
    print(t[i])
print()
dict_v, dict_t = convert_cnf(v,t)
print("\nini dict V nya")
print(dict_v)
print()
print("\nini dict T nya")
print(dict_t)