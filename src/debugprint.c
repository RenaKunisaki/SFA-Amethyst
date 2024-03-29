/** Display some debug information on-screen.
 */
#include "main.h"
#include "revolution/os.h"
#include <math.h>

u32 debugTextFlags =
    //DEBUGTEXT_TRICKY |
    DEBUGTEXT_PLAYER_COORDS |
    DEBUGTEXT_CAMERA_COORDS |
    //DEBUGTEXT_RESTART_POINT |
    DEBUGTEXT_MEMORY_INFO |
    DEBUGTEXT_INTERACT_OBJ_INFO |
    //DEBUGTEXT_HEAP_STATE |
    DEBUGTEXT_GAMEBIT_LOG |
    //DEBUGTEXT_PLAYER_STATE |
    //DEBUGTEXT_PERFORMANCE |
    DEBUGTEXT_FPS |
    //DEBUGTEXT_RNG |
    //DEBUGTEXT_AUDIO_STREAMS |
    //DEBUGTEXT_AUDIO_SFX |
    //DEBUGTEXT_ENVIRONMENT |
    DEBUGTEXT_OBJSEQ |
    0;
u32 debugRenderFlags =
    //DEBUGRENDER_WORLD_MAP |
    //DEBUGRENDER_DEBUG_OBJS |
    //DEBUGRENDER_PERF_METERS |
    //DEBUGRENDER_RNG |
    //DEBUGRENDER_HITBOXES |
    //DEBUGRENDER_ATTACH_POINTS |
    //DEBUGRENDER_FOCUS_POINTS |
    //DEBUGRENDER_UNK_POINTS |
    0;


void debugPrintSetPos(s16 x, s16 y) {
    if(!enableDebugText) return; //or else game hangs
    *(debugLogEnd++) = DPRINT_POS[0];
    *(debugLogEnd++) = x & 0xFF;
    *(debugLogEnd++) = x >> 8;
    *(debugLogEnd++) = y & 0xFF;
    *(debugLogEnd++) = y >> 8;
    *debugLogEnd = 0;
}
void debugPrintSetColor(u8 r, u8 g, u8 b, u8 a) {
    if(!enableDebugText) return; //or else game hangs
    *(debugLogEnd++) = DPRINT_COLOR[0];
    *(debugLogEnd++) = r;
    *(debugLogEnd++) = g;
    *(debugLogEnd++) = b;
    *(debugLogEnd++) = a;
    *debugLogEnd = 0;
}
void debugPrintSetBgColor(u8 r, u8 g, u8 b, u8 a) {
    if(!enableDebugText) return; //or else game hangs
    *(debugLogEnd++) = DPRINT_BGCOLOR[0];
    *(debugLogEnd++) = r;
    *(debugLogEnd++) = g;
    *(debugLogEnd++) = b;
    *(debugLogEnd++) = a;
    *debugLogEnd = 0;
}

static void printObjName(const char *fmt, ObjInstance *obj) {
    //print object's name, with sanity checking
    //in case the object is unloaded or such
    char name[12];
    name[0] = 0;

    if(PTR_VALID(obj) && PTR_VALID(obj->file) && PTR_VALID(obj->file->name)) {
        for(int i=0; i<11; i++) {
            name[i] = 0;
            name[i+1] = 0;
            char c = obj->file->name[i];
            if(!c) break;
            if(c >= 0x20 && c <= 0x7E) name[i] = c;
            else name[i] = '?';
        }
    }
    debugPrintf(fmt, name);
}

static void printBaddieInfo(ObjInstance *target) {
    char name[16];
    void *state = (void*)target->state;
    debugPrintf("  baddie state@" DPRINT_FIXED "%08X" DPRINT_NOFIXED
        "; HP: " DPRINT_FIXED "%3d" DPRINT_NOFIXED "; ", state,
        *(s16*)(state+0x2B0));

    ObjInstance *theirTarget = *(ObjInstance**)(state+0x29C);
    getObjName(name, theirTarget);
    debugPrintf("Target: " DPRINT_FIXED "%08X" DPRINT_NOFIXED " %s\n"
    "  state " DPRINT_FIXED "%02X %02X %02X %02X" DPRINT_NOFIXED,
        theirTarget, name,
        *(u8*)(state+0x33A), *(u8*)(state+0x33B),
        *(u8*)(state+0x33C), *(u8*)(state+0x33D));
    debugPrintf(" anim %04X\n  timer %f hit %f\n",
        *(u16*)(state+0x338),
        *(float*)(state+0x324),
        *(float*)(state+0x2D8));
    debugPrintf("  flags " DPRINT_FIXED "%08X %08X %08X" DPRINT_NOFIXED "\n",
        *(u32*)(state+0x2DC),
        *(u32*)(state+0x2E4),
        *(u32*)(state+0x2F0));
}

