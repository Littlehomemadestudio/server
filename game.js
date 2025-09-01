// Game data and configuration
const GAME_DATA = {
    countries: {
        usa: {
            name: "🇺🇸 آمریکا",
            description: "قدرت نظامی و اقتصادی برتر جهان",
            starting_money: 800000,
            income_methods: {
                military_exports: { name: "صادرات نظامی", base_income: 180000, multiplier: 1.5 },
                technology_sales: { name: "فروش فناوری", base_income: 120000, multiplier: 2.0 },
                alliance_support: { name: "حمایت اتحاد", base_income: 80000, multiplier: 1.3 }
            },
            bonus: "قدرت نظامی +20%"
        },
        russia: {
            name: "🇷🇺 روسیه",
            description: "قدرت نظامی سنتی با منابع طبیعی فراوان",
            starting_money: 650000,
            income_methods: {
                resource_exports: { name: "صادرات منابع", base_income: 220000, multiplier: 1.4 },
                nuclear_technology: { name: "فناوری هسته‌ای", base_income: 150000, multiplier: 1.8 },
                military_cooperation: { name: "همکاری نظامی", base_income: 95000, multiplier: 1.2 }
            },
            bonus: "فناوری هسته‌ای +15%"
        },
        china: {
            name: "🇨🇳 چین",
            description: "اقتصاد در حال رشد با نیروی انسانی عظیم",
            starting_money: 720000,
            income_methods: {
                manufacturing: { name: "تولید انبوه", base_income: 250000, multiplier: 1.6 },
                trade_routes: { name: "مسیرهای تجاری", base_income: 140000, multiplier: 1.7 },
                infrastructure: { name: "زیرساخت", base_income: 110000, multiplier: 1.4 }
            },
            bonus: "تولید +25%"
        },
        iran: {
            name: "🇮🇷 ایران",
            description: "قدرت منطقه‌ای با منابع انرژی فراوان",
            starting_money: 500000,
            income_methods: {
                oil_exports: { name: "صادرات نفت", base_income: 280000, multiplier: 1.3 },
                regional_trade: { name: "تجارت منطقه‌ای", base_income: 160000, multiplier: 1.5 },
                cultural_exports: { name: "صادرات فرهنگی", base_income: 70000, multiplier: 1.2 }
            },
            bonus: "درآمد نفتی +30%"
        },
        germany: {
            name: "🇩🇪 آلمان",
            description: "قدرت صنعتی و مهندسی پیشرفته",
            starting_money: 680000,
            income_methods: {
                automotive_industry: { name: "صنعت خودروسازی", base_income: 210000, multiplier: 1.7 },
                engineering_exports: { name: "صادرات مهندسی", base_income: 170000, multiplier: 1.6 },
                research_grants: { name: "کمک‌های تحقیقاتی", base_income: 120000, multiplier: 1.8 }
            },
            bonus: "تحقیق و توسعه +20%"
        }
    },

    military_assets: {
        // Infantry & Special Forces
        militia: { cost: 15000, power: 1, name: "شبه نظامی", ability: "پایگاه", tech_required: null, country_restricted: null },
        infantry: { cost: 25000, power: 2, name: "پیاده نظام", ability: "تحرک بالا", tech_required: null, country_restricted: null },
        marines: { cost: 60000, power: 4, name: "تفنگداران", ability: "عملیات آبخاکی", tech_required: null, country_restricted: null },

        navy_seal: { cost: 300000, power: 20, name: "سیل نیروی دریایی", ability: "عملیات ویژه", tech_required: "advanced_training", country_restricted: "usa" },
        delta_force: { cost: 450000, power: 35, name: "نیروی دلتا", ability: "ضد تروریسم", tech_required: "advanced_training", country_restricted: "usa" },
        spetsnaz: { cost: 380000, power: 32, name: "اسپتسناز", ability: "جنگ نامتقارن", tech_required: "advanced_training", country_restricted: "russia" },
        sas: { cost: 420000, power: 38, name: "اس‌ای‌اس", ability: "عملیات مخفی", tech_required: "advanced_training", country_restricted: "uk" },
        gsg9: { cost: 400000, power: 36, name: "جی‌اس‌جی۹", ability: "ضد تروریسم", tech_required: "advanced_training", country_restricted: "germany" },
        gign: { cost: 390000, power: 34, name: "ژاندارمری ویژه", ability: "مقابله تروریسم", tech_required: "advanced_training", country_restricted: "france" },
        quds_force: { cost: 320000, power: 28, name: "نیروی قدس", ability: "عملیات منطقه‌ای", tech_required: "advanced_training", country_restricted: "iran" },
        takavar: { cost: 280000, power: 25, name: "تکاور", ability: "عملیات ویژه", tech_required: "advanced_training", country_restricted: "iran" },

        // Armor
        humvee: { cost: 80000, power: 5, name: "هاموی", ability: "تحرک سریع", tech_required: "military_engineering", country_restricted: null },
        bradley: { cost: 1800000, power: 9, name: "بردلی", ability: "نقل زرهی", tech_required: "military_engineering", country_restricted: "usa" },
        m1_abrams: { cost: 2200000, power: 12, name: "ام۱ آبرامز", ability: "زره مستحکم", tech_required: "military_engineering", country_restricted: "usa" },
        t90: { cost: 4200000, power: 25, name: "تی-۹۰", ability: "شلیک حرکتی", tech_required: "advanced_metallurgy", country_restricted: "russia" },
        t14_armata: { cost: 6800000, power: 45, name: "تی-۱۴ آرماتا", ability: "زره فعال", tech_required: "advanced_metallurgy", country_restricted: "russia" },
        leopard_2: { cost: 7200000, power: 40, name: "لئوپارد ۲", ability: "توپ پیشرفته", tech_required: "advanced_metallurgy", country_restricted: "germany" },
        challenger_2: { cost: 6500000, power: 38, name: "چلنجر ۲", ability: "زره چوبهام", tech_required: "advanced_metallurgy", country_restricted: "uk" },
        leclerc: { cost: 6200000, power: 36, name: "لکلرک", ability: "سیستم آتش", tech_required: "advanced_metallurgy", country_restricted: "france" },
        karrar: { cost: 4800000, power: 28, name: "کرار", ability: "تانک بومی", tech_required: "advanced_metallurgy", country_restricted: "iran" },
        zulfiqar: { cost: 3200000, power: 22, name: "ذوالفقار", ability: "طراحی ایرانی", tech_required: "military_engineering", country_restricted: "iran" },

        // Aircraft (subset)
        apache: { cost: 2800000, power: 18, name: "آپاچی", ability: "بالگرد تهاجمی", tech_required: "aerodynamics", country_restricted: "usa" },
        f16: { cost: 3200000, power: 22, name: "اف-۱۶", ability: "جنگنده چندمنظوره", tech_required: "aerodynamics", country_restricted: "usa" },
        a10: { cost: 3800000, power: 28, name: "ای-۱۰", ability: "نابودگر زمینی", tech_required: "aerodynamics", country_restricted: "usa" },
        mi_24: { cost: 2200000, power: 15, name: "می-۲۴", ability: "بالگرد جنگی", tech_required: "aerodynamics", country_restricted: "russia" },
        su_35: { cost: 3600000, power: 26, name: "سوخو-۳۵", ability: "مانور بالا", tech_required: "aerodynamics", country_restricted: "russia" },
        eurofighter: { cost: 4200000, power: 32, name: "یوروفایتر", ability: "جنگنده اروپایی", tech_required: "aerodynamics", country_restricted: "germany" },
        tornado: { cost: 3400000, power: 24, name: "تورنادو", ability: "حمله زمینی", tech_required: "aerodynamics", country_restricted: "uk" },
        rafale: { cost: 4000000, power: 30, name: "رافال", ability: "چندمنظوره", tech_required: "aerodynamics", country_restricted: "france" },
        saeqeh: { cost: 1800000, power: 12, name: "صاعقه", ability: "جنگنده بومی", tech_required: "aerodynamics", country_restricted: "iran" },
        kowsar: { cost: 2400000, power: 16, name: "کوثر", ability: "فناوری پیشرفته", tech_required: "aerodynamics", country_restricted: "iran" },

        // Navy (subset)
        patrol_boat: { cost: 120000, power: 8, name: "قایق گشتی", ability: "گشت ساحلی", tech_required: "naval_engineering", country_restricted: null },
        destroyer: { cost: 5500000, power: 35, name: "ناوچه", ability: "دفاع هوایی", tech_required: "naval_engineering", country_restricted: null },
        fateh_submarine: { cost: 8000000, power: 45, name: "فاتح", ability: "زیردریایی کوچک", tech_required: "naval_engineering", country_restricted: "iran" },

        // Missiles/Artillery (subset)
        stinger: { cost: 95000, power: 7, name: "استینگر", ability: "دفاع هوایی محمول", tech_required: "rocket_science", country_restricted: null },
        hellfire: { cost: 180000, power: 15, name: "هلفایر", ability: "موشک ضد تانک", tech_required: "rocket_science", country_restricted: "usa" },
        javelin: { cost: 350000, power: 28, name: "جاولین", ability: "ضد زره پیشرفته", tech_required: "rocket_science", country_restricted: "usa" },
        sejjil: { cost: 800000, power: 45, name: "سجیل", ability: "موشک بالستیک", tech_required: "ballistic_missiles", country_restricted: "iran" },
        emad: { cost: 950000, power: 55, name: "عماد", ability: "موشک دقیق", tech_required: "ballistic_missiles", country_restricted: "iran" },
        shahed_136: { cost: 25000, power: 8, name: "شاهد ۱۳۶", ability: "پهپاد انتحاری", tech_required: "rocket_science", country_restricted: "iran" },
        mohajer: { cost: 180000, power: 12, name: "مهاجر", ability: "پهپاد نظارت", tech_required: "aerodynamics", country_restricted: "iran" }
    },

    tech_tree: {
        military_engineering: { name: "مهندسی نظامی", cost: 1200000, required_level: 2, prerequisites: [] },
        aerodynamics: { name: "آیرودینامیک", cost: 1800000, required_level: 4, prerequisites: [] },
        naval_engineering: { name: "مهندسی دریایی", cost: 1500000, required_level: 3, prerequisites: [] },
        rocket_science: { name: "علم موشکی", cost: 2200000, required_level: 5, prerequisites: ["military_engineering"] },
        advanced_metallurgy: { name: "متالوژی پیشرفته", cost: 2800000, required_level: 6, prerequisites: ["military_engineering"] },
        advanced_training: { name: "آموزش پیشرفته", cost: 3000000, required_level: 7, prerequisites: ["military_engineering"] },
        ballistic_missiles: { name: "موشک های بالستیک", cost: 4200000, required_level: 12, prerequisites: ["rocket_science"] }
    },

    daily_missions: [
        { id: "messages", name: "پیام رسان", desc: "۱۰ پیام", target: 10, points: 80000, exp: 50 },
        { id: "purchases", name: "خریدار", desc: "۵ خرید", target: 5, points: 120000, exp: 75 },
        { id: "battles", name: "جنگجو", desc: "۳ برد", target: 3, points: 160000, exp: 100 },
        { id: "power", name: "قدرت", desc: "قدرت ۵۰۰", target: 500, points: 250000, exp: 150 }
    ],

    level_requirements: [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500, 6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000, 21000, 23500, 26000, 29000, 32500]
};

