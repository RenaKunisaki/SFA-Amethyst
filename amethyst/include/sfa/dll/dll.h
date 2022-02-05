typedef struct PACKED DLL {
    u32 headerSize;       //0x00 always zero (used in DP)
    s32 dataOffset;       //0x04 always zero (used in DP)
    s32 roDataOffset;     //0x08 always zero (used in DP)
    u16	exportCount;      //0x0c
    u16 padding0E;        //0x0e
    void (*initialise)(void *self, u16 param); //0x10; param is DLL*
    void (*release)();    //0x14
    void *functions[];    //0x18 count = exportCount; first is always NULL
    //note, this was originally a dynamic relocation system in DP, and there
    //could be lots of offsets here, not just function pointers. while SFA no
    //longer uses relocation, some DLLs do still have a ton of extra things here
    //that aren't function pointers, and maybe aren't pointers at all.
} DLL;

extern DLL *g_dlls[NUM_DLLS];
extern void *g_dllsLoaded[NUM_DLLS]; // -> dll->functions
extern s16 g_dllRefCount[NUM_DLLS];
