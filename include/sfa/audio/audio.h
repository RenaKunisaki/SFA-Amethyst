#define NUM_SONGS 99
#define NUM_STREAMS 830

typedef enum { //type:u32
	AudioChannelEnum_SFX = 0x16,
	AudioChannelEnum_Music = 0x15,
} AudioChannelEnum;

typedef enum { //type:u16
	MusicId_DIM_Day_3C = 0x90,
	MusicId_galleon_battle_92 = 0xE8,
	MusicId_guard_theme_77 = 0xCD,
	MusicId_drako_1_56 = 0xAC,
	MusicId_windydocks_3D = 0x91,
	MusicId_blizzard_4C = 0xA2,
	MusicId_downthewell_96 = 0xEC,
	MusicId_ice_walkaround_7E = 0xD4,
	MusicId_capeclaw_seaside_68 = 0xBE,
	MusicId_communicator_85 = 0xDB,
	MusicId_CRF_Bridge_0A = 0xC,
	MusicId_trex_chase_35 = 0x37,
	MusicId_guard_theme_7D = 0xD3,
	MusicId_dark_ice_boss_1_40 = 0x94,
	MusicId_cldrnr_dungeon_27 = 0x29,
	MusicId_galleon_battle_9B = 0xF1,
	MusicId_teleport_2D = 0x2F,
	MusicId_nightjungle_9A = 0xF0,
	MusicId_mammoth_walk_78 = 0xCE,
	MusicId_trex_hit_36 = 0x38,
	MusicId_Slow_Motion_39 = 0x3B,
	MusicId_DIM_Cavern_3E = 0x92,
	MusicId_inside_galleon_6F = 0xC5,
	MusicId_kpanomaly_79 = 0xCF,
	MusicId_minecaves_59 = 0xAF,
	MusicId_downthewell_80 = 0xD6,
	MusicId_inside_warlock_72 = 0xC8,
	MusicId_starfox_area_6_9E = 0xF4,
	MusicId_test_of_combat_2E = 0x30,
	MusicId_test_of_strength_61 = 0xB7,
	MusicId_test_of_fear_49 = 0x9D,
	MusicId_CRF_Treasure_0D = 0xF,
	MusicId_warlockmagic_41 = 0x95,
	MusicId_amb_ingae_rain_3A = 0x8E,
	MusicId_back_of_cloudrunner_45 = 0x99,
	MusicId_PU1_Mysterious_82 = 0xD8,
	MusicId_vfp_walkabout_62 = 0xB8,
	MusicId_PU3_Adventure_8C = 0xE2,
	MusicId_slope_9D = 0xF3,
	MusicId_galleon_outside_71 = 0xC7,
	MusicId_volcano_fp_42 = 0x96,
	MusicId_WLC_Puzzle_84 = 0xDA,
	MusicId_sforestday_24 = 0x26,
	MusicId_amb_ingae_rain_3B = 0x8F,
	MusicId_ewt_outside_20 = 0x22,
	MusicId_drako_3_58 = 0xAE,
	MusicId_communicator_26 = 0x28,
	MusicId_DIM_Snow_43 = 0x97,
	MusicId_amb_ingae_rain_05 = 0x7,
	MusicId_drako_2_06 = 0x8,
	MusicId_Arwing_Crash_03 = 0x5,
	MusicId_back_of_cloudrunner_18 = 0x1A,
	MusicId_amb_ingae_rain_02 = 0x4,
	MusicId_cldrnr_dungeon_8B = 0xE1,
	MusicId_starfox_rwing_1_2A = 0x2C,
	MusicId_Dark_Ice_Lava_53 = 0xA9,
	MusicId_test_of_skill_32 = 0x34,
	MusicId_amb_ingae_rain_07 = 0x9,
	MusicId_DIM_Mines_52 = 0xA8,
	MusicId_DIM_Mines_51 = 0xA7,
	MusicId_test_of_magic_30 = 0x32,
	MusicId_amb_ingae_rain_0E = 0x10,
	MusicId_amb_ingae_rain_0F = 0x11,
	MusicId_starfox_map_67 = 0xBD,
	MusicId_test_of_fear_2F = 0x31,
	MusicId_nightjungle_7F = 0xD5,
	MusicId_Krazoa_Docks_11 = 0x13,
	MusicId_amb_ingae_rain_16 = 0x18,
	MusicId_cldrnr_tune1_8F = 0xE5,
	MusicId_test_of_sacrifice_31 = 0x33,
	MusicId_amb_ingae_rain_12 = 0x14,
	MusicId_communicator_94 = 0xEA,
	MusicId_galleon_docks_8E = 0xE4,
	MusicId_CRF_Suspense_0B = 0xD,
	MusicId_swapstone_circle_2C = 0x2E,
	MusicId_nightjungle_8A = 0xE0,
	MusicId_amb_ingae_rain_19 = 0x1B,
	MusicId_DIM_Snow_5D = 0xB3,
	MusicId_amb_lavapits_5A = 0xB0,
	MusicId_test_of_strength_33 = 0x35,
	MusicId_amb_ingae_rain_1B = 0x1D,
	MusicId_barren_1D = 0x1F,
	MusicId_amb_ingae_rain_1C = 0x1E,
	MusicId_LFV_Strength_6B = 0xC1,
	MusicId_barrels_1E = 0x20,
	MusicId_amb_ingae_rain_1A = 0x1C,
	MusicId_test_of_magic_5E = 0xB4,
	MusicId_capeclaw_seaside_21 = 0x23,
	MusicId_test_of_sacrifice_48 = 0x9C,
	MusicId_Krazoa_Docks_86 = 0xDC,
	MusicId_DIM_Mines_6A = 0xC0,
	MusicId_WLC_Chase_69 = 0xBF,
	MusicId_amb_moonlink_90 = 0xE6,
	MusicId_ewt_chase_57 = 0xAD,
	MusicId_barrels_76 = 0xCC,
	MusicId_galleon_storm_7A = 0xD0,
	MusicId_menu_page_88 = 0xDE,
	MusicId_options_page_81 = 0xD7,
	MusicId_drako_1_8D = 0xE3,
	MusicId_teleport_6E = 0xC4,
	MusicId_volcano_fp_97 = 0xED,
	MusicId_volcano_fp_98 = 0xEE,
	MusicId_WLC_Chase_70 = 0xC6,
	MusicId_amb_ingae_rain_75 = 0xCB,
	MusicId_cldrnr_tune1_28 = 0x2A,
	MusicId_DIM_Snow_74 = 0xCA,
	MusicId_teleport_63 = 0xB9,
	MusicId_DIM_Cn_Blt_4B = 0xA1,
	MusicId_PU2_Heroic_83 = 0xD9,
	MusicId_swapstone_circle_47 = 0x9B,
	MusicId_bloop_6C = 0xC2,
	MusicId_wcity_day_4E = 0xA4,
	MusicId_trex_2a_34 = 0x36,
	MusicId_amb_ingae_rain_7B = 0xD1,
	MusicId_kptext_73 = 0xC9,
	MusicId_teleport_5C = 0xB2,
	MusicId_starfox_rwing_1_46 = 0x9A,
	MusicId_test_of_skill_64 = 0xBA,
	MusicId_TTH_Night_37 = 0x39,
	MusicId_LVF_Tracking_6D = 0xC3,
	MusicId_vfp_walkabout_4A = 0x9E,
	MusicId_test_of_strength_93 = 0xE9,
	MusicId_windydocks_5F = 0xB5,
	MusicId_back_of_cloudrunner_5B = 0xB1,
	MusicId_Arwing_Crash_44 = 0x98,
	MusicId_Dark_Ice_Lava_10 = 0x12,
	MusicId_sforestday_9C = 0xF2,
	MusicId_starfox_map_29 = 0x2B,
	MusicId_CRF_Swim_0C = 0xE,
	MusicId_crun_dungeon_3F = 0x93,
	MusicId_blizzard_1F = 0x21,
	MusicId_citytombs_25 = 0x27,
	MusicId_LFV_Swamp_14 = 0x16,
	MusicId_minecaves_89 = 0xDF,
	MusicId_swaphol_night_2B = 0x2D,
	MusicId_newstorm_87 = 0xDD,
	MusicId_dynamic_95 = 0xEB,
	MusicId_amb_moonlink_00 = 0x2,
	MusicId_cave_trade_22 = 0x24,
	MusicId_cldrnr_walkabout_38 = 0x3A,
	MusicId_windydocks_4D = 0xA3,
	MusicId_Krazoa_Shrine_15 = 0x17,
	MusicId_windydocks_4F = 0xA5,
	MusicId_Krazoa_Shrine_13 = 0x15,
	MusicId_kpwin_99 = 0xEF,
	MusicId_windydocks_54 = 0xAA,
	MusicId_windydocks_50 = 0xA6,
	MusicId_greatfox_int_7C = 0xD2,
	MusicId_cclaw_caves_23 = 0x25,
	MusicId_trex_hit_60 = 0xB6,
	MusicId_windydocks_55 = 0xAB,
	MusicId_amb_lavapits_17 = 0x19,
	MusicId_seq_swaphol1_91 = 0xE7,
	MusicId_trex_hit_66 = 0xBC,
	MusicId_trex_hit_65 = 0xBB,
} MusicId;

