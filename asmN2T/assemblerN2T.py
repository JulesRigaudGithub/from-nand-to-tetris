# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:12:44 2020

@author: jules
"""

import sys

add = sys.argv[1]



with open(add, "r") as asmprog:
    asmstr = asmprog.read().replace(" ","")



asmlst = []

for l in asmstr.split("\n"):
    if not(l.startswith("//") or l == ""):
        asmlst.append(l)
def fstRead(code):
    val = {"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576,"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4}
    m = 16
    ncode = []
    cnt = 0
    for l in code:
        if l.startswith('('):
            k = l.find(")")
            val[l[1:k]] = cnt
        else:
            cnt += 1

    for l in code:
        if l.startswith('@'):
            s = l[1:]
            if not(s.isnumeric()):
                if s in val:
                    ncode.append("@"+str(val[s]))
                else:
                    ncode.append("@"+str(m))
                    val[s] = m
                    m+=1
            else :
                ncode.append(l)
                
        elif not l.startswith("("):
            ncode.append(l)
    return ncode 

def delCom(l):
    k = l.find('//')
    if k > -1 :
        return l[:k]
    else :
        return l
            
def codeLine(s):
    s = delCom(s)
    if s.startswith('@'):
        sbin = bin(int(s[1:]))[2:]
        b = sbin.zfill(16)
    else:
        lst=s.split(";")
        if len(lst)==2:
            j = lst[1]
            if j.startswith("JGT"):
                b1="001"
            elif j.startswith("JEQ"):
                b1="010"
            elif j.startswith("JGE"):
                b1="011"
            elif j.startswith("JLT"):
                b1="100"
            elif j.startswith("JNE"):
                b1="101"
            elif j.startswith("JLE"):
                b1="110"
            elif j.startswith("JMP"):
                b1="111"
            elif j.startswith(""):
                b1="000"
            debut=lst[0]
        else:
            debut=lst[0]
            b1= "000"
        lst2 = debut.split("=")
        
        if len(lst2)==2 :
            
            dest = lst2[0]
            
            if dest == "A":
                d="100"
            elif dest == "M":
                d="001"
            elif dest == "D":
                d="010"
            elif dest == "AM":
                d="101"
            elif dest == "MD":
                d="011"
            elif dest == "AD":
                d="110"
            elif dest == "AMD":
                d="111"
            elif dest == "":
                d = "000"
                
            comp= lst2[1]
            
        else:
            d="000"
            comp=lst2[0]
        
        if comp =="0":
            c = "0101010"
        elif comp =="1":
            c = "0111111"
        elif comp =="-1":
            c = "0111010"
        elif comp =="D":
            c = "0001100"
        elif comp =="A":
            c = "0110000"
        elif comp =="!D":
            c = "0001101"
        elif comp =="!A":
            c = "0110001"
        elif comp =="-D":
            c = "0001111"
        elif comp =="-A":
            c = "0110011"
        elif comp =="-M":
            c = "1001111"
        elif comp =="D+1":
            c = "0011111"
        elif comp =="A+1":
            c = "0110111"
        elif comp =="D-1":
            c = "0001110"
        elif comp =="A-1":
            c = "0110010"
        elif comp =="D+A":
            c = "0000010"
        elif comp =="D-A":
            c = "0010011"
        elif comp =="A-D":
            c = "0000111"
        elif comp =="D&A":
            c = "0000000"
        elif comp =="D|A":
            c = "0010101"
        elif comp =="D|M":
            c = "1010101"
        elif comp =="D&M":
            c = "1000000"
        elif comp =="M-D":
            c = "1000111"
        elif comp =="D-M":
            c = "1010011"  
        elif comp =="D+M":
            c = "1000010"
        elif comp =="M-1":
            c = "1110010"
        elif comp =="M+1":
            c = "1110111"
        elif comp =="!M":
            c = "1110001"
        elif comp =="M":
            c = "1110000"
        b = "111" + c + d + b1
    return b
                
def finalRead(code):
    bcode = []
    for l in code :
        bcode.append(codeLine(l))
    return bcode


addlst = add.split("\\")

name = addlst.pop() 

namelst = name.split(".")

nname = namelst[0] + ".hack"
addlst.append(nname)
nadd = '\\'.join(addlst)

hacklst = finalRead(fstRead(asmlst))
hacktxt = "\n".join(hacklst)

with open(nadd, "w") as hackprog:
    hackprog.write(hacktxt)
