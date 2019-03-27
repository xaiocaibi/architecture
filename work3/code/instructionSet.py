'''
系统指令集合
'''
import CONST
import re
import I_MEM
import D_MEM
#负数处理
#可能存在的异常信息
massage = [0] 
#对立即数范围进行限制(20 bits)，T为U时为无符号位，否则为有符号
def data_pro_20(para3,T):
      if T== 'U':
        imme_num = int(para3)&0xfffff#(20位）
      else:
        imme_num = int(para3)
      return imme_num
#对立即数范围进行限制(12 bits)
def data_pro_12(para3):
      if para3>0:
        boun = (para3)&0x800#取最高长度
        if boun != 0:
          imme_num = -(int(para3)&0x7ff)#如果最高位（第12位）为1，负数，变号处理
        else:
          imme_num = int(para3)&0x7ff#如果最高位（第12位）为1，正数
      else:
        if para3 > -0xfff:
          imme_num = -(int(-para3)&0x7ff)
        else:
          boun = (-para3)&0x800#取最高长度
          if boun != 0:
            imme_num = -(int(-para3)&0x7ff)#如果最高位（第12位）为1，负数，变号处理
          else:
            imme_num = int(-para3)&0xfff#如果最高位（第12位）为1，正数
      return imme_num
#对立即数范围进行限制(7 bits)
def data_pro_7(para3):
      if para3>0:
        boun = (para3)&0x70#取最高长度
        if boun != 0:
          imme_num = -(int(para3)&0x3f)#如果最高位（第12位）为1，负数，变号处理
        else:
          imme_num = int(para3)&0x3f#如果最高位（第12位）为1，正数
      else:
        if para3 > -0x3f:
          imme_num = -(int(-para3)&0x3f)
        else:
          boun = (-para3)&0x70#取最高长度
          if boun != 0:
            imme_num = -(int(-para3)&0x3f)#如果最高位（第12位）为1，负数，变号处理
          else:
            imme_num = int(-para3)&0x3f#如果最高位（第12位）为1，正数
      return imme_num

def Instruction(instruction):
    flag = 0;#指令状态
    #Decoding
    command=instruction.split()[0]#分解出指令
    #分析指令并且执行
    '''
     立即数指令ADDI  rd,rs1,a   -> rd = rs1 + a
    '''
    if command== 'ADDI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[rs]+imme_num
        #CONST.reg[rd]=CONST.reg[rd] & 0xffffffff#溢出处理
#STLI  rd,rs1,a   -> rd = rs1 < a? 1:0
    elif command== 'STLI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd != 0:
        if CONST.reg[rs]<imme_num:
          CONST.reg[rd] = 1
        else:
          CONST.reg[rd] = 0
#STLIU rd,rs1,a   -> rd = Unsign(rs1) < Unsign(a)? 1:0
    elif command== 'STLIU':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd != 0:
        if (CONST.reg[rs]& 0xffffffff)<(imme_num&0xffffffff):
          CONST.reg[rd] = 1
        else:
          CONST.reg[rd] = 0
#位与ANDI  rd,rs1,a   -> rd = rs1 & a
    elif command== 'ANDI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd !=0:
        CONST.reg[rd]=CONST.reg[rs]&imme_num
#位或ORI   rd,rs1,a   -> rd = rs1 | a
    elif command== 'ORI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[rs] | imme_num
#位异或XORI  rd,rs1,a   -> rd = rs1 ^ a
    elif command== 'XORI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      rs = int(re.sub("\D","",para2))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[rs] ^ imme_num
#SLLI指令 逻辑左移SLLI  rd,rs1,a -> rd = rs1 <<< a
    elif command== 'SLLI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      if para3>0:#立即数禁止负数
        imme_num = data_pro_7(para3)#立即数越界判断处理
        rd = int(re.sub("\D","",para1))
        rs = int(re.sub("\D","",para2))
        if rd != 0:
          try:
            num=CONST.reg[rs] << imme_num
            if (num&0x80000000)==0:#判高位符号
              CONST.reg[rd] = num & 0x7fffffff
            else:
              CONST.reg[rd] = -(num & 0x7fffffff)
          except:
            print('SLLI error!')
      else:
        print( "negative shift count!")