typedef enum { //type:u16
	SoundId_Warping = 0x467,
	SoundId_FoxFallScream2 = 0x20F,
	SoundId_Tricky_Yawn = 0x354,
	SoundId_FoxFallScream1 = 0x20E,
	SoundId_Zap = 0x41C,
	SoundId_TitleScreenCloseMenu = 0x100,
	SoundId_MenuOpen3EE = 0x3EE,
	SoundId_Blip = 0x405,
	SoundId_FoxClimbUp2 = 0x25,
	SoundId_FoxGrabLedge = 0x29,
	SoundId_TrickyCommandGoGetIt = 0x3FA,
	SoundId_TrickySpewingFire = 0x3DC,
	SoundId_BombSporePickup = 0xA7,
	SoundId_FoxAttack378 = 0x378,
	SoundId_TrickyCommandDecoy = 0x3F7,
	SoundId_RecoverHealth = 0x49,
	SoundId_GlassSmash = 0x47B,
	SoundId_PauseMenuClose = 0x3F2,
	SoundId_Tricky_GetMFox = 0x35B,
	SoundId_FoxFallScream = 0x26,
	SoundId_IceSpell = 0x382,
	SoundId_DootF4 = 0xF4,
	SoundId_Whoosh28B = 0x28B,
	SoundId_PutOutFlame = 0x395,
	SoundId_ZipDown = 0x400,
	SoundId_Drop = 0x287,
	SoundId_ClimbOutOfWater = 0x2F,
	SoundId_Whoosh288 = 0x288,
	SoundId_Tricky_Hello = 0x35E,
	SoundId_Whoosh289 = 0x289,
	SoundId_CMenuEquip = 0xF7,
	SoundId_Tricky_BadGuy = 0x358,
	SoundId_MapZoom = 0x3F0,
	SoundId_Pip3F1 = 0x3F1,
	SoundId_TrickyCommandWhistle = 0x3FB,
	SoundId_Tricky_ImStuffed = 0x364,
	SoundId_Tricky_Sniff = 0x357,
	SoundId_Ding = 0xFB,
	SoundId_TrickyCommandStay = 0x3FC,
	SoundId_Splash42B = 0x42B,
	SoundId_RobotHover = 0xE8,
	SoundId_FoxHurt = 0x24,
	SoundId_KrystalRoll2 = 0x3CE,
	SoundId_KrystalRoll1 = 0x3CD,
	SoundId_StaffTakeOut = 0xC0,
	SoundId_TitleScreenChangePage = 0x37B,
	SoundId_HagabonWoosh = 0x236,
	SoundId_MapChangeMode = 0x3ED,
	SoundId_KrystalJump = 0x2D7,
	SoundId_Clang = 0x6F,
	SoundId_FoxClimbUp = 0x1D,
	SoundId_ElectricCrackle = 0x9E,
	SoundId_TrickyFinishFlame = 0x29D,
	SoundId_ZipUp = 0x3FF,
	SoundId_BombPlantGrow = 0xA1,
	SoundId_FoxJump = 0x2D6,
	SoundId_SpellCastFailed = 0x10A,
	SoundId_Tricky_WhereAreWeGoing = 0x365,
	SoundId_TrickyCommandFind = 0x3F8,
	SoundId_CymbalCrash = 0x28D,
	SoundId_Tricky_Dumdedum = 0x360,
	SoundId_CMenuOpen = 0x408,
	SoundId_SomeKindOfWhoosh = 0x374,
	SoundId_KrystalHurt = 0x1F,
	SoundId_FuelCell = 0x403,
	SoundId_TitleScreenOpenMenu = 0xFF,
	SoundId_SmackC2 = 0xC2,
	SoundId_Drip = 0x285,
	SoundId_SmackC3 = 0xC3,
	SoundId_BombPlantBoom = 0xA3,
	SoundId_Tricky_HiFella = 0x35F,
	SoundId_BallBounce = 0x16C,
	SoundId_Thud17C = 0x17C,
	SoundId_TitleScreenBeep = 0x41A,
	SoundId_Thud17B = 0x17B,
	SoundId_EvilLaugh = 0x470,
	SoundId_WarningBeep = 0x38D,
	SoundId_Tricky_Food = 0x359,
	SoundId_Tricky_Hey = 0x34F,
	SoundId_Tricky_WaitForMe = 0x34E,
	SoundId_FoxLandOof = 0x27,
	SoundId_Trick_Chewing = 0x362,
	SoundId_Tricky_ImHungry = 0x352,
	SoundId_NO_SOUND = 0xFFFF,
	SoundId_FoxThrow = 0x379,
	SoundId_Teleport = 0x4A2,
	SoundId_MagicPickupRinging = 0x56,
	SoundId_TrickyDigging = 0x13D,
	SoundId_EnterFirstPersonNoGoggles = 0x3F3,
	SoundId_Tricky_LookAtThis = 0x351,
	SoundId_SplashBA = 0xBA,
	SoundId_Tricky_Cool = 0x356,
	SoundId_StaffPutAway = 0xC1,
	SoundId_CannonFire = 0x1FD,
	SoundId_PauseMenuOpen = 0x3E5,
	SoundId_Tricky_GetOff = 0x350,
	SoundId_Tricky_LetsPlay = 0x355,
	SoundId_Tricky_Laugh = 0x361,
	SoundId_KrystalFallScream = 0x2D0,
	SoundId_MenuOpen = 0x98,
	SoundId_RobotTalk = 0xE7,
	SoundId_Tricky_Yeah = 0x35C,
	SoundId_MenuSlide = 0x401,
	SoundId_FireyExplosion = 0x6E,
	SoundId_Tricky_TheresSomethingNear = 0x35A,
	SoundId_TrickyCommandFlame = 0x3F9,
	SoundId_TextPip = 0x397,
	SoundId_MenuClose3EF = 0x3EF,
	SoundId_TitleScreenSelect = 0x418,
	SoundId_EnterViewFinder = 0x3F5,
	SoundId_CMenuClose = 0x37C,
	SoundId_KrystalLandOof = 0x399,
	SoundId_Tricky_ImNotDoingIt = 0x35D,
	SoundId_Woosh471 = 0x471,
	SoundId_Tricky_MmmmTasty = 0x363,
	SoundId_Woosh472 = 0x472,
	SoundId_HagabonWhir = 0x3E8,
	SoundId_KrystalThrow = 0x327,
	SoundId_TickTickTick = 0x28C,
	SoundId_StaticyRadarBeep = 0x3D8,
	SoundId_RobotActivate = 0x3F4,
	SoundId_FoxPant = 0x452,
	SoundId_CameraTurnBehindPlayer = 0x286,
	SoundId_RollInWater = 0x427,
	SoundId_MenuOpenF5 = 0xF5,
	SoundId_Tricky_WaitUpFox = 0x34D,
	SoundId_Tricky_Yawn2 = 0x353,
	SoundId_TitleScreenZip = 0xFC,
	SoundId_GenericItemPickup = 0x58,
	SoundId_KrystalGrabLedge = 0x2CB,
	SoundId_Squak = 0xFD,
	SoundId_FoxRoll = 0x2E,
	SoundId_Burning = 0x394,
	SoundId_WarpIn = 0x420,
	SoundId_KrystalClimbUp = 0x398,
	SoundId_ZipUp41B = 0x41B,
	SoundId_PipF3 = 0xF3,
	SoundId_Chime = 0x402,
	SoundId_ElectronicChime3EB = 0x3EB,
	SoundId_RobotZap = 0xE9,
	SoundId_TitleScreenCancel = 0x419,
	SoundId_ElectronicChime3EC = 0x3EC,
	SoundId_ToggleDisguise = 0x69,
} SoundId;