static void printCoords() {
    //Display player coords
    //debugPrintf doesn't support eg '%+7.2f'
    char buf[256];
    if(pPlayer) {
        sprintf(buf, "%+7.2f %+7.2f %+7.2f",
            pPlayer->pos.pos.x, pPlayer->pos.pos.y, pPlayer->pos.pos.z);
        debugPrintf("P:" DPRINT_FIXED "%s" DPRINT_NOFIXED, buf);
    }

    //Display map coords
    int mapNo = curMapId;
    if(mapNo >= NUM_MAP_DIRS) mapNo = mapActLut[mapNo];
    debugPrintf(" M:" DPRINT_FIXED "%3d,%3d,%d #%02X T%X %08X" DPRINT_NOFIXED,
        (int)(mapCoords.mapX / MAP_CELL_SCALE), (int)(mapCoords.mapZ / MAP_CELL_SCALE),
        curMapLayer, curMapId,
        mainGetBit(mapActBitIdx[mapNo]),
        mainGetBit(mapObjGroupBit[mapNo]));

    //Display locked map IDs
    debugPrintf(" L:"DPRINT_FIXED "%02X%02X %02X%02X\n" DPRINT_NOFIXED,
        loadedFileMapIds[FILE_BLOCKS_BIN] & 0xFF,
        loadedFileMapIds[FILE_BLOCKS_BIN2] & 0xFF,
        //buckets are int, but we really only need lowest byte.
        levelLockBuckets[0] & 0xFF, levelLockBuckets[1] & 0xFF);

    //display velocity and angle
    ObjInstance *player = getArwing();
    if(!player) player = pPlayer;
    if(player) {
        //not entirely sure what the velocity is relative to.
        //seems to be something involving both world and camera space.
        //in any case it's not that important since we only care about XZ distance.
        vec3f vel = player->vel;
        /* float fwdX, fwdZ, sideX, sideZ;
        angleToVec2(pCamera->pos.rotation.x,          &fwdX,  &fwdZ);
        angleToVec2(pCamera->pos.rotation.x + 0x4000, &sideX, &sideZ);

        float mx = (vel.x * sideX) + (vel.z * fwdX);
        float mz = (vel.z * fwdZ ) + (vel.x * sideZ);
        vel.x = mx; vel.z = mz; */
        vec3f zero = {0, 0, 0};
        vel.z = vec3f_xzDistance(&vel, &zero);

        s16 rxAdj = 0x8000 - player->pos.rotation.x; //for consistency with viewfinder
        float rx = ((float)rxAdj)                   * (360.0 / 65536.0);
        float ry = ((float)player->pos.rotation.y) * (360.0 / 65536.0);
        float rz = ((float)player->pos.rotation.z) * (360.0 / 65536.0);
        if(rx < 0.0) rx += 360.0;
        if(ry < 0.0) ry += 360.0;
        if(rz < 0.0) rz += 360.0;

        sprintf(buf, "V:" DPRINT_FIXED "%+7.3f %+7.3f R:%5.1f %5.1f %5.1f\n" DPRINT_NOFIXED,
            vel.z, vel.y, rx, ry, rz);
        debugPrintf("%s", buf);
    }
}

