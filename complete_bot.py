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
USER_DATA_FILE = "global_user_data.json"
bot = Bot(token=TOKEN)

# -------------------- COUNTRIES AND ECONOMICS --------------------
AVAILABLE_COUNTRIES = {
    "usa": {
        "name": "🇺🇸 آمریکا",
        "description": "قدرت نظامی و اقتصادی برتر جهان",
        "starting_money": 800000,
        "income_methods": {
            "military_exports": {"name": "صادرات نظامی", "base_income": 180000, "multiplier": 1.5},
            "technology_sales": {"name": "فروش فناوری", "base_income": 120000, "multiplier": 2.0},
            "alliance_support": {"name": "حمایت اتحاد", "base_income": 80000, "multiplier": 1.3}
        },
        "bonus": "قدرت نظامی +20%"
    },
    "russia": {
        "name": "🇷🇺 روسیه",
        "description": "قدرت نظامی سنتی با منابع طبیعی فراوان",
        "starting_money": 650000,
        "income_methods": {
            "resource_exports": {"name": "صادرات منابع", "base_income": 220000, "multiplier": 1.4},
            "nuclear_technology": {"name": "فناوری هسته‌ای", "base_income": 150000, "multiplier": 1.8},
            "military_cooperation": {"name": "همکاری نظامی", "base_income": 95000, "multiplier": 1.2}
        },
        "bonus": "فناوری هسته‌ای +15%"
    },
    "china": {
        "name": "🇨🇳 چین",
        "description": "اقتصاد در حال رشد با نیروی انسانی عظیم",
        "starting_money": 720000,
        "income_methods": {
            "manufacturing": {"name": "تولید انبوه", "base_income": 250000, "multiplier": 1.6},
            "trade_routes": {"name": "مسیرهای تجاری", "base_income": 140000, "multiplier": 1.7},
            "infrastructure": {"name": "زیرساخت", "base_income": 110000, "multiplier": 1.4}
        },
        "bonus": "تولید +25%"
    },
    "iran": {
        "name": "🇮🇷 ایران",
        "description": "قدرت منطقه‌ای با منابع انرژی فراوان",
        "starting_money": 500000,
        "income_methods": {
            "oil_exports": {"name": "صادرات نفت", "base_income": 280000, "multiplier": 1.3},
            "regional_trade": {"name": "تجارت منطقه‌ای", "base_income": 160000, "multiplier": 1.5},
            "cultural_exports": {"name": "صادرات فرهنگی", "base_income": 70000, "multiplier": 1.2}
        },
        "bonus": "درآمد نفتی +30%"
    },
    "germany": {
        "name": "🇩🇪 آلمان",
        "description": "قدرت صنعتی و مهندسی پیشرفته",
        "starting_money": 680000,
        "income_methods": {
            "automotive_industry": {"name": "صنعت خودروسازی", "base_income": 210000, "multiplier": 1.7},
            "engineering_exports": {"name": "صادرات مهندسی", "base_income": 170000, "multiplier": 1.6},
            "research_grants": {"name": "کمک‌های تحقیقاتی", "base_income": 120000, "multiplier": 1.8}
        },
        "bonus": "تحقیق و توسعه +20%"
    },
    "japan": {
        "name": "🇯🇵 ژاپن",
        "description": "فناوری پیشرفته و اقتصاد دیجیتال",
        "starting_money": 720000,
        "income_methods": {
            "technology_exports": {"name": "صادرات فناوری", "base_income": 240000, "multiplier": 1.9},
            "digital_services": {"name": "خدمات دیجیتال", "base_income": 180000, "multiplier": 1.8},
            "innovation_grants": {"name": "کمک‌های نوآوری", "base_income": 150000, "multiplier": 2.0}
        },
        "bonus": "فناوری +25%"
    },
    "uk": {
        "name": "🇬🇧 بریتانیا",
        "description": "قدرت مالی و تجاری جهانی",
        "starting_money": 680000,
        "income_methods": {
            "financial_services": {"name": "خدمات مالی", "base_income": 280000, "multiplier": 1.6},
            "global_trade": {"name": "تجارت جهانی", "base_income": 190000, "multiplier": 1.5},
            "intelligence_sharing": {"name": "اشتراک اطلاعات", "base_income": 110000, "multiplier": 1.4}
        },
        "bonus": "درآمد مالی +20%"
    },
    "france": {
        "name": "🇫🇷 فرانسه",
        "description": "فرهنگ غنی و صنعت پیشرفته",
        "starting_money": 620000,
        "income_methods": {
            "luxury_goods": {"name": "کالاهای لوکس", "base_income": 210000, "multiplier": 1.8},
            "nuclear_energy": {"name": "انرژی هسته‌ای", "base_income": 180000, "multiplier": 1.6},
            "cultural_exports": {"name": "صادرات فرهنگی", "base_income": 140000, "multiplier": 1.5}
        },
        "bonus": "فرهنگ و هنر +25%"
    },
    "india": {
        "name": "🇮🇳 هند",
        "description": "اقتصاد در حال رشد با نیروی انسانی جوان",
        "starting_money": 450000,
        "income_methods": {
            "it_services": {"name": "خدمات آی‌تی", "base_income": 210000, "multiplier": 1.7},
            "agriculture": {"name": "کشاورزی", "base_income": 180000, "multiplier": 1.4},
            "pharmaceuticals": {"name": "داروسازی", "base_income": 140000, "multiplier": 1.6}
        },
        "bonus": "خدمات +20%"
    },
    "south_korea": {
        "name": "🇰🇷 کره جنوبی",
        "description": "فناوری پیشرفته و صنعت الکترونیک",
        "starting_money": 620000,
        "income_methods": {
            "electronics_exports": {"name": "صادرات الکترونیک", "base_income": 240000, "multiplier": 1.8},
            "entertainment": {"name": "سرگرمی", "base_income": 180000, "multiplier": 1.9},
            "automotive": {"name": "خودروسازی", "base_income": 150000, "multiplier": 1.6}
        },
        "bonus": "فناوری +30%"
    },
    "israel": {
        "name": "🇮🇱 اسرائیل",
        "description": "فناوری پیشرفته و امنیت سایبری",
        "starting_money": 520000,
        "income_methods": {
            "cybersecurity": {"name": "امنیت سایبری", "base_income": 280000, "multiplier": 2.0},
            "medical_technology": {"name": "فناوری پزشکی", "base_income": 210000, "multiplier": 1.8},
            "defense_exports": {"name": "صادرات دفاعی", "base_income": 180000, "multiplier": 1.7}
        },
        "bonus": "امنیت سایبری +25%"
    }
}