// Game state
let gameState = {
    player: null,
    currentScreen: 'loading',
    selectedCountry: null,
    dailyPurchaseLimit: 50,
    incomeCooldown: 3600 // seconds
};

// Initialize game
class MilitaryGame {
    constructor() {
        this.initializeGame();
        this.setupEventListeners();
        this.loadGameData();
        this.initializeMap();
    }

    initializeGame() {
        this.showScreen('loading');
        setTimeout(() => this.showScreen('login'), 1200);
    }

    setupEventListeners() {
        const loginBtn = document.getElementById('login-btn');
        const usernameInput = document.getElementById('username');
        if (loginBtn) loginBtn.addEventListener('click', () => this.handleLogin());
        if (usernameInput) usernameInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') this.handleLogin(); });

        document.addEventListener('click', (e) => {
            const card = e.target.closest('.dashboard-card');
            if (card) this.showGameSection(card.dataset.section);

            const backBtn = e.target.closest('.btn-back');
            if (backBtn) this.showGameSection(backBtn.dataset.back);

            const countryCard = e.target.closest('.country-card');
            if (countryCard) this.selectCountry(countryCard.dataset.country);

            if (e.target.classList.contains('category-btn')) this.showMilitaryCategory(e.target.dataset.category);
            if (e.target.classList.contains('buy-btn')) this.showBuyModal(e.target.dataset.unit);
            if (e.target.classList.contains('research-btn')) this.showResearchModal(e.target.dataset.tech);
            if (e.target.classList.contains('modal-close')) this.closeModal();
        });

        const shopBtn = document.getElementById('shop-btn');
        if (shopBtn) shopBtn.addEventListener('click', () => this.showGameSection('military'));

        const qty = document.getElementById('quantity');
        if (qty) qty.addEventListener('input', () => this.updateTotalCost());
        const confirmBuy = document.getElementById('confirm-buy');
        if (confirmBuy) confirmBuy.addEventListener('click', () => this.confirmPurchase());
        const confirmResearch = document.getElementById('confirm-research');
        if (confirmResearch) confirmResearch.addEventListener('click', () => this.confirmResearch());

        const collectBtn = document.getElementById('collect-income-btn');
        if (collectBtn) collectBtn.addEventListener('click', () => this.collectIncome());

        const aiBattleBtn = document.getElementById('ai-battle-btn');
        if (aiBattleBtn) aiBattleBtn.addEventListener('click', () => this.startAIBattle());

        const placeCpBtn = document.getElementById('place-cp-btn');
        if (placeCpBtn) placeCpBtn.addEventListener('click', () => this.placeCommandPostFromSelection());
        const attackBtn = document.getElementById('attack-btn');
        if (attackBtn) attackBtn.addEventListener('click', () => this.attackSelectedCountry());
    }

