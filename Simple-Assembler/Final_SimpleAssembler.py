import sys

lineCount = 0  # Counting number of lines entered till now
cmd_list = [] #List where commads readd from file are stored
variables = []
commands = []
labels = {}
instrn_count = 0 
parentstr=""

# f1=open("machine_code_ouput.txt","w")
opcode = {
    "add": ("00000", "A"),
    "addf":("10000","A"),
    "sub": ("00001", "A"),
    "subf":("10001","A"),
    "mov": [("00010", "B"), ("00011", "C")],
    "movf":("10010","A"),
    "ld": ("00100", "D"),
    "st": ("00101", "D"),
    "mul": ("00110", "A"),
    "div": ("00111", "C"),
    "rs": ("01000", "B"),
    "ls": ("01001", "B"),
    "xor": ("01010", "A"),
    "or": ("01011", "A"),
    "and": ("01100", "A"),
    "not": ("01101", "C"),
    "cmp": ("01110", "C"),
    "jmp": ("01111", "E"),
    "jlt": ("11100", "E"),
    "jgt": ("11101", "E"),
    "je": ("11111", "E"),
    "hlt": ("11010", "F")
}

registers = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
}

registersF = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111",
}

def isValidCmd(line: str):
    cmd = (line.strip()).split()[0]
    if cmd in opcode.keys():
        return True
    if cmd == "var":
        return True
    return False


def duplicateVar(varName: str, variables: list):
    if varName in variables:
        return False
    else:
        return False


def duplicateLabel(labelName: str):
    for label in labels.keys():
        if label == labelName:
            return True


def labelValidity(labelName: str):
    if duplicateLabel(labelName):
        sys.stdout.write("Error: Duplicate label name: " + labelName)
        exit()
    elif duplicateVar(labelName,variables):
        sys.stdout.write("Error: Label name is same as variable name: " + labelName)
        exit()
    else:
        return True


def varNameValidity(varName: str):
    if duplicateVar(varName,variables):
        sys.stdout.write("Error: Duplicate Variable Name")
        return False
    if varName.isdigit(): 
        sys.stdout.write("Error:Varibale name cant be all digits ")
        return False
    if duplicateLabel(varName):
        sys.stdout.write("Error: Variable name is same as label name: " + varName)
        return False
    return True


def regValidity(reg: str):
    if reg in registersF.keys():
        return True
    return False


def immediateValidity(imm: str):
    imm = list(imm)
    if imm[0] == "$":
        imm = "".join(imm[1:])
        if imm.isdigit() and (int(imm) in range(0, 128)):
            return True
        else:
            sys.stdout.write("Error: Imm more than 7 bits: " + imm)
            return False
    return False


def lenChecker(line: str):
    if isValidCmd(line) or line[-1] == ":":
        line = line.split()
        cmd = line[0]
        if cmd == "mov" and immediateValidity(line[2]):
            return True
        elif cmd == "mov" and regValidity(line[2]):
            return True
        elif opcode[cmd][1] == "A" and len(line) == 4:
            return True
        elif opcode[cmd][1] == "B" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "C" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "D" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "E" and len(line) == 2:
            return True
        elif opcode[cmd][1] == "F" and len(line) == 1:
            return True
        elif line[-1] == ":":
            if line[:-1].isalnum():
                return True
            else:
                sys.stdout.write("Label isn't alphanumeric")
    return False


def isValidMemAddr(line: str):
    cmd = line.split()[0]
    jumpCommands = ["jmp", "jlt", "jgt", "je"]
    loadStore = ["ld", "st"]
    if cmd in jumpCommands:
        if line.split()[1] in labels.keys():
            return True
        else:
            sys.stdout.write("Label not found: " + line.split()[1])
            exit()
    elif cmd in loadStore:
        if line.split()[2] in variables:
            return True
        else:
            sys.stdout.write("Variable not found: " + line.split()[2])
            exit()

    return False



def isLineValid(line: str):
    if lenChecker(line):
        line = line.split()
        cmd = line[0]
        if cmd == "mov":
            if regValidity(line[1]):
                if immediateValidity(line[2]):
                    return True
                elif regValidity(line[2]):
                    return True
                else:
                    return False
            elif line[1] == "FLAGS" and regValidity(line[2]):
                return True
            elif line[2] == "FLAGS":
                sys.stdout.write("Illegal use of FLAGS register. Command: " + " ".join(line))
                exit()
            else:
                return False
        if "FLAGS" in line:
            if(line[0] == "mov"): 
                return True
            else: 
                sys.stdout.write("Illegal use of FLAGS register. Command: " + " ".join(line))
                exit()
        if opcode[cmd][1] == "A":
            if regValidity(line[1]) and regValidity(line[2]) and regValidity(line[3]):
                return True
        elif opcode[cmd][1] == "B":
            if regValidity(line[1]) and immediateValidity(line[2]):
                return True
        elif opcode[cmd][1] == "C":
            if regValidity(line[1]) and regValidity(line[2]):
                return True
        elif opcode[cmd][1] == "D":
            if regValidity(line[1]) and isValidMemAddr(" ".join(line)):
                return True
        elif opcode[cmd][1] == "E":
            if isValidMemAddr(" ".join(line)):
                return True
        elif opcode[cmd][1] == "F":
            if len(line) == 1:
                return True #False
        elif line[-1] == ":":
            return True 
        else:
            return False
    else:
        return False

