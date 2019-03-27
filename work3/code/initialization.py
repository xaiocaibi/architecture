import CONST
#初始化各类参数
def initial():
	CONST.dMem = bytearray(256 &0xffffffff)
	CONST.reg = [0 &0xffffffff]*32
	CONST.IMem = ['']*1024
	CONST.instNum = [0]
	CONST.reg[CONST.pcNum] = 0

	