static int restartPointFrameCount[3] = {0, 0, 0};
static vec3f prevRestartPoint    [3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
static s8 prevRestartPointLayer  [3] = {0, 0, 0};
static u8 prevRestartPointMap    [3] = {0, 0, 0};

static void printRestartPointForSave(SaveGame *save, int which, const char *name) {
    if(save) {
        //PlayerCharState *chrState = save->charState[save->character];
        PlayerCharPos   *chrPos   = &save->charPos  [save->character];

        //if restart point has changed, highlight it
        if(chrPos->pos.x    != prevRestartPoint[which].x
        || chrPos->pos.y    != prevRestartPoint[which].y
        || chrPos->pos.z    != prevRestartPoint[which].z
        || chrPos->mapLayer != prevRestartPointLayer[which]
        || chrPos->mapId    != prevRestartPointMap[which]) {
            restartPointFrameCount[which] = 60;
            prevRestartPoint[which].x    = chrPos->pos.x;
            prevRestartPoint[which].y    = chrPos->pos.y;
            prevRestartPoint[which].z    = chrPos->pos.z;
            prevRestartPointLayer[which] = chrPos->mapLayer;
            prevRestartPointMap[which]   = chrPos->mapId;
        }
        else if(restartPointFrameCount[which] > 0) restartPointFrameCount[which]--;

        //u8 color = pRestartPoint ? 0xFF : 0x7F;
        u8 color = 255 - (restartPointFrameCount[which] * 4);
        char sColor[6] = {0x81, 0xFF, color, 0xFF, 0xFF, 0};

        //map ID is 0xFF sometimes, no idea why
        debugPrintf("%s" DPRINT_FIXED "%s:%6d %6d %6d %d ",
            sColor, name,
            (int)chrPos->pos.x, (int)chrPos->pos.y, (int)chrPos->pos.z,
            chrPos->mapLayer);
        //after a certain number of params, it starts printing nonsense.
        debugPrintf("M%02X" DPRINT_NOFIXED DPRINT_COLOR "\xFF\xFF\xFF\xFF\n",
            chrPos->mapId & 0xFF);

        if(restartPointFrameCount[which] >= 60) {
            //log changes to console too
            OSReport("%s: %6d %6d %6d %d %02X", name,
                (int)chrPos->pos.x, (int)chrPos->pos.y, (int)chrPos->pos.z,
                chrPos->mapLayer, chrPos->mapId & 0xFF);
        }
    }
    else debugPrintf(DPRINT_FIXED "%s: none" DPRINT_NOFIXED "\n", name);
}

static void printRestartPoint() {
    printRestartPointForSave(pRestartPoint,  0, "RST"); //used when voiding out
    printRestartPointForSave(pLastSavedGame, 1, "LSV"); //is this used?
    printRestartPointForSave(pCurSaveGame,   2, "CSV"); //where you respawn when loading the save
}

static void printCamera() {
    //Display camera coords
    char buf[256];
    if(pCamera) {
        sprintf(buf, "%+7.2f %+7.2f %+7.2f",
            pCamera->pos.xf.pos.x, pCamera->pos.xf.pos.y, pCamera->pos.xf.pos.z);
        debugPrintf("C:" DPRINT_FIXED "%s M%02X", buf, cameraMode);
        int seq = READ32(0x803dd064);
        if(seq) {
            debugPrintf(DPRINT_NOFIXED " S:" DPRINT_FIXED "%02X", seq);
        }
        debugPrintf(DPRINT_NOFIXED "\n");
    }
}

static void printObjCount() {
    //Display number of objects
    debugPrintf("Obj:" DPRINT_FIXED "%3d" DPRINT_NOFIXED " ", numLoadedObjs);
}

static void printMemory() {
    //Display memory used percentages
    u32 totalBlocks=0, totalBytes=0, usedBlocks=0, usedBytes=0;
    for(int i=0; i<NUM_HEAPS; i++) {
        totalBytes  += heaps[i].dataSize;
        totalBlocks += heaps[i].avail;
        usedBytes   += heaps[i].size;
        usedBlocks  += heaps[i].used;
    }
    int bytesPct  = (usedBytes  * 100) / totalBytes;
    int blocksPct = (usedBlocks * 100) / totalBlocks;
    u32 color = 0xFFFFFFFF; //rgba
    if     (bytesPct >= 90 || blocksPct >= 90) color = 0xFF0000FF;
    else if(bytesPct >= 85 || blocksPct >= 85) color = 0xFF0000FF;
    char sColor[6] = {0x81, (color >> 24), (color >> 16), (color >> 8), color, 0};
    debugPrintf("%sMem " DPRINT_FIXED "%3d %3d" DPRINT_COLOR "\xFF\xFF\xFF\xFF"
        DPRINT_NOFIXED "\n", sColor, bytesPct, blocksPct);
}

static void printHeapInfo() {
    //Display detailed heap info
    debugPrintf(DPRINT_FIXED "Free Blocks   Free KBytes\n" DPRINT_NOFIXED);
    for(int i=0; i<NUM_HEAPS; i++) {
        debugPrintf(DPRINT_FIXED "%5d/%5d %6d/%6d\n" DPRINT_NOFIXED,
            heaps[i].avail - heaps[i].used, heaps[i].avail, //blocks
            (heaps[i].dataSize - heaps[i].size) / 1024, heaps[i].dataSize / 1024 //bytes
        );
    }

    debugPrintf("Emerg frees: %d; alloc fails: %d\n", emergFreeCount, allocFailCount);
    if(allocFailCount > 0) {
        debugPrintf(DPRINT_FIXED "FailSize FailTag  FailAddr" DPRINT_NOFIXED "\n");
        for(int i=0; i<MIN(allocFailCount, ALLOC_FAIL_LOG_SIZE); i++) {
            if(i == allocFailLogIdx) debugPrintf(DPRINT_COLOR "\x00\xFF\x00\xFF");
            else debugPrintf(DPRINT_COLOR "\xFF\xFF\xFF\xFF");
            debugPrintf(DPRINT_FIXED "%08X %08X %08X" DPRINT_NOFIXED "\n",
                allocFailLog[i].size, allocFailLog[i].tag, allocFailLog[i].lr);
        }
        debugPrintf(DPRINT_COLOR "\xFF\xFF\xFF\xFF");
    }

    u32 totalBlocks=0, totalBytes=0;
    for(int i=0; i<NUM_HEAPS; i++) {
        totalBytes  += heaps[i].dataSize;
        totalBlocks += heaps[i].avail;
    }
    debugPrintf("Max blocks=%d/%d KBytes=%d/%d\n", maxBlocksUsed, totalBlocks,
        maxMemUsed / 1024, totalBytes / 1024);
}

static void printTarget() {
    //Display target that player is focused on
    if(pCamera && pCamera->target) {
        debugPrintf("Target: " DPRINT_FIXED "%08X %08X %04X %04X " DPRINT_NOFIXED,
            pCamera->target,
            pCamera->target->objDef->id,
            pCamera->target->defNo,
            pCamera->target->animId);
        char name[16];
        getObjName(name, pCamera->target);
        debugPrintf("%s; d=%f (%f, %f)\n", name,
            vec3f_distance(&pCamera->target->pos.pos, &pCamera->focus->pos.pos),
            vec3f_xzDistance(&pCamera->target->pos.pos, &pCamera->focus->pos.pos),
            ABS(pCamera->target->pos.pos.y - pCamera->focus->pos.pos.y));

        switch(pCamera->target->catId) {
            case ObjCatId_baddie: printBaddieInfo(pCamera->target); break;
            default: break;
        }
    }
}

static void printHeldObj() {
    //Display object that player is carrying
    if(pCamera && pCamera->target) {
        debugPrintf("Held: " DPRINT_FIXED "%08X %08X %04X " DPRINT_NOFIXED,
            pCamera->target,
            pCamera->target->objDef->id,
            pCamera->target->defNo);
        char name[16];
        getObjName(name, pCamera->target);
        debugPrintf("%s; d=%f (%f, %f)\n", name,
            vec3f_distance(&pCamera->target->pos.pos, &pCamera->focus->pos.pos),
            vec3f_xzDistance(&pCamera->target->pos.pos, &pCamera->focus->pos.pos),
            ABS(pCamera->target->pos.pos.y - pCamera->focus->pos.pos.y));

        switch(pCamera->target->catId) {
            case ObjCatId_baddie: printBaddieInfo(pCamera->target); break;
            default: break;
        }
    }
}

static void printPlayerObj(const char *name, ObjInstance *obj) {
    if(!(PTR_VALID(obj) && PTR_VALID(obj->file))) return;
    debugPrintf("%s " DPRINT_FIXED "%08X ", name, obj);
    printObjName("%s", obj);

    char buf[256];
    sprintf(buf, "%08X %+7.2f %+7.2f %+7.2f", obj->objDef->id,
        obj->pos.pos.x, obj->pos.pos.y, obj->pos.pos.z);
    debugPrintf(" %s" DPRINT_NOFIXED, buf);

    sprintf(buf, "; DLL:" DPRINT_FIXED "%08X\n", obj->dll);
    debugPrintf("%s", buf);
}

static void printArwingState(ObjInstance *arwing) {
    void *state = arwing->state;
    if(!PTR_VALID(state)) return;

    char buf[256];
    sprintf(buf, "Arwing[" DPRINT_FIXED "%08X" DPRINT_NOFIXED
        "] HP=%d/%d BombCool:%1.0f GunCool:%1.0f BoostCool:%1.0f\n", state,
        *(u8*)(state+0x468),
        *(u8*)(state+0x469),
        *(float*)(state+0x440),
        *(float*)(state+0x408),
        *(float*)(state+0xB4));
    debugPrintf("%s", buf);
}

static void printPlayerState() {
    ObjInstance *player = getArwing();
    if(player) {
        printArwingState(player);
        return;
    }
    player = pPlayer;
    debugPrintf("Player=%08X: ", player);
    printObjName("%s\n", player);
    if(!(player && player->file)) return;
    if(player->catId != ObjCatId_Player) return; //don't apply to title screen Fox, Arwing

    void *pState = player ? player->state : NULL;
    if(!pState) return;
    PlayerCharState *cState = *(PlayerCharState**)(pState + 0x35C);

    float onFire = *(float*)(pState + 0x79C);
    if(onFire) debugPrintf("On fire %f\n", onFire);
    //float castTimer = *(float*)(pState + 0x85C); //always 0?
    //if(castTimer) debugPrintf("Cast spell %f\n", castTimer);

    //most of these are unknown
    debugPrintf(DPRINT_FIXED "%02X %08X %08X %08X %08X ",
        *(u16*)(pState + 0x274),  //state number
        *(u32*)(pState + 0x310),  //various flags
        *(u32*)(pState + 0x314),  //various flags
        *(u32*)(pState + 0x318),  //various flags
        *(u32*)(pState + 0x31C)); //various flags

    debugPrintf("%08X %08X %08X %04X %02X" DPRINT_NOFIXED "\n",
        *(u32*)(pState + 0x360),
        *(u32*)(pState + 0x3F0),
        *(u32*)(pState + 0x3F4),
        cState ? ((cState->flags02 << 8) | cState->field_03) : 0,
        cState ? cState->field_0B : 0);

    float waterCurrentRelX = *(float*)(pState + 0x43C); //water current, player-relative
    float waterCurrentRelZ = *(float*)(pState + 0x440);
    float waterCurrentAbsX = *(float*)(pState + 0x648); //water current, world-relative
    float waterCurrentAbsZ = *(float*)(pState + 0x64C);
    float waterDepth       = *(float*)(pState + 0x838); //how deep we are in it
    float waterHeight      = *(float*)(pState + 0x83C); //Y pos of top
    float waterBottomDist  = *(float*)(pState + 0x1B0); //distance to bottom
    float curAbsLen = sqrtf( //current's absolute-vector length
        (waterCurrentAbsX*waterCurrentAbsX)+
        (waterCurrentAbsZ*waterCurrentAbsZ));
    float curRelLen = sqrtf( //current's relative-vector length
        (waterCurrentRelX*waterCurrentRelX)+
        (waterCurrentRelZ*waterCurrentRelZ));
    if(waterDepth > 0) {
        debugPrintf("Water plane @" DPRINT_FIXED "%5d" DPRINT_NOFIXED ", "
            DPRINT_FIXED "%4d" DPRINT_NOFIXED " from bottom, "
            DPRINT_FIXED "%4d" DPRINT_NOFIXED " from surface\n",
            (int)waterHeight, (int)waterBottomDist, (int)waterDepth);
        debugPrintf("current: " DPRINT_FIXED "%f, %f (%f)" DPRINT_NOFIXED
            "\ncur rel: " DPRINT_FIXED "%f, %f (%f)" DPRINT_NOFIXED "\n",
            waterCurrentAbsX, waterCurrentAbsZ, curAbsLen,
            waterCurrentRelX, waterCurrentRelZ, curRelLen);
    }

    static const struct {
        const char *name;
        u16 offset;
    } objPtrs[] = {
        {"Enemy obj",   0x2D0},
        {"Death obj",   0x46C},
        //{"Staff obj",   0x4B8}, //just same as target?
        {"Obj4BC",      0x4BC},
        {"Obj4C0",      0x4C0},
        {"Obj4C4",      0x4C4},
        {"Collect obj", 0x684},
        {"Obj67C",      0x67C},
        {"Obj700",      0x700},
        {"Obj7B0",      0x7B0},
        {"Ride obj",    0x7F0},
        {"Obj7F4",      0x7F4},
        {"Hold obj",    0x7F8},
        {"Push obj",    0x7FC},
        {NULL,          0}
    };
    for(int i=0; objPtrs[i].name; i++) {
        printPlayerObj(objPtrs[i].name,
            *(ObjInstance**)(pState + objPtrs[i].offset));
    }
}

static u32 ticksToUsec(u64 ticks) {
    return (u32)((float)ticksToSecs(ticks)  * 1000000.0);
}

static void printPerformance() {
    //wtf is this coordinate system
    static const int x=390, startY=16, h=10;
    int y = startY;
    char msg[256]; //debugPrintf doesn't support "%4.1f"

    debugPrintSetPos(x, y);
    debugPrintSetColor(0, 255, 0, 255);
    sprintf(msg, "Logic %3d%%%6dus",
        (int)(pctLogic  * 100.0), ticksToUsec(tLogic));
    debugPrintf(DPRINT_FIXED "%s", msg);
    y += h;

    debugPrintSetPos(x, y);
    debugPrintSetColor(255, 255, 0, 255);
    sprintf(msg, "Rendr %3d%%%6dus",
        (int)(pctRender * 100.0), ticksToUsec(tRender));
    debugPrintf("%s", msg);
    y += h;

    debugPrintSetPos(x, y);
    debugPrintSetColor(0, 128, 255, 255);
    sprintf(msg, "Audio %3d%%%6dus",
        (int)(pctAudio  * 100.0), ticksToUsec(tAudio));
    debugPrintf("%s", msg);
    y += h;

    debugPrintSetPos(x, y);
    debugPrintSetColor(255, 0, 0, 255);
    sprintf(msg, "Load  %3d%%%6dus",
        (int)(pctLoad  * 100.0), ticksToUsec(tLoad));
    debugPrintf("%s", msg);
    y += h;

    debugPrintSetPos(x, y);
    debugPrintSetColor(255, 255, 255, 255);
    sprintf(msg, "Idle  %3d%%%6dus\n",
        (int)((1.0-pctTotal) * 100.0),
        (int)((1000000.0/60.0) - ticksToUsec(tLogic+tRender+tAudio+tLoad)));
    debugPrintf("%s" DPRINT_NOFIXED, msg);
}

static void printFPS() {
    char color[] = {0x81, 255, (gxFrameQueue.nPending > 1) ? 1 : 255, 255, 255, 0};

    //msecsThisFrame goes very low sometimes when it's lagging... frameskip?
    //or more like it's only measuring a partial frame

    //XXX will these positions need changing for console?
    debugPrintSetPos(480, 0); //wtf is this coordinate system
    debugPrintf(DPRINT_FIXED "%s%3d" DPRINT_NOFIXED
        DPRINT_COLOR "\xFF\xFF\xFF\xFF", color,
        //(int)((frame / totalSecs) * 60.0));
        (int)(1000.0 / msecsThisFrame)
    );
    debugPrintSetPos(0, 0);
}

static void printStreams() {
    static StreamsBinEntry *prevStream = NULL;
    if(curStream) {
        StreamsBinEntry *stream = &pStreamsBin[curStream - 1];
        debugPrintf("Stream #" DPRINT_FIXED "0x%03X ID 0x%04X %d,%d,%d pos %f" DPRINT_NOFIXED " %s\n",
            curStream-1, stream->id,
            stream->unk02, stream->unk03, stream->unk04,
            streamPos, stream->name);
        if(stream != prevStream) {
            prevStream = stream;
            OSReport("Started stream: %s", stream->name);
        }
    }
    else if(prevStream) {
        OSReport("Stopped stream: %s", prevStream->name);
        prevStream = NULL;
    }
}

static void printSFX() {
    for(s16 iObj=0; iObj < nObjsPlayingSounds; iObj++) {
        char name[12];
        getObjName(name, objsPlayingSounds[iObj]);
        debugPrintf(DPRINT_FIXED "%08X %-11s %04X %02X" DPRINT_NOFIXED "\n",
            objsPlayingSounds[iObj], name,
            objCurPlayingSounds[iObj], objSoundQueueFlags[iObj]);
    }
}

static void printEnvironment() {
    debugPrintf("Day " DPRINT_FIXED "%2d, ", mainGetBit(0x2BA));
    if(pSkyStruct) {
        int now = (int)pSkyStruct->timeOfDay;
        debugPrintf("%02d:%02d:%02d s %d %f" DPRINT_NOFIXED "\n",
            (int)(now / 3600),
            (int)(now /   60) % 60,
            (int)(now)        % 60,
            pSkyStruct->timeSpeed210, pSkyStruct->timeSpeed);
    }
    else debugPrintf(DPRINT_NOFIXED "no sky\n");
    SaveGameEnvState *env = saveGame_getEnv();
    if(env) {
        debugPrintf("Saved FX: " DPRINT_FIXED);
        for(int i=0; i<8; i++) {
            //this is an array of 5 and another array of 3
            //not sure why
            debugPrintf("%04X ", env->envFxActIdx[i] & 0xFFFF);
        }
        debugPrintf(DPRINT_NOFIXED "flags=" DPRINT_FIXED "%02X"
            DPRINT_NOFIXED "\nUnk: " DPRINT_FIXED, env->flags40);
        u8 *data = (u8*)&env->unk38;
        for(int i=0; i<8; i++) {
            debugPrintf("%02X ", data[i]);
        }
        debugPrintf(DPRINT_NOFIXED "Objs " DPRINT_FIXED "%d %d %d" DPRINT_NOFIXED "\n",
            env->skyObjIdx[0], env->skyObjIdx[1], env->skyObjIdx[2]);
    }
}

static void printObjSeq() {
    if(curSeqNo) {
        debugPrintf("Seq " DPRINT_FIXED "%02X" DPRINT_NOFIXED "\n",
            curSeqNo);
    }
}

static void printTrickyInfo() {
    //this is in addition to a bunch of vanilla info
    if(!(pTricky && pTricky->state && pTricky->defNo == ObjDefEnum_Tricky)) return;

    static const char *stateNames[] = {
        "Init", "Idle", "DigGround", "DigTunnel",
        "Dummy4", "Move", "Dummy6", "Flame",
        "Guard", "Unk9", "UnkA", "PlayBall",
        "UnkC", "BaddieAlert", "Growl", "Stay",
    };

    void *state = (void*)pTricky->state;
    //float timer364 = *(float*)(state + 0x364);
    float lastDamageTimer = *(float*)(state + 0x370);
    float timer71C = *(float*)(state + 0x71C);
    float hitByPlayerTimer = *(float*)(state + 0x720);
    //float float740 = *(float*)(state + 0x740);
    char objName[16];

    getObjName(objName, *(ObjInstance**)(state + 0x360));
    debugPrintf("Tricky lastDmg:" DPRINT_FIXED "%5d" DPRINT_NOFIXED
        " Type " DPRINT_FIXED "%02X" DPRINT_NOFIXED " Src %s",
        (int)lastDamageTimer, *(u32*)(state + 0x368), objName);

    if(*(u32*)(state+0x54) & 0x10) debugPrintf("; not obeying");

    getObjName(objName, *(ObjInstance**)(state + 0x24));
    debugPrintf("\nAct:" DPRINT_FIXED "%s %02X" DPRINT_NOFIXED
        " 71C:" DPRINT_FIXED "%5d" DPRINT_NOFIXED
        " hitByPlayer:" DPRINT_FIXED "%7d 3A8:%02X" DPRINT_NOFIXED
        " Target:%s\n",
        stateNames[*(u8*)(state+0x08) & 0xF], *(u8*)(state+0x0A),
        (int)timer71C, (int)hitByPlayerTimer,
        *(u8*)(state + 0x3A8), objName);
}

void mainLoopDebugPrint() {
    drawHeaps();
    if(debugRenderFlags & DEBUGRENDER_PERF_METERS) renderPerfMeters();
    if(debugRenderFlags & DEBUGRENDER_RNG) drawRNG();
    if(debugRenderFlags & DEBUGRENDER_WORLD_MAP) drawMapGrid();

    if(!enableDebugText) {
        //WRITE32(0x800559C8, 0x4082000C); //turn off logging object loads
        return; //or else game hangs
    }
    //WRITE_NOP(0x800559C8); //enable logging object loads (very slow)
    debugPrintf(DPRINT_COLOR "\xFF\xFF\xFF\xFF"
        DPRINT_BGCOLOR "\x01\x01\x01\x3F"); //reset color

    //do this first because it changes text position
    //and trying to restore it is a pain
    if(debugTextFlags & DEBUGTEXT_PERFORMANCE)       printPerformance();
    if(debugTextFlags & DEBUGTEXT_FPS)               printFPS();

    if(debugTextFlags & DEBUGTEXT_PLAYER_COORDS)     printCoords();
    if(debugTextFlags & DEBUGTEXT_CAMERA_COORDS)     printCamera();
    if(debugTextFlags & DEBUGTEXT_RESTART_POINT)     printRestartPoint();
    if(debugTextFlags & DEBUGTEXT_MEMORY_INFO)     { printObjCount(); printMemory(); }
    if(debugTextFlags & DEBUGTEXT_HEAP_STATE)        printHeapInfo();
    if(debugTextFlags & DEBUGTEXT_INTERACT_OBJ_INFO) printTarget();
    if(debugTextFlags & DEBUGTEXT_RNG)               printRNG();
    if(debugTextFlags & DEBUGTEXT_PLAYER_STATE)      printPlayerState();
    if(debugTextFlags & DEBUGTEXT_AUDIO_STREAMS)     printStreams();
    if(debugTextFlags & DEBUGTEXT_AUDIO_SFX)         printSFX();
    if(debugTextFlags & DEBUGTEXT_ENVIRONMENT)       printEnvironment();
    if(debugTextFlags & DEBUGTEXT_OBJSEQ)            printObjSeq();
    if(debugTextFlags & DEBUGTEXT_TRICKY)            printTrickyInfo();

    //not sure what these are, seem to never be used?
    /* extern ObjInstance *objVar_802cada0[5];
    for(int i=0; i<5; i++) {
        ObjInstance *obj = objVar_802cada0[i];
        if(obj) {
            char name[12];
            debugPrintf("Obj" DPRINT_FIXED "%d %08X" DPRINT_NOFIXED " %s\n", i, obj, name);
        }
    } */

    //temporary
    #if 0
    for(int iObj=0; iObj<numLoadedObjs; iObj++) {
        ObjInstance *obj = loadedObjects[iObj];
        if(!obj) continue;
        if(obj->defNo == 0x76A) {
            void *state = obj->state;
            if(!state) continue;
            ObjInstance *lHand = *(ObjInstance**)(state+0x4);
            ObjInstance *rHand = *(ObjInstance**)(state+0x8);
            ObjInstance *brain = *(ObjInstance**)(state+0xC);

            debugPrintf("Andross[%08X] act=%02X flag=%02X %f LH:%02X RH:%02X B:%02X\n",
                state, *(u32*)(state+0x88),
                *(u8*)(state+0xAD),
                *(float*)(state+0x9C),
                (lHand && PTR_VALID(lHand->state)) ? *(u8*)(lHand->state + 0x23) : 0xFF,
                (rHand && PTR_VALID(rHand->state)) ? *(u8*)(rHand->state + 0x23) : 0xFF,
                (brain && PTR_VALID(brain->state)) ? *(u8*)(brain->state + 0x1C) : 0xFF);
        }
    }
    #endif

    rngCalls = 0; //reset logging
    rngReseeds = 0;
    debugPrintf("\n"); //for game's own messages
    printHits();
}
