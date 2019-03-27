#InstInit（）将指令存入内存
#GetInst(pcNum)将指令取出
import sys
sys.path.append('../')
import CONST
import initialization

def InstInit():
    fInst=open("instructions.md")
    line=fInst.readline()
    tInstNum=0
    while line:
        tLine = line.replace("\n","")
        CONST.IMem[tInstNum] = tLine
        tInstNum=tInstNum+1
        line=fInst.readline()
    CONST.instNum[0]=tInstNum

def GetInst(pcNum):
    Iplace = int(pcNum/4)
    if int(Iplace > CONST.instNum[0]-1):
        return "xxxx"
    else:
        return CONST.IMem[Iplace]

if __name__ == '__main__':
    initialization.initial()
    InstInit()
    for i in range(0,3):
        print(GetInst(i*4))

