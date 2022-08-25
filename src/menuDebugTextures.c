/** Debug Texture Viewer submenu.
 */
#include "main.h"
#define TEXTURE_MENU_XPOS      15
#define TEXTURE_MENU_YPOS      40
#define TEXTURE_MENU_WIDTH    620
#define TEXTURE_MENU_HEIGHT   110
#define TEXTURE_IMAGE_XPOS     15
#define TEXTURE_IMAGE_YPOS    145
#define TEXTURE_IMAGE_PADDING   7

static s8 textureMenuFrame = 0;
static bool textureMenuAnimate = false;
static u8 textureMenuAnimTimer = 0;

static const char *wrapModeNames[] = {
    "CLAMP ", "REPEAT", "MIRROR"
};
static const char *filterModeNames[] = {
    "NEAREST      ", "LINEAR      ",
    "NEAR_MIP_NEAR", "LIN_MIP_NEAR",
    "NEAR_MIP_LIN ", "LIN_MIP_LIN "
};
static const char *formatNames[] = {
    "I4", "I8", "IA4", "IA8", "RGB565", "RGB5A3", "RGBA8",
    "", "C4", "C8", "C14X2", "", "", "", "CMPR"
};

void textureMenu_draw(Menu *self) {
    //Draw function for Texture Viewer menu
    menuAnimFrame++;
    char str[256];

    drawMenuBox(TEXTURE_MENU_XPOS, TEXTURE_MENU_YPOS,
        TEXTURE_MENU_WIDTH, TEXTURE_MENU_HEIGHT);
    gameTextSetColor(0xFF,0xFF,0xFF,0xFF);

    int x = TEXTURE_MENU_XPOS + MENU_PADDING;
    int y = TEXTURE_MENU_YPOS + MENU_PADDING;

    if(self->selected >= numLoadedTextures) {
        self->selected = numLoadedTextures - 1;
    }
    LoadedTexture *ltex = &loadedTextures[self->selected];
    Texture *tex = ltex ? ltex->texture : NULL;

    int id = ltex->id;
    char sign = (id < 0) ? '-' : ' ';
    if(id < 0) id = -id;

    /* #00AD Frame 00 ID -0725 @80FF0C60 RC:  1
       Fmt: RGB565        Size 512x256
       Min: NEAR_MIP_NEAR Mag: NEAR_MIP_NEAR
       WS:  REPEAT        WT:  REPEAT
       10:  0100   1E:00  50:0 */

    sprintf(str, "\eF#%04X Frame %02X ID %c%04X @%08X RC:%3d\eF",
        self->selected, textureMenuFrame, sign,
        id & 0x7FFF, tex, tex->usage);
    menuDrawText(str, x, y, false);
    y += LINE_HEIGHT+2;

    if(tex) {
        sprintf(str, "\eFFmt: %-13s Size %3dx%3d\eF",
            tex->format < 0xF ? formatNames[tex->format] : "",
            tex->width, tex->height);
        menuDrawText(str, x, y, false);
        y += LINE_HEIGHT+2;

        sprintf(str, "\eFMin: %-13s Mag: %-13s\eF",
            tex->minFilter < 6 ? filterModeNames[tex->minFilter] : "",
            tex->magFilter < 6 ? filterModeNames[tex->magFilter] : "");
        menuDrawText(str, x, y, false);
        y += LINE_HEIGHT+2;

        //space out WS, WT so the W doesn't overlap
        sprintf(str, "\eFW S: %-13s W T: %-13s\eF",
            tex->wrapS < 3 ? wrapModeNames[tex->wrapS] : "",
            tex->wrapT < 3 ? wrapModeNames[tex->wrapT] : "");
        menuDrawText(str, x, y, false);
        y += LINE_HEIGHT+2;

        sprintf(str, "\eF10:  %04X   1E:%02X  50:%X\eF",
            tex->frameVal10, tex->unk1E, tex->tevVal50);
        menuDrawText(str, x, y, false);
        y += LINE_HEIGHT+2;

        //get frame
        if(textureMenuAnimate) {
            if(textureMenuAnimTimer < 10) textureMenuAnimTimer++;
            else {
                textureMenuAnimTimer = 0;
                textureMenuFrame++;
            }
        }

        int frm = textureMenuFrame;
        Texture *pFrm = tex;
        while(pFrm && frm) {
            pFrm = pFrm->next;
            frm--;
        }
        if(!pFrm) { //passed last frame
            pFrm = tex;
            textureMenuFrame = 0;
        }
        tex = pFrm;

        if(tex) {
            drawMenuBox(TEXTURE_IMAGE_XPOS, TEXTURE_IMAGE_YPOS,
                tex->width  + (TEXTURE_IMAGE_PADDING*2),
                tex->height + (TEXTURE_IMAGE_PADDING*2));
            drawTexture(TEXTURE_IMAGE_XPOS + TEXTURE_IMAGE_PADDING,
                TEXTURE_IMAGE_YPOS + TEXTURE_IMAGE_PADDING, tex, 255, 0x100);
        }
    }
}