#SRLI指令 逻辑右移SRLI  rd,rs1,a -> rd = rs1 >>> a
    elif command== 'SRLI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      if para3>0:#立即数禁止负数
        imme_num = data_pro_7(para3)#立即数越界判断处理
        rd = int(re.sub("\D","",para1))
        rs = int(re.sub("\D","",para2))
        if rd != 0:
          try:
            if CONST.reg[rs]>0:
              CONST.reg[rd]=(CONST.reg[rs]&0x7fffffff) >> imme_num
            else:
              num=(CONST.reg[rs]&0x7fffffff) >> imme_num
              num=(num | 0x80000000) >> imme_num#负数时高位取1再移动
              if num &0x80000000==0:
                CONST.reg[rd] = num 
              else:
                CONST.reg[rd] = -(num & 0x7fffffff)
          except:
            print('SRLI error!')
      else:
        print( "negative shift count!")
#SRAI指令算术右移SRAI  rd,rs1,a -> rd = rs1 >> a
    elif command== 'SRAI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      rs = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#rs
      para3 = opData.split(',')[2]#Immediate number
      para3 = int(para3)
      if para3>0:#立即数禁止负数
        imme_num = data_pro_7(para3)#立即数越界判断处理
        rd = int(re.sub("\D","",para1))
        rs = int(re.sub("\D","",para2))
        if rd !=0:  
          try:
            CONST.reg[rd]=CONST.reg[rs] >> imme_num
          except:
            print('SRLI error!')
      else:
        print( "negative shift count!")
#LUI指令LUI   rd,a       -> rd = 'Unsign(a)'+ 0x000
    elif command== 'LUI':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      para1 = opData.split(',')[0]#rd
      para3 = opData.split(',')[1]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_20(para3,'Y')#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      CONST.reg[rd]=(imme_num & 0xfffff)<<20+0x000
#AUIPC指令!!讨论AUIPC rd,a       -> rd = pc + ('Unsign(a)<<20+0x000')
    elif command== 'AUIPC':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      para1 = opData.split(',')[0]#rd
      para3 = opData.split(',')[1]#Immediate number
      para3 = int(para3)
      imme_num = data_pro_20(para3,'U')#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      if rd !=0:
        CONST.reg[rd]=imme_num<<20+0x000+CONST.reg[CONST.pcNum]-4#将提前移动的量减去
        CONST.reg[rd]=CONST.reg[rd] & 0xffffffff
#ADD指令ADD   rd,rs1,rs2 -> rd = rs1 + rs2
    elif command== 'ADD':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1]+CONST.reg[r2]
        #CONST.reg[rd]=CONST.reg[rd] & 0xffffffff
#SLT指令，比较SLT   rd,rs1,rs2 -> rd = rs1 < rs2? 1:0
    elif command== 'SLT':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd !=0:
        if CONST.reg[r1]<CONST.reg[r2]:
          CONST.reg[rd]=1
        else:
          CONST.reg[rd]=0
#SLTU指令，无符号比较??SLTU  rd,rs1,rs2 -> rd = Unsign(rs1) < Unsign(rs2)?1:0
    elif command== 'SLTU':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd !=0:
        if (CONST.reg[r1]&0xffffffff)<(CONST.reg[r2]&0xffffffff):
          CONST.reg[rd]=1
        else:
          CONST.reg[rd]=0
#AND,寄存器按位与运算AND   rd,rs1,rs2 -> rd = rs1 & rs2
    elif command== 'AND':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1]&CONST.reg[r2]
#OR,寄存器按位或运算OR    rd,rs1,rs2 -> rd = rs1 | rs2
    elif command== 'OR':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd !=0:
        CONST.reg[rd]=CONST.reg[r1] | CONST.reg[r2]
#XOR,寄存器按位或运算XOR   rd,rs1,rs2 -> rd = rs1 ^ rs2
    elif command== 'XOR':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1] ^ CONST.reg[r2]
#SLL,逻辑左移SLL   rd,rs1,rs2 -> rd = rs1 <<< (rs2 & 0x1f)
    elif command== 'SLL':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1] << (CONST.reg[r2]&0x1f)#移位次数为r2低五位
#SRL,逻辑右移SRL   rd,rs1,rs2 -> rd = rs1 >>> (rs2 & 0x1f)
    elif command== 'SRL':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1] >> (CONST.reg[r2]&0x1f)#移位次数为r2低五位
#SRA,算术右移！！！SRA   rd,rs1,rs2 -> rd = rs1 >> (rs2 & 0x1f)
    elif command== 'SRA':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1] >> (CONST.reg[r2]&0x1f)#移位次数为r2低五位
#SUB,减法SUB   rd,rs1,rs2 -> rd = rs1 - rs2
    elif command== 'SUB':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#r2
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      r2 = int(re.sub("\D","",para3))
      if rd != 0:
        CONST.reg[rd]=CONST.reg[r1] - CONST.reg[r2]
        #CONST.reg[rd]=CONST.reg[rd] & 0xffffffff
