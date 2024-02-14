# *********************** IMPORTS *****************************
import sys

# *********************** REGS *****************************
# Register File (RF): The RF takes in the register name (R0, R1, ... R6 or FLAGS) and
# returns the value stored at that register.
# here R is the RF
#f1 = open("Simple_Simulator/input.txt","r")
#f2 = open("Simple_Simulator/output.txt","w")

R = {
    "000": 0,
    "001": 0,
    "010": 0,
    "011": 0,
    "100": 0,
    "101": 0,
    "110": 0,
    "111": 0,
}


opcodeStack = {
    "00000": "A",
    "00001": "A",
    "00010": "B",
    "00011": "C",
    "00100": "D",
    "00101": "D",
    "00110": "A",
    "00111": "C",
    "01000": "B",
    "01001": "B",
    "01010": "A",
    "01011": "A",
    "01100": "A",
    "01101": "C",
    "01110": "C",
    "01111": "E",
    "11100": "E",
    "11101": "E",
    "11111": "E",
    "11010": "F",
}

# *********************** CONVERSIONS *****************************

def decimalConverter(binStr): #binary to integer
    l=len(binStr)
    sum=0
    pow=0
    for i in range(l-1,-1,-1):
        sum=sum+((2**pow)*int(binStr[i]))
        pow=pow+1
    return sum  
        

def binaryConverter(num, bitSize): #integer to binary
   
    con_num = []
    while num >= 1:
        rem = num % 2
        con_num.append(str(int(rem)))
        num = num // 2
    con_num = con_num[::-1]
    bin = "".join(con_num)
    if len(bin) < bitSize:
        bin = "0" * (bitSize - len(bin)) + bin
    return bin


# ************************ BHAI YE CHAHIYE Q2 KE LIYE?, PLS CONFIRM!   NAHII NAHII Q3 KE LIYE ***************************

def floatValidity(imm: str):
    imm = list(imm)
    if imm[0] == "$":
        try:
            imm = float("".join(imm[1:]))
            if (
                type(imm) == float
            ):  # ADD and imm in range(), the range of M and exponent
                return True
        except ValueError:
            print("Invalid immediate.")
            return False
    return False

# *************************** MEM *****************************

# Memory (MEM): MEM takes in an 7 bit address and returns a 16 bit value as the data.
# The MEM stores 256 bytes, initialized to 0s.

TOT_SIZE = 128
mem_stack = ["0000000000000000"] * TOT_SIZE


def fileReader():
    assembleOut = []
    for kx in sys.stdin:
        assembleOut.append(kx)
    i=0
    for line in assembleOut:
        mem_stack[i] = line.rstrip("\n")
        i=i+1

def dump_memory():
    for Address in mem_stack:
        sys.stdout.write(Address+'\n')

PC = 0 #Program Counter (PC): The PC is an 7 bit register which points to the current instruction.
Cycle = 0
Cycle = -1
temp = []

hltFlag = 0

fileReader()
#print("REACHED")

# ******************************** EE *******************************

# Execution Engine (EE): The EE takes the address of the instruction from the PC, uses it
# to get the stored instruction from MEM, and executes the instruction by updating the RF
# and PC.

def FloatConversion(binNum: str):
    e = binNum[:3]
    M = binNum[3:]
    str_M = "".join(M)
    str_M = "1"+str_M # significand

    e = bin(decimalConverter(e))[2:]
    new = decimalConverter(M[: -(len(e))])

    e = list(e)
    e1 = []
    for i in e:
        e1.append(int(i))
    res = 0
    j = 1
    for i in e1:
        res += (i * 2) ** (-j)
        j += 1
    ans = new + res
    return ans


def resetFlag(): # !!!!!!!!!!!!!!! PLS EXPLAIN THE PURPOSE OF THIS !!!!!!!!!!!!!!!!
    R["111"] = 0


def findOpcodeType(op_bin):  # takes the opcodeode in binary
    return opcodeStack[op_bin]


def movImm(reg1, imm):  # assuming immediate is already a decimal here
    R[reg1] = imm
    resetFlag()
    dump()


def movReg(reg1, reg2):
    R[reg2] = R[reg1]
    resetFlag()
    dump()


def add(reg1, reg2, reg3):
    R[reg1] = R[reg2] + R[reg3]
    if R[reg1] > 65535:
        R[reg1] = R[reg1] % 65535  # make all bits 1 in reg1
        R["111"] = 8  # setting overflow flag
        dump()
    else:
        resetFlag()
        dump()


def sub(reg1, reg2, reg3):
    R[reg1] = R[reg2] - R[reg3]
    if R[reg1] < 0:
        R[reg1] = 0  # case of underflow
        R["111"] = 8  # setting overflow flag
        dump()
    else:
        resetFlag()
        dump()


def OR(reg1, reg2, reg3):
    R[reg1] = R[reg2] | R[reg3]
    resetFlag()
    dump()


def mul(r1, r2, r3):
    R[r1] = R[r2] * R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def divide(r1, r2):
    R["000"] = int(R[r1] / R[r2])
    R["001"] = int(R[r1] % R[r2])
    if R[r1] < 0:
        R["000"] = 0  # case of underflow
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def rShift(r1, imm):
    R[r1] = R[r1] >> imm
    if R[r1] < 0:
        R[r1] = 0  # case of underflow
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def lShift(r1, imm):
    R[r1] = R[r1] << imm
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8
        dump()
    else:
        resetFlag()
        dump()


