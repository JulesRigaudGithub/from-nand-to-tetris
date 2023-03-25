# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 15:43:36 2022

@author: jules
"""


import sys
import re



PUSH_D_TO_SP = """@SP
A=M
M=D
@SP
M=M+1
"""

POP_SP_TO_D = """@SP
AM=M-1
D=M
"""


VIRTUAL_MEMORY_TO_D = {
"DynamicSegment" : """@{index}
D=A
@{segment}
A=D+M
D=M
""",

"StaticPointer" : """@{staticAddress}
D=M
""",

"Constant" : """@{constant}
D=A
"""
}

D_TO_VIRTUAL_MEMORY = {
"DynamicSegment" : """@R13
M=D
@{index}
D=A
@{segment}
D=D+M
@R14
M=D
@R13
D=M
@R14
A=M
M=D
""",

"StaticPointer" : """@{staticAddress}
M=D
"""
}


SEGMENT_ADDRESS = {
    "local" : "LCL",
    "argument" : "ARG",
    "this" : "THIS",
    "that" : "THAT",
    "temp" : 5,
    "pointer" : 3,
    "constant" : None,
    "static" : None
}


ARITHMETIC_TRANSLATION = {
"add" : """@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
""",
"sub" : """@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
""",
"neg" : """@SP
A=M-1
M=-M
""",
"eq" : """@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@{jumpLabel}
D;JEQ
@SP
A=M-1
M=0
({jumpLabel})
""",
"gt" : """@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@{jumpLabel}
D;JGT
@SP
A=M-1
M=0
({jumpLabel})
""",
"lt" : """@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@{jumpLabel}
D;JLT
@SP
A=M-1
M=0
({jumpLabel})
""",
"and" : """@SP
AM=M-1
D=M
@SP
A=M-1
M=D&M
""",
"or" : """@SP
AM=M-1
D=M
@SP
A=M-1
M=D|M
""",
"not" : """@SP
A=M-1
M=!M
""",
}

COMMAND_TYPE = {
    "add" : (1, "C_ARITHMETIC"),
    "sub" : (1, "C_ARITHMETIC"),
    "neg" : (1, "C_ARITHMETIC"),
    "eq" : (1, "C_ARITHMETIC"),
    "gt" : (1, "C_ARITHMETIC"),
    "lt" : (1, "C_ARITHMETIC"),
    "and" : (1, "C_ARITHMETIC"),
    "or" : (1, "C_ARITHMETIC"),
    "not" : (1, "C_ARITHMETIC"),

    "pop" : (3, "C_POP"),
    "push" : (3, "C_PUSH"),

    "label" : (2, "C_LABEL"),
    "goto" : (2, "C_GOTO"),
    "if-goto" : (2, "C_IF"),

    "function" : (3, "C_FUNCTION"),
    "call" : (3, "C_CALL"),
    "return" : (1, "C_RETURN")
}



class VMSyntaxError(Exception):
    pass

class Parser:

    def __init__(self, path):

        self._file = []
        self.currentCommand = None
        self.name = path.split('.')[-2]

        with open(path, 'r') as file:
            self._file = file.readlines()
        
        self._cleanLines()
    
    @staticmethod
    def _checkSyntax(commandLine):
        command_length = len(commandLine)

        if (command_length == 0) or (command_length > 3):
            return False

        mainCommand = commandLine[0]
        
        if mainCommand not in COMMAND_TYPE:
            return False

        if command_length != COMMAND_TYPE[mainCommand][0]:
            return False

        commandType = COMMAND_TYPE[mainCommand][1]
        if commandType == "C_ARIMTHMETIC":
            pass
        elif commandType == "C_POP":

            if commandLine[1] not in SEGMENT_ADDRESS or not(commandLine[2].isnumeric()):
                return False
            if commandLine[1] == "constant":
                return False

        elif commandType == "C_PUSH":

            if commandLine[1] not in SEGMENT_ADDRESS or not(commandLine[2].isnumeric()):
                return False

        elif commandType == "C_FUNCTION":

            return False

        elif commandType == "C_CALL":

            return False

        elif commandType == "C_RETURN":

            return False

        elif commandType == "C_LABEL":

            return False

        elif commandType == "C_GOTO":

            return False

        elif commandType == "C_IF":

            return False
        
        return True

    def _cleanLines(self):
        tmp_lst = []
        for line in self._file:
            if not line.startswith("//") and not line == "":
                line = line.lstrip()   #On enlève les espaces à gauche
                line = re.sub('//.*', '', line) #On enlève le commentaire
                line = line.rstrip() #On enlève les espaces à gauche
                line = re.sub('\s+', ' ', line) #On enlève les espaces multiples

                if line == "":
                    pass
                elif self._checkSyntax(line.split(" ")):
                    tmp_lst.append(line)
                else:
                    raise VMSyntaxError("Erreur syntaxe : " + repr(line))
        
        self._file = tmp_lst

    def hasMoreCommand(self):
        return not(self._file==[])

    def advance(self):
        try:
            instruction = self._file.pop(0)
        except IndexError:
            return None
        instruction = instruction.split(" ")
        self.currentCommand = instruction
    
    def commandType(self):
        nameCmd = self.currentCommand[0]
        return COMMAND_TYPE[nameCmd][1]
    
    def arg1(self):
        if self.commandType() == 'C_ARITHMETIC':
            return self.currentCommand[0]
        elif self.commandType() == 'C_RAISE':
            return None
        else:
            return self.currentCommand[1]


    def arg2(self):
        if self.commandType() == 'C_POP' or self.commandType() == 'C_PUSH' or self.commandType() == 'C_FUNCTION' or self.commandType() == 'C_CALL':
            return int(self.currentCommand[2])
        else:
            return None




class CodeWriter:

    def __init__(self, name):
        self._labelCount = 0
        self._name = name
        self._path = self._name + '.asm'
        self._file = open(self._path, 'w')
    
    
    def _newLabel(self):
        self._labelCount += 1
        return str(self._labelCount)

    def closeWriter(self):
        self._file.close()
    
    def writeArithmetic(self, command):
        comment = "//" + command + "\n"
        ASMCode = ARITHMETIC_TRANSLATION[command]

        if command in ('eq', 'gt', 'lt'):
            ASMCode = ASMCode.format(jumpLabel=command + self._newLabel())

        self._file.write(comment)
        self._file.write(ASMCode)
    
    def _readVirtualMemory(self, currentSegment, currentIndex):
        """returns asm code to load virtual memory address to D register"""

        if currentSegment in ("local", "argument", "this", "that"):
            addressLabel = SEGMENT_ADDRESS[currentSegment]
            ASMCode = VIRTUAL_MEMORY_TO_D["DynamicSegment"].format(index=currentIndex, segment=addressLabel)

        elif currentSegment in ("static", "temp", "pointer"):
            ASMCode = VIRTUAL_MEMORY_TO_D["StaticPointer"]
            if currentSegment == "static":
                address = self._name + f".{currentIndex}"
            else:
                address = SEGMENT_ADDRESS[currentSegment] + int(currentIndex)

            ASMCode = ASMCode.format(staticAddress=address)
        else:
            """cas constant"""
            ASMCode = VIRTUAL_MEMORY_TO_D["Constant"]
            ASMCode = ASMCode.format(constant=currentIndex)
        
        return ASMCode
    

    def _writeVirtualMemory(self, currentSegment, currentIndex):
        """returns asm code to write D register content to virtual memory"""

        if currentSegment in ("local", "argument", "this", "that"):
            addressLabel = SEGMENT_ADDRESS[currentSegment]
            ASMCode = D_TO_VIRTUAL_MEMORY["DynamicSegment"].format(index=currentIndex, segment=addressLabel)

        else:
            ASMCode = D_TO_VIRTUAL_MEMORY["StaticPointer"]
            if currentSegment == "static":
                address = self._name + f".{currentIndex}"
            else:
                address = SEGMENT_ADDRESS[currentSegment] + int(currentIndex)

            ASMCode = ASMCode.format(staticAddress=address)
        
        return ASMCode
    

    def writePushPop(self, command, segment, index):

        comment = "//" + " ".join([command, segment, index]) + "\n"
        

        if command == 'push':
            readMemory = self._readVirtualMemory(segment, index)
            ASMCode = comment + readMemory + PUSH_D_TO_SP
            
            self._file.write(ASMCode)
        
        if command == 'pop':
            writeMemory = self._writeVirtualMemory(segment, index)
            ASMCode = comment + POP_SP_TO_D + writeMemory
            
            self._file.write(ASMCode)

        else:
            return None







def main():

    VMFileName = sys.argv[1]

    mainParser = Parser(VMFileName)

    output = CodeWriter(mainParser.name)

    while mainParser.hasMoreCommand():
        mainParser.advance()
        nextCommandType = mainParser.commandType()

        if nextCommandType == 'C_ARITHMETIC':
            command = mainParser.arg1()
            output.writeArithmetic(command)

        elif nextCommandType in ('C_PUSH', 'C_POP'):
            output.writePushPop(*mainParser.currentCommand)
    
    output.closeWriter()

if __name__ == "__main__":
    main()
