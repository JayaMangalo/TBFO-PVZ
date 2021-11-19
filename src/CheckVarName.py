def CheckVariableName(var_name):
    if(not CheckAtoz(var_name[0])):
        return False
    for i in range(len(var_name)-1):
        if not (CheckAtoz(var_name[i]) or Check0to9(var_name[i])):
            return False
    return True
def CheckAtoz(input):
    asci = ord(input)
    return (asci >=65 and asci <=90) or (asci >=97 and asci <=122)
    # if (asci >=65 and asci <=90) or (asci >=97 and asci <=122):
    #     return True
    # else:
    #     return False
def Check0to9(input):
    asci = ord(input)
    return asci >=48 and asci <=57
    # if (asci >=97 and asci <=122):
    #     return True
    # else:
    #     return False


#Tester
Filename = input("MASUKAN NAMA FILE: ");

f = open(Filename, "r")
contents = f.read()
f.close()


print(contents)

if CheckVariableName(contents):
    print("True")
else:
    print("False")