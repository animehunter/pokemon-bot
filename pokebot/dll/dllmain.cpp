#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <signal.h>

extern "C" 
{
#include "gnuboy.h"
#include "input.h"
#include "rc.h"
#include "loader.h"

#include "cpu.h"
#include "mem.h"
#include "rtc.h"
}


#define VERSION "1.0.6-svn" /*
VERSION = 1.0.6-svn
# */

#define CDECL_CALL __cdecl
#define DLL_EXPORT __declspec(dllexport)

typedef void(*HOOKPROC)(void);
static HOOKPROC hooks[65535] = {0};

static struct emu_state
{
    struct cpu *cpu;
    struct mbc *mbc;
    struct rom *rom;
    struct ram *ram;
    struct rtc *rtc;
} state = { &cpu, &mbc, &rom, &ram, &rtc};

static char *defaultconfig[] =
{
    "bind esc quit",
    "bind up +up",
    "bind down +down",
    "bind left +left",
    "bind right +right",
    "bind d +a",
    "bind s +b",
    "bind enter +start",
    "bind space +select",
    "bind tab +select",
    "bind joyup +up",
    "bind joydown +down",
    "bind joyleft +left",
    "bind joyright +right",
    "bind joy0 +b",
    "bind joy1 +a",
    "bind joy2 +select",
    "bind joy3 +start",
    "bind 1 \"set saveslot 1\"",
    "bind 2 \"set saveslot 2\"",
    "bind 3 \"set saveslot 3\"",
    "bind 4 \"set saveslot 4\"",
    "bind 5 \"set saveslot 5\"",
    "bind 6 \"set saveslot 6\"",
    "bind 7 \"set saveslot 7\"",
    "bind 8 \"set saveslot 8\"",
    "bind 9 \"set saveslot 9\"",
    "bind 0 \"set saveslot 0\"",
    "bind ins savestate",
    "bind del loadstate",
    "source gnuboy.rc",
    NULL
};


void doevents()
{
    event_t ev;
    int st;

    ev_poll();
    while (ev_getevent(&ev))
    {
        if (ev.type != EV_PRESS && ev.type != EV_RELEASE)
            continue;
        st = (ev.type != EV_RELEASE);
        rc_dokey(ev.code, st);
    }

    HOOKPROC h = hooks[cpu.pc.w[0]];
    if (h)
    {
        h();
    }
}


static void shutdown()
{
    vid_close();
    pcm_close();
}

void die(char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    exit(1);
}

static int bad_signals[] =
{
    /* These are all standard, so no need to #ifdef them... */
    SIGINT, SIGSEGV, SIGTERM, SIGFPE, SIGABRT, SIGILL,
#ifdef SIGQUIT
    SIGQUIT,
#endif
#ifdef SIGPIPE
    SIGPIPE,
#endif
    0
};

static void fatalsignal(int s)
{
    die("Signal %d\n", s);
}

static void catch_signals()
{
    int i;
    for (i = 0; bad_signals[i]; i++)
        signal(bad_signals[i], fatalsignal);
}

static char *base(char *s)
{
    char *p;
    p = strrchr(s, DIRSEP_CHAR);
    if (p) return p + 1;
    return s;
}

extern "C" DLL_EXPORT emu_state* CDECL_CALL EmuGetState()
{
    return &state;
}

extern "C" DLL_EXPORT void CDECL_CALL EmuSetHook(unsigned short addr, HOOKPROC proc)
{
    hooks[addr] = proc;
}

extern "C" DLL_EXPORT void CDECL_CALL EmuMain(char *rom)
{
    int i;
    char *s;

    /* If we have special perms, drop them ASAP! */
    vid_preinit();

    init_exports();

    s = strdup(".");
    sys_sanitize(s);
    sys_initpath(s);

    for (i = 0; defaultconfig[i]; i++)
        rc_command(defaultconfig[i]);

    /* FIXME - make interface modules responsible for atexit() */
    atexit(shutdown);
    catch_signals();
    vid_init();
    pcm_init();

    rom = strdup(rom);
    sys_sanitize(rom);

    loader_init(rom);

    emu_reset();
    emu_run();
}

