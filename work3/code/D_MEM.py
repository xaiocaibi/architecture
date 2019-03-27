import sys
sys.path.append('../')

import CONST 

def StoreInt(value, addr):
    signFlag = 1
    if value < 0:
        value = -value
        signFlag = -1
    else:
        value = value
        signFlag = 1
    CONST.dMem[CONST.ALIGNMENT*addr+0] = (value>>0) &0xff
    CONST.dMem[CONST.ALIGNMENT*addr+1] = (value>>8) &0xff
    CONST.dMem[CONST.ALIGNMENT*addr+2] = (value>>16) &0xff
    CONST.dMem[CONST.ALIGNMENT*addr+3] = (value>>24) &0x7f
    if signFlag<0:
        CONST.dMem[CONST.ALIGNMENT*addr+3] = CONST.dMem[CONST.ALIGNMENT*addr+3] |0x80
    else:
        CONST.dMem[CONST.ALIGNMENT*addr+3] = CONST.dMem[CONST.ALIGNMENT*addr+3]

    #print(mem[CONST.ALIGNMENT*addr+0],mem[CONST.ALIGNMENT*addr+1],
    #    mem[CONST.ALIGNMENT*addr+2],mem[CONST.ALIGNMENT*addr+3])
    
def LoadInt(addr):
    value = 0
    v0T7 = CONST.dMem[CONST.ALIGNMENT*addr+0] &0xffffffff
    v8T15 = CONST.dMem[CONST.ALIGNMENT*addr+1] &0xffffffff
    v16T23 = CONST.dMem[CONST.ALIGNMENT*addr+2] &0xffffffff
    v24T32 = CONST.dMem[CONST.ALIGNMENT*addr+3] &0xffffffff
    value = v0T7+(v8T15<<8)+(v16T23<<16)+((v24T32&0x7f)<<24)
    if v24T32 &0x80 > 0:
        value = value*(-1)#设置边界，溢出则判负
    else:
        value = value
    return value

def MemInit():
    for memAddr in range(0,255):
        CONST.dMem[memAddr] = 0
    fData=open("data.md")
    line=fData.readline()
    num = 0
    while line:
        StoreInt(int(line),num)
        num = num + 1
        line=fData.readline()

#if __name__ == '__main__':
#    MemInit()
#    for i in range(0,32):
#        print(LoadInt(i))

