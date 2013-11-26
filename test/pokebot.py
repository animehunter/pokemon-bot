from pokebot_emu import *

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
