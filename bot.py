import os
import json
import time
import random
import asyncio
import traceback
from datetime import datetime, timedelta
from bale import Bot, Message, User, Chat, ChatMember

# -------------------- CONFIGURATION --------------------
TOKEN = "1014684452:DsvPJv7fND2xZcx7C4VfydXiJDfDnBhvL1nitb4S"
DATA_FILE = "group_data.json"
USER_DATA_FILE = "global_user_data.json"  # New file for global user data
bot = Bot(token=TOKEN)

# -------------------- COUNTRIES AND ECONOMICS --------------------
AVAILABLE_COUNTRIES = {
    "usa": {
        "name": "🇺🇸 آمریکا",
        "description": "قدرت نظامی و اقتصادی برتر جهان",
        "starting_money": 800000,  # Reduced from 5B to 800K
        "income_methods": {
            "military_exports": {"name": "صادرات نظامی", "base_income": 180000, "multiplier": 1.5},  # Reduced from 25M to 180K
            "technology_sales": {"name": "فروش فناوری", "base_income": 120000, "multiplier": 2.0},  # Reduced from 15M to 120K
            "alliance_support": {"name": "حمایت اتحاد", "base_income": 80000, "multiplier": 1.3}  # Reduced from 10M to 80K
        },
        "bonus": "قدرت نظامی +20%"
    },
    "russia": {
        "name": "🇷🇺 روسیه",
        "description": "قدرت نظامی سنتی با منابع طبیعی فراوان",
        "starting_money": 650000,  # Reduced from 3B to 650K
        "income_methods": {
            "resource_exports": {"name": "صادرات منابع", "base_income": 220000, "multiplier": 1.4},  # Reduced from 30M to 220K
            "nuclear_technology": {"name": "فناوری هسته‌ای", "base_income": 150000, "multiplier": 1.8},  # Reduced from 20M to 150K
            "military_cooperation": {"name": "همکاری نظامی", "base_income": 95000, "multiplier": 1.2}  # Reduced from 12.5M to 95K
        },
        "bonus": "فناوری هسته‌ای +15%"
    },
    "china": {
        "name": "🇨🇳 چین",
        "description": "اقتصاد در حال رشد با نیروی انسانی عظیم",
        "starting_money": 720000,  # Reduced from 4B to 720K
        "income_methods": {
            "manufacturing": {"name": "تولید انبوه", "base_income": 250000, "multiplier": 1.6},  # Reduced from 35M to 250K
            "trade_routes": {"name": "مسیرهای تجاری", "base_income": 140000, "multiplier": 1.7},  # Reduced from 17.5M to 140K
            "infrastructure": {"name": "زیرساخت", "base_income": 110000, "multiplier": 1.4}  # Reduced from 15M to 110K
        },
        "bonus": "تولید +25%"
    },
    "iran": {
        "name": "🇮🇷 ایران",
        "description": "قدرت منطقه‌ای با منابع انرژی فراوان",
        "starting_money": 500000,  # Reduced from 2B to 500K
        "income_methods": {
            "oil_exports": {"name": "صادرات نفت", "base_income": 280000, "multiplier": 1.3},  # Reduced from 40M to 280K
            "regional_trade": {"name": "تجارت منطقه‌ای", "base_income": 160000, "multiplier": 1.5},  # Reduced from 20M to 160K
            "cultural_exports": {"name": "صادرات فرهنگی", "base_income": 70000, "multiplier": 1.2}  # Reduced from 10M to 70K
        },
        "bonus": "درآمد نفتی +30%"
    },
    "germany": {
        "name": "🇩🇪 آلمان",
        "description": "قدرت صنعتی و مهندسی پیشرفته",
        "starting_money": 680000,  # Reduced from 3.5B to 680K
        "income_methods": {
            "automotive_industry": {"name": "صنعت خودروسازی", "base_income": 210000, "multiplier": 1.7},  # Reduced from 30M to 210K
            "engineering_exports": {"name": "صادرات مهندسی", "base_income": 170000, "multiplier": 1.6},  # Reduced from 22.5M to 170K
            "research_grants": {"name": "کمک‌های تحقیقاتی", "base_income": 120000, "multiplier": 1.8}  # Reduced from 15M to 120K
        },
        "bonus": "تحقیق و توسعه +20%"
    },
    "japan": {
        "name": "🇯🇵 ژاپن",
        "description": "فناوری پیشرفته و اقتصاد دیجیتال",
        "starting_money": 720000,  # Reduced from 4B to 720K
        "income_methods": {
            "technology_exports": {"name": "صادرات فناوری", "base_income": 240000, "multiplier": 1.9},  # Reduced from 35M to 240K
            "digital_services": {"name": "خدمات دیجیتال", "base_income": 180000, "multiplier": 1.8},  # Reduced from 25M to 180K
            "innovation_grants": {"name": "کمک‌های نوآوری", "base_income": 150000, "multiplier": 2.0}  # Reduced from 20M to 150K
        },
        "bonus": "فناوری +25%"
    },
    "uk": {
        "name": "🇬🇧 بریتانیا",
        "description": "قدرت مالی و تجاری جهانی",
        "starting_money": 680000,  # Reduced from 3.5B to 680K
        "income_methods": {
            "financial_services": {"name": "خدمات مالی", "base_income": 280000, "multiplier": 1.6},  # Reduced from 40M to 280K
            "global_trade": {"name": "تجارت جهانی", "base_income": 190000, "multiplier": 1.5},  # Reduced from 25M to 190K
            "intelligence_sharing": {"name": "اشتراک اطلاعات", "base_income": 110000, "multiplier": 1.4}  # Reduced from 15M to 110K
        },
        "bonus": "درآمد مالی +20%"
    },
    "france": {
        "name": "🇫🇷 فرانسه",
        "description": "فرهنگ غنی و صنعت پیشرفته",
        "starting_money": 620000,  # Reduced from 3B to 620K
        "income_methods": {
            "luxury_goods": {"name": "کالاهای لوکس", "base_income": 210000, "multiplier": 1.8},  # Reduced from 30M to 210K
            "nuclear_energy": {"name": "انرژی هسته‌ای", "base_income": 180000, "multiplier": 1.6},  # Reduced from 25M to 180K
            "cultural_exports": {"name": "صادرات فرهنگی", "base_income": 140000, "multiplier": 1.5}  # Reduced from 20M to 140K
        },
        "bonus": "فرهنگ و هنر +25%"
    },
    "india": {
        "name": "🇮🇳 هند",
        "description": "اقتصاد در حال رشد با نیروی انسانی جوان",
        "starting_money": 450000,  # Reduced from 1.5B to 450K
        "income_methods": {
            "it_services": {"name": "خدمات آی‌تی", "base_income": 210000, "multiplier": 1.7},  # Reduced from 30M to 210K
            "agriculture": {"name": "کشاورزی", "base_income": 180000, "multiplier": 1.4},  # Reduced from 25M to 180K
            "pharmaceuticals": {"name": "داروسازی", "base_income": 140000, "multiplier": 1.6}  # Reduced from 20M to 140K
        },
        "bonus": "خدمات +20%"
    },
    "south_korea": {
        "name": "🇰🇷 کره جنوبی",
        "description": "فناوری پیشرفته و صنعت الکترونیک",
        "starting_money": 620000,  # Reduced from 3B to 620K
        "income_methods": {
            "electronics_exports": {"name": "صادرات الکترونیک", "base_income": 240000, "multiplier": 1.8},  # Reduced from 35M to 240K
            "entertainment": {"name": "سرگرمی", "base_income": 180000, "multiplier": 1.9},  # Reduced from 25M to 180K
            "automotive": {"name": "خودروسازی", "base_income": 150000, "multiplier": 1.6}  # Reduced from 20M to 150K
        },
        "bonus": "فناوری +30%"
    },
    "israel": {
        "name": "🇮🇱 اسرائیل",
        "description": "فناوری پیشرفته و امنیت سایبری",
        "starting_money": 520000,  # Reduced from 2B to 520K
        "income_methods": {
            "cybersecurity": {"name": "امنیت سایبری", "base_income": 280000, "multiplier": 2.0},  # Reduced from 40M to 280K
            "medical_technology": {"name": "فناوری پزشکی", "base_income": 210000, "multiplier": 1.8},  # Reduced from 30M to 210K
            "defense_exports": {"name": "صادرات دفاعی", "base_income": 180000, "multiplier": 1.7}  # Reduced from 25M to 180K
        },
        "bonus": "امنیت سایبری +25%"
    }
}