typedef enum { //type:u16
	SoundId2_KrystalRoll2 = 0x265,
	SoundId2_Stay = 0x261,
} SoundId2;

typedef struct PACKED SfxBinEntry {
	u16 id;         //0x00 SoundId
	u8  baseVolume; //0x02
	u8  volumeRand; //0x03 volume = rand(baseVolume - volumeRand, baseVolume + volumeRand)
	u8  basePan;    //0x04 127 = center
	u8  panRand;    //0x05 never used, but works same as volumeRand
	u16 unk06;      //0x06
	u16 range;      //0x08 how far from source object to silence
	u16 fxIds[6];   //0x0A actual sound to play (not same as SoundId)
	u8  fxChance[6];//0x16 chance to pick each sound
	u16 randMax;    //0x1C sum of fxChance
	u8  unk1E;      //0x1E maybe queue slot? high 4bits are idx into sfxTable_803db248
	u8  numIdxs : 4;//0x1F num items in randVals
	u8  prevIdx : 4;//0x1F previously played idx, to avoid playing same random idx twice in a row.
} SfxBinEntry;
extern SfxBinEntry *pSfxBin;
extern u32 sfxBinSize; //bytes

typedef struct PACKED SoundEffect {
	ushort id;          //0x0
	ushort unk02;       //0x2
	byte   unk04;       //0x4
	byte   unk05;       //0x5
	byte   unk06;       //0x6
	byte   unk07;       //0x7
	u32    idxAndOffset;//0x8
	u16    rate;        //0xC
	u16    pitch;       //0xE
	int    length;      //0x10
	u32    repeatStart; //0x14
	u32    repeatEnd;   //0x18
	u32    variation;   //0x1C
} SoundEffect;

typedef struct PACKED SongTableEntry {
    s16 unk00; //0x0
    s8  unk02; //0x2
    s8  unk03; //0x3
    const char *name; //0x4
    int unk08; //0x8
    int unk0C; //0xc
} SongTableEntry;
extern SongTableEntry songTable[NUM_SONGS];

typedef struct {
    u16	 id;       //0x0
    s8   unk02;    //0x2
    s8   unk03;    //0x3
    u16  unk04;    //0x4
    char name[16]; //0x6
} StreamsBinEntry;
extern StreamsBinEntry *pStreamsBin;

#define MAX_OBJS_PLAYING_SOUNDS 128
extern ObjInstance *objsPlayingSounds[MAX_OBJS_PLAYING_SOUNDS];
extern s16 objCurPlayingSounds[MAX_OBJS_PLAYING_SOUNDS]; //SoundId
extern u8 objSoundQueueFlags[MAX_OBJS_PLAYING_SOUNDS];
extern s16 nObjsPlayingSounds;

extern int curStream; //stream ID +1
extern float streamPos;