    handleLogin() {
        const username = (document.getElementById('username')?.value || '').trim();
        if (username.length < 2) {
            this.showNotification('نام کاربری معتبر وارد کنید (حداقل ۲ کاراکتر)', 'error');
            return;
        }

        gameState.player = {
            name: username,
            country: null,
            country_selected: false,
            points: 0,
            experience: 0,
            level: 1,
            military: {},
            technologies: [],
            battles_won: 0,
            battles_lost: 0,
            daily_purchases: 0,
            last_purchase_date: null,
            daily_missions: {},
            missions_completed_today: 0,
            last_mission_date: null,
            total_messages: 0,
            last_activity: new Date().toISOString(),
            last_income_time: 0,
            income_cooldown: 3600
        };

        this.showScreen('country');
        this.populateCountries();
    }

    populateCountries() {
        const grid = document.getElementById('countries-grid');
        if (!grid) return;
        grid.innerHTML = '';

        Object.entries(GAME_DATA.countries).forEach(([code, country]) => {
            const card = document.createElement('div');
            card.className = 'country-card';
            card.dataset.country = code;
            card.innerHTML = `
                <div class="country-name">${country.name}</div>
                <div class="country-desc">${country.description}</div>
                <div class="country-bonus">${country.bonus}</div>
                <div class="country-income">
                    <strong>پول شروع:</strong> $${country.starting_money.toLocaleString()}<br>
                    <strong>درآمدها:</strong><br>
                    ${Object.values(country.income_methods).map(m => `• ${m.name}: $${m.base_income.toLocaleString()} (${m.multiplier}x)`).join('<br>')}
                </div>
            `;
            grid.appendChild(card);
        });
    }

    selectCountry(countryCode) {
        const country = GAME_DATA.countries[countryCode];
        if (!country) return;

        gameState.player.country = countryCode;
        gameState.player.country_selected = true;
        gameState.player.points = country.starting_money;

        this.showScreen('game');
        this.showGameSection('dashboard');
        this.updateGameDisplay();
        this.showNotification(`خوش آمدید به ${country.name}!`, 'success');
    }

