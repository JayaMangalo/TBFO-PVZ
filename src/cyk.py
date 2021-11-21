import os

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

def read_inp(filename):
    file = os.path.join(os.getcwd(), filename)
    file_content = []
    
    with open(file) as fileinp:
        inp_line = fileinp.readlines()
        for line in inp_line:
            line.replace("    ", "")
            file_content.append(line[:-1])
    
    return file_content

# fc = read_inp("src\inputAcc.py")
# print(fc)

# v, t = read_cnf()
# print("ini v")
# print(v)
# print("ini t")
# print(t)