# -------------------- GAME DATA --------------------
MILITARY_ASSETS = {
    # ==================== INFANTRY UNITS ====================
    # Basic Infantry (No tech required)
    "militia": {"cost": 15000, "power": 1, "name": "شبه نظامی", "ability": "پایگاه", "tech_required": None, "country_restricted": None},
    "infantry": {"cost": 25000, "power": 2, "name": "پیاده نظام", "ability": "تحرک بالا", "tech_required": None, "country_restricted": None},
    "marines": {"cost": 60000, "power": 4, "name": "تفنگداران", "ability": "عملیات آبخاکی", "tech_required": None, "country_restricted": None},
    
    # Special Forces (Advanced Training Required)
    "navy_seal": {"cost": 300000, "power": 20, "name": "سیل نیروی دریایی", "ability": "عملیات ویژه", "tech_required": "advanced_training", "country_restricted": "usa"},
    "delta_force": {"cost": 450000, "power": 35, "name": "نیروی دلتا", "ability": "ضد تروریسم", "tech_required": "advanced_training", "country_restricted": "usa"},
    "spetsnaz": {"cost": 380000, "power": 32, "name": "اسپتسناز", "ability": "جنگ نامتقارن", "tech_required": "advanced_training", "country_restricted": "russia"},
    "sas": {"cost": 420000, "power": 38, "name": "اس‌ای‌اس", "ability": "عملیات مخفی", "tech_required": "advanced_training", "country_restricted": "uk"},
    "gsg9": {"cost": 400000, "power": 36, "name": "جی‌اس‌جی۹", "ability": "ضد تروریسم", "tech_required": "advanced_training", "country_restricted": "germany"},
    "707th_smb": {"cost": 410000, "power": 37, "name": "واحد ۷۰۷", "ability": "عملیات شهری", "tech_required": "advanced_training", "country_restricted": "south_korea"},
    "gign": {"cost": 390000, "power": 34, "name": "ژاندارمری ویژه", "ability": "مقابله تروریسم", "tech_required": "advanced_training", "country_restricted": "france"},
    "marcos": {"cost": 350000, "power": 30, "name": "مارکوس", "ability": "عملیات دریایی", "tech_required": "advanced_training", "country_restricted": "india"},
    "shayetet_13": {"cost": 480000, "power": 42, "name": "شایطت ۱۳", "ability": "عملیات زیرآبی", "tech_required": "advanced_training", "country_restricted": "israel"},
    "quds_force": {"cost": 320000, "power": 28, "name": "نیروی قدس", "ability": "عملیات منطقه‌ای", "tech_required": "advanced_training", "country_restricted": "iran"},
    "takavar": {"cost": 280000, "power": 25, "name": "تکاور", "ability": "عملیات ویژه", "tech_required": "advanced_training", "country_restricted": "iran"},

    # ==================== ARMORED UNITS ====================
    # Basic Armored (Military Engineering)
    "humvee": {"cost": 80000, "power": 5, "name": "هاموی", "ability": "تحرک سریع", "tech_required": "military_engineering", "country_restricted": None},
    "bradley": {"cost": 1800000, "power": 9, "name": "بردلی", "ability": "نقل زرهی", "tech_required": "military_engineering", "country_restricted": "usa"},
    "m1_abrams": {"cost": 2200000, "power": 12, "name": "ام۱ آبرامز", "ability": "زره مستحکم", "tech_required": "military_engineering", "country_restricted": "usa"},
    
    # Advanced Armored (Advanced Metallurgy)
    "t90": {"cost": 4200000, "power": 25, "name": "تی-۹۰", "ability": "شلیک حرکتی", "tech_required": "advanced_metallurgy", "country_restricted": "russia"},
    "t14_armata": {"cost": 6800000, "power": 45, "name": "تی-۱۴ آرماتا", "ability": "زره فعال", "tech_required": "advanced_metallurgy", "country_restricted": "russia"},
    "leopard_2": {"cost": 7200000, "power": 40, "name": "لئوپارد ۲", "ability": "توپ پیشرفته", "tech_required": "advanced_metallurgy", "country_restricted": "germany"},
    "challenger_2": {"cost": 6500000, "power": 38, "name": "چلنجر ۲", "ability": "زره چوبهام", "tech_required": "advanced_metallurgy", "country_restricted": "uk"},
    "leclerc": {"cost": 6200000, "power": 36, "name": "لکلرک", "ability": "سیستم آتش", "tech_required": "advanced_metallurgy", "country_restricted": "france"},
    "type_90": {"cost": 7500000, "power": 42, "name": "تایپ ۹۰", "ability": "فناوری ژاپنی", "tech_required": "advanced_metallurgy", "country_restricted": "japan"},
    "k2_black_panther": {"cost": 8200000, "power": 48, "name": "پلنگ سیاه", "ability": "سیستم C4I", "tech_required": "advanced_metallurgy", "country_restricted": "south_korea"},
    "arjun": {"cost": 5800000, "power": 32, "name": "ارجون", "ability": "زره کامپوزیت", "tech_required": "advanced_metallurgy", "country_restricted": "india"},
    "merkava": {"cost": 9200000, "power": 52, "name": "مرکاوا", "ability": "حفاظت جانبی", "tech_required": "advanced_metallurgy", "country_restricted": "israel"},
    "karrar": {"cost": 4800000, "power": 28, "name": "کرار", "ability": "تانک بومی", "tech_required": "advanced_metallurgy", "country_restricted": "iran"},
    "zulfiqar": {"cost": 3200000, "power": 22, "name": "ذوالفقار", "ability": "طراحی ایرانی", "tech_required": "military_engineering", "country_restricted": "iran"},

    # ==================== AIRCRAFT UNITS ====================
    # Basic Aircraft (Aerodynamics)
    "apache": {"cost": 2800000, "power": 18, "name": "آپاچی", "ability": "بالگرد تهاجمی", "tech_required": "aerodynamics", "country_restricted": "usa"},
    "f16": {"cost": 3200000, "power": 22, "name": "اف-۱۶", "ability": "جنگنده چندمنظوره", "tech_required": "aerodynamics", "country_restricted": "usa"},
    "a10": {"cost": 3800000, "power": 28, "name": "ای-۱۰", "ability": "نابودگر زمینی", "tech_required": "aerodynamics", "country_restricted": "usa"},
    "mi_24": {"cost": 2200000, "power": 15, "name": "می-۲۴", "ability": "بالگرد جنگی", "tech_required": "aerodynamics", "country_restricted": "russia"},
    "su_35": {"cost": 3600000, "power": 26, "name": "سوخو-۳۵", "ability": "مانور بالا", "tech_required": "aerodynamics", "country_restricted": "russia"},
    "eurofighter": {"cost": 4200000, "power": 32, "name": "یوروفایتر", "ability": "جنگنده اروپایی", "tech_required": "aerodynamics", "country_restricted": "germany"},
    "tornado": {"cost": 3400000, "power": 24, "name": "تورنادو", "ability": "حمله زمینی", "tech_required": "aerodynamics", "country_restricted": "uk"},
    "rafale": {"cost": 4000000, "power": 30, "name": "رافال", "ability": "چندمنظوره", "tech_required": "aerodynamics", "country_restricted": "france"},
    "f2": {"cost": 3800000, "power": 28, "name": "میتسوبیشی اف-۲", "ability": "دفاع جزیره", "tech_required": "aerodynamics", "country_restricted": "japan"},
    "kf21": {"cost": 4500000, "power": 35, "name": "کی‌اف-۲۱", "ability": "فایتر کره‌ای", "tech_required": "aerodynamics", "country_restricted": "south_korea"},
    "tejas": {"cost": 2800000, "power": 18, "name": "تجس", "ability": "جنگنده سبک", "tech_required": "aerodynamics", "country_restricted": "india"},
    "f15i": {"cost": 4800000, "power": 38, "name": "اف-۱۵ آی", "ability": "برد طولانی", "tech_required": "aerodynamics", "country_restricted": "israel"},
    "saeqeh": {"cost": 1800000, "power": 12, "name": "صاعقه", "ability": "جنگنده بومی", "tech_required": "aerodynamics", "country_restricted": "iran"},
    "kowsar": {"cost": 2400000, "power": 16, "name": "کوثر", "ability": "فناوری پیشرفته", "tech_required": "aerodynamics", "country_restricted": "iran"},
    
    # Stealth Aircraft (Stealth Technology)
    "f22_raptor": {"cost": 85000000, "power": 80, "name": "اف-۲۲ رپتور", "ability": "پنهانکاری", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "f35_lightning": {"cost": 120000000, "power": 95, "name": "اف-۳۵ لایتنینگ", "ability": "چندگانگی نقش", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "b2_spirit": {"cost": 180000000, "power": 140, "name": "بی-۲ اسپیریت", "ability": "بمب افکن استراتژیک", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "su_57": {"cost": 95000000, "power": 85, "name": "سوخو-۵۷", "ability": "پنهانکاری روسی", "tech_required": "stealth_technology", "country_restricted": "russia"},
    "j20": {"cost": 110000000, "power": 90, "name": "جی-۲۰", "ability": "اژدهای قدرتمند", "tech_required": "stealth_technology", "country_restricted": "china"},
    "kf21_stealth": {"cost": 125000000, "power": 98, "name": "کی‌اف-۲۱ پنهان", "ability": "پنهانکاری کره‌ای", "tech_required": "stealth_technology", "country_restricted": "south_korea"},
    
    # Future Aircraft (Quantum Computing)
    "aurora": {"cost": 400000000, "power": 250, "name": "اورورا", "ability": "فناوری آینده", "tech_required": "quantum_computing", "country_restricted": "usa"},
    "pak_da": {"cost": 380000000, "power": 240, "name": "پاک دا", "ability": "بمب افکن آینده", "tech_required": "quantum_computing", "country_restricted": "russia"},

    # ==================== NAVAL UNITS ====================
    # Basic Naval (Naval Engineering)
    "patrol_boat": {"cost": 120000, "power": 8, "name": "قایق گشتی", "ability": "گشت ساحلی", "tech_required": "naval_engineering", "country_restricted": None},
    "destroyer": {"cost": 5500000, "power": 35, "name": "ناوچه", "ability": "دفاع هوایی", "tech_required": "naval_engineering", "country_restricted": None},
    "cruiser": {"cost": 9200000, "power": 60, "name": "رزمناو", "ability": "فرماندهی ناوگان", "tech_required": "naval_engineering", "country_restricted": None},
    
    # Advanced Naval (Nuclear Technology)
    "virginia_sub": {"cost": 16000000, "power": 100, "name": "زیردریایی ویرجینیا", "ability": "پنهانکاری زیرآبی", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "nimitz_carrier": {"cost": 28000000, "power": 180, "name": "ناوگان نیمیتز", "ability": "پایگاه شناور", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "ohio_submarine": {"cost": 32000000, "power": 220, "name": "زیردریایی اوهایو", "ability": "موشک بالستیک", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "yasen_submarine": {"cost": 18000000, "power": 110, "name": "یاسن", "ability": "زیردریایی تهاجمی", "tech_required": "nuclear_technology", "country_restricted": "russia"},
    "kirov_cruiser": {"cost": 22000000, "power": 150, "name": "کیروف", "ability": "رزمناو هسته‌ای", "tech_required": "nuclear_technology", "country_restricted": "russia"},
    "type_055": {"cost": 15000000, "power": 95, "name": "تایپ ۰۵۵", "ability": "ناوچه پیشرفته", "tech_required": "nuclear_technology", "country_restricted": "china"},
    "queen_elizabeth": {"cost": 25000000, "power": 165, "name": "ملکه الیزابت", "ability": "ناوگان بریتانیا", "tech_required": "nuclear_technology", "country_restricted": "uk"},
    "charles_de_gaulle": {"cost": 24000000, "power": 160, "name": "شارل دوگل", "ability": "ناوگان فرانسه", "tech_required": "nuclear_technology", "country_restricted": "france"},
    "izumo": {"cost": 20000000, "power": 125, "name": "ایزومو", "ability": "ناو هلیکوپتری", "tech_required": "nuclear_technology", "country_restricted": "japan"},
    "dokdo": {"cost": 18000000, "power": 115, "name": "دوکدو", "ability": "ناو دوزیست", "tech_required": "nuclear_technology", "country_restricted": "south_korea"},
    "vikrant": {"cost": 14000000, "power": 85, "name": "ویکرانت", "ability": "ناوگان هند", "tech_required": "nuclear_technology", "country_restricted": "india"},
    "saar_6": {"cost": 12000000, "power": 75, "name": "ساعر ۶", "ability": "کشتی جنگی", "tech_required": "naval_engineering", "country_restricted": "israel"},
    "fateh_submarine": {"cost": 8000000, "power": 45, "name": "فاتح", "ability": "زیردریایی کوچک", "tech_required": "naval_engineering", "country_restricted": "iran"},
    "ghadir_submarine": {"cost": 4500000, "power": 25, "name": "غدیر", "ability": "زیردریایی ساحلی", "tech_required": "naval_engineering", "country_restricted": "iran"},

    # ==================== MISSILE UNITS ====================
    # Basic Missiles (Rocket Science)
    "stinger": {"cost": 95000, "power": 7, "name": "استینگر", "ability": "دفاع هوایی محمول", "tech_required": "rocket_science", "country_restricted": None},
    "hellfire": {"cost": 180000, "power": 15, "name": "هلفایر", "ability": "موشک ضد تانک", "tech_required": "rocket_science", "country_restricted": "usa"},
    "javelin": {"cost": 350000, "power": 28, "name": "جاولین", "ability": "ضد زره پیشرفته", "tech_required": "rocket_science", "country_restricted": "usa"},
    
    # Advanced Missiles (Ballistic Missiles)
    "tomahawk": {"cost": 1100000, "power": 75, "name": "توماهاوک", "ability": "برد طولانی", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "patriot": {"cost": 850000, "power": 55, "name": "پاتریوت", "ability": "دفاع موشکی", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "thaad": {"cost": 1400000, "power": 90, "name": "تاد", "ability": "دفاع بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "iskander": {"cost": 1200000, "power": 80, "name": "اسکندر", "ability": "موشک بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "russia"},
    "s400": {"cost": 1600000, "power": 95, "name": "اس-۴۰۰", "ability": "دفاع هوایی", "tech_required": "ballistic_missiles", "country_restricted": "russia"},
    "df21": {"cost": 1300000, "power": 85, "name": "دی‌اف-۲۱", "ability": "کشتی کش", "tech_required": "ballistic_missiles", "country_restricted": "china"},
    "storm_shadow": {"cost": 950000, "power": 65, "name": "طوفان سایه", "ability": "کروز بریتانیا", "tech_required": "ballistic_missiles", "country_restricted": "uk"},
    "scalp": {"cost": 920000, "power": 62, "name": "اسکالپ", "ability": "کروز فرانسه", "tech_required": "ballistic_missiles", "country_restricted": "france"},
    "type_12": {"cost": 1100000, "power": 72, "name": "تایپ ۱۲", "ability": "موشک ضد کشتی", "tech_required": "ballistic_missiles", "country_restricted": "japan"},
    "hyunmoo": {"cost": 1250000, "power": 78, "name": "هیونمو", "ability": "موشک بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "south_korea"},
    "brahmos": {"cost": 1050000, "power": 70, "name": "براهموس", "ability": "سوپرسونیک", "tech_required": "ballistic_missiles", "country_restricted": "india"},
    "iron_dome": {"cost": 1800000, "power": 100, "name": "گنبد آهنین", "ability": "دفاع موشکی", "tech_required": "ballistic_missiles", "country_restricted": "israel"},
    "david_sling": {"cost": 2200000, "power": 120, "name": "فلاخن داوود", "ability": "دفاع متوسط", "tech_required": "ballistic_missiles", "country_restricted": "israel"},
    "sejjil": {"cost": 800000, "power": 45, "name": "سجیل", "ability": "موشک بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    "emad": {"cost": 950000, "power": 55, "name": "عماد", "ability": "موشک دقیق", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    "khorramshahr": {"cost": 1200000, "power": 75, "name": "خرمشهر", "ability": "برد متوسط", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    
    # Nuclear Weapons (Nuclear Weapons Tech)
    "minuteman": {"cost": 55000000, "power": 500, "name": "مینوت من", "ability": "موشک هسته ای", "tech_required": "nuclear_weapons", "country_restricted": "usa"},
    "trident": {"cost": 82000000, "power": 750, "name": "ترایدنت", "ability": "موشک قاره پیما", "tech_required": "nuclear_weapons", "country_restricted": "usa"},
    "topol_m": {"cost": 65000000, "power": 600, "name": "توپول-ام", "ability": "موشک قاره‌پیما", "tech_required": "nuclear_weapons", "country_restricted": "russia"},
    "sarmat": {"cost": 95000000, "power": 850, "name": "سارمات", "ability": "ابرموشک", "tech_required": "nuclear_weapons", "country_restricted": "russia"},

    # ==================== ARTILLERY UNITS ====================
    # Artillery (Advanced Materials)
    "m777_howitzer": {"cost": 680000, "power": 45, "name": "ام۷۷۷ هویتزر", "ability": "آتش پشتیبانی", "tech_required": "advanced_materials", "country_restricted": "usa"},
    "himars": {"cost": 950000, "power": 65, "name": "هایمارس", "ability": "راکت انداز", "tech_required": "advanced_materials", "country_restricted": "usa"},
    "paladin": {"cost": 780000, "power": 50, "name": "پالادین", "ability": "خودکششی", "tech_required": "advanced_materials", "country_restricted": "usa"},
    "grad": {"cost": 420000, "power": 32, "name": "گراد", "ability": "راکت انداز", "tech_required": "advanced_materials", "country_restricted": "russia"},
    "tos1": {"cost": 680000, "power": 48, "name": "تی‌او‌اس-۱", "ability": "آتش‌افکن سنگین", "tech_required": "advanced_materials", "country_restricted": "russia"},
    "pzh2000": {"cost": 850000, "power": 58, "name": "پی‌زت‌اچ۲۰۰۰", "ability": "خودکار آلمانی", "tech_required": "advanced_materials", "country_restricted": "germany"},
    "as90": {"cost": 720000, "power": 52, "name": "ای‌اس۹۰", "ability": "توپ بریتانیا", "tech_required": "advanced_materials", "country_restricted": "uk"},
    "caesar": {"cost": 650000, "power": 48, "name": "سزار", "ability": "توپ چرخدار", "tech_required": "advanced_materials", "country_restricted": "france"},
    "type_99": {"cost": 620000, "power": 46, "name": "تایپ ۹۹", "ability": "خودکار ژاپنی", "tech_required": "advanced_materials", "country_restricted": "japan"},
    "k9_thunder": {"cost": 780000, "power": 54, "name": "رعد کی۹", "ability": "توپ کره‌ای", "tech_required": "advanced_materials", "country_restricted": "south_korea"},
    "pinaka": {"cost": 480000, "power": 38, "name": "پیناکا", "ability": "راکت انداز هند", "tech_required": "advanced_materials", "country_restricted": "india"},
    "atmos": {"cost": 720000, "power": 50, "name": "اتموس", "ability": "توپ اسرائیل", "tech_required": "advanced_materials", "country_restricted": "israel"},
    "raad": {"cost": 380000, "power": 28, "name": "رعد", "ability": "راکت انداز", "tech_required": "advanced_materials", "country_restricted": "iran"},
    "fajr": {"cost": 280000, "power": 22, "name": "فجر", "ability": "راکت انداز", "tech_required": "military_engineering", "country_restricted": "iran"},

    # ==================== ADVANCED TECHNOLOGY UNITS ====================
    # Future Technology (Quantum Computing)
    "laser_defense": {"cost": 48000000, "power": 400, "name": "سیستم لیزری", "ability": "شعاع انرژی", "tech_required": "quantum_computing", "country_restricted": "usa"},
    "rail_gun": {"cost": 68000000, "power": 600, "name": "توپ ریلی", "ability": "سرعت نور", "tech_required": "quantum_computing", "country_restricted": "usa"},
    "cyber_unit": {"cost": 22000000, "power": 150, "name": "واحد سایبری", "ability": "جنگ الکترونیک", "tech_required": "quantum_computing", "country_restricted": None},
    "ai_system": {"cost": 32000000, "power": 200, "name": "سیستم هوش مصنوعی", "ability": "تحلیل پیشرفته", "tech_required": "quantum_computing", "country_restricted": None},
    "quantum_radar": {"cost": 45000000, "power": 350, "name": "رادار کوانتومی", "ability": "تشخیص پنهان", "tech_required": "quantum_computing", "country_restricted": "china"},
    "hypersonic_glider": {"cost": 75000000, "power": 650, "name": "گلایدر مافوق صوت", "ability": "سرعت بالا", "tech_required": "quantum_computing", "country_restricted": "russia"},
    "plasma_cannon": {"cost": 85000000, "power": 700, "name": "توپ پلاسما", "ability": "انرژی خالص", "tech_required": "quantum_computing", "country_restricted": "germany"},
    "nano_swarm": {"cost": 65000000, "power": 550, "name": "ازدحام نانو", "ability": "روبات‌های کوچک", "tech_required": "quantum_computing", "country_restricted": "japan"},
    "emp_weapon": {"cost": 42000000, "power": 320, "name": "سلاح ای‌ام‌پی", "ability": "خاموش کردن", "tech_required": "quantum_computing", "country_restricted": "south_korea"},
    "drone_swarm": {"cost": 38000000, "power": 280, "name": "ازدحام پهپاد", "ability": "حمله گروهی", "tech_required": "quantum_computing", "country_restricted": "israel"},
    "shahed_136": {"cost": 25000, "power": 8, "name": "شاهد ۱۳۶", "ability": "پهپاد انتحاری", "tech_required": "rocket_science", "country_restricted": "iran"},
    "mohajer": {"cost": 180000, "power": 12, "name": "مهاجر", "ability": "پهپاد نظارت", "tech_required": "aerodynamics", "country_restricted": "iran"}
}

TECH_TREE = {
    "military_engineering": {"name": "مهندسی نظامی", "cost": 1200000, "required_level": 2, "prerequisites": []},  # Reduced from 50M to 1.2M
    "aerodynamics": {"name": "آیرودینامیک", "cost": 1800000, "required_level": 4, "prerequisites": []},  # Reduced from 80M to 1.8M
    "naval_engineering": {"name": "مهندسی دریایی", "cost": 1500000, "required_level": 3, "prerequisites": []},  # Reduced from 70M to 1.5M
    "rocket_science": {"name": "علم موشکی", "cost": 2200000, "required_level": 5, "prerequisites": ["military_engineering"]},  # Reduced from 100M to 2.2M
    "advanced_metallurgy": {"name": "متالوژی پیشرفته", "cost": 2800000, "required_level": 6, "prerequisites": ["military_engineering"]},  # Reduced from 120M to 2.8M
    "stealth_technology": {"name": "فناوری پنهانکاری", "cost": 3500000, "required_level": 8, "prerequisites": ["aerodynamics", "advanced_metallurgy"]},  # Reduced from 150M to 3.5M
    "nuclear_technology": {"name": "فناوری هسته ای", "cost": 4500000, "required_level": 10, "prerequisites": ["rocket_science", "advanced_metallurgy"]},  # Reduced from 200M to 4.5M
    "ballistic_missiles": {"name": "موشک های بالستیک", "cost": 4200000, "required_level": 12, "prerequisites": ["rocket_science", "nuclear_technology"]},  # Reduced from 180M to 4.2M
    "advanced_training": {"name": "آموزش پیشرفته", "cost": 3000000, "required_level": 7, "prerequisites": ["military_engineering"]},  # Reduced from 130M to 3M
    "advanced_materials": {"name": "مواد پیشرفته", "cost": 3800000, "required_level": 9, "prerequisites": ["advanced_metallurgy", "rocket_science"]},  # Reduced from 160M to 3.8M
    "quantum_computing": {"name": "محاسبات کوانتومی", "cost": 6800000, "required_level": 15, "prerequisites": ["nuclear_technology", "stealth_technology"]},  # Reduced from 300M to 6.8M
    "nuclear_weapons": {"name": "تسلیحات هسته ای", "cost": 12000000, "required_level": 18, "prerequisites": ["nuclear_technology", "ballistic_missiles", "quantum_computing"]},  # Reduced from 500M to 12M
}

DAILY_MISSIONS = [
    {"id": "messages", "name": "پیام رسان", "desc": "۱۰ پیام", "target": 10, "points": 80000, "exp": 50},  # Reduced from 1M to 80K
    {"id": "purchases", "name": "خریدار", "desc": "۵ خرید", "target": 5, "points": 120000, "exp": 75},  # Reduced from 1.5M to 120K
    {"id": "battles", "name": "جنگجو", "desc": "۳ برد", "target": 3, "points": 160000, "exp": 100},  # Reduced from 2M to 160K
    {"id": "power", "name": "قدرت", "desc": "قدرت ۵۰۰", "target": 500, "points": 250000, "exp": 150},  # Reduced from 3M to 250K
]

BASE_POINTS_PER_MESSAGE = 3500  # Reduced from 50K to 3.5K per message
DAILY_PURCHASE_LIMIT = 50
COOLDOWN_MINUTES = 0.2
EXP_PER_MESSAGE = 8
LEVEL_REQUIREMENTS = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500, 6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000, 21000, 23500, 26000, 29000, 32500]

group_data = {}

# Global user data storage
global_user_data = {}

def load_data():
    global group_data, global_user_data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            group_data = json.load(f)
    except:
        group_data = {}
    
    # Load global user data
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            global_user_data = json.load(f)
    except:
        global_user_data = {}

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(group_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving group data: {e}")
    
    # Save global user data
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(global_user_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving user data: {e}")

def get_chat_data(chat_id):
    chat_id_str = str(chat_id)
    if chat_id_str not in group_data:
        group_data[chat_id_str] = {
            "owner_id": None, "warnings": {}, "muted_users": {}, "rules": "قوانین تنظیم نشده",
            "welcome_message": "خوش آمدید", "admins": [], "users": {}, "alliances": {},
            "daily_missions": {}, "last_mission_reset": datetime.now().date().isoformat()
        }
    return group_data[chat_id_str]

def get_global_user_data(user_id):
    """Get global user data that persists across all groups"""
    user_id_str = str(user_id)
    if user_id_str not in global_user_data:
        global_user_data[user_id_str] = {
            "country": None, "country_selected": False, "points": 0, "experience": 0, "level": 1, "last_message_time": 0,
            "military": {asset: 0 for asset in MILITARY_ASSETS}, "technologies": [],
            "battles_won": 0, "battles_lost": 0, "alliance": None,
            "daily_purchases": 0, "last_purchase_date": None, "daily_missions": {},
            "missions_completed_today": 0, "last_mission_date": None,
            "total_messages": 0, "last_activity": datetime.now().isoformat(),
            "last_income_time": 0, "income_cooldown": 3600  # 1 hour cooldown for income
        }
    
    user_data = global_user_data[user_id_str]
    today = datetime.now().date().isoformat()
    
    # Reset daily limits if it's a new day
    if user_data.get("last_purchase_date") != today:
        user_data["daily_purchases"] = 0
        user_data["last_purchase_date"] = today
    if user_data.get("last_mission_date") != today:
        user_data["daily_missions"] = {}
        user_data["missions_completed_today"] = 0
        user_data["last_mission_date"] = today
    
    # Update last activity
    user_data["last_activity"] = datetime.now().isoformat()
    
    return user_data

def get_user_data(chat_id, user_id):
    """Get user data for a specific chat (for chat-specific features like warnings)"""
    chat_data = get_chat_data(chat_id)
    user_id_str = str(user_id)
    if user_id_str not in chat_data["users"]:
        chat_data["users"][user_id_str] = {
            "warnings": [], "chat_specific_data": {}
        }
    return chat_data["users"][user_id_str]

def calculate_total_power(user_data):
    total_power = sum(MILITARY_ASSETS[asset]["power"] * count for asset, count in user_data["military"].items() if count > 0)
    level_bonus = 1 + (user_data.get("level", 1) * 0.03)
    return int(total_power * level_bonus)

def can_buy_asset(user_data, asset_type):
    asset = MILITARY_ASSETS.get(asset_type)
    if not asset: return False, "تجهیز نامعتبر"
    
    # Check country restriction
    country_restricted = asset.get("country_restricted")
    if country_restricted and user_data.get("country") != country_restricted:
        country_name = AVAILABLE_COUNTRIES[country_restricted]["name"] if country_restricted in AVAILABLE_COUNTRIES else country_restricted
        return False, f"فقط برای {country_name}"
    
    # Check technology requirement
    tech_required = asset.get("tech_required")
    if tech_required and tech_required not in user_data["technologies"]:
        return False, f"نیاز به: {TECH_TREE[tech_required]['name']}"
    
    return True, ""

def can_research_tech(user_data, tech_id):
    if tech_id not in TECH_TREE: return False, "فناوری نامعتبر"
    tech = TECH_TREE[tech_id]
    if user_data.get("level", 1) < tech["required_level"]: return False, f"نیاز سطح {tech['required_level']}"
    if tech_id in user_data["technologies"]: return False, "تحقیق شده"
    for prereq in tech["prerequisites"]:
        if prereq not in user_data["technologies"]: return False, f"نیاز: {TECH_TREE[prereq]['name']}"
    return True, ""

def calculate_level(experience):
    for level, exp_required in enumerate(LEVEL_REQUIREMENTS):
        if experience < exp_required: return level
    return len(LEVEL_REQUIREMENTS)

def check_level_up(user_data):
    current_level = user_data.get("level", 1)
    new_level = calculate_level(user_data["experience"])
    if new_level > current_level:
        user_data["level"] = new_level
        return new_level
    return None

def generate_daily_missions(chat_id):
    chat_data = get_chat_data(chat_id)
    today = datetime.now().date().isoformat()
    if chat_data.get("last_mission_reset") != today:
        selected = random.sample(DAILY_MISSIONS, 3)
        chat_data["daily_missions"] = {m["id"]: {**m, "completed_by": []} for m in selected}
        chat_data["last_mission_reset"] = today
        save_data()

def check_mission_progress(user_data, chat_data, mission_type, value=1, user_id=None):
    completed = []
    for mid, mission in chat_data["daily_missions"].items():
        if mission["id"] == mission_type and str(user_id) not in mission["completed_by"]:
            if mid not in user_data["daily_missions"]: user_data["daily_missions"][mid] = 0
            if mission_type == "power":
                user_data["daily_missions"][mid] = calculate_total_power(user_data)
            else:
                user_data["daily_missions"][mid] += value
            if user_data["daily_missions"][mid] >= mission["target"]:
                mission["completed_by"].append(str(user_id))
                user_data["points"] += mission["points"]
                user_data["experience"] += mission["exp"]
                completed.append(mission["name"])
    return completed

# Import the handlers from the separate file
exec(open('/workspace/bot_handlers.py').read())

async def show_available_countries(message):
    """Show list of available countries with their descriptions"""
    try:
        text = "🌍 **کشورهای موجود برای انتخاب:**\n\n"
        
        for country_code, country_data in AVAILABLE_COUNTRIES.items():
            text += f"**{country_data['name']}**\n"
            text += f"📝 {country_data['description']}\n"
            text += f"💰 پول شروع: ${country_data['starting_money']:,}\n"
            text += f"🎯 {country_data['bonus']}\n"
            text += f"💼 روش‌های درآمد:\n"
            
            for method_id, method_data in country_data['income_methods'].items():
                text += f"  • {method_data['name']}: ${method_data['base_income']:,} (ضریب: {method_data['multiplier']}x)\n"
            
            text += f"🔑 کد: `{country_code}`\n\n"
        
        text += "**برای انتخاب کشور:**\n/select_country [کد کشور]\n\n"
        text += "**مثال:**\n/select_country usa\n/select_country iran\n/select_country germany"
        
        # Split message if too long
        if len(text) > 4000:
            parts = text.split("\n\n")
            current_part = ""
            
            for part in parts:
                if len(current_part + part) > 3500:
                    await message.reply(current_part)
                    await asyncio.sleep(1)
                    current_part = part + "\n\n"
                else:
                    current_part += part + "\n\n"
            
            if current_part.strip():
                await message.reply(current_part)
        else:
            await message.reply(text)
            
    except Exception as e:
        print(f"Countries display error: {e}")
        await message.reply("⚠️ خطا در نمایش کشورها!")

async def select_country(message, chat_id, user_id):
    """Allow user to select a country"""
    try:
        parts = message.content.split()
        if len(parts) < 2:
            await message.reply("⚠️ /select_country [کد کشور]\n\nمثال:\n/select_country usa\n/select_country iran\n\nبرای مشاهده کشورها: /countries")
            return
        
        country_code = parts[1].lower()
        user_data = get_global_user_data(user_id)
        
        # Check if user already selected a country
        if user_data.get("country_selected", False):
            current_country = user_data.get("country", "نامشخص")
            current_country_name = AVAILABLE_COUNTRIES.get(current_country, {}).get("name", current_country)
            await message.reply(f"⚠️ شما قبلاً کشور {current_country_name} را انتخاب کرده‌اید!\n\nبرای تغییر کشور، ابتدا باید از کشور فعلی خارج شوید.")
            return
        
        # Check if country exists
        if country_code not in AVAILABLE_COUNTRIES:
            await message.reply(f"⚠️ کشور '{country_code}' وجود ندارد!\n\nبرای مشاهده کشورهای موجود: /countries")
            return
        
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        # Set user's country
        user_data["country"] = country_code
        user_data["country_selected"] = True
        user_data["points"] = country_data["starting_money"]
        
        # Save data
        save_data()
        
        # Send confirmation message
        welcome_text = f"🎉 **خوش آمدید به {country_data['name']}!**\n\n"
        welcome_text += f"📝 {country_data['description']}\n"
        welcome_text += f"💰 پول شروع: ${country_data['starting_money']:,}\n"
        welcome_text += f"🎯 {country_data['bonus']}\n\n"
        welcome_text += f"💼 **روش‌های درآمد شما:**\n"
        
        for method_id, method_data in country_data['income_methods'].items():
            welcome_text += f"• {method_data['name']}: ${method_data['base_income']:,} (ضریب: {method_data['multiplier']}x)\n"
        
        welcome_text += f"\n🔄 **برای جمع‌آوری درآمد:**\n/income\n\n"
        welcome_text += f"📊 **برای مشاهده اقتصاد:**\n/economy\n\n"
        welcome_text += f"🎮 **حالا می‌توانید بازی کنید!**\n"
        welcome_text += f"• خرید تجهیزات: /buy [نوع] [تعداد]\n"
        welcome_text += f"• تحقیق فناوری: /research [tech_id]\n"
        welcome_text += f"• حمله: /attack [ریپلای]\n\n"
        welcome_text += f"⏰ **نکته مهم**: با تنظیمات جدید اقتصادی، رسیدن به اهداف بالا حدود ۱۳-۱۵ روز زمان خواهد برد."
        
        await message.reply(welcome_text)
        
    except Exception as e:
        print(f"Country selection error: {e}")
        await message.reply("⚠️ خطا در انتخاب کشور!")

async def collect_income(message, chat_id, user_id):
    """Collect income from country's economic activities"""
    try:
        user_data = get_global_user_data(user_id)
        
        # Check if user has selected a country
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        current_time = time.time()
        country_code = user_data["country"]
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        # Check cooldown
        if current_time - user_data.get("last_income_time", 0) < user_data.get("income_cooldown", 3600):
            remaining_time = int(user_data.get("income_cooldown", 3600) - (current_time - user_data.get("last_income_time", 0)))
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            await message.reply(f"⏳ باید {minutes} دقیقه و {seconds} ثانیه صبر کنید تا بتوانید دوباره درآمد جمع‌آوری کنید!")
            return
        
        # Calculate income from all methods
        total_income = 0
        income_details = []
        
        for method_id, method_data in country_data['income_methods'].items():
            base_income = method_data['base_income']
            multiplier = method_data['multiplier']
            
            # Apply level bonus
            level_bonus = 1 + (user_data.get("level", 1) * 0.02)
            
            # Apply technology bonus
            tech_bonus = 1 + (len(user_data.get("technologies", [])) * 0.05)
            
            # Calculate final income for this method
            method_income = int(base_income * multiplier * level_bonus * tech_bonus)
            total_income += method_income
            
            income_details.append(f"• {method_data['name']}: ${method_income:,}")
        
        # Add income to user's points
        user_data["points"] += total_income
        user_data["last_income_time"] = current_time
        user_data["experience"] += total_income // 20  # Some experience for collecting income
        
        # Save data
        save_data()
        
        # Send income report
        income_text = f"💰 **درآمد جمع‌آوری شد!**\n\n"
        income_text += f"🏛️ کشور: {country_data['name']}\n"
        income_text += f"📊 جزئیات درآمد:\n"
        income_text += "\n".join(income_details)
        income_text += f"\n\n💵 **کل درآمد:** ${total_income:,}\n"
        income_text += f"💎 **موجودی جدید:** ${user_data['points']:,}\n"
        income_text += f"⭐ **تجربه کسب شده:** {total_income // 20}\n\n"
        income_text += f"🔄 **دفعه بعد:** {user_data.get('income_cooldown', 3600) // 60} دقیقه دیگر"
        
        await message.reply(income_text)
        
    except Exception as e:
        print(f"Income collection error: {e}")
        await message.reply("⚠️ خطا در جمع‌آوری درآمد!")

async def show_economy_info(message, chat_id, user_id):
    """Show detailed economy information for user's country"""
    try:
        user_data = get_global_user_data(user_id)
        
        # Check if user has selected a country
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        country_code = user_data["country"]
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        # Calculate current income potential
        current_income = 0
        income_breakdown = []
        
        for method_id, method_data in country_data['income_methods'].items():
            base_income = method_data['base_income']
            multiplier = method_data['multiplier']
            
            # Apply bonuses
            level_bonus = 1 + (user_data.get("level", 1) * 0.02)
            tech_bonus = 1 + (len(user_data.get("technologies", [])) * 0.05)
            
            method_income = int(base_income * multiplier * level_bonus * tech_bonus)
            current_income += method_income
            
            income_breakdown.append(f"• {method_data['name']}: ${method_income:,}")
        
        # Check income cooldown
        current_time = time.time()
        last_income = user_data.get("last_income_time", 0)
        cooldown = user_data.get("income_cooldown", 3600)
        
        if current_time - last_income < cooldown:
            remaining = int(cooldown - (current_time - last_income))
            minutes = remaining // 60
            seconds = remaining % 60
            cooldown_status = f"⏳ {minutes} دقیقه و {seconds} ثانیه باقی"
        else:
            cooldown_status = "✅ آماده برای جمع‌آوری"
        
        # Economy report
        economy_text = f"🏛️ **اقتصاد {country_data['name']}**\n\n"
        economy_text += f"📝 {country_data['description']}\n"
        economy_text += f"🎯 {country_data['bonus']}\n\n"
        economy_text += f"💰 **درآمد فعلی (هر ساعت):**\n"
        economy_text += "\n".join(income_breakdown)
        economy_text += f"\n\n💵 **کل درآمد:** ${current_income:,}\n"
        economy_text += f"🔄 **وضعیت جمع‌آوری:** {cooldown_status}\n\n"
        economy_text += f"📊 **آمار اقتصادی:**\n"
        economy_text += f"• سطح: {user_data.get('level', 1)} (بونوس: +{user_data.get('level', 1) * 2}%)\n"
        economy_text += f"• فناوری: {len(user_data.get('technologies', []))} (بونوس: +{len(user_data.get('technologies', [])) * 5}%)\n"
        economy_text += f"• موجودی: ${user_data['points']:,}\n\n"
        economy_text += f"🛒 **برای جمع‌آوری درآمد:**\n/income"
        
        await message.reply(economy_text)
        
    except Exception as e:
        print(f"Economy info error: {e}")
        await message.reply("⚠️ خطا در نمایش اطلاعات اقتصادی!")

# -------------------- RUN BOT --------------------
if __name__ == "__main__":
    print("🚀 Starting bot...")
    load_data()
    bot.run()