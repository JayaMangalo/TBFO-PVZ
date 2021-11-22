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
dict = convert_cnf(v,t)
print("\nini dict nya")
print(dict)