# -------------------- MILITARY ASSETS --------------------
MILITARY_ASSETS = {
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

    # Armored Units
    "humvee": {"cost": 80000, "power": 5, "name": "هاموی", "ability": "تحرک سریع", "tech_required": "military_engineering", "country_restricted": None},
    "bradley": {"cost": 1800000, "power": 9, "name": "بردلی", "ability": "نقل زرهی", "tech_required": "military_engineering", "country_restricted": "usa"},
    "m1_abrams": {"cost": 2200000, "power": 12, "name": "ام۱ آبرامز", "ability": "زره مستحکم", "tech_required": "military_engineering", "country_restricted": "usa"},
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

    # Aircraft
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
    
    # Stealth Aircraft
    "f22_raptor": {"cost": 85000000, "power": 80, "name": "اف-۲۲ رپتور", "ability": "پنهانکاری", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "f35_lightning": {"cost": 120000000, "power": 95, "name": "اف-۳۵ لایتنینگ", "ability": "چندگانگی نقش", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "b2_spirit": {"cost": 180000000, "power": 140, "name": "بی-۲ اسپیریت", "ability": "بمب افکن استراتژیک", "tech_required": "stealth_technology", "country_restricted": "usa"},
    "su_57": {"cost": 95000000, "power": 85, "name": "سوخو-۵۷", "ability": "پنهانکاری روسی", "tech_required": "stealth_technology", "country_restricted": "russia"},
    "j20": {"cost": 110000000, "power": 90, "name": "جی-۲۰", "ability": "اژدهای قدرتمند", "tech_required": "stealth_technology", "country_restricted": "china"},
    
    # Naval Units
    "patrol_boat": {"cost": 120000, "power": 8, "name": "قایق گشتی", "ability": "گشت ساحلی", "tech_required": "naval_engineering", "country_restricted": None},
    "destroyer": {"cost": 5500000, "power": 35, "name": "ناوچه", "ability": "دفاع هوایی", "tech_required": "naval_engineering", "country_restricted": None},
    "cruiser": {"cost": 9200000, "power": 60, "name": "رزمناو", "ability": "فرماندهی ناوگان", "tech_required": "naval_engineering", "country_restricted": None},
    "virginia_sub": {"cost": 16000000, "power": 100, "name": "زیردریایی ویرجینیا", "ability": "پنهانکاری زیرآبی", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "nimitz_carrier": {"cost": 28000000, "power": 180, "name": "ناوگان نیمیتز", "ability": "پایگاه شناور", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "ohio_submarine": {"cost": 32000000, "power": 220, "name": "زیردریایی اوهایو", "ability": "موشک بالستیک", "tech_required": "nuclear_technology", "country_restricted": "usa"},
    "fateh_submarine": {"cost": 8000000, "power": 45, "name": "فاتح", "ability": "زیردریایی کوچک", "tech_required": "naval_engineering", "country_restricted": "iran"},
    "ghadir_submarine": {"cost": 4500000, "power": 25, "name": "غدیر", "ability": "زیردریایی ساحلی", "tech_required": "naval_engineering", "country_restricted": "iran"},

    # Missiles
    "stinger": {"cost": 95000, "power": 7, "name": "استینگر", "ability": "دفاع هوایی محمول", "tech_required": "rocket_science", "country_restricted": None},
    "hellfire": {"cost": 180000, "power": 15, "name": "هلفایر", "ability": "موشک ضد تانک", "tech_required": "rocket_science", "country_restricted": "usa"},
    "javelin": {"cost": 350000, "power": 28, "name": "جاولین", "ability": "ضد زره پیشرفته", "tech_required": "rocket_science", "country_restricted": "usa"},
    "tomahawk": {"cost": 1100000, "power": 75, "name": "توماهاوک", "ability": "برد طولانی", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "patriot": {"cost": 850000, "power": 55, "name": "پاتریوت", "ability": "دفاع موشکی", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "thaad": {"cost": 1400000, "power": 90, "name": "تاد", "ability": "دفاع بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "usa"},
    "iskander": {"cost": 1200000, "power": 80, "name": "اسکندر", "ability": "موشک بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "russia"},
    "s400": {"cost": 1600000, "power": 95, "name": "اس-۴۰۰", "ability": "دفاع هوایی", "tech_required": "ballistic_missiles", "country_restricted": "russia"},
    "iron_dome": {"cost": 1800000, "power": 100, "name": "گنبد آهنین", "ability": "دفاع موشکی", "tech_required": "ballistic_missiles", "country_restricted": "israel"},
    "sejjil": {"cost": 800000, "power": 45, "name": "سجیل", "ability": "موشک بالستیک", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    "emad": {"cost": 950000, "power": 55, "name": "عماد", "ability": "موشک دقیق", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    "khorramshahr": {"cost": 1200000, "power": 75, "name": "خرمشهر", "ability": "برد متوسط", "tech_required": "ballistic_missiles", "country_restricted": "iran"},
    "shahed_136": {"cost": 25000, "power": 8, "name": "شاهد ۱۳۶", "ability": "پهپاد انتحاری", "tech_required": "rocket_science", "country_restricted": "iran"},
    "mohajer": {"cost": 180000, "power": 12, "name": "مهاجر", "ability": "پهپاد نظارت", "tech_required": "aerodynamics", "country_restricted": "iran"},
    
    # Nuclear Weapons
    "minuteman": {"cost": 55000000, "power": 500, "name": "مینوت من", "ability": "موشک هسته ای", "tech_required": "nuclear_weapons", "country_restricted": "usa"},
    "trident": {"cost": 82000000, "power": 750, "name": "ترایدنت", "ability": "موشک قاره پیما", "tech_required": "nuclear_weapons", "country_restricted": "usa"},
    
    # Artillery
    "m777_howitzer": {"cost": 680000, "power": 45, "name": "ام۷۷۷ هویتزر", "ability": "آتش پشتیبانی", "tech_required": "advanced_materials", "country_restricted": "usa"},
    "grad": {"cost": 420000, "power": 32, "name": "گراد", "ability": "راکت انداز", "tech_required": "advanced_materials", "country_restricted": "russia"},
    "raad": {"cost": 380000, "power": 28, "name": "رعد", "ability": "راکت انداز", "tech_required": "advanced_materials", "country_restricted": "iran"},
    "fajr": {"cost": 280000, "power": 22, "name": "فجر", "ability": "راکت انداز", "tech_required": "military_engineering", "country_restricted": "iran"},
    
    # Advanced Technology
    "laser_defense": {"cost": 48000000, "power": 400, "name": "سیستم لیزری", "ability": "شعاع انرژی", "tech_required": "quantum_computing", "country_restricted": "usa"},
    "cyber_unit": {"cost": 22000000, "power": 150, "name": "واحد سایبری", "ability": "جنگ الکترونیک", "tech_required": "quantum_computing", "country_restricted": None},
}

TECH_TREE = {
    "military_engineering": {"name": "مهندسی نظامی", "cost": 1200000, "required_level": 2, "prerequisites": []},
    "aerodynamics": {"name": "آیرودینامیک", "cost": 1800000, "required_level": 4, "prerequisites": []},
    "naval_engineering": {"name": "مهندسی دریایی", "cost": 1500000, "required_level": 3, "prerequisites": []},
    "rocket_science": {"name": "علم موشکی", "cost": 2200000, "required_level": 5, "prerequisites": ["military_engineering"]},
    "advanced_metallurgy": {"name": "متالوژی پیشرفته", "cost": 2800000, "required_level": 6, "prerequisites": ["military_engineering"]},
    "stealth_technology": {"name": "فناوری پنهانکاری", "cost": 3500000, "required_level": 8, "prerequisites": ["aerodynamics", "advanced_metallurgy"]},
    "nuclear_technology": {"name": "فناوری هسته ای", "cost": 4500000, "required_level": 10, "prerequisites": ["rocket_science", "advanced_metallurgy"]},
    "ballistic_missiles": {"name": "موشک های بالستیک", "cost": 4200000, "required_level": 12, "prerequisites": ["rocket_science", "nuclear_technology"]},
    "advanced_training": {"name": "آموزش پیشرفته", "cost": 3000000, "required_level": 7, "prerequisites": ["military_engineering"]},
    "advanced_materials": {"name": "مواد پیشرفته", "cost": 3800000, "required_level": 9, "prerequisites": ["advanced_metallurgy", "rocket_science"]},
    "quantum_computing": {"name": "محاسبات کوانتومی", "cost": 6800000, "required_level": 15, "prerequisites": ["nuclear_technology", "stealth_technology"]},
    "nuclear_weapons": {"name": "تسلیحات هسته ای", "cost": 12000000, "required_level": 18, "prerequisites": ["nuclear_technology", "ballistic_missiles", "quantum_computing"]},
}

DAILY_MISSIONS = [
    {"id": "messages", "name": "پیام رسان", "desc": "۱۰ پیام", "target": 10, "points": 80000, "exp": 50},
    {"id": "purchases", "name": "خریدار", "desc": "۵ خرید", "target": 5, "points": 120000, "exp": 75},
    {"id": "battles", "name": "جنگجو", "desc": "۳ برد", "target": 3, "points": 160000, "exp": 100},
    {"id": "power", "name": "قدرت", "desc": "قدرت ۵۰۰", "target": 500, "points": 250000, "exp": 150},
]

BASE_POINTS_PER_MESSAGE = 3500
DAILY_PURCHASE_LIMIT = 50
COOLDOWN_MINUTES = 0.2
EXP_PER_MESSAGE = 8
LEVEL_REQUIREMENTS = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500, 6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000, 21000, 23500, 26000, 29000, 32500]

group_data = {}
global_user_data = {}

# -------------------- DATA FUNCTIONS --------------------
def load_data():
    global group_data, global_user_data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            group_data = json.load(f)
    except:
        group_data = {}
    
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
    user_id_str = str(user_id)
    if user_id_str not in global_user_data:
        global_user_data[user_id_str] = {
            "country": None, "country_selected": False, "points": 0, "experience": 0, "level": 1, "last_message_time": 0,
            "military": {asset: 0 for asset in MILITARY_ASSETS}, "technologies": [],
            "battles_won": 0, "battles_lost": 0, "alliance": None,
            "daily_purchases": 0, "last_purchase_date": None, "daily_missions": {},
            "missions_completed_today": 0, "last_mission_date": None,
            "total_messages": 0, "last_activity": datetime.now().isoformat(),
            "last_income_time": 0, "income_cooldown": 3600
        }
    
    user_data = global_user_data[user_id_str]
    today = datetime.now().date().isoformat()
    
    if user_data.get("last_purchase_date") != today:
        user_data["daily_purchases"] = 0
        user_data["last_purchase_date"] = today
    if user_data.get("last_mission_date") != today:
        user_data["daily_missions"] = {}
        user_data["missions_completed_today"] = 0
        user_data["last_mission_date"] = today
    
    user_data["last_activity"] = datetime.now().isoformat()
    return user_data

def get_user_data(chat_id, user_id):
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
    
    country_restricted = asset.get("country_restricted")
    if country_restricted and user_data.get("country") != country_restricted:
        country_name = AVAILABLE_COUNTRIES[country_restricted]["name"] if country_restricted in AVAILABLE_COUNTRIES else country_restricted
        return False, f"فقط برای {country_name}"
    
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

# -------------------- BOT EVENTS --------------------
@bot.event
async def on_ready():
    print(f"{bot.user.username} آماده است!")
    load_data()

@bot.event
async def on_message(message: Message):
    try:
        if message.author.is_bot: return
        chat_id, user_id, text = message.chat.id, message.author.user_id, message.content or ""
        generate_daily_missions(chat_id)
        await handle_points_and_exp(message, chat_id, user_id)
        if text.startswith("/"): await handle_command(message, text.lower(), chat_id, user_id)
    except Exception as e:
        print(f"Error: {e}")

async def handle_points_and_exp(message, chat_id, user_id):
    try:
        user_data, chat_data = get_global_user_data(user_id), get_chat_data(chat_id)
        current_time = time.time()
        if current_time - user_data["last_message_time"] >= COOLDOWN_MINUTES * 60:
            user_data["points"] += BASE_POINTS_PER_MESSAGE
            user_data["experience"] += EXP_PER_MESSAGE
            user_data["last_message_time"] = current_time
            user_data["total_messages"] += 1
            new_level = check_level_up(user_data)
            if new_level:
                bonus = new_level * 400000
                user_data["points"] += bonus
                await message.reply(f"🎉 سطح {new_level}! جایزه: ${bonus:,} دلار")
            completed = check_mission_progress(user_data, chat_data, "messages", 1, user_id)
            if completed: await message.reply(f"🏆 ماموریت: {', '.join(completed)}")
            save_data()
    except Exception as e:
        print(f"Error points: {e}")

async def handle_command(message, command, chat_id, user_id):
    try:
        if command == "/start":
            await message.reply("🤖 ربات فعال!\n\n🌍 **برای شروع بازی ابتدا کشور خود را انتخاب کنید:**\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور\n\n📚 **راهنما:**\n/help - راهنمای کامل\n/game_help - راهنمای بازی\n\n🌍 **سیستم جهانی**: تمام پیشرفت‌ها، خریدها و تحقیقات شما در تمام گروه‌ها قابل دسترسی است!")
        elif command == "/help": await show_help(message)
        elif command == "/rules": await show_rules(message, chat_id)
        elif command == "/info": await user_info(message, chat_id, user_id)
        elif command == "/game_help": await game_help(message)
        elif command == "/points": await show_points(message, chat_id, user_id)
        elif command == "/military": await show_military(message, chat_id, user_id)
        elif command == "/tech": await show_tech_tree(message, chat_id, user_id)
        elif command.startswith("/research"): await research_technology(message, chat_id, user_id)
        elif command.startswith("/buy"): await buy_asset(message, chat_id, user_id)
        elif command.startswith("/attack"): await attack_user(message, chat_id, user_id)
        elif command == "/missions": await show_daily_missions(message, chat_id, user_id)
        elif command == "/leaderboard": await show_leaderboard(message, chat_id)
        elif command == "/assets": await show_all_assets(message, chat_id, user_id)
        elif command == "/global": await show_global_stats(message, user_id)
        elif command.startswith("/alliance"): await handle_alliance_command(message, chat_id, user_id)
        elif command == "/countries": await show_available_countries(message)
        elif command.startswith("/select_country"): await select_country(message, chat_id, user_id)
        elif command == "/income": await collect_income(message, chat_id, user_id)
        elif command == "/economy": await show_economy_info(message, chat_id, user_id)
        else: await message.reply("🚫 دستور نامعتبر!")
    except Exception as e:
        print(f"Command error: {e}")

# -------------------- COMMAND FUNCTIONS --------------------
async def show_help(message):
    await message.reply("🤖 راهنما:\n🌍 کشور و اقتصاد:\n/countries - مشاهده کشورهای موجود\n/select_country [کد] - انتخاب کشور\n/income - جمع‌آوری درآمد\n/economy - اطلاعات اقتصادی\n\n🎮 بازی:\n/game_help - راهنمای بازی\n/points - امتیاز\n/military - ارتش\n/assets - کاتالوگ تجهیزات\n/tech - فناوری\n/missions - ماموریت\n/attack - حمله\n/global - آمار جهانی")

async def show_rules(message, chat_id):
    chat_data = get_chat_data(chat_id)
    await message.reply(f"📜 قوانین:\n{chat_data['rules']}")

async def user_info(message, chat_id, user_id):
    try:
        user = message.author
        user_data = get_global_user_data(user_id)
        level = user_data.get("level", 1)
        next_exp = LEVEL_REQUIREMENTS[level] if level < len(LEVEL_REQUIREMENTS) else "MAX"
        current_exp = LEVEL_REQUIREMENTS[level-1] if level > 1 else 0
        progress = user_data["experience"] - current_exp
        alliance_info = f"🤝 اتحاد: {user_data['alliance']}\n" if user_data["alliance"] else ""
        
        if user_data.get("country_selected", False):
            country_code = user_data["country"]
            country_data = AVAILABLE_COUNTRIES[country_code]
            country_info = f"🏛️ کشور: {country_data['name']}\n"
        else:
            country_info = "🏛️ کشور: انتخاب نشده\n"
        
        await message.reply(f"👤 {user.first_name}\nآیدی: {user.user_id}\n{country_info}{alliance_info}"
                          f"💰 بودجه: ${user_data['points']:,}\n⭐ سطح: {level}\n"
                          f"📊 تجربه: {progress}/{next_exp}\n💪 قدرت: {calculate_total_power(user_data)}")
    except Exception as e:
        print(f"Info error: {e}")

async def game_help(message):
    await message.reply("🎮 راهنمای بازی:\n\n🌍 **ابتدا کشور انتخاب کنید:**\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور\n\n💰 **اقتصاد و درآمد:**\n/income - جمع‌آوری درآمد (هر ساعت)\n/economy - اطلاعات اقتصادی کشور\n\n🎯 **بازی اصلی:**\n/buy [نوع] [تعداد] - خرید تجهیزات\n/research [فناوری] - تحقیق فناوری\n/attack [ریپلای] - حمله به کاربران\n/missions - ماموریت روزانه\n/tech - درخت فناوری\n/military - نیروی نظامی\n/leaderboard - رتبه بندی\n\n🌍 **سیستم جهانی**: تمام پیشرفت‌ها، خریدها و تحقیقات شما در تمام گروه‌ها قابل دسترسی است!\n\n⏰ **زمان بندی پیشرفت**: با تنظیمات جدید، رسیدن به اهداف بالا حدود ۱۳-۱۵ روز زمان می‌برد.")

async def show_points(message, chat_id, user_id):
    try:
        user_data = get_global_user_data(user_id)
        level = user_data.get("level", 1)
        next_exp = LEVEL_REQUIREMENTS[level] if level < len(LEVEL_REQUIREMENTS) else "MAX"
        current_exp = LEVEL_REQUIREMENTS[level-1] if level > 1 else 0
        progress = user_data["experience"] - current_exp
        needed = next_exp - current_exp if next_exp != "MAX" else 0
        
        response = (f"💰 بودجه: ${user_data['points']:,}\n⭐ سطح: {level}\n"
                   f"📊 تجربه: {progress}/{needed}\n🛒 خرید امروز: {user_data['daily_purchases']}/{DAILY_PURCHASE_LIMIT}\n"
                   f"🎯 ماموریت امروز: {user_data['missions_completed_today']}\n🔬 فناوری: {len(user_data['technologies'])}")
        
        await message.reply(response)
    except Exception as e:
        print(f"Points error: {e}")

async def show_tech_tree(message, chat_id, user_id):
    try:
        user_data = get_global_user_data(user_id)
        tech_text = "🔬 فناوری:\n\n"
        for tech_id, tech in TECH_TREE.items():
            status = "✅" if tech_id in user_data["technologies"] else "🔒"
            prereq = f" (نیاز: {', '.join([TECH_TREE[p]['name'] for p in tech['prerequisites']])})" if tech["prerequisites"] else ""
            tech_text += f"{status} [{tech_id}] {tech['name']} - ${tech['cost']:,} (سطح {tech['required_level']}){prereq}\n"
        await message.reply(tech_text + "\n/research [tech_id] برای تحقیق")
    except Exception as e:
        print(f"Tech error: {e}")

async def research_technology(message, chat_id, user_id):
    try:
        parts = message.content.split()
        if len(parts) < 2: 
            await message.reply("⚠️ /research [tech_id]")
            return
        
        user_data = get_global_user_data(user_id)
        
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        tech_id = parts[1].lower()
        can_research, error = can_research_tech(user_data, tech_id)
        if not can_research:
            await message.reply(f"⚠️ {error}")
            return
        tech = TECH_TREE[tech_id]
        if user_data["points"] < tech["cost"]:
            await message.reply(f"⚠️ نیاز: ${tech['cost']:,} دلار")
            return
        user_data["points"] -= tech["cost"]
        user_data["technologies"].append(tech_id)
        user_data["experience"] += tech["cost"] // 10
        unlocked = [MILITARY_ASSETS[a]["name"] for a, asset in MILITARY_ASSETS.items() if asset.get("tech_required") == tech_id]
        save_data()
        await message.reply(f"✅ {tech['name']} تحقیق شد!\n🔓 باز شد: {', '.join(unlocked) if unlocked else 'هیچی'}")
    except Exception as e:
        print(f"Research error: {e}")

async def buy_asset(message, chat_id, user_id):
    try:
        parts = message.content.split()
        if len(parts) < 3:
            await message.reply("⚠️ /buy [نوع] [تعداد]")
            return
        
        user_data = get_global_user_data(user_id)
        
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        asset_type = parts[1].lower()
        try:
            quantity = int(parts[2])
            if quantity <= 0 or quantity > 100: raise ValueError
        except:
            await message.reply("⚠️ تعداد ۱ تا ۱۰۰")
            return
        
        chat_data = get_chat_data(chat_id)
        
        if user_data["daily_purchases"] + quantity > DAILY_PURCHASE_LIMIT:
            await message.reply(f"⚠️ محدودیت روزانه! باقی: {DAILY_PURCHASE_LIMIT - user_data['daily_purchases']}")
            return
        
        can_buy, error = can_buy_asset(user_data, asset_type)
        if not can_buy:
            await message.reply(f"⚠️ {error}")
            return
        
        cost = MILITARY_ASSETS[asset_type]["cost"] * quantity
        if user_data["points"] < cost:
            await message.reply(f"⚠️ نیاز: ${cost:,} دلار")
            return
        
        user_data["points"] -= cost
        user_data["military"][asset_type] += quantity
        user_data["daily_purchases"] += quantity
        
        completed = check_mission_progress(user_data, chat_data, "purchases", quantity, user_id)
        completed.extend(check_mission_progress(user_data, chat_data, "power", 1, user_id))
        save_data()
        
        name = MILITARY_ASSETS[asset_type]["name"]
        response = f"✅ {quantity} {name} خریداری شد!\n💰 باقی: ${user_data['points']:,}\n🛒 خرید امروز: {user_data['daily_purchases']}/{DAILY_PURCHASE_LIMIT}"
        if completed: response += f"\n🏆 ماموریت: {', '.join(completed)}"
        await message.reply(response)
    except Exception as e:
        print(f"Buy error: {e}")

async def attack_user(message, chat_id, user_id):
    try:
        if not message.reply_to_message:
            await message.reply("⚠️ ریپلای کنید!")
            return
        target = message.reply_to_message.author
        if target.user_id == user_id:
            await message.reply("⚠️ خودتان را نمی توانید حمله کنید!")
            return
        
        attacker_data = get_global_user_data(user_id)
        
        if not attacker_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        defender_data = get_global_user_data(target.user_id)
        chat_data = get_chat_data(chat_id)
        attacker_power, defender_power = calculate_total_power(attacker_data), calculate_total_power(defender_data)
        
        if attacker_power == 0:
            await message.reply("⚠️ نیروی نظامی ندارید!")
            return
        if defender_power == 0:
            await message.reply("⚠️ هدف نیروی نظامی ندارد!")
            return
        
        tech_bonus_att = 1 + len(attacker_data["technologies"]) * 0.05
        tech_bonus_def = 1 + len(defender_data["technologies"]) * 0.05
        level_bonus = 1 + (attacker_data.get("level", 1) - defender_data.get("level", 1)) * 0.03
        
        attack_str = attacker_power * random.uniform(0.7, 1.3) * tech_bonus_att * level_bonus
        defense_str = defender_power * random.uniform(0.7, 1.3) * tech_bonus_def
        
        stealth_assets = ["f22_raptor", "f35_lightning", "virginia_sub"]
        stealth_bonus = ""
        if any(attacker_data["military"].get(a, 0) > 0 for a in stealth_assets) and random.random() < 0.3:
            attack_str *= 1.5
            stealth_bonus = " (پنهانی!)"
        
        if attack_str > defense_str:
            damage = min(0.25, (attack_str - defense_str) / attack_str * 0.4)
            stolen = int(defender_data["points"] * damage)
            attacker_data["points"] += stolen
            defender_data["points"] = max(0, defender_data["points"] - stolen)
            attacker_data["experience"] += max(15, stolen // 10)
            attacker_data["battles_won"] += 1
            defender_data["battles_lost"] += 1
            
            completed = check_mission_progress(attacker_data, chat_data, "battles", 1, user_id)
            mission_text = f"\n🏆 ماموریت: {', '.join(completed)}" if completed else ""
            
            result = f"⚔️ {message.author.first_name} پیروز شد!{stealth_bonus}\n💰 غنیمت: ${stolen:,}{mission_text}"
        else:
            damage = min(0.15, (defense_str - attack_str) / defense_str * 0.3)
            lost = int(attacker_data["points"] * damage)
            attacker_data["points"] = max(0, attacker_data["points"] - lost)
            defender_data["experience"] += max(10, lost // 15)
            attacker_data["battles_lost"] += 1
            defender_data["battles_won"] += 1
            result = f"🛡 {target.first_name} دفاع کرد!{stealth_bonus}\n💸 جریمه: ${lost:,}"
        
        save_data()
        await message.reply(result)
    except Exception as e:
        print(f"Attack error: {e}")

async def show_military(message, chat_id, user_id):
    try:
        user_data = get_global_user_data(user_id)
        text = "🎖 ارتش:\n\n"
        cats = {
            "پیاده": ["militia", "infantry", "marines", "navy_seal", "delta_force", "spetsnaz", "sas", "quds_force", "takavar"],
            "زرهی": ["humvee", "bradley", "m1_abrams", "t90", "t14_armata", "leopard_2", "challenger_2", "leclerc", "karrar", "zulfiqar", "merkava"],
            "هوایی": ["apache", "f16", "a10", "mi_24", "su_35", "eurofighter", "tornado", "rafale", "saeqeh", "kowsar", "f22_raptor", "f35_lightning", "b2_spirit", "su_57", "j20"],
            "دریایی": ["patrol_boat", "destroyer", "cruiser", "virginia_sub", "nimitz_carrier", "ohio_submarine", "fateh_submarine", "ghadir_submarine"],
            "موشک": ["stinger", "hellfire", "javelin", "tomahawk", "patriot", "thaad", "iskander", "s400", "iron_dome", "sejjil", "emad", "khorramshahr", "shahed_136", "mohajer", "minuteman", "trident"],
            "توپخانه": ["m777_howitzer", "grad", "raad", "fajr"],
            "پیشرفته": ["laser_defense", "cyber_unit"]
        }
        
        total = 0
        for cat, assets in cats.items():
            items = []
            for asset in assets:
                count = user_data["military"].get(asset, 0)
                if count > 0:
                    items.append(f"{MILITARY_ASSETS[asset]['name']}: {count}")
                    total += count
            if items: text += f"**{cat}:** {', '.join(items)}\n"
        
        power = calculate_total_power(user_data)
        text += f"\n💪 قدرت: {power} | 🎖 کل: {total}\n🏆 برد: {user_data['battles_won']} | 💀 باخت: {user_data['battles_lost']}"
        await message.reply(text)
    except Exception as e:
        print(f"Military error: {e}")

async def show_daily_missions(message, chat_id, user_id):
    try:
        chat_data, user_data = get_chat_data(chat_id), get_global_user_data(user_id)
        generate_daily_missions(chat_id)
        if not chat_data["daily_missions"]:
            await message.reply("⚠️ ماموریتی نیست!")
            return
        
        text = "🎯 ماموریت امروز:\n\n"
        for mid, mission in chat_data["daily_missions"].items():
            completed = str(user_id) in mission["completed_by"]
            status = "✅" if completed else "⏳"
            current = user_data["daily_missions"].get(mid, 0)
            if mission["id"] == "power": current = calculate_total_power(user_data)
            progress = "(کامل)" if completed else f"({current}/{mission['target']})"
            text += f"{status} {mission['name']} {progress}\n{mission['desc']} - {mission['points']} امتیاز\n\n"
        
        text += f"🏆 کامل امروز: {user_data['missions_completed_today']}"
        await message.reply(text)
    except Exception as e:
        print(f"Missions error: {e}")

async def show_leaderboard(message, chat_id):
    try:
        users = [(int(uid), calculate_total_power(get_global_user_data(uid)), get_global_user_data(uid).get("level", 1)) 
                for uid in global_user_data.keys()]
        users.sort(key=lambda x: x[1], reverse=True)
        
        text = "🏆 رتبه بندی:\n\n"
        for i, (uid, power, level) in enumerate(users[:10]):
            try:
                member = await bot.get_chat_member(chat_id, uid)
                name = member.user.first_name
            except:
                name = f"User#{uid}"
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            text += f"{medal} {name} - قدرت: {power} | سطح: {level}\n"
        await message.reply(text)
    except Exception as e:
        print(f"Leaderboard error: {e}")

async def show_all_assets(message, chat_id, user_id):
    try:
        user_data = get_global_user_data(user_id)
        user_points = user_data["points"]
        user_techs = user_data["technologies"]
        
        text = f"🛒 کاتالوگ تجهیزات نظامی\n💰 بودجه شما: ${user_points:,}\n\n"
        
        categories = {
            "پیاده نظام (بدون نیاز فناوری)": ["militia", "infantry", "marines"],
            "نیروی ویژه (نیاز: آموزش پیشرفته)": ["navy_seal", "delta_force", "spetsnaz", "sas", "quds_force", "takavar"],
            "زرهی پایه (نیاز: مهندسی نظامی)": ["humvee", "bradley", "m1_abrams"],
            "زرهی پیشرفته (نیاز: متالوژی پیشرفته)": ["t90", "t14_armata", "leopard_2", "challenger_2", "leclerc", "karrar", "zulfiqar", "merkava"],
            "هوایی پایه (نیاز: آیرودینامیک)": ["apache", "f16", "a10", "mi_24", "su_35", "eurofighter", "tornado", "rafale", "saeqeh", "kowsar"],
            "هوایی پیشرفته (نیاز: فناوری پنهانکاری)": ["f22_raptor", "f35_lightning", "b2_spirit", "su_57", "j20"],
            "دریایی پایه (نیاز: مهندسی دریایی)": ["patrol_boat", "destroyer", "cruiser", "fateh_submarine", "ghadir_submarine"],
            "دریایی پیشرفته (نیاز: فناوری هسته ای)": ["virginia_sub", "nimitz_carrier", "ohio_submarine"],
            "موشک پایه (نیاز: علم موشکی)": ["stinger", "hellfire", "javelin", "shahed_136", "mohajer"],
            "موشک پیشرفته (نیاز: موشک های بالستیک)": ["tomahawk", "patriot", "thaad", "iskander", "s400", "iron_dome", "sejjil", "emad", "khorramshahr"],
            "موشک هسته ای (نیاز: تسلیحات هسته ای)": ["minuteman", "trident"],
            "توپخانه (نیاز: مواد پیشرفته)": ["m777_howitzer", "grad", "raad", "fajr"],
            "فناوری آینده (نیاز: محاسبات کوانتومی)": ["laser_defense", "cyber_unit"]
        }
        
        for category_name, asset_list in categories.items():
            category_text = f"**{category_name}:**\n"
            category_items = []
            
            for asset_id in asset_list:
                if asset_id not in MILITARY_ASSETS:
                    continue
                asset_data = MILITARY_ASSETS[asset_id]
                can_buy, error_msg = can_buy_asset(user_data, asset_id)
                
                if can_buy:
                    if user_points >= asset_data["cost"]:
                        status = "✅"
                    else:
                        status = "💰"
                else:
                    status = "🔒"
                
                owned = user_data["military"].get(asset_id, 0)
                owned_text = f" (دارید: {owned})" if owned > 0 else ""
                
                item_text = (f"{status} {asset_id}: {asset_data['name']}\n"
                           f"   💰 قیمت: ${asset_data['cost']:,} | ⚡ قدرت: {asset_data['power']} | 🎯 {asset_data['ability']}{owned_text}")
                
                if not can_buy:
                    item_text += f"\n   🔒 {error_msg}"
                
                category_items.append(item_text)
            
            if category_items:
                text += category_text + "\n".join(category_items) + "\n\n"
        
        text += (f"📊 وضعیت خرید امروز: {user_data['daily_purchases']}/{DAILY_PURCHASE_LIMIT}\n"
                f"🔬 فناوری های شما: {len(user_techs)}/12\n\n"
                f"🛒 برای خرید: /buy [asset_id] [تعداد]\n"
                f"🔬 برای تحقیق: /research [tech_id]")
        
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
        print(f"Assets display error: {e}")
        await message.reply("⚠️ خطا در نمایش تجهیزات!")

async def show_global_stats(message, user_id):
    try:
        user_data = get_global_user_data(user_id)
        total_assets = sum(user_data["military"].values())
        total_power = calculate_total_power(user_data)
        total_value = sum(MILITARY_ASSETS[asset]["cost"] * count for asset, count in user_data["military"].items())
        
        last_activity = datetime.fromisoformat(user_data.get("last_activity", datetime.now().isoformat()))
        days_active = (datetime.now() - last_activity).days
        
        stats_text = f"🌍 **آمار جهانی شما**\n\n"
        stats_text += f"💰 **بودجه کل**: ${user_data['points']:,}\n"
        stats_text += f"⭐ **سطح**: {user_data.get('level', 1)}\n"
        stats_text += f"📊 **تجربه**: {user_data['experience']:,}\n"
        stats_text += f"💪 **قدرت کل**: {total_power:,}\n"
        stats_text += f"🎖 **تجهیزات کل**: {total_assets:,}\n"
        stats_text += f"🔬 **فناوری**: {len(user_data['technologies'])}/12\n"
        stats_text += f"🏆 **برد**: {user_data['battles_won']} | 💀 **باخت**: {user_data['battles_lost']}\n"
        stats_text += f"📝 **پیام کل**: {user_data.get('total_messages', 0):,}\n"
        stats_text += f"🛒 **خرید امروز**: {user_data['daily_purchases']}/{DAILY_PURCHASE_LIMIT}\n"
        stats_text += f"🎯 **ماموریت امروز**: {user_data['missions_completed_today']}\n"
        stats_text += f"🤝 **اتحاد**: {user_data['alliance'] or 'بدون اتحاد'}\n"
        stats_text += f"📅 **آخرین فعالیت**: {days_active} روز پیش\n"
        stats_text += f"💎 **ارزش کل دارایی**: ${total_value:,} دلار\n\n"
        stats_text += f"🌍 **نکته**: تمام پیشرفت‌های شما در تمام گروه‌ها قابل دسترسی است!"
        
        await message.reply(stats_text)
    except Exception as e:
        print(f"Global stats error: {e}")
        await message.reply("⚠️ خطا در نمایش آمار جهانی!")

async def handle_alliance_command(message, chat_id, user_id):
    parts = message.content.split()
    if len(parts) < 2: return
    sub = parts[1].lower()
    
    if sub == "create" and len(parts) >= 3: await alliance_create(message, chat_id, user_id, " ".join(parts[2:]))
    elif sub == "join" and len(parts) >= 3: await alliance_join(message, chat_id, user_id, " ".join(parts[2:]))
    elif sub == "leave": await alliance_leave(message, chat_id, user_id)
    elif sub == "info" and len(parts) >= 3: await alliance_info(message, chat_id, " ".join(parts[2:]))
    elif sub == "list": await alliance_list(message, chat_id)
    else: await message.reply("⚠️ دستور اتحاد نامعتبر")

async def alliance_create(message, chat_id, user_id, name):
    try:
        chat_data, user_data = get_chat_data(chat_id), get_global_user_data(user_id)
        if user_data["alliance"]: 
            await message.reply("⚠️ قبلا عضو اتحاد هستید")
            return
        if name in chat_data.get("alliances", {}):
            await message.reply("⚠️ نام تکراری")
            return
        
        if "alliances" not in chat_data:
            chat_data["alliances"] = {}
        chat_data["alliances"][name] = {"creator": user_id, "members": [user_id], "created": datetime.now().isoformat()}
        user_data["alliance"] = name
        save_data()
        await message.reply(f"✅ اتحاد '{name}' ایجاد شد!")
    except Exception as e:
        print(f"Alliance create error: {e}")

async def alliance_join(message, chat_id, user_id, name):
    try:
        chat_data, user_data = get_chat_data(chat_id), get_global_user_data(user_id)
        if user_data["alliance"]: 
            await message.reply("⚠️ قبلا عضو هستید")
            return
        if name not in chat_data.get("alliances", {}):
            await message.reply("⚠️ اتحاد وجود ندارد")
            return
        
        chat_data["alliances"][name]["members"].append(user_id)
        user_data["alliance"] = name
        save_data()
        await message.reply(f"✅ به '{name}' پیوستید!")
    except Exception as e:
        print(f"Alliance join error: {e}")

async def alliance_leave(message, chat_id, user_id):
    try:
        chat_data, user_data = get_chat_data(chat_id), get_global_user_data(user_id)
        if not user_data["alliance"]:
            await message.reply("⚠️ عضو اتحادی نیستید")
            return
        
        name = user_data["alliance"]
        if name in chat_data.get("alliances", {}):
            alliance = chat_data["alliances"][name]
            if user_id in alliance["members"]: alliance["members"].remove(user_id)
            if not alliance["members"]: del chat_data["alliances"][name]
            elif alliance["creator"] == user_id: alliance["creator"] = alliance["members"][0]
        
        user_data["alliance"] = None
        save_data()
        await message.reply(f"✅ از '{name}' خارج شدید!")
    except Exception as e:
        print(f"Alliance leave error: {e}")

async def alliance_info(message, chat_id, name):
    try:
        chat_data = get_chat_data(chat_id)
        if name not in chat_data.get("alliances", {}):
            await message.reply("⚠️ اتحاد وجود ندارد")
            return
        
        alliance = chat_data["alliances"][name]
        members = len(alliance["members"])
        total_power = sum(calculate_total_power(get_global_user_data(mid)) for mid in alliance["members"])
        created = datetime.fromisoformat(alliance["created"]).strftime("%Y-%m-%d")
        
        await message.reply(f"🤝 اتحاد '{name}':\n👥 اعضا: {members}\n💪 قدرت کل: {total_power}\n📅 ایجاد: {created}")
    except Exception as e:
        print(f"Alliance info error: {e}")

async def alliance_list(message, chat_id):
    try:
        chat_data = get_chat_data(chat_id)
        if not chat_data.get("alliances", {}):
            await message.reply("⚠️ اتحادی وجود ندارد")
            return
        
        text = "🤝 اتحادها:\n\n"
        for name, data in chat_data["alliances"].items():
            text += f"• {name} ({len(data['members'])} عضو)\n"
        await message.reply(text)
    except Exception as e:
        print(f"Alliance list error: {e}")

async def show_available_countries(message):
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
    try:
        parts = message.content.split()
        if len(parts) < 2:
            await message.reply("⚠️ /select_country [کد کشور]\n\nمثال:\n/select_country usa\n/select_country iran\n\nبرای مشاهده کشورها: /countries")
            return
        
        country_code = parts[1].lower()
        user_data = get_global_user_data(user_id)
        
        if user_data.get("country_selected", False):
            current_country = user_data.get("country", "نامشخص")
            current_country_name = AVAILABLE_COUNTRIES.get(current_country, {}).get("name", current_country)
            await message.reply(f"⚠️ شما قبلاً کشور {current_country_name} را انتخاب کرده‌اید!\n\nبرای تغییر کشور، ابتدا باید از کشور فعلی خارج شوید.")
            return
        
        if country_code not in AVAILABLE_COUNTRIES:
            await message.reply(f"⚠️ کشور '{country_code}' وجود ندارد!\n\nبرای مشاهده کشورهای موجود: /countries")
            return
        
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        user_data["country"] = country_code
        user_data["country_selected"] = True
        user_data["points"] = country_data["starting_money"]
        
        save_data()
        
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
    try:
        user_data = get_global_user_data(user_id)
        
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        current_time = time.time()
        country_code = user_data["country"]
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        if current_time - user_data.get("last_income_time", 0) < user_data.get("income_cooldown", 3600):
            remaining_time = int(user_data.get("income_cooldown", 3600) - (current_time - user_data.get("last_income_time", 0)))
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            await message.reply(f"⏳ باید {minutes} دقیقه و {seconds} ثانیه صبر کنید تا بتوانید دوباره درآمد جمع‌آوری کنید!")
            return
        
        total_income = 0
        income_details = []
        
        for method_id, method_data in country_data['income_methods'].items():
            base_income = method_data['base_income']
            multiplier = method_data['multiplier']
            
            level_bonus = 1 + (user_data.get("level", 1) * 0.02)
            tech_bonus = 1 + (len(user_data.get("technologies", [])) * 0.05)
            
            method_income = int(base_income * multiplier * level_bonus * tech_bonus)
            total_income += method_income
            
            income_details.append(f"• {method_data['name']}: ${method_income:,}")
        
        user_data["points"] += total_income
        user_data["last_income_time"] = current_time
        user_data["experience"] += total_income // 20
        
        save_data()
        
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
    try:
        user_data = get_global_user_data(user_id)
        
        if not user_data.get("country_selected", False):
            await message.reply("⚠️ ابتدا باید کشور خود را انتخاب کنید!\n/countries - مشاهده کشورهای موجود\n/select_country [کد کشور] - انتخاب کشور")
            return
        
        country_code = user_data["country"]
        country_data = AVAILABLE_COUNTRIES[country_code]
        
        current_income = 0
        income_breakdown = []
        
        for method_id, method_data in country_data['income_methods'].items():
            base_income = method_data['base_income']
            multiplier = method_data['multiplier']
            
            level_bonus = 1 + (user_data.get("level", 1) * 0.02)
            tech_bonus = 1 + (len(user_data.get("technologies", [])) * 0.05)
            
            method_income = int(base_income * multiplier * level_bonus * tech_bonus)
            current_income += method_income
            
            income_breakdown.append(f"• {method_data['name']}: ${method_income:,}")
        
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
    print("🚀 Starting Complete Bale Bot...")
    load_data()
    bot.run()