void textureMenu_run(Menu *self) {
    //Run function for Texture Viewer menu
    int sel = self->selected;
    LoadedTexture *ltex = &loadedTextures[sel];

    if(buttonsJustPressed == PAD_BUTTON_B) { //close menu
        menuInputDelayTimer = MENU_INPUT_DELAY_CLOSE;
        self->close(self);
    }
    else if(buttonsJustPressed == PAD_BUTTON_X) { //next frame
        menuInputDelayTimer = MENU_INPUT_DELAY_ADJUST;
        textureMenuFrame++;
    }
    else if(buttonsJustPressed == PAD_BUTTON_Y) { //prev frame
        menuInputDelayTimer = MENU_INPUT_DELAY_ADJUST;
        textureMenuFrame--;
    }
    else if(buttonsJustPressed == PAD_TRIGGER_Z) { //toggle animation
        menuInputDelayTimer = MENU_INPUT_DELAY_ADJUST;
        textureMenuAnimate = !textureMenuAnimate;
        textureMenuAnimTimer = 0;
    }
    else if(controllerStates[0].stickX < -MENU_ANALOG_STICK_THRESHOLD
    ||      controllerStates[0].substickX < -MENU_CSTICK_THRESHOLD) { //left
        menuInputDelayTimer =
            (controllerStates[0].stickX < -MENU_ANALOG_STICK_THRESHOLD)
            ? MENU_INPUT_DELAY_MOVE : MENU_INPUT_DELAY_MOVE_FAST;
        if(sel == 0) sel = numLoadedTextures;
        self->selected = sel - 1;
    }
    else if(controllerStates[0].stickX > MENU_ANALOG_STICK_THRESHOLD
    ||      controllerStates[0].substickX > MENU_CSTICK_THRESHOLD) { //right
        menuInputDelayTimer = (controllerStates[0].stickX > MENU_ANALOG_STICK_THRESHOLD)
            ? MENU_INPUT_DELAY_MOVE : MENU_INPUT_DELAY_MOVE_FAST;
        sel++;
        if(sel >= numLoadedTextures) sel = 0;
        self->selected = sel;
    }
    else if(controllerStates[0].triggerLeft > MENU_TRIGGER_THRESHOLD) { //L
        sel -= 0x10;
        if(sel <= 0) sel = numLoadedTextures;
        self->selected = sel - 1;
        menuInputDelayTimer = MENU_INPUT_DELAY_MOVE;
    }
    else if(controllerStates[0].triggerRight > MENU_TRIGGER_THRESHOLD) { //R
        sel += 0x10;
        if(sel >= numLoadedTextures) sel = 0;
        self->selected = sel;
        menuInputDelayTimer = MENU_INPUT_DELAY_MOVE;
    }

    if(self->selected >= numLoadedTextures) self->selected = numLoadedTextures - 1;
}

Menu menuDebugTextureView = {
    "View Textures", 0,
    textureMenu_run, textureMenu_draw, debugRenderSubMenu_close,
    NULL,
};
