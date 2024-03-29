#define MAX_LIGHTS 50

typedef struct PACKED {
    ObjInstance *obj;             //0x00
    vec3f        unk04;           //0x04
    vec3f        vLight;          //0x10
    vec3f        vPos;            //0x1c
    vec3f        vIn;             //0x28
    vec3f        vOut;            //0x34 =F(obj, vIn)
    vec3f        vSpec;           //0x40 specular direction
    bool         bOn;             //0x4c is light on?
    byte         unk4D;           //0x4d
    u8           unk4E;           //0x4e
    u8           unk4F;           //0x4f
    uint         mode;            //0x50
    u8          *unk54;           //0x54
    u32          state;           //0x58
    u32          unk5C;           //0x5c
    void        *unk60;           //0x60
    byte         lightFlags_0x64; //0x64
    u8           unk65;           //0x65
    u8           unk66;           //0x66
    u8           unk67;           //0x67
    GXLightObj   gxLight;         //0x68
    Color4b      lightColorA8;    //0xa8
    Color4b      unkAC;           //0xac
    Color4b      unkB0;           //0xb0
    float        unkB4;           //0xb4
    u32          unkB8;           //0xb8
    byte         unkBC;           //0xbc
    u8           unkBD;           //0xbd
    u8           unkBE;           //0xbe
    u8           unkBF;           //0xbf
    GXLightObj   light_c0;        //0xc0
    Color4b      lightColor;      //0x100 gets copied into light
    Color4b      unk104;          //0x104
    Color4b      unk108;          //0x108
    float        unk10c;          //0x10c
    float        unk110;          //0x110
    byte         unk114;          //0x114
    u8           unk115;          //0x115
    u8           unk116;          //0x116
    u8           unk117;          //0x117
    u8           unk118;          //0x118
    u8           unk119;          //0x119
    u8           unk11a;          //0x11a
    u8           unk11b;          //0x11b
    u8           unk11c;          //0x11c
    u8           unk11d;          //0x11d
    u8           unk11e;          //0x11e
    u8           unk11f;          //0x11f
    u8           unk120;          //0x120
    u8           unk121;          //0x121
    u8           unk122;          //0x122
    u8           unk123;          //0x123
    float        distAttenA0;     //0x124
    float        distAttenA1;     //0x128
    float        distAttenA2;     //0x12c
    float        colorVal_0x130;  //0x130 relates to lightAmount; maybe distance? capped to range (0, 1000)
    float        lightAmount;     //0x134 R, G, B are multiplied by this
    float        fadeTarget;      //0x138
    float        fadeSpeed;       //0x13c
    float        refDistance;     //0x140
    float        unk144;          //0x144
    u8           unk148;          //0x148
    u8           unk149;          //0x149
    u8           unk14A;          //0x14a
    u8           unk14B;          //0x14b
    u8           unk14C;          //0x14c
    u8           unk14D;          //0x14d
    u8           unk14E;          //0x14e
    u8           unk14F;          //0x14f
    float        unk150;          //0x150
    float        unk154;          //0x154
    float        unk158;          //0x158
    float        unk15C;          //0x15c
    float        unk160;          //0x160
    float        unk164;          //0x164
    dword        unk168;          //0x168
    dword        unk16C;          //0x16c
    Mtx          unk170;          //0x170
    u8           unk1A0;          //0x1a0
    u8           unk1A1;          //0x1a1
    u8           unk1A2;          //0x1a2
    u8           unk1A3;          //0x1a3
    u8           unk1A4;          //0x1a4
    u8           unk1A5;          //0x1a5
    u8           unk1A6;          //0x1a6
    u8           unk1A7;          //0x1a7
    u8           unk1A8;          //0x1a8
    u8           unk1A9;          //0x1a9
    u8           unk1AA;          //0x1aa
    u8           unk1AB;          //0x1ab
    u8           unk1AC;          //0x1ac
    u8           unk1AD;          //0x1ad
    u8           unk1AE;          //0x1ae
    u8           unk1AF;          //0x1af
    u8           unk1B0;          //0x1b0
    u8           unk1B1;          //0x1b1
    u8           unk1B2;          //0x1b2
    u8           unk1B3;          //0x1b3
    u8           unk1B4;          //0x1b4
    u8           unk1B5;          //0x1b5
    u8           unk1B6;          //0x1b6
    u8           unk1B7;          //0x1b7
    u8           unk1B8;          //0x1b8
    u8           unk1B9;          //0x1b9
    u8           unk1BA;          //0x1ba
    u8           unk1BB;          //0x1bb
    u8           unk1BC;          //0x1bc
    u8           unk1BD;          //0x1bd
    u8           unk1BE;          //0x1be
    u8           unk1BF;          //0x1bf
    u8           unk1C0;          //0x1c0
    u8           unk1C1;          //0x1c1
    u8           unk1C2;          //0x1c2
    u8           unk1C3;          //0x1c3
    u8           unk1C4;          //0x1c4
    u8           unk1C5;          //0x1c5
    u8           unk1C6;          //0x1c6
    u8           unk1C7;          //0x1c7
    u8           unk1C8;          //0x1c8
    u8           unk1C9;          //0x1c9
    u8           unk1CA;          //0x1ca
    u8           unk1CB;          //0x1cb
    u8           unk1CC;          //0x1cc
    u8           unk1CD;          //0x1cd
    u8           unk1CE;          //0x1ce
    u8           unk1CF;          //0x1cf
    u8           unk1D0;          //0x1d0
    u8           unk1D1;          //0x1d1
    u8           unk1D2;          //0x1d2
    u8           unk1D3;          //0x1d3
    u8           unk1D4;          //0x1d4
    u8           unk1D5;          //0x1d5
    u8           unk1D6;          //0x1d6
    u8           unk1D7;          //0x1d7
    u8           unk1D8;          //0x1d8
    u8           unk1D9;          //0x1d9
    u8           unk1DA;          //0x1da
    u8           unk1DB;          //0x1db
    u8           unk1DC;          //0x1dc
    u8           unk1DD;          //0x1dd
    u8           unk1DE;          //0x1de
    u8           unk1DF;          //0x1df
    u8           unk1E0;          //0x1e0
    u8           unk1E1;          //0x1e1
    u8           unk1E2;          //0x1e2
    u8           unk1E3;          //0x1e3
    u8           unk1E4;          //0x1e4
    u8           unk1E5;          //0x1e5
    u8           unk1E6;          //0x1e6
    u8           unk1E7;          //0x1e7
    u8           unk1E8;          //0x1e8
    u8           unk1E9;          //0x1e9
    u8           unk1EA;          //0x1ea
    u8           unk1EB;          //0x1eb
    u8           unk1EC;          //0x1ec
    u8           unk1ED;          //0x1ed
    u8           unk1EE;          //0x1ee
    u8           unk1EF;          //0x1ef
    Mtx          unk1F0;          //0x1f0
    u8           unk220;          //0x220
    u8           unk221;          //0x221
    u8           unk222;          //0x222
    u8           unk223;          //0x223
    u8           unk224;          //0x224
    u8           unk225;          //0x225
    u8           unk226;          //0x226
    u8           unk227;          //0x227
    u8           unk228;          //0x228
    u8           unk229;          //0x229
    u8           unk22A;          //0x22a
    u8           unk22B;          //0x22b
    u8           unk22C;          //0x22c
    u8           unk22D;          //0x22d
    u8           unk22E;          //0x22e
    u8           unk22F;          //0x22f
    u8           unk230;          //0x230
    u8           unk231;          //0x231
    u8           unk232;          //0x232
    u8           unk233;          //0x233
    u8           unk234;          //0x234
    u8           unk235;          //0x235
    u8           unk236;          //0x236
    u8           unk237;          //0x237
    u8           unk238;          //0x238
    u8           unk239;          //0x239
    u8           unk23A;          //0x23a
    u8           unk23B;          //0x23b
    u8           unk23C;          //0x23c
    u8           unk23D;          //0x23d
    u8           unk23E;          //0x23e
    u8           unk23F;          //0x23f
    u8           unk240;          //0x240
    u8           unk241;          //0x241
    u8           unk242;          //0x242
    u8           unk243;          //0x243
    u8           unk244;          //0x244
    u8           unk245;          //0x245
    u8           unk246;          //0x246
    u8           unk247;          //0x247
    u8           unk248;          //0x248
    u8           unk249;          //0x249
    u8           unk24A;          //0x24a
    u8           unk24B;          //0x24b
    u8           unk24C;          //0x24c
    u8           unk24D;          //0x24d
    u8           unk24E;          //0x24e
    u8           unk24F;          //0x24f
    u8           unk250;          //0x250
    u8           unk251;          //0x251
    u8           unk252;          //0x252
    u8           unk253;          //0x253
    u8           unk254;          //0x254
    u8           unk255;          //0x255
    u8           unk256;          //0x256
    u8           unk257;          //0x257
    u8           unk258;          //0x258
    u8           unk259;          //0x259
    u8           unk25A;          //0x25a
    u8           unk25B;          //0x25b
    u8           unk25C;          //0x25c
    u8           unk25D;          //0x25d
    u8           unk25E;          //0x25e
    u8           unk25F;          //0x25f
    u8           unk260;          //0x260
    u8           unk261;          //0x261
    u8           unk262;          //0x262
    u8           unk263;          //0x263
    u8           unk264;          //0x264
    u8           unk265;          //0x265
    u8           unk266;          //0x266
    u8           unk267;          //0x267
    u8           unk268;          //0x268
    u8           unk269;          //0x269
    u8           unk26A;          //0x26a
    u8           unk26B;          //0x26b
    u8           unk26C;          //0x26c
    u8           unk26D;          //0x26d
    u8           unk26E;          //0x26e
    u8           unk26F;          //0x26f
    u8           unk270;          //0x270
    u8           unk271;          //0x271
    u8           unk272;          //0x272
    u8           unk273;          //0x273
    u8           unk274;          //0x274
    u8           unk275;          //0x275
    u8           unk276;          //0x276
    u8           unk277;          //0x277
    u8           unk278;          //0x278
    u8           unk279;          //0x279
    u8           unk27A;          //0x27a
    u8           unk27B;          //0x27b
    u8           unk27C;          //0x27c
    u8           unk27D;          //0x27d
    u8           unk27E;          //0x27e
    u8           unk27F;          //0x27f
    u8           unk280;          //0x280
    u8           unk281;          //0x281
    u8           unk282;          //0x282
    u8           unk283;          //0x283
    u8           unk284;          //0x284
    u8           unk285;          //0x285
    u8           unk286;          //0x286
    u8           unk287;          //0x287
    u8           unk288;          //0x288
    u8           unk289;          //0x289
    u8           unk28A;          //0x28a
    u8           unk28B;          //0x28b
    u8           unk28C;          //0x28c
    u8           unk28D;          //0x28d
    u8           unk28E;          //0x28e
    u8           unk28F;          //0x28f
    u8           unk290;          //0x290
    u8           unk291;          //0x291
    u8           unk292;          //0x292
    u8           unk293;          //0x293
    u8           unk294;          //0x294
    u8           unk295;          //0x295
    u8           unk296;          //0x296
    u8           unk297;          //0x297
    u8           unk298;          //0x298
    u8           unk299;          //0x299
    u8           unk29A;          //0x29a
    u8           unk29B;          //0x29b
    u8           unk29C;          //0x29c
    u8           unk29D;          //0x29d
    u8           unk29E;          //0x29e
    u8           unk29F;          //0x29f
    u8           unk2A0;          //0x2a0
    u8           unk2A1;          //0x2a1
    u8           unk2A2;          //0x2a2
    u8           unk2A3;          //0x2a3
    u8           unk2A4;          //0x2a4
    u8           unk2A5;          //0x2a5
    u8           unk2A6;          //0x2a6
    u8           unk2A7;          //0x2a7
    u8           unk2A8;          //0x2a8
    u8           unk2A9;          //0x2a9
    u8           unk2AA;          //0x2aa
    u8           unk2AB;          //0x2ab
    u8           unk2AC;          //0x2ac
    u8           unk2AD;          //0x2ad
    u8           unk2AE;          //0x2ae
    u8           unk2AF;          //0x2af
    u8           unk2B0;          //0x2b0
    u8           unk2B1;          //0x2b1
    u8           unk2B2;          //0x2b2
    u8           unk2B3;          //0x2b3
    u8           unk2B4;          //0x2b4
    u8           unk2B5;          //0x2b5
    u8           unk2B6;          //0x2b6
    u8           unk2B7;          //0x2b7
    u8           unk2B8;          //0x2b8
    u8           unk2B9;          //0x2b9
    u8           unk2BA;          //0x2ba
    u8           unk2BB;          //0x2bb
    u8           unk2BC;          //0x2bc
    u8           unk2BD;          //0x2bd
    u8           unk2BE;          //0x2be
    u8           unk2BF;          //0x2bf
    u8           unk2C0;          //0x2c0
    u8           unk2C1;          //0x2c1
    u8           unk2C2;          //0x2c2
    u8           unk2C3;          //0x2c3
    u8           unk2C4;          //0x2c4
    u8           unk2C5;          //0x2c5
    u8           unk2C6;          //0x2c6
    u8           unk2C7;          //0x2c7
    u8           unk2C8;          //0x2c8
    u8           unk2C9;          //0x2c9
    u8           unk2CA;          //0x2ca
    u8           unk2CB;          //0x2cb
    u8           unk2CC;          //0x2cc
    u8           unk2CD;          //0x2cd
    u8           unk2CE;          //0x2ce
    u8           unk2CF;          //0x2cf
    u8           unk2D0;          //0x2d0
    u8           unk2D1;          //0x2d1
    u8           unk2D2;          //0x2d2
    u8           unk2D3;          //0x2d3
    u8           unk2D4;          //0x2d4
    u8           unk2D5;          //0x2d5
    u8           unk2D6;          //0x2d6
    u8           unk2D7;          //0x2d7
    int          unk2D8;          //0x2d8
    float        unk2DC;          //0x2dc
    float        rand2E0;         //0x2e0
    float        unk2E4;          //0x2e4
    Texture     *texture;         //0x2e8
    u8           unk2EC;          //0x2ec
    u8           unk2ED;          //0x2ed
    u8           unk2EE;          //0x2ee
    u8           unk2EF;          //0x2ef
    u8           unk2F0;          //0x2f0
    u8           unk2F1;          //0x2f1
    u8           unk2F2;          //0x2f2
    u8           unk2F3;          //0x2f3
    u8           unk2F4;          //0x2f4
    u8           unk2F5;          //0x2f5
    u8           unk2F6;          //0x2f6
    u8           unk2F7;          //0x2f7
    byte         texRelated2F8;   //0x2f8
    u8           unk2F9;          //0x2f9
    u8           unk2FA;          //0x2fa
    u8           unk2FB;          //0x2fb
    byte         colorVal_0x2fc;  //0x2fc
    u8           unk2FD;          //0x2fd
    u8           unk2FE;          //0x2fe
    u8           unk2FF;          //0x2ff
} Light;
extern Light* g_lights[MAX_LIGHTS];
extern u8 nLights;