    showScreen(screenName) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        const el = document.getElementById(`${screenName}-screen`);
        if (el) el.classList.add('active');
        gameState.currentScreen = screenName;
    }

    showGameSection(sectionName) {
        document.querySelectorAll('.game-section').forEach(s => s.classList.remove('active'));
        const el = document.getElementById(sectionName);
        if (el) el.classList.add('active');

        switch (sectionName) {
            case 'military': this.loadMilitarySection(); break;
            case 'economy': this.loadEconomySection(); break;
            case 'technology': this.loadTechnologySection(); break;
            case 'missions': this.loadMissionsSection(); break;
            case 'leaderboard': this.loadLeaderboardSection(); break;
            case 'map': this.loadMapSection(); break;
            default: break;
        }
    }

    updateGameDisplay() {
        const player = gameState.player;
        if (!player) return;

        const nameEl = document.getElementById('player-name');
        const countryEl = document.getElementById('player-country');
        const moneyEl = document.getElementById('money-display');
        const levelEl = document.getElementById('level-display');
        const powerEl = document.getElementById('power-display');

        if (nameEl) nameEl.textContent = player.name;
        if (countryEl && player.country) countryEl.textContent = GAME_DATA.countries[player.country].name;
        if (moneyEl) moneyEl.textContent = `$${player.points.toLocaleString()}`;
        if (levelEl) levelEl.textContent = `Level ${player.level}`;
        if (powerEl) powerEl.textContent = `Power: ${this.calculateTotalPower()}`;
    }

    calculateTotalPower() {
        const player = gameState.player;
        if (!player) return 0;

        let totalPower = 0;
        Object.entries(player.military).forEach(([id, count]) => {
            const unit = GAME_DATA.military_assets[id];
            if (unit && count > 0) totalPower += unit.power * count;
        });
        const levelBonus = 1 + (player.level * 0.03);
        return Math.floor(totalPower * levelBonus);
    }

    // Military
    loadMilitarySection() {
        this.updateMilitaryStats();
        this.showMilitaryCategory('infantry');
    }

    updateMilitaryStats() {
        const totalPower = this.calculateTotalPower();
        const totalUnits = Object.values(gameState.player.military).reduce((a, b) => a + b, 0);

        const tp = document.getElementById('total-power');
        const tu = document.getElementById('total-units');
        const bw = document.getElementById('battles-won');
        if (tp) tp.textContent = totalPower.toLocaleString();
        if (tu) tu.textContent = totalUnits.toLocaleString();
        if (bw) bw.textContent = gameState.player.battles_won;
    }

    showMilitaryCategory(category) {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        const btn = document.querySelector(`[data-category="${category}"]`);
        if (btn) btn.classList.add('active');

        const units = this.getUnitsByCategory(category);
        this.displayUnits(units);
    }

    getUnitsByCategory(category) {
        const categoryMap = {
            infantry: ['militia', 'infantry', 'marines', 'navy_seal', 'delta_force', 'spetsnaz', 'quds_force', 'takavar'],
            armor: ['humvee', 'bradley', 'm1_abrams', 't90', 't14_armata', 'leopard_2', 'challenger_2', 'leclerc', 'karrar', 'zulfiqar'],
            air: ['apache', 'f16', 'a10', 'mi_24', 'su_35', 'eurofighter', 'tornado', 'rafale', 'saeqeh', 'kowsar'],
            navy: ['patrol_boat', 'destroyer', 'fateh_submarine'],
            missiles: ['stinger', 'hellfire', 'javelin', 'sejjil', 'emad', 'shahed_136', 'mohajer'],
            artillery: ['stinger', 'hellfire', 'sejjil', 'emad'] // kept minimal for UI sample
        };
        const ids = categoryMap[category] || [];
        return ids.map(id => ({ id, ...GAME_DATA.military_assets[id] })).filter(Boolean);
    }

    displayUnits(units) {
        const grid = document.getElementById('military-units');
        if (!grid) return;
        grid.innerHTML = '';

        units.forEach(unit => {
            const canBuy = this.canBuyUnit(unit.id);
            const owned = gameState.player.military[unit.id] || 0;
            const affordable = gameState.player.points >= unit.cost;

            const card = document.createElement('div');
            card.className = 'unit-card';
            card.innerHTML = `
                <div class="unit-header">
                    <div class="unit-name">${unit.name}</div>
                    <div class="unit-cost">$${unit.cost.toLocaleString()}</div>
                </div>
                <div class="unit-stats">
                    <span>قدرت: ${unit.power}</span>
                    <span>تعداد: ${owned}</span>
                </div>
                <div class="unit-ability">${unit.ability}</div>
                ${!canBuy.can ? `<div class="unit-requirements">${canBuy.reason}</div>` : ''}
                <div class="unit-actions">
                    <button class="buy-btn" data-unit="${unit.id}" ${!canBuy.can || !affordable ? 'disabled' : ''}>خرید</button>
                    <button class="info-btn">اطلاعات</button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    canBuyUnit(unitId) {
        const unit = GAME_DATA.military_assets[unitId];
        if (!unit) return { can: false, reason: 'نامعتبر' };
        if (unit.country_restricted && gameState.player.country !== unit.country_restricted) {
            const c = GAME_DATA.countries[unit.country_restricted];
            return { can: false, reason: `فقط برای ${c?.name || unit.country_restricted}` };
        }
        if (unit.tech_required && !gameState.player.technologies.includes(unit.tech_required)) {
            const t = GAME_DATA.tech_tree[unit.tech_required];
            return { can: false, reason: `نیاز به: ${t?.name || unit.tech_required}` };
        }
        return { can: true, reason: '' };
        }

    showBuyModal(unitId) {
        const unit = GAME_DATA.military_assets[unitId];
        if (!unit) return;

        document.getElementById('buy-modal-title').textContent = `خرید ${unit.name}`;
        document.getElementById('buy-unit-name').textContent = unit.name;
        document.getElementById('buy-unit-desc').textContent = unit.ability;
        document.getElementById('buy-unit-cost').textContent = `$${unit.cost.toLocaleString()}`;
        document.getElementById('buy-unit-power').textContent = unit.power;

        const qty = document.getElementById('quantity');
        if (qty) qty.value = 1;
        this.updateTotalCost();

        document.getElementById('buy-modal')?.classList.add('active');
    }

    updateTotalCost() {
        const title = document.getElementById('buy-modal-title')?.textContent || '';
        const name = title.replace('خرید ', '').trim();
        const quantity = Math.min(100, Math.max(1, parseInt(document.getElementById('quantity')?.value || '1', 10)));
        const unit = Object.values(GAME_DATA.military_assets).find(u => u.name === name);
        const total = unit ? unit.cost * quantity : 0;
        const target = document.getElementById('total-cost');
        if (target) target.textContent = `$${total.toLocaleString()}`;
    }

    confirmPurchase() {
        const title = document.getElementById('buy-modal-title')?.textContent || '';
        const name = title.replace('خرید ', '').trim();
        const unitEntry = Object.entries(GAME_DATA.military_assets).find(([_, u]) => u.name === name);
        if (!unitEntry) return;
        const [unitId, unit] = unitEntry;

        const quantity = Math.min(100, Math.max(1, parseInt(document.getElementById('quantity')?.value || '1', 10)));
        const totalCost = unit.cost * quantity;

        if (gameState.player.points < totalCost) return this.showNotification('بودجه کافی نیست!', 'error');
        if (gameState.player.daily_purchases + quantity > gameState.dailyPurchaseLimit) {
            const left = gameState.dailyPurchaseLimit - gameState.player.daily_purchases;
            return this.showNotification(`محدودیت خرید روزانه! باقی‌مانده: ${left}`, 'error');
        }

        gameState.player.points -= totalCost;
        gameState.player.military[unitId] = (gameState.player.military[unitId] || 0) + quantity;
        gameState.player.daily_purchases += quantity;

        this.closeModal();
        this.updateGameDisplay();
        this.loadMilitarySection();
        this.showNotification(`خریداری شد: ${quantity} × ${unit.name}`, 'success');
        this.saveGameData();
    }

    // Economy
    loadEconomySection() {
        this.updateIncomeDisplay();
        this.updateEconomyStats();
    }

    updateIncomeDisplay() {
        const player = gameState.player;
        if (!player?.country) return;

        const sourcesDiv = document.getElementById('income-sources');
        if (!sourcesDiv) return;
        sourcesDiv.innerHTML = '';

        const country = GAME_DATA.countries[player.country];
        Object.values(country.income_methods).forEach(method => {
            const levelBonus = 1 + (player.level * 0.02);
            const techBonus = 1 + (player.technologies.length * 0.05);
            const income = Math.floor(method.base_income * method.multiplier * levelBonus * techBonus);

            const row = document.createElement('div');
            row.className = 'income-source';
            row.innerHTML = `
                <div class="income-name">${method.name}</div>
                <div class="income-amount">$${income.toLocaleString()}</div>
            `;
            sourcesDiv.appendChild(row);
        });
    }

    updateEconomyStats() {
        const now = Math.floor(Date.now() / 1000);
        const last = gameState.player.last_income_time || 0;
        const cd = gameState.player.income_cooldown || 3600;
        const el = document.getElementById('next-income-time');

        if (el) {
            if (now - last < cd) {
                const remaining = cd - (now - last);
                const m = Math.floor(remaining / 60);
                const s = remaining % 60;
                el.textContent = `${m}m ${s}s`;
            } else el.textContent = 'آماده!';
        }
        const dp = document.getElementById('daily-purchases');
        if (dp) dp.textContent = `${gameState.player.daily_purchases}/${gameState.dailyPurchaseLimit}`;
    }

    collectIncome() {
        if (!gameState.player.country) return this.showNotification('ابتدا کشور را انتخاب کنید!', 'error');

        const now = Math.floor(Date.now() / 1000);
        const last = gameState.player.last_income_time || 0;
        const cd = gameState.player.income_cooldown || 3600;
        if (now - last < cd) {
            const rem = cd - (now - last);
            const m = Math.floor(rem / 60), s = rem % 60;
            return this.showNotification(`⏳ ${m} دقیقه و ${s} ثانیه دیگر صبر کنید!`, 'error');
        }

        const country = GAME_DATA.countries[gameState.player.country];
        let total = 0;
        Object.values(country.income_methods).forEach(method => {
            const levelBonus = 1 + (gameState.player.level * 0.02);
            const techBonus = 1 + (gameState.player.technologies.length * 0.05);
            total += Math.floor(method.base_income * method.multiplier * levelBonus * techBonus);
        });

        gameState.player.points += total;
        gameState.player.last_income_time = now;
        gameState.player.experience += Math.floor(total / 20);
        this.checkLevelUp();

        this.updateGameDisplay();
        this.updateEconomyStats();
        this.showNotification(`💰 درآمد: $${total.toLocaleString()}`, 'success');
        this.saveGameData();
    }

    // Technology
    loadTechnologySection() {
        const tree = document.getElementById('tech-tree');
        if (!tree) return;
        tree.innerHTML = '';

        Object.entries(GAME_DATA.tech_tree).forEach(([id, tech]) => {
            const researched = gameState.player.technologies.includes(id);
            const can = this.canResearchTech(id);
            const status = researched ? 'researched' : (can.can ? 'available' : 'locked');

            const card = document.createElement('div');
            card.className = `tech-card ${status}`;
            card.innerHTML = `
                <div class="tech-header">
                    <div class="tech-name">${tech.name}</div>
                    <div class="tech-cost">$${tech.cost.toLocaleString()}</div>
                </div>
                <div class="tech-level">نیاز سطح: ${tech.required_level}</div>
                <div class="tech-requirements">
                    ${tech.prerequisites.length ? `پیش‌نیاز: ${tech.prerequisites.map(p => GAME_DATA.tech_tree[p].name).join(', ')}` : 'بدون پیش‌نیاز'}
                </div>
                ${status === 'available' ? `<button class="research-btn" data-tech="${id}">تحقیق</button>` : ''}
            `;
            if (status === 'available') card.addEventListener('click', () => this.showResearchModal(id));
            tree.appendChild(card);
        });
    }

    canResearchTech(techId) {
        const t = GAME_DATA.tech_tree[techId];
        if (!t) return { can: false, reason: 'نامعتبر' };
        if (gameState.player.level < t.required_level) return { can: false, reason: `نیاز سطح ${t.required_level}` };
        if (gameState.player.technologies.includes(techId)) return { can: false, reason: 'تحقیق شده' };
        for (const p of t.prerequisites) if (!gameState.player.technologies.includes(p)) return { can: false, reason: `نیاز: ${GAME_DATA.tech_tree[p].name}` };
        return { can: true, reason: '' };
    }

    showResearchModal(techId) {
        const tech = GAME_DATA.tech_tree[techId];
        if (!tech) return;

        document.getElementById('research-modal-title').textContent = `تحقیق ${tech.name}`;
        document.getElementById('research-tech-name').textContent = tech.name;
        document.getElementById('research-tech-desc').textContent = `هزینه: $${tech.cost.toLocaleString()} | سطح لازم: ${tech.required_level}`;

        const ul = document.getElementById('research-requirements');
        if (ul) {
            ul.innerHTML = '';
            if (tech.prerequisites.length) tech.prerequisites.forEach(p => { const li = document.createElement('li'); li.textContent = GAME_DATA.tech_tree[p].name; ul.appendChild(li); });
            else { const li = document.createElement('li'); li.textContent = 'بدون پیش‌نیاز'; ul.appendChild(li); }
        }
        document.getElementById('research-modal')?.classList.add('active');
    }

    confirmResearch() {
        const name = document.getElementById('research-tech-name')?.textContent || '';
        const entry = Object.entries(GAME_DATA.tech_tree).find(([_, t]) => t.name === name);
        if (!entry) return;
        const [id, tech] = entry;

        const can = this.canResearchTech(id);
        if (!can.can) return this.showNotification(can.reason, 'error');
        if (gameState.player.points < tech.cost) return this.showNotification('بودجه کافی نیست!', 'error');

        gameState.player.points -= tech.cost;
        gameState.player.technologies.push(id);
        gameState.player.experience += Math.floor(tech.cost / 10);
        this.checkLevelUp();

        this.closeModal();
        this.updateGameDisplay();
        this.loadTechnologySection();
        this.showNotification(`✅ تحقیق شد: ${tech.name}`, 'success');
        this.saveGameData();
    }

    checkLevelUp() {
        const reqs = GAME_DATA.level_requirements;
        let newLevel = gameState.player.level;
        for (let i = 0; i < reqs.length; i++) {
            if (gameState.player.experience >= reqs[i]) newLevel = i + 1;
        }
        if (newLevel > gameState.player.level) {
            gameState.player.level = newLevel;
            this.showNotification(`🎉 سطح ${newLevel}!`, 'success');
        }
    }

    // Missions
    loadMissionsSection() {
        const list = document.getElementById('missions-list');
        if (!list) return;
        list.innerHTML = '';

        GAME_DATA.daily_missions.forEach(m => {
            const progress = this.getMissionProgress(m.id);
            const completed = progress >= m.target;
            const card = document.createElement('div');
            card.className = `mission-card ${completed ? 'completed' : ''}`;
            card.innerHTML = `
                <div class="mission-header">
                    <div class="mission-name">${m.name}</div>
                    <div class="mission-status ${completed ? 'completed' : 'in-progress'}">${completed ? 'کامل' : 'در حال انجام'}</div>
                </div>
                <div class="mission-progress">
                    <div class="progress-bar"><div class="progress-fill" style="width:${Math.min(100, (progress/m.target)*100)}%"></div></div>
                    <div>${progress}/${m.target} - ${m.desc}</div>
                </div>
                <div class="mission-reward">پاداش: $${m.points.toLocaleString()} + ${m.exp} XP</div>
            `;
            list.appendChild(card);
        });
    }

    getMissionProgress(id) {
        switch (id) {
            case 'messages': return gameState.player.total_messages || 0;
            case 'purchases': return gameState.player.daily_purchases || 0;
            case 'battles': return gameState.player.battles_won || 0;
            case 'power': return this.calculateTotalPower();
            default: return 0;
        }
    }

    // Leaderboard (local)
    loadLeaderboardSection() {
        const el = document.getElementById('leaderboard-list');
        if (!el) return;
        el.innerHTML = `
            <div class="leaderboard-entry rank-1">
                <div class="rank">1</div>
                <div class="player-name">${gameState.player.name}</div>
                <div class="power">${this.calculateTotalPower()}</div>
                <div class="level">${gameState.player.level}</div>
                <div class="country">${gameState.player.country ? GAME_DATA.countries[gameState.player.country].name : '-'}</div>
            </div>
        `;
    }

    // Battle
    startAIBattle() {
        const power = this.calculateTotalPower();
        if (power === 0) return this.showNotification('برای نبرد، نیرو تهیه کنید!', 'error');

        const aiPower = Math.floor(power * (0.6 + Math.random()));
        const techBonus = 1 + (gameState.player.technologies.length * 0.05);
        const levelBonus = 1 + (gameState.player.level * 0.03);

        const attack = power * (0.7 + Math.random() * 0.6) * techBonus * levelBonus;
        const defense = aiPower * (0.7 + Math.random() * 0.6);

        if (attack > defense) {
            const damage = Math.min(0.25, (attack - defense) / attack * 0.4);
            const reward = Math.floor(aiPower * damage * 100);
            gameState.player.points += reward;
            gameState.player.battles_won += 1;
            gameState.player.experience += Math.max(15, Math.floor(reward / 10));
            this.showNotification(`⚔️ پیروزی! +$${reward.toLocaleString()}`, 'success');
        } else {
            const damage = Math.min(0.15, (defense - attack) / defense * 0.3);
            const loss = Math.floor(gameState.player.points * damage);
            gameState.player.points = Math.max(0, gameState.player.points - loss);
            gameState.player.battles_lost += 1;
            this.showNotification(`🛡 شکست! -$${loss.toLocaleString()}`, 'error');
        }

        this.updateGameDisplay();
        this.loadMilitarySection();
        this.saveGameData();

        const log = document.getElementById('battle-history');
        if (log) {
            const entry = document.createElement('div');
            entry.className = `battle-entry ${attack > defense ? 'victory' : 'defeat'}`;
            entry.textContent = `${attack > defense ? 'پیروزی' : 'شکست'} | قدرت شما: ${Math.floor(attack)} | دشمن: ${Math.floor(defense)}`;
            log.prepend(entry);
        }
    }

    // Map
    initializeMap() {
        const container = document.getElementById('leaflet-map');
        if (!container || !window.L) return;
        this.map = L.map('leaflet-map', { worldCopyJump: true, attributionControl: false }).setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 5,
            minZoom: 2
        }).addTo(this.map);

        this.selectedCountryLayer = null;
        this.commandMarker = null;

        // Load world countries data with fallback
        this.loadWorldMap();
    }

    loadWorldMap() {
        const urls = [
            'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson',
            'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'
        ];

        const tryLoadMap = async (urlIndex = 0) => {
            if (urlIndex >= urls.length) {
                console.error('All map data sources failed, creating simple world map');
                this.createFallbackMap();
                return;
            }

            try {
                const url = urls[urlIndex];
                const response = await fetch(url);
                const data = await response.json();
                
                let geo;
                if (url.includes('geojson')) {
                    // Direct GeoJSON
                    geo = data;
                } else {
                    // TopoJSON - convert to GeoJSON
                    if (window.topojson && data.objects && data.objects.countries) {
                        geo = topojson.feature(data, data.objects.countries);
                    } else {
                        throw new Error('TopJSON conversion failed');
                    }
                }

                if (!geo || !geo.features) {
                    throw new Error('Invalid map data structure');
                }

                this.countriesLayer = L.geoJSON(geo, {
                    style: {
                        color: 'rgba(255,255,255,0.2)',
                        weight: 1,
                        fillOpacity: 0.15
                    },
                    onEachFeature: (feature, layer) => {
                        layer.on('click', () => this.selectCountryOnMap(feature, layer));
                        layer.on('mouseover', () => layer.setStyle({ fillOpacity: 0.3 }));
                        layer.on('mouseout', () => {
                            if (layer !== this.selectedCountryLayer) {
                                layer.setStyle({ fillOpacity: 0.15 });
                            }
                        });
                    }
                }).addTo(this.map);

                console.log('Map loaded successfully from:', url);
                
            } catch (error) {
                console.warn(`Failed to load map from ${urls[urlIndex]}:`, error);
                tryLoadMap(urlIndex + 1);
            }
        };

        tryLoadMap();
    }

    createFallbackMap() {
        // Create a simple world map with basic country shapes
        const basicCountries = [
            { name: "United States", coords: [[[40, -100], [50, -100], [50, -80], [40, -80], [40, -100]]] },
            { name: "Russia", coords: [[[50, 40], [70, 40], [70, 180], [50, 180], [50, 40]]] },
            { name: "China", coords: [[[20, 100], [40, 100], [40, 120], [20, 120], [20, 100]]] },
            { name: "Iran", coords: [[[25, 50], [40, 50], [40, 65], [25, 65], [25, 50]]] }
        ];

        basicCountries.forEach(country => {
            const polygon = L.polygon(country.coords[0], {
                color: 'rgba(255,255,255,0.2)',
                weight: 1,
                fillOpacity: 0.15
            }).addTo(this.map);
            
            polygon.bindPopup(country.name);
            polygon.on('click', () => {
                this.selectCountryOnMap({ properties: { name: country.name } }, polygon);
            });
        });

        console.log('Fallback map created with basic country shapes');
    }

    loadMapSection() {
        if (this.map) {
            setTimeout(() => this.map.invalidateSize(), 0);
        } else {
            this.initializeMap();
        }
        const info = document.getElementById('map-info');
        if (!info) return;
        if (gameState.player?.command_post) {
            info.textContent = 'Command post is set — select a country to attack or relocate.';
        } else {
            info.textContent = 'Select a country.';
        }
    }

    selectCountryOnMap(feature, layer) {
        if (this.selectedCountryLayer && this.selectedCountryLayer !== layer) {
            this.selectedCountryLayer.setStyle({ color: 'rgba(255,255,255,0.2)', weight: 1, fillOpacity: 0.15 });
        }
        this.selectedCountryLayer = layer;
        layer.setStyle({ color: '#00d4ff', weight: 2, fillOpacity: 0.35 });
        const name = (feature.properties && (feature.properties.name || feature.properties.NAME)) || 'Unknown';
        this.selectedCountryName = name;
        const info = document.getElementById('map-info');
        if (info) info.textContent = `Selected: ${name}`;
        const placeBtn = document.getElementById('place-cp-btn');
        if (placeBtn) placeBtn.disabled = false;
        const attackBtn = document.getElementById('attack-btn');
        if (attackBtn) attackBtn.disabled = this.calculateTotalPower() === 0;
    }

    placeCommandPostFromSelection() {
        if (!this.selectedCountryLayer || !this.map || !gameState.player) return;
        const bounds = this.selectedCountryLayer.getBounds();
        const center = bounds.getCenter();
        gameState.player.command_post = { lat: center.lat, lng: center.lng };
        this.updateCommandMarker(center);
        this.showNotification('📍 Command post established', 'success');
        this.saveGameData();
    }

    updateCommandMarker(latlng) {
        if (!this.map) return;
        if (!this.commandMarker) {
            this.commandMarker = L.marker(latlng, { title: 'Command Post' }).addTo(this.map);
        } else {
            this.commandMarker.setLatLng(latlng);
        }
    }

    restoreCommandMarker() {
        const pos = gameState.player?.command_post;
        if (!pos || !this.map) return;
        this.updateCommandMarker(pos);
        this.map.setView([pos.lat, pos.lng], 3);
    }

    attackSelectedCountry() {
        if (!this.selectedCountryLayer || !this.selectedCountryName) return;
        const power = this.calculateTotalPower();
        if (power === 0) return this.showNotification('برای نبرد، نیرو تهیه کنید!', 'error');
        const aiPower = Math.floor(power * (0.5 + Math.random()));
        const attack = power * (0.8 + Math.random() * 0.5);
        const defense = aiPower * (0.7 + Math.random() * 0.6);
        if (attack > defense) {
            const reward = Math.floor(aiPower * 150);
            gameState.player.points += reward;
            gameState.player.battles_won += 1;
            gameState.player.experience += Math.max(25, Math.floor(reward / 8));
            this.showNotification(`⚔️ Victory over ${this.selectedCountryName}! +$${reward.toLocaleString()}`, 'success');
        } else {
            const loss = Math.floor(gameState.player.points * 0.05);
            gameState.player.points = Math.max(0, gameState.player.points - loss);
            gameState.player.battles_lost += 1;
            this.showNotification(`🛡 Defeat against ${this.selectedCountryName}! -$${loss.toLocaleString()}`, 'error');
        }
        this.updateGameDisplay();
        this.loadMilitarySection();
        this.saveGameData();
    }

    // Common
    closeModal() {
        document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notifications');
        if (!container) return;
        const n = document.createElement('div');
        n.className = `notification ${type}`;
        n.textContent = message;
        container.appendChild(n);
        setTimeout(() => n.remove(), 5000);
    }

    // Persistence
    loadGameData() {
        try {
            const saved = localStorage.getItem('militaryGame');
            if (!saved) return;
            const data = JSON.parse(saved);
            if (!data?.player) return;
            gameState.player = data.player;

            if (gameState.player.country_selected) {
                this.showScreen('game');
                this.showGameSection('dashboard');
                this.updateGameDisplay();
            } else {
                this.showScreen('country');
                this.populateCountries();
            }
        } catch {}
    }

    saveGameData() {
        try {
            localStorage.setItem('militaryGame', JSON.stringify({ player: gameState.player, ts: Date.now() }));
        } catch {}
    }
}

// Auto-save
setInterval(() => {
    if (window.game && gameState.player) window.game.saveGameData();
}, 30000);

// Init
document.addEventListener('DOMContentLoaded', () => {
    window.game = new MilitaryGame();
});
// =======================
// Map Conquest Mechanics
// =======================
function colorCountriesByOwnership() {
  if (!window.__countryLayers) return;
  Object.entries(window.__countryLayers).forEach(([name, layer]) => {
    const owned = player.owned_territories?.includes(name);
    const selected = window.__selectedCountry?.properties?.name === name;
    layer.setStyle({
      fillColor: owned ? '#34d399' : selected ? '#60a5fa' : '#9ca3af',
      fillOpacity: owned ? 0.55 : selected ? 0.45 : 0.25,
      color: owned ? '#10b981' : '#6b7280',
      weight: owned ? 1.5 : 1,
    });
  });
}

function isAdjacent(targetName) {
  if (!player.owned_territories?.length) return false;
  const targetLayer = window.__countryLayers[targetName];
  if (!targetLayer) return false;
  const tb = targetLayer.getBounds();
  return player.owned_territories.some(name => {
    const l = window.__countryLayers[name];
    if (!l) return false;
    const b = l.getBounds();
    return b.intersects(tb) || (b.overlaps ? b.overlaps(tb) : false);
  });
}

function placeCommandPostFromSelection() {
  if (!window.__selectedCountry) return;
  const name = window.__selectedCountry.properties.name;
  if (player.owned_territories?.length) {
    showToast('You already placed your base.', 'info');
    return;
  }
  player.command_post = name;
  player.owned_territories = [name];
  saveGameData();
  updateMapInfo();
  colorCountriesByOwnership();
  showToast(`Base established in ${name}.`, 'success');
}

function attackSelectedCountry() {
  if (!window.__selectedCountry) return;
  const name = window.__selectedCountry.properties.name;
  if (player.owned_territories.includes(name)) {
    showToast('You already control this country.', 'info');
    return;
  }
  if (!isAdjacent(name)) {
    showToast('You can only attack neighboring countries.', 'warning');
    return;
  }
  const yourPower = (player.attack_power || 10) + (player.level || 1) * 2;
  const aiPower = Math.max(6, 8 + Math.floor(Math.random() * 8));
  const win = Math.random() < yourPower / (yourPower + aiPower);
  if (win) {
    player.owned_territories.push(name);
    saveGameData();
    colorCountriesByOwnership();
    updateMapInfo();
    showToast(`Victory! You annexed ${name}.`, 'success');
  } else {
    player.score = Math.max(0, (player.score || 0) - 5);
    saveGameData();
    showToast('Attack failed. Your forces are regrouping.', 'error');
  }
}

function updateMapInfo() {
  const infoEl = document.getElementById('map-info');
  if (!infoEl) return;
  const ownedCount = player.owned_territories?.length || 0;
  const baseName = player.command_post || 'None';
  const selName = window.__selectedCountry?.properties?.name || '—';
  infoEl.innerHTML = `<b>Base:</b> ${baseName} &nbsp;|&nbsp; <b>Owned:</b> ${ownedCount} &nbsp;|&nbsp; <b>Selected:</b> ${selName}`;

  const placeBtn = document.getElementById('place-cp-btn');
  const attackBtn = document.getElementById('attack-btn');
  if (placeBtn) {
    placeBtn.disabled = !(window.__selectedCountry && !player.command_post);
  }
  if (attackBtn) {
    attackBtn.disabled = !(window.__selectedCountry &&
      player.command_post &&
      !player.owned_territories.includes(selName) &&
      isAdjacent(selName));
  }
}

function loadMapSection() {
  console.log(">>> loadMapSection triggered");
  const mapWrapper = document.getElementById('leaflet-map');
  if (!mapWrapper) return;
  if (!window.__leafletMap) {
    window.__leafletMap = L.map('leaflet-map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap'
    }).addTo(window.__leafletMap);

    window.__countryLayers = {};
    // Use a simpler, more reliable world map data source
    fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
      .then(r => r.json())
      .then(geo => {
        if (!geo || !geo.features) {
          console.error('Failed to load map data');
          return;
        }
        L.geoJSON(geo, {
          style: { weight: 1, color: '#6b7280', fillColor: '#9ca3af', fillOpacity: 0.25 },
          onEachFeature: (feature, layer) => {
            const name = feature.properties.name || feature.properties.admin;
            feature.properties.name = name;
            window.__countryLayers[name] = layer;
            layer.on('click', () => {
              window.__selectedCountry = feature;
              colorCountriesByOwnership();
              updateMapInfo();
            });
          }
        }).addTo(window.__leafletMap);
        colorCountriesByOwnership();
        updateMapInfo();
      });
  } else {
    setTimeout(() => {
      window.__leafletMap.invalidateSize();
      colorCountriesByOwnership();
      updateMapInfo();
    }, 0);
  }

  document.getElementById('place-cp-btn')
    ?.addEventListener('click', placeCommandPostFromSelection);
  document.getElementById('attack-btn')
    ?.addEventListener('click', attackSelectedCountry);
}