def xor(r1, r2, r3):
    R[r1] = R[r2] ^ R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def AND(r1, r2, r3):
    R[r1] = R[r2] & R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def invert(reg1, reg2):
    R[reg1] = 65535 ^ R[reg2]
    resetFlag()
    dump()


def compare(r1, r2):
    resetFlag()
    if R[r1] == R[r2]:
        R["111"] = 1
    elif R[r1] > R[r2]:
        R["111"] = 2
    else:
        R["111"] = 4
    dump()


def load(r1, mem):
    R[r1] = decimalConverter(mem_stack[decimalConverter(mem)])
    resetFlag()
    dump()


def store(r1, mem):
    
    mem_stack[decimalConverter(mem)] = binaryConverter(R[r1], 16)
    resetFlag()
    dump()


def jmp(mem):
    resetFlag()
    dump()
    global PC
    PC = decimalConverter(mem)


def jgt(line):
    global PC
    if R["111"] == 2:
        resetFlag()
        dump()
        PC = decimalConverter(line)
    else:
        resetFlag()
        dump()
        PC += 1

def float_add(r1, r2, r3):
    # add floating point r2 and r3 and store in r1
    dec_r2 = FloatConversion(R[r2])
    dec_r3 = FloatConversion(R[r3])
    R[r1] = dec_r2 + dec_r3
    if FloatConversion(R[r2])+FloatConversion(R[r3]) > 15.75:
        R["111"] = 8
        R[r1] = 15.75
        dump()
    else:
        resetFlag()
        dump()


def float_sub(r1, r2, r3):
    # subtract floating point r2 and r3 and store in r1
    dec_r2 = FloatConversion(R[r2])
    dec_r3 = FloatConversion(R[r3])
    R[r1] = dec_r2 - dec_r3
    if FloatConversion(R[r2])-FloatConversion(R[r3]) < 0:
        R["111"] = 8

        R[r1] = 0
        
        dump()
    else:
        resetFlag()
        dump()


def float_mov(r1, imm):
    R[r1] = FloatConversion(imm)
    resetFlag()
    dump()


def je(line):
    global PC
    if R["111"] == 1:
        resetFlag()
        dump()
        PC = decimalConverter(line)
    else:
        resetFlag()
        dump()
        PC += 1


def jlt(line):
    global PC
    if R["111"] == 4:
        resetFlag()
        dump()
        PC = decimalConverter(line)
    else:
        resetFlag()
        dump()
        PC += 1


def dump():
    # print(binaryConverter(int(PC), 7), end=" ")
    sys.stdout.write(binaryConverter(int(PC), 7))
    sys.stdout.write("        ")
    
    for reg in R:
        # print(binaryConverter(int(R[reg]), 16), end=" ")
        sys.stdout.write(binaryConverter(int(R[reg]), 16))
        sys.stdout.write(" ")
    sys.stdout.write("\n")


lines = []

count = 0
while hltFlag != 1:
    count += 1
    if count > 100000:
        break
    Cycle += 1
    line = mem_stack[PC]
    opcode = line[0:5]
    opcodeType = findOpcodeType(opcode)

    if opcodeType == "A":
        reg1 = line[7:10].strip()
        reg2 = line[10:13].strip()
        reg3 = line[13:].strip()

        if opcode == "00000":
            add(reg1, reg2, reg3)
            PC += 1

        elif opcode == "00001":
            sub(reg1, reg2, reg3)
            PC += 1

        elif opcode == "00010":
            mul(reg1, reg2, reg3)
            PC += 1

        elif opcode == "01010":
            xor(reg1, reg2, reg3)
            PC += 1

        elif opcode == "01011":
            OR(reg1, reg2, reg3)
            PC += 1

        elif opcode == "01100":
            AND(reg1, reg2, reg3)
            PC += 1


        elif opcode == "10000":
            float_add(reg1, reg2, reg3)

        elif opcode == "10001":
            float_sub(reg1, reg2, reg3)
          

    elif opcodeType == "B":
        reg1 = line[6:9].strip()
        imm1 = line[9:].strip()
        imm = decimalConverter(line[9:].strip())

        if opcode == "00010":
            movImm(reg1, imm)
            PC += 1

        elif opcode == "01001":
            lShift(reg1, imm)
            PC += 1

        elif opcode == "01000":
            rShift(reg1, imm)
            PC += 1

        elif opcode == "10010":
            reg1=line[5:8].strip()
            imm1=line[8:].strip()
            float_mov(reg1, imm1)

    elif opcodeType == "C":
        reg1 = line[10:13].strip()
        reg2 = line[13:].strip()

        if opcode == "00011":
            movReg(reg1, reg2)
            PC += 1

        elif opcode == "00111":
            divide(reg1, reg2)
            PC += 1

        elif opcode == "01101":
            invert(reg1, reg2)
            PC += 1

        elif opcode == "01110":
            compare(reg1, reg2)
            PC += 1

    elif opcodeType == "D":
        reg1 = line[6:9].strip()

        memAddr = line[9:].strip()

        if opcode == "00100":
            load(reg1, memAddr)
            PC += 1

        elif opcode == "00101":
            store(reg1, memAddr)
            PC += 1

    elif opcodeType == "E":
        memAddr = line[9:].strip()

        if opcode == "01111":
            jmp(memAddr)

        elif opcode == "11100":
            jlt(memAddr)

        elif opcode == "11101":
            jgt(memAddr)

        elif opcode == "11111":
            je(memAddr)

    elif opcodeType == "F":
        hltFlag = 1
        resetFlag()
        dump()
        break
dump_memory()