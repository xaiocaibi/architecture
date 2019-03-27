'''
系统入口函数
'''
import initialization
import I_MEM
import D_MEM
import CONST
import instructionSet

if __name__ == '__main__':
    initialization.initial()#初始化系统
    D_MEM.MemInit()#数据载入内存
    I_MEM.InstInit()#代码载入内存
    for i in range (1,1000):
      CONST.reg[CONST.IR] =I_MEM.GetInst(CONST.reg[CONST.pcNum])#根据pc读取指令
      if CONST.reg[CONST.IR] !='xxxx':
       print('pc:',CONST.reg[CONST.pcNum],CONST.reg[CONST.IR])
       CONST.reg[CONST.pcNum] = CONST.reg[CONST.pcNum] + 4
       inst = CONST.reg[CONST.IR]
       instructionSet.Instruction(inst)#执行
      else:
       break
    print('-----------------------------------')
    for i in range (0,32):
      print(D_MEM.LoadInt(i))


