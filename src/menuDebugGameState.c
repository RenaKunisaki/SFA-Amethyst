#include "main.h"

void debugGameSubMenu_close(const Menu *self) {
    //Close function for submenus of the debug game state menu
    curMenu = &menuDebugGameState;
    audioPlaySound(NULL, MENU_CLOSE_SOUND);
}

void menuDebugGameStateBits_select(const MenuItem *self, int amount) {
    if(amount) return;
    curMenu = &menuDebugGameBits;
    audioPlaySound(NULL, MENU_OPEN_SOUND);
}

void menuDebugGameStatePlayer_select(const MenuItem *self, int amount) {
    if(amount) return;
    if(pPlayer) {
        editPlayerIdx = (pPlayer->defNo == ObjDefEnum_Sabre) ?
            PLAYER_ID_FOX : PLAYER_ID_KRYSTAL;
    }
    curMenu = &menuDebugEditPlayer;
    audioPlaySound(NULL, MENU_OPEN_SOUND);
}

void menuDebugGameStateTricky_select(const MenuItem *self, int amount) {
    if(amount) return;
    curMenu = &menuDebugEditTricky;
    audioPlaySound(NULL, MENU_OPEN_SOUND);
}

Menu menuDebugGameState = {
    "Game State", 0,
    genericMenu_run, genericMenu_draw, debugSubMenu_close,
    "GameBits",          "%s", genericMenuItem_draw, menuDebugGameStateBits_select,
    "Edit Player State", "%s", genericMenuItem_draw, menuDebugGameStatePlayer_select,
    "Edit Tricky State", "%s", genericMenuItem_draw, menuDebugGameStateTricky_select,
    NULL,
};
