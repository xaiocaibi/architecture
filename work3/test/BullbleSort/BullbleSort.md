LOAD r19,x0,0
ADDI r19,r19,-2
ADD r17,x0,x0
ADDI r18,r19,0
LOAD r20,r18,1
LOAD r21,r18,2
BLT r21,r20,12
STORE r18,r20,2
STORE r18,r21,1
ADDI r18,r18,-1
BGE r18,r17,-24
ADDI r17,r17,1
BGE r19,r17,-36
ADDI x0,x0,0