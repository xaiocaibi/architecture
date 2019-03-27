#全局参数
'''
32位CPU所含有的寄存器有：

4个数据寄存器(EAX、EBX、ECX和EDX)
2个变址和指针寄存器(ESI和EDI) 2个指针寄存器(ESP和EBP)
6个段寄存器(ES、CS、SS、DS、FS和GS)
1个指令指针寄存器(EIP) 1个标志寄存器(EFlags)
其余为通用寄存器
因为部分专用寄存器不需要使用
定义ro寄存器只读，且值为0
pc寄存器号为1，IR寄存器（指令寄存器）为2.
定义flag寄存器为3
通用寄存器号从16号到31号，可以任意使用 ，其余暂时保留
'''
ALIGNMENT= 4
r0 = 0
r1 = 1
pcNum = 2
IR = 3
MEM_CELL = 0xff
REGISTER = 0xffffffff
UINT_LEN = 0x7fffffff

# 定义硬件资源mem和reg
# 用于数据存储的mem
global dMem
#用于表示寄存器
global reg
# 用于指令存储的mem
global IMem
# 指令数量，用于标记内存中指令的有效长度
global instNum

def set_value(value):
    # 告诉编译器我在这个方法中使用的a是刚才定义的全局变量a,而不是方法内部的局部变量.
    global a
    a = value

def get_value():
    # 同样告诉编译器我在这个方法中使用的a是刚才定义的全局变量a,并返回全局变量a,而不是方法内部的局部变量.
    global a
    return a
