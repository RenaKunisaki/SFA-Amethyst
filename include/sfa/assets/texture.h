typedef enum { //type:u32
    HudTextureId_BoxCorner            = 0x0A,
    HudTextureId_BoxSide              = 0x0B,
    HudTextureId_BoxInterior          = 0x0C,
	HudTextureId_BoxTopBottom         = 0x0D,
    HudTextureId_TrickyFace           = 0x55,
	HudTextureId_TrickyFoodMeterEmpty = 0x56,
	HudTextureId_TrickyFoodMeterFull  = 0x57,
} HudTextureId;

typedef enum { //type:u32
    TextureFileId_DebugFontUppercase = 0x1,
	TextureFileId_DebugFontLowercase = 0x2,
    TextureFileId_WaterFx0056        = 0x56,
	TextureFileId_DebugFontDigits    = 0x25D,
	TextureFileId_AirMeterEmpty      = 0x5D2,
    TextureFileId_AirMeterFull       = 0x5D3,
    TextureFileId_AirMeterRightSide  = 0x5D4,
    TextureFileId_AirMeterIconFox    = 0x603,
    TextureFileId_WaterFx0C2A        = 0xC2A,
	TextureFileId_WaterFx0C2C        = 0xC2C,
	TextureFileId_WaterFx0C2D        = 0xC2D,
} TextureFileId;

typedef enum { //type:u8
    TextureFormat_I4     = 0x0,
    TextureFormat_I8     = 0x1,
    TextureFormat_IA4    = 0x2,
    TextureFormat_IA8    = 0x3,
    TextureFormat_RGB565 = 0x4,
    TextureFormat_RGB5A3 = 0x5,
    TextureFormat_RGBA32 = 0x6,
    TextureFormat_C4     = 0x8,
	TextureFormat_C8     = 0x9,
	TextureFormat_C14X2  = 0xA,
    TextureFormat_BC1    = 0xE,
} TextureFormat;

//SDK includes a definition of this struct but it's opaque
typedef struct PACKED {
	u32   mode0;    //00
	u32   mode1;    //04
	u32   image0;   //08
	u32   image3;   //0C
	void* userData; //10 game stores the Texture* here
    u32   format;   //14 GXTexFmt
	u32   tlutName; //18
	u16   loadCnt;  //1C
	u8    loadFmt;  //1E 0=CMPR 1=4bpp 2=8bpp 3=32bpp
	u8    flags;    //1F 1=mipmap 2=isRGB
} GXTexObj_real;
CASSERT(sizeof(GXTexObj_real) == 0x20, sizeof_GXTexObj_real);

typedef struct PACKED Texture {
	//^ denotes fields that are always 0 in the files on disc
	Texture*      next;                 //^00
	u32           flags;                //^04
	s16           xOffset;              //^08
	u16           width;                // 0A
	u16           height;               // 0C
	s16           usage;                // 0E ref count
	s16           frameVal10;           // 10 related to anim frame count
	s16           unk12;                //^12 always 0, never accessed?
	u16           framesPerTick;        // 14 how many frames to advance each tick
	u8            format;               // 16 GXTexFmt
	u8            wrapS;                // 17 GXTexWrapMode
	u8            wrapT;                // 18 GXTexWrapMode
	u8            minFilter;            // 19 FilterMode
	u8            magFilter;            // 1A FilterMode
	u8            _padding1B;           //^1B always 0, never accessed (odd place for padding; maybe unused field)
	u8            minLod;               // 1C (bias hardcoded to -2)
	u8            maxLod;               // 1D
	u8            unk1E;                // 1E padding? never accessed, but some files have 0xFF
	u8            _padding1F;           //^1F padding
	GXTexObj_real texObj;               //^20 all zero in file
	GXTexRegion*  texRegion;            //^40
	s32           bufSize;              //^44 raw image data size
	bool          bNoTexRegionCallback; // ^48 bool use gxSetTexImage0 instead of gxCallTexRegionCallback
	bool          bDoNotFree;           // ^49 bool (maybe memory region?)
	s8            unk4A;                // ^4A never accessed
	s8            unk4B;                // ^4B set to 10 on free, otherwise never acccessed (memory region?)
	u32           bufSize2;             //^4C same as bufSize (allocated size?)
	u32           tevVal50;             // 50 0:use 1 TEV stage, not 2 (maybe bHasTwoTevStages?)
	u32           _padding54[3];        //^54
	u8            data[0];              // 60 variable size
} Texture;
CASSERT(sizeof(Texture) == 0x60, sizeof_Texture);

typedef struct LoadedTexture {
	int        id;       //0x0
	Texture   *texture;  //0x4
	int        unk08;    //0x8
	int        heapSize; //0xC
} LoadedTexture;
