/** Display message on-screen during startup.
 */
#include "main.h"

void (*runLoadingScreens_replaced)() = NULL;
void runLoadingScreens_hook() {
    /** Runs every frame during the loading screens at the start of the game.
     */
    runLoadingScreens_replaced();

    if(initFrameCount < 3) {
        //if we crashed while a stream was playing and hit Start to reset,
        //the stream might still be playing. we don't stop it there because
        //we don't know if the system is stable, so do it here instead.
        streamStopAll();
    }

    if(initFrameCount < 200) {
        enableDebugText = 1;
        debugPrintfxy(200, 420, "Amethyst Edition v" MOD_VERSION_STR);
    }
    else if(initFrameCount < 400) {
        debugPrintfxy(250, 420, "segment6.net");
    }
    else if(initFrameCount < 600) {
        debugPrintfxy(60, 420, "\t\tThis is a free fan creation.\n"
            "If you paid for this, you've been scammed.");
    }

    //let's show some console info too, for fun.
    static const char *tvModes[] = {"NTSC", "PAL", "DEBUG", "DEBUGPAL", "MPAL", "PAL60"};
    debugPrintfxy(30, 30, "CPU: PowerPC Gekko @ %dMHz type %04X %04X\n"
        "RAM: %d / %dK @ %dMHz + %dK ARAM",
        __OSCoreClock / 1000000, consoleType >> 16, consoleType & 0xFFFF,
        simMemSize / 1024, realMemSize / 1024,
        __OSBusClock / 1000000, aramSize / 1024);

    u32 tvMode = READ32(0x800000CC);
    debugPrintfxy(30, 54, "SYS: %s %s",
        OSGetFontEncode() ? "JP" : "US",
        (tvMode < 6) ? tvModes[tvMode] : "UNKNOWN");
}


void (*startMsg_initDoneHook_replaced)() = NULL;
void startMsg_initDoneHook() {
    /** Runs after loading screens.
     *  Turns off debug text if Z isn't held.
     *  We have to do this with a separate hook rather than checking for the
     *  initFrameCount because that's not guaranteed to reach any particular
     *  value if the game loads quickly (especially in Dolphin with fast disc
     *  reading enabled).
     */
    //XXX what does this do besides eat a ton of RAM?
    //the game seems fine without it.
    //startMsg_initDoneHook_replaced();

    //check current and previous frame
    u16 buttons = controllerStates[0].button | controllerStates[4].button;
    if(!(buttons & PAD_TRIGGER_Z)) {
        enableDebugText = 0;
        //DPRINT("Turning debug text off");
    }
    //else DPRINT("Leaving debug text on");

    if((buttons &
    (PAD_BUTTON_Y|PAD_BUTTON_B|PAD_BUTTON_X|PAD_BUTTON_A|PAD_BUTTON_MENU))
    == (PAD_BUTTON_X | PAD_BUTTON_MENU)) {
        krystalModelNo = 1;
    }
}