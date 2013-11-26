from ctypes import *

# For use with EmuSetKey
PAD_RIGHT  = 0x01
PAD_LEFT   = 0x02
PAD_UP     = 0x04
PAD_DOWN   = 0x08
PAD_A      = 0x10
PAD_B      = 0x20
PAD_SELECT = 0x40
PAD_START  = 0x80

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
                ('enableram', c_int),
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

class VISSPRITE(Structure):
    _fields_ = [('buf', POINTER(c_ubyte)),
                ('x', c_int),
                ('pal', c_ubyte),
                ('pri', c_ubyte),
                ('pad', c_ubyte*6),]
    _pack_ = PACK
    
class SCAN(Structure):
    _fields_ = [('bg', c_int*64),
                ('wnd', c_int*64),
                ('buf', c_ubyte*256),
                ('pal1', c_ubyte*128),
                ('pal2', c_ushort*64),
                ('pal4', c_uint*64),
                ('pri', c_ubyte*256),
                ('vs', VISSPRITE*16),
                
                ('ns', c_int),
                ('l', c_int),
                ('x', c_int),
                ('y', c_int),
                ('s', c_int),
                ('t', c_int),
                ('u', c_int),
                ('v', c_int),
                ('wx', c_int),
                ('wy', c_int),
                ('wt', c_int),
                ('wv', c_int),]
    _pack_ = PACK
    
    
class OBJ(Structure):
    _fields_ = [('x', c_ubyte),
                ('y', c_ubyte),
                ('pat', c_ubyte),
                ('flags', c_ubyte),]
    _pack_ = PACK
    
class OAM(Union):
    _fields_ = [('mem', c_ubyte*256), 
                ('obj', OBJ*40),]
    _pack_ = PACK
    
class LCD(Structure):
    _fields_ = [('vbank', c_ubyte*2*8192), 
                ('oam', OAM),
                ('pal', c_ubyte*128),]
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
    _fields_ = [('cpu',  POINTER(CPU)), 
                ('mbc',  POINTER(MBC)),
                ('rom',  POINTER(ROM)), 
                ('ram',  POINTER(RAM)),
                ('lcd',  POINTER(LCD)),
                ('scan', POINTER(SCAN)),
                ('rtc',  POINTER(RTC)),]
    _pack_ = PACK

HOOKPROC = CFUNCTYPE(None)

# emu_state* EmuGetState()
EmuGetState = cdll.pokebot.EmuGetState
EmuGetState.argtypes = None
EmuGetState.restype = POINTER(EmuState)

# void EmuSetHook(HOOKPROC proc)
EmuSetHook = cdll.pokebot.EmuSetHook
EmuSetHook.argtypes = [HOOKPROC]
EmuSetHook.restype = None

# void EmuSetKey(byte key, int onOff)
EmuSetKey = cdll.pokebot.EmuSetKey
EmuSetKey.argtypes = [c_ubyte, c_int]
EmuSetKey.restype = None

# void EmuMain(char *rom)
EmuMain = cdll.pokebot.EmuMain
EmuMain.argtypes = [c_char_p]
EmuMain.restype = None

state = EmuGetState()

pressed = False

def testhook():
    #print(hex(state.contents.cpu.contents.pc.w[0]) + ' ' + str(state.contents.mbc.contents.rombank))
    global pressed
    if pressed: EmuSetKey(PAD_START|PAD_A, 0)
    else: EmuSetKey(PAD_START|PAD_A, 1)
    pressed = not pressed
    
def main():
    h = HOOKPROC(testhook)
    EmuSetHook(h)
    EmuMain(b'pokered.gb')

if __name__ == '__main__':
    main()
