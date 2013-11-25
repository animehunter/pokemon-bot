from ctypes import *

PACK = 8

class REG(Union):
    _fields_ = [('d', c_uint), 
                ('w', c_ushort*2),
                ('b', c_ubyte*4),]
    _pack_ = PACK

class CPU(Structure):
    _fields_ = [('pc', REG), 
                ('sp', REG),
                ('bc', REG), 
                ('de', REG), 
                ('hl', REG),
                ('af', REG),
                ('ime', c_int),
                ('ima', c_int),
                ('speed', c_int),
                ('halt', c_int),
                ('div', c_int),
                ('tim', c_int),
                ('lcdc', c_int),
                ('snd', c_int),]
    _pack_ = PACK
    
class MBC(Structure):
    _fields_ = [('type', c_int), 
                ('model', c_int),
                ('rombank', c_int),
                ('rambank', c_int),
                ('romsize', c_int),
                ('ramsize', c_int),
                ('emableram', c_int),
                ('batt', c_int),
                ('rmap', POINTER(c_ubyte)*0x10),
                ('wmap', POINTER(c_ubyte)*0x10),]
    _pack_ = PACK
    
class ROM(Structure):
    _fields_ = [('bank', POINTER(c_ubyte*16384)), 
                ('name', c_char*20),]
    _pack_ = PACK
    
class RAM(Structure):
    _fields_ = [('hi', c_ubyte*256),
                ('ibank', c_ubyte*8*4096),
                ('sbank', POINTER(c_ubyte*8192)),
                ('loaded', c_int),]
    _pack_ = PACK

class RTC(Structure):
    _fields_ = [('batt', c_int),
                ('sel', c_int),
                ('latch', c_int),
                ('d', c_int),
                ('h', c_int),
                ('m', c_int),
                ('s', c_int),
                ('t', c_int),
                ('stop', c_int),
                ('carry', c_int),
                ('regs', c_ubyte*8),]
    _pack_ = PACK
    
class EmuState(Structure):
    _fields_ = [('cpu', POINTER(CPU)), 
                ('mbc', POINTER(MBC)),
                ('rom', POINTER(ROM)), 
                ('ram', POINTER(RAM)), 
                ('rtc', POINTER(RTC)),]
    _pack_ = PACK

EmuGetState = cdll.pokebot.EmuGetState
EmuGetState.argtypes = None
EmuGetState.restype = POINTER(EmuState)

EmuMain = cdll.pokebot.EmuMain
EmuMain.argtypes = [c_char_p]
EmuMain.restype = None

def main():
    state = EmuGetState()
    EmuMain(b'pokered.gb')

if __name__ == '__main__':
    main()