# f=open("input_file.txt","r")
# cmd_list = f.readlines()
for kx in sys.stdin:
    cmd_list.append(kx)
org_cmd_list = [line.strip() for line in cmd_list]
cmd_list = [line for line in org_cmd_list if line != ""]
# f.close()
#print(cmd_list) #Extra

def splitter():
    parentstr = ""

    if len(cmd_list) > 128: 
       print("Lines exceed 128")
       exit()

    flagVarOver = 0
    for i in range(0,len(cmd_list)):
        line=cmd_list[i].split()
        #checking for variable validity
        if line[0] == "var":
            if len(line) == 2:
                if flagVarOver: 
                    sys.stdout.write("Error in line "+str(i+1)+" Variables found after the beginning")
                    exit()
                else:
                    var = line[1]
                    if duplicateVar(var,variables):
                        sys.stdout.write("Error in line"+str(i+1)+": Duplicate variable name: {var}")
                        exit()
                    else:
                        if varNameValidity(var):
                            variables.append(var)
                            continue
                        else:
                            exit()
            else:
                sys.stdout.write("General Syntax Error in line"+str (i+1))
                exit()
        else:
            flagVarOver = 1 #1 = True
        #checking for label validity        
        if line[0][-1] == ":": 
            if not labelValidity(line[0][:-1]):
                exit()
            else:
                labels[line[0][:-1]] = i - len(variables) 
                continue
            
    #checking for validity of other commands
    for cmd in cmd_list[len(variables):]:
        if ":" in cmd: 
            cmd1 = cmd.split(":")[1].strip()
            #print(cmd1)
            if (cmd1==""):
                sys.stdout.write("Error in line"+str(org_cmd_list.index(cmd)+1)+" : Empty label defined")
                exit()
            
            if isValidCmd(cmd1):
                if isLineValid(cmd1): 
                    commands.append(cmd1)
                else:
                    sys.stdout.write("General Syntax Error on line"+ str(org_cmd_list.index(cmd)+1)+str(cmd))
                    exit()
            else:
                sys.stdout.write("General Syntax Error on line {org_cmd_list.index(cmd)+1}:"+str(cmd))
                exit()
        elif isValidCmd(cmd):
            if isLineValid(cmd): 
                commands.append(cmd)
            else:
                sys.stdout.write("General Syntax Error on line"+str(org_cmd_list.index(cmd)+1)+":"+str(cmd))
                exit()
        else:
            sys.stdout.write("Error: Invalid Command on line " +  str({org_cmd_list.index(cmd)+1}) + ": " + cmd)
            exit()
    
    for cmd in cmd_list[len(variables) :]:
        if (cmd[0] == "ld") or (cmd[0] == "st"):
            if cmd[-1] not in variables:
                sys.stdout.write("Error: Invalid Command: Variable Does NOT Exist " + str({org_cmd_list.index(cmd)+1}) + ": " + cmd)
                exit()
    
    #print(variables) #EXTRA
    #print(commands)
    #print(labels)

    hltCount = 0
    #checking for halt commands
    for c in commands:
        if c == "hlt":
            hltCount += 1

    #print(hltCount) #EXTRA
    if hltCount > 1:
            sys.stdout.write("Error: More than one hlt instruction found")
            exit()
    elif hltCount == 0:
        sys.stdout.write("Error: No hlt instruction found")
        exit()
    elif commands[-1]!="hlt":
        sys.stdout.write("Error: hlt should be the last command")
    else:
        for key in labels.keys(): 
            labels[key] = make_7bit_binary(labels[key])

    #Calling main function        
    # for i in range(len(variables),len(cmd_list)):
    #     line=cmd_list[i].split()
    #     parentstr += assembleOut(line) 
    #     parentstr += "\n"
    
    for cc in commands:
        parentstr += assembleOut(cc.strip().split())
        parentstr += "\n"
    
    
    sys.stdout.write(parentstr)   
        
        

def make_7bit_binary(num):
    con_num = []
    while num >= 1:
        rem = num % 2
        con_num.append(str(int(rem)))
        num = num // 2
    con_num = con_num[::-1]
    bin = "".join(con_num)
    if len(bin) < 7:
        bin = "0" * (7 - len(bin)) + bin
    return bin

