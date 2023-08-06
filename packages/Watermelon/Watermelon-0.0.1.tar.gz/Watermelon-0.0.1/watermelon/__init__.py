def squeeze(codeFile : str ,outputFile : str):
    cf = open(codeFile)
    of = open(outputFile,"w+b")
    f = ' '.join(format(ord(x), 'b') for x in cf.read())
    of.write(bytes(f,"UTF-8"))

def smash(file : str):
    of = open(file, "r+b")
    binary_values = of.read().split()
    ascii_string = ""
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character
    open(file + ".py","w").write(ascii_string)