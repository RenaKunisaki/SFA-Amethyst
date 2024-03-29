#include <sfa/sfa.h>

#define MOD_VERSION_MAJOR 2
#define MOD_VERSION_MINOR 4
#define MOD_VERSION_PATCH 0
#define __STR(x) #x
#define _STR(x) __STR(x)
#define MOD_VERSION_STR _STR(MOD_VERSION_MAJOR) "." _STR(MOD_VERSION_MINOR) "." _STR(MOD_VERSION_PATCH)

#define SCREEN_WIDTH  640
#define SCREEN_HEIGHT 480

//text sizing
#define LINE_HEIGHT 16
#define LINE_HEIGHT_JAPANESE 16
#define TAB_WIDTH 64
#define TAB_WIDTH_JAPANESE 64
#define FIXED_CHR_WIDTH 10
#define FIXED_CHR_WIDTH_JAPANESE 14

#define MIN(a,b) \
    ({ __typeof__ (a) _a = (a); \
        __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b; })
#define MAX(a,b) \
    ({ __typeof__ (a) _a = (a); \
        __typeof__ (b) _b = (b); \
    _a > _b ? _a : _b; })
#define ABS(n) \
    ({ __typeof__ (n) _n = (n); \
        _n < 0 ? -_n : _n; })

#include "alloc.h"
#include "args.h"
#include "camera.h"
#include "debug.h"
#include "krystal.h"
#include "menu.h"

typedef enum {
    MINIMAP_SIZE_SMALL = 0,
    MINIMAP_SIZE_NORMAL,
    MINIMAP_SIZE_BIG,
    NUM_MINIMAP_SIZES,
} OverrideMinimapSize;

typedef enum {
    //order same as backpack modes for consistency
    FURFX_NORMAL = 0,
    FURFX_NEVER,
    FURFX_ALWAYS,
    NUM_FURFX_MODES,
} FurFxMode;

typedef enum {
    DBGCHT_INF_HP        = (1 << 0),
    DBGCHT_INF_MP        = (1 << 1),
    DBGCHT_INF_MONEY     = (1 << 2),
    DBGCHT_INF_LIVES     = (1 << 3),
    DBGCHT_ENEMY_FROZEN  = (1 << 4),
    DBGCHT_INF_TRICKY    = (1 << 5),
    DBGCHT_10_RINGS      = (1 << 6),
    DBGCHT_ARW_INF_BOMBS = (1 << 7),
} DebugCheat;

typedef enum {
    HUD_LOW_HP_FLASH = (1 << 0), //flash hearts continuously when low HP
    HUD_LOW_HP_BEEP  = (1 << 1), //for players who hate themselves
} HudFlag;

typedef enum { //for savedata (field unused01)
    EXTRA_FEATURE_RUMBLE_BLUR   = (1 << 0),
    EXTRA_FEATURE_NO_PARTICLEFX = (1 << 1),
    EXTRA_FEATURE_NO_AIM_SNAP   = (1 << 2), //disable staff aim snapback
    EXTRA_FEATURE_SENSITIVE_AIM = (1 << 3), //disable staff aim interpolation
} ExtraFeatureFlag;

//see also CameraFlags in camera.h

//boot.c
void initBootHacks();

//bsod.c
void bsodHook(void);

//bugfixes.c
void initBugFixes();

//dll.c
void dllHooksInit();

//draw.c
void begin2D(Color4b *color);
void write2Dvtx(float x, float y);
void draw2Dbox(float x, float y, float w, float h, const Color4b *color);

//drawarrow.c
void drawArrow(vec3f pos, vec3s rot, float scale, Color4b color);

//drawbox.c
void drawBox(float x, float y, int w, int h, u8 opacity, bool fill);

//drawheap.c
void drawHeaps();

//drawmap.c
void drawMapGrid();

//drawsphere.c
extern const float pi;
extern const float two_pi;
void drawSolidVtx(vec3f pos, Color4b *color);
void drawSphere(vec3f pos, float radius, Color4b color);

//drawtext.c
#define TEXT_FIXED   (1 << 0) //render fixed-width
#define TEXT_COLORED (1 << 1) //enable color
#define TEXT_SHADOW  (1 << 2) //enable drop shadow
#define TEXT_MEASURE (1 << 3) //don't render, only measure
int drawText(const char *str, int x, int y, int *outX, int *outY, u32 flags, Color4b color, float scale);
int drawColorText(const char *str, int x, int y, Color4b color);
int drawSimpleText(const char *str, int x, int y);

//env.c
void envHooksInit();

//freemove.c
extern bool bFreeMove;
extern vec3f freeMoveCoords;
void doFreeMove();

//gameBitLog.c
void gameBitHookInit();
void gameBitHookUpdate();