#NOP
    elif command== 'NOP':
      CONST.reg[0]=CONST.reg[0]+0
      #CONST.reg[rd]=CONST.reg[rd] & 0xffffffff#溢出处理
#JAL,跳转JAL   rd,a       -> x1 = pc+a, rd = pc+4
    elif command== 'JAL':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      para1 = opData.split(',')[0]#rd
      para3 = opData.split(',')[1]#r2
      para3 = int(para3) 
      imme_num = data_pro_20(para3,'Y')#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      if rd != 0:#保存到r0中的话这一步不执行，等效J
        CONST.reg[rd]=CONST.reg[CONST.pcNum] #将跳转指令的后一条指令赋予rd
      #pc的值也应该改变
      CONST.reg[CONST.pcNum] = CONST.reg[CONST.pcNum] + imme_num - 4 #将后移的量减回来
      print('JAL:',CONST.reg[CONST.pcNum])

#JALR,间接跳转指令   JALR  rd,rs1,a   -> R1 = (rs1+a)&0xfffffffe, rd(x0) = pc+4
    elif command== 'JALR':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_20(para3,'Y')#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      if rd != 0:#保存到r0中的话这一步不执行，等效J
        CONST.reg[rd]=CONST.reg[CONST.pcNum]#将跳转指令的后一条指令赋予rd
      #pcNum的值也应该改变,并且减掉之前的偏移量
      CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)&0xfffffffe

#BEQ,间接跳转指令  BEQ   rs1,rs2,a    -> x1 = rs1==rs2? pc+a:pc
    elif command== 'BEQ':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if CONST.reg[r1] == CONST.reg[r2]:
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)
      print('BEQ:',CONST.reg[r1] , CONST.reg[r2])
#  BNQ   rs1,rs2,a    -> x1 = rs1!=rs2? pc+a:pc
    elif command== 'BNQ':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if CONST.reg[r1] != CONST.reg[r2]:
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)
# BLT   rs1,rs2,a    -> x1 = rs1<rs2? pc+a:pc
    elif command== 'BLT':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if CONST.reg[r1] < CONST.reg[r2]:
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)
# BLTU  rs1,rs2,a    -> x1 = Unsign(rs1)<Unsign(rs2)? pc+a:pc
    elif command== 'BLTU':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if (CONST.reg[r1]&0xffffffff) < (CONST.reg[r2]&0xffffffff):
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)
#BGE,间接跳转指令   BGE   rs1,rs2,a    -> x1 = rs1>=rs2? pc+a:pc
    elif command== 'BGE':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if CONST.reg[r1] >= CONST.reg[r2]:
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num -4)
      print('BGE',CONST.reg[r1] , CONST.reg[r2])
#  BGEU  rs1,rs2,a    -> x1 = Unsign(rs1)>=Unsign(rs2)? pc+a:pc
    elif command== 'BGEU':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3) 
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      if (CONST.reg[r1]&0xffffffff) >= (CONST.reg[r2]&0xffffffff):
        CONST.reg[CONST.pcNum] = (CONST.reg[CONST.pcNum]+ imme_num - 4)
        
#  LOAD rd,rs1,a     -> rd = Mem(#(rs1+a))
    elif command== 'LOAD':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      rd = -1
      r1 = -1
      para1 = opData.split(',')[0]#rd
      para2 = opData.split(',')[1]#r1
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      rd = int(re.sub("\D","",para1))
      r1 = int(re.sub("\D","",para2))
      if rd != 0:
        print(CONST.reg[r1], imme_num)
        CONST.reg[rd]=D_MEM.LoadInt(CONST.reg[r1]+ imme_num)#读取内存
#  STORE rs1,rs2,a    -> Mem(#(rs1+a)) = rs2
    elif command== 'STORE':
      opData=instruction.split()[1] #分解出参数
      #提取指令中相关参数
      r1 = -1
      r2 = -1
      para1 = opData.split(',')[0]#r1
      para2 = opData.split(',')[1]#r2
      para3 = opData.split(',')[2]#立即数
      para3 = int(para3)
      imme_num = data_pro_12(para3)#立即数越界判断处理
      r1 = int(re.sub("\D","",para1))
      r2 = int(re.sub("\D","",para2))
      D_MEM.StoreInt(CONST.reg[r2],CONST.reg[r1]+imme_num)#向内存存数
    return flag

       