def isFloatValid(immStr: str):
    immList = list(immStr)
    if immList[0] == "$":
        try:
            immFloat = float("".join(immList[1:]))
            if type(immFloat) == float:
                # Add additional conditions for range check
                # Example: if immFloat >= lower_bound and immFloat <= upper_bound:
                return True
        except ValueError:
            print("Invalid immediate.")
            return False
    return False


def make_8bit_binary_float(floatNumStr: str):
    def isFloatValid(floatStr):
        try:
            float(floatStr)
            return True
        except ValueError:
            return False

    if not isFloatValid(floatNumStr):
        sys.stdout.write("Invalid float")
        
        exit()

    floatNum = float(floatNumStr)
    if floatNum < 1:
        sys.stdout.write("Invalid float. Cannot be represented since it is less than 1.")
        
        exit()

    integerPart = int(floatNum)
    fractionalPart = floatNum - integerPart
    binaryIntPart = bin(integerPart)[2:]
    mantissa = list(str(binaryIntPart))

    fractionalBits = []
    while len(mantissa) != 5:
        fractionalPart *= 2

        if fractionalPart > 1:
            fractionalBits.append(str(1))
            fractionalPart -= 1
        elif fractionalPart < 1:
            fractionalBits.append(str(0))
        elif fractionalPart == 1:
            fractionalBits.append(str(1))
            break

    mantissa = mantissa[1:] + fractionalBits

    if len(mantissa) > 5:
        mantissa = mantissa[:5]

    exponent = len(str(binaryIntPart))

    if exponent > 7:
        sys.stdout.write("Exponent > 7. Overflow.")
        exit()

    exponent = bin(exponent - 1)[2:].zfill(3)

    while len(mantissa) < 5:
        mantissa.append("0")

    mantissa = "".join(mantissa)
    return exponent + mantissa




def typeA(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "00"
    r1 = registersF[cmd[1]]
    r2 = registersF[cmd[2]]
    r3 = registersF[cmd[3]]
    strout += r1 + r2 + r3
    return strout

def typeB(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    if cmd[0] == "movf":
        strout+=opcode[cmd[0]]
        r1 = registersF[cmd[1]]
        strout += r1
        imm = cmd[2][1:]
        immbin=make_8bit_binary_float(imm)
        strout+=immbin
        return strout
        
    else:        
        if cmd[0] == "mov":
            strout += opcode[cmd[0]][0][0]
        else:
            strout += opcode[cmd[0]][0]
        strout += "0"
        r1 = registersF[cmd[1]]
        strout += r1
        imm = cmd[2][1:] #as 0 is $
        immbin = make_7bit_binary(int(imm))
        strout += immbin
        return strout

def typeC(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    if cmd[0] == "mov":
        strout += opcode[cmd[0]][1][0]
    else:
        strout += opcode[cmd[0]][0]
    strout += "00000"
    r1 = registersF[cmd[1]]
    strout += r1
    r2 = registersF[cmd[2]]
    strout += r2
    return strout

def typeD(cmd): #the same list given to "assembleOut" is given here
    ind = 0
    strout = ""
    if cmd[-1] in variables:
            for i in range(len(variables)):
                if variables[i] == cmd[-1]:
                    ind = i + len(commands) - 1 
                    break
            mem_addr = instrn_count + (ind + 1)
            bin_mem_addr = make_7bit_binary(mem_addr)
            strout = opcode[cmd[0]][0] + "0" + registersF[cmd[1]] + bin_mem_addr
    else:
        pass 
    return strout

def typeE(cmd): #the same list given to "assembleOut" is given here
    ind = 0
    if cmd[-1] in variables:
        for i in range(len(variables)):
            if variables[i] == cmd[-1]:
                ind = i + len(commands) - 1 
                break
        mem_addr = instrn_count + (ind + 1)
        bin_mem_addr = make_7bit_binary(mem_addr)
    elif cmd[-1] in labels:
        bin_mem_addr = labels[cmd[-1]]
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "0000"
    strout += bin_mem_addr
    return strout


def assembleOut(cmd):
    #if encountered type is A
    typeA_ins = ["add", "sub", "mul", "xor", "or", "and","addf"]
    if (cmd[0] in typeA_ins): return typeA(cmd)

    #if encountered type is B
    typeB_ins = ["mov", "rs", "ls"]
    if((cmd[0] in typeB_ins) and ('$' in cmd[2])): return typeB(cmd)

    #if encountered type is C
    typeC_ins = ["mov", "div", "not", "cmp"]
    if (cmd[0] in typeC_ins): return typeC(cmd)

    #if encountered type is D
    typeD_ins = ["ld", "st"]
    if (cmd[0] in typeD_ins): return typeD(cmd)

    #if encountered type is E
    typeE_ins = ["jmp", "jlt", "jgt", "je"]
    if (cmd[0] in typeE_ins): return typeE(cmd)

    #if encountered type is F
    else: 
        return "1101000000000000"

splitter()
#f1.close()