//hitbox.c
void hitboxHooksInit();

//hook.c
uint32_t hookBranch(uint32_t addr, void *target, int isBl);

//hud.c
extern uint8_t hudFlags;
void doHudHacks();

//loghits.c
void printHits();
void logHitsInit();

//main.c
extern u64 tBootStart;
extern u32 debugCheats;
extern s16 overrideColorScale;
extern u8 overrideFov;
extern u8 furFxMode;
extern u16 dayOfYear, curYear;
extern bool bRumbleBlur;
extern bool bDisableParticleFx;
extern bool bNoAimSnap;
extern bool bSensitiveAim;
extern const char *languageNames[NUM_LANGUAGES];
extern const char *languageNamesShort[NUM_LANGUAGES];
void setGameLanguage(GameLanguageEnum lang);

//map.c
void initMapHacks();

//menu.c
void runMenu();

//menuDebugGameBits.c
extern const char *bitNames;
BitTableEntry* getBitTableEntry(int bit);
const char* getBitName(int bit);

//minimap.c
extern u8 overrideMinimapSize;
extern u8 overrideMinimapAlpha;
void minimapMainLoopHook();

//objects.c
bool isObjectEnabled(ObjInstance *obj);

//pdahook.c
void pdaHookInit();

//perf.c
extern u64 tLoopStart;   //start time of main loop
extern u64 tLoopEnd;     //end   time of main loop
extern u64 tLogicStart;  //start time of game logic section
extern u64 tLogicEnd;    //end   time of game logic section, start of audio
extern u64 tAudioEnd;    //end   time of audio section
extern u64 tRenderStart; //start time of render section
extern u64 tRenderEnd;   //end   time of render section
extern u64 tLoadStart;   //start time of loading section
extern u64 tLoadEnd;     //end   time of loading section
extern u64 tLoop, tLogic, tAudio, tRender, tLoad; //durations
//extern u32 audioIrqCnt;
extern float pctLogic, pctRender, pctAudio, pctLoad, pctTotal;
void renderPerfMeters();
void perfMonInit();

//player.c
extern PlayerStateFunc origClimbWallFn;
void initPlayerStatesHook(void);
PlayerStateEnum playerStateClimbWallHook(double dT, ObjInstance *player, void *state);
void playerMainLoopHook();
void firstPersonHook(void *param1, void *param2);

//race.c
void raceTimerToggle(bool start);
void raceTimerUpdate();

//random.c
extern u32 rngCalls;
extern u32 rngReseeds;
extern s8 rngMode;
u32 rngHook();
void rngSeedHook(u32 seed);
int randIntHook(int min, int max);
void rngHooksInit();
void drawRNG();
void printRNG();

//save.c
extern bool bAutoSave;
void saveLoadHook();
void updateSaveData();
void saveUpdateHook();
void* saveMapLoadHook(MapDirIdx32 map, DataFileEnum file);
void saveShowMsgHook(int param);

//seq.c
void seqHooksInit();

//sort.c
typedef int(*CompareFunc)(const void *itemA, const void *itemB);
//void quicksortStrings(const char **items, int iStart, int iEnd);
void quicksort(const void **items, int iStart, int iEnd, CompareFunc compare);

//stafffx.c
void staffFxInit(void);

//startmsg.c
extern void (*runLoadingScreens_replaced)();
extern void (*startMsg_initDoneHook_replaced)();
void runLoadingScreens_hook();
void startMsg_initDoneHook();

//strings.c
extern const char *strings_English[];
extern const char *strings_Japanese[];
const char* T(const char *s);

//texthook.c
void textHookInit();

//title.c
void Amethyst_loadSaveFile(int slot);
void titleHooksInit();

//ui.c
bool motionBlurHook();
void hudDrawHook(int p1, int p2, int p3);

//util.c
char* bin2str(char *str, u32 val, int len);
int roundTo(int num, int target);
int getObjRealId(int defNo);
ObjectFileStruct* getObjFile(int defNo);
bool getObjName(char *dest, ObjInstance *obj);
bool getObjFileName(char *dest, ObjectFileStruct *file);
int strcmpi(const char *sa, const char *sb);
int compareObjsByType(const void *objA, const void *objB);
int compareObjsById(const void *objA, const void *objB);
int compareObjsByName(const void *objA, const void *objB);
int compareObjsByDistance(const void *objA, const void *objB);
int compareObjsByAddr(const void *objA, const void *objB);
double u64toDouble(u64 val);
double ticksToSecs(u64 ticks);
double fmod(double x, double y);
Color4b hsv2rgb(u8 h, u8 s, u8 v, u8 a);
bool isDllValid(int id);

//worldmap.c
void worldMapHook();
