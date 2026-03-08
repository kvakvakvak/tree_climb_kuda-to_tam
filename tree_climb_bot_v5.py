import random
import json
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# ==============================================================
# АААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
# ==============================================================

GROUP_TOKEN = "vk1.a.-BTzntO46GkOubI4_KRgcvEL41LVqqoFWO19UtBTEOoRDtCyp1B9ZXhPI4gVG7ZeqJbJi-_BJ660LMkUo130Wa-6FPS_lmvtI-LZk74c5P3Pe9vD0egBeGH5TnBBk5hJDD99EyCBPrKbFR1zH3Fk0OybWeL8EYdEwHitDFLia9EP4BfqT_S5pHff_Hg3MXKaB8zxeyKqTrQKjLESABnGOQ"
GROUP_ID = 216712536  # ID группы (число)

# ==============================================================

vk_session = vk_api.VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

def send(peer_id, message, keyboard=None):
    params = {"peer_id": peer_id, "message": message, "random_id": 0}
    if keyboard:
        params["keyboard"] = keyboard
    vk.messages.send(**params)

# ==============================================================
# ААААААААААААААААААА МАСТЕР ИГРЫ АААААААААААААААААААААААААААААА
# ==============================================================

GM_CLIMB_FLAVOR = [
    "Ветер шуршит в листве. Где-то вдалеке кричит птица.",
    "Кора под лапами тёплая от солнца.",
    "Муравьи ползут по стволу. Им нет дела до котов.",
    "Белка метнулась по соседней ветке и исчезла.",
    "Откуда-то пахнет смолой. Приятный запах.",
    "Ветка чуть скрипнула, но держит, вроде.",
    "Внизу кто-то прошуршал в траве.",
    "Облако закрыло солнце. Стало прохладнее.",
    "На соседнем дереве сидит ворона и смотрит. Наверное, ждет, когда кто-то сорвется?",
    "Паутина блеснула между веток.",
    "Жук-короед выглянул из коры и спрятался обратно.",
    "От сюда вся поляна как на подушечке лапы. Ощущаешь себя самым высоким.",
    "Где-то внизу хрустнула ветка. Может, ветер, а может и не ветер...",
    "Солнечный луч пробился сквозь крону. Приятно теплит шерсть.",
    "Ствол здесь шершавый, когти цепляются хорошо.",
    "Лишайник на коре мягкий и чуть скользкий.",
    "Два муравья тащат гусеницу вверх по стволу. Ну, рудяги!",
    "Птица сорвалась с ветки и поспешила прочь от котов.",
    "Посещает навязчивая мысль ослабить хватку. Интересно, какого это, когда ломается лапа?",
    "Сверху донёсся стук дятла.",
    "Лёгкий порыв ветра шевелит усы.",
    "Между веток натянута старая паутина, но паука нет.",
    "На коре кто-то оставил глубокие царапины. Это был точно не кот.",
    "Откуда-то ветром доносится запах цветов.",
    "Настырная мошка кружит перед носом. Костекрад тебя дери, в глаз попала!",
    "Ствол слегка вибрирует от ветра. Чувствуется лапами.",
    "Что-то сорвалось с ветки и полетело вниз, стукнув по дороге о ствол.",
    "Где-то каркнула ворона. Аж по ушам режет.",
    "Кора в этом месте отслаивается. Под ней — жучки.",
    "Сойка прошмыгнула между ветками и затихла.",
]

GM_DESCEND_FLAVOR = [
    "Спускаться оказывается труднее, чем казалось.",
    "Лапы нащупывают следующую ветку. Есть!",
    "Внизу трава кажется обманчиво мягкой.",
    "Кора здесь более гладкая, осторожнее.",
    "Ветер качает ветки. Не стоит торопиться.",
    "Земля приближается.",
    "Когти скребут по коре. Медленно, медленно, медленно.",
    "Падает сук — летит долго. Не хочется также.",
    "Чем ниже, тем толще ветки, надежнее и спокойнее.",
    "Снизу тянет прохладой. Тень от кроны густая.",
    "Паук удирает в сторону — потревожили!",
    "Ветка прогибается, но не трещит. Нормально, тихонечко.",
    "Ствол здесь во мху — мягко, но скользко.",
    "Запах земли всё ближе.",
    "Муравьиная тропа идёт вниз параллельно.",
]

GM_EXPLORE_FLAVOR = [
    "Тишина. Только шелест листьев.",
    "Если присмотреться, тут много интересного.",
    "Дерево старое, в нём должно быть полно щелей и дупел.",
    "Свет пробивается через крону пятнами.",
    "Кора вся в трещинах. Стоит заглянуть.",
    "Мох покрывает кору. Под ним может быть что-то.",
    "В тени ветвей прохладно и тихо.",
    "Ветви переплетаются. Есть где порыскать.",
    "Пахнет грибами — где-то на стволе трутовик.",
    "Лишайник бахромой свисает с ветки. Красиво, но бесполезно.",
]

GM_WAIT_FLAVOR = [
    "Иногда лучше просто подождать.",
    "Ветер стихает. Можно передохнуть.",
    "Короткая передышка не помешает.",
    "Тишина, и только сердце стучит.",
    "Лапы немного дрожат. Передышка — хорошая идея.",
    "Отдых.",
    "Закрыть глаза на секунду. Вдохнуть. Выдохнуть.",
    "Облако проплывает вверху. Спешить некуда.",
    "На миг кажется, что дерево дышит в такт.",
    "Тёплый ветер. Шерсть продувает. Хорошо...",
]

GM_CLIMB_MINOR_INJURY_FLAVOR = [
    "Неловкое движение не обошлось без последствий.",
    "Зацепило ощутимо неудачно.",
    "Лапа соскользнула на мгновение.",
    "Кора подвела. Мелочь, но неприятно.",
    "Чуть замешкался — и вот результат.",
    "По веткам прягать — не по тропинкам скакать!",
    "Не повезло. Бывает.",
    "Один неверный шаг — вот и мелкая неприятность.",
    "Ветка качнулась не вовремя.",
    "На удар сердца теряется равновесие.",
]

GM_EXPLORE_FALL_RISK = [
    "Ветка под лапами прогибается. Стоять тут долго — не лучшая идея.",
    "Опора становится ненадёжной. Кора трескается.",
    "Лапы начинают скользить. Слишком долго на одном месте.",
    "Ветка скрипит. Пора двигаться.",
    "Дерево покачивается. Чем дольше тут торчишь, тем хуже.",
    "Равновесие держать всё сложнее.",
    "Кажется, ветки тут уже не такие прочные.",
    "Когти теряют сцепление с корой.",
]

def gm_says(flavor_list):
    return random.choice(flavor_list)

# ==============================================================
# ААААААААААААААААА ПАРАМЕТРЫ ПЕРСОНАЖА АААААААААААААААААААААААА
# ==============================================================

HUNGER_LEVELS = {
    "сыт":                {"percent": 100, "label": "сыт"},
    "голоден":            {"percent": 85,  "label": "голоден"},
    "сильно_голоден":     {"percent": 50,  "label": "сильно голоден"},
    "смертельно_голоден": {"percent": 30,  "label": "смертельно голоден"},
}

SIZE_LEVELS = {
    "малорослый":  {"max_hp": 100, "label": "малорослый"},
    "стандартный":  {"max_hp": 100, "label": "стандартный"},
    "высокий":      {"max_hp": 100, "label": "высокий"},
    "здоровяк":     {"max_hp": 125, "label": "здоровяк"},
}

def calculate_max_hp(size_key):
    return SIZE_LEVELS[size_key]["max_hp"]

def calculate_current_hp(hunger_key, size_key):
    max_hp = SIZE_LEVELS[size_key]["max_hp"]
    percent = HUNGER_LEVELS[hunger_key]["percent"]
    return int(max_hp * percent / 100)

# ==============================================================
# ААААААААААААААААААА ТРАВМЫ ААААААААААААААААААААААААААААААААААА
# ==============================================================

CAT_PAWS = ["передняя правая лапа", "передняя левая лапа",
            "задняя правая лапа", "задняя левая лапа"]

INJURIES_MINOR = [
    {"name": "царапина",   "dmg": (3, 5),  "ongoing": 0.0,  "ongoing_dmg": (0, 0)},
    {"name": "ссадина",    "dmg": (1, 3),  "ongoing": 0.05, "ongoing_dmg": (1, 2)},
    {"name": "ушиб",       "dmg": (1, 4),  "ongoing": 0.08, "ongoing_dmg": (1, 2)},
    {"name": "синяк",      "dmg": (2, 4),  "ongoing": 0.05, "ongoing_dmg": (1, 2)},
    {"name": "гематома",   "dmg": (4, 5),  "ongoing": 0.10, "ongoing_dmg": (1, 3)},
    {"name": "занозы в подушечках лап", "dmg": (1, 3), "ongoing": 1.0, "ongoing_dmg": (1, 1)},
    {"name": "разодранные подушечки лап", "dmg": (1, 3), "ongoing": 1.0, "ongoing_dmg": (1, 1)},
]

INJURIES_MEDIUM = [
    {"name": "растяжение",       "dmg": (2, 7),  "ongoing": 0.20, "ongoing_dmg": (2, 5), "agility_penalty": 3},
    {"name": "вывих",            "dmg": (5, 10),  "ongoing": 0.25, "ongoing_dmg": (3, 6), "agility_penalty": 3},
    {"name": "надорванный коготь", "dmg": (2, 10),  "ongoing": 0.22, "ongoing_dmg": (2, 5), "agility_penalty": 3},
]

INJURY_FRACTURE = {"name": "перелом", "dmg": (10, 21), "ongoing": 0.40, "ongoing_dmg": (5, 10)}

INJURY_MULTIPLE_ABRASIONS = {"name": "множественные ссадины", "dmg": (4, 5),
                              "ongoing": 0.08, "ongoing_dmg": (1, 2)}

def _roll_dislocation():
    paw = random.choice(CAT_PAWS)
    dmg = random.randint(20, 33)
    return {"name": f"вывернутая конечность ({paw})",
            "dmg": dmg, "ongoing": 0.30, "ongoing_dmg": (5, 10)}

def _roll_tail_fracture():
    dmg = random.randint(15, 29)
    return {"name": "перелом хвоста", "dmg": dmg,
            "ongoing": 0.25, "ongoing_dmg": (3, 7),
            "agility_penalty": 20}

def roll_injury_minor():
    chosen = random.choice(INJURIES_MINOR)
    dmg = random.randint(*chosen["dmg"])
    return {"name": chosen["name"], "dmg": dmg,
            "ongoing": chosen["ongoing"], "ongoing_dmg": chosen["ongoing_dmg"]}

def roll_injury_medium():
    chosen = random.choice(INJURIES_MEDIUM)
    dmg = random.randint(*chosen["dmg"])
    result = {"name": chosen["name"], "dmg": dmg,
              "ongoing": chosen["ongoing"], "ongoing_dmg": chosen["ongoing_dmg"]}
    if "agility_penalty" in chosen:
        result["agility_penalty"] = chosen["agility_penalty"]
    return result

def roll_fracture():
    dmg = random.randint(*INJURY_FRACTURE["dmg"])
    return {"name": INJURY_FRACTURE["name"], "dmg": dmg,
            "ongoing": INJURY_FRACTURE["ongoing"],
            "ongoing_dmg": INJURY_FRACTURE["ongoing_dmg"]}

def roll_multiple_abrasions():
    dmg = random.randint(*INJURY_MULTIPLE_ABRASIONS["dmg"])
    return {"name": INJURY_MULTIPLE_ABRASIONS["name"], "dmg": dmg,
            "ongoing": INJURY_MULTIPLE_ABRASIONS["ongoing"],
            "ongoing_dmg": INJURY_MULTIPLE_ABRASIONS["ongoing_dmg"]}

def roll_climb_injury():
    roll = random.randint(1, 100)
    if roll <= 60:
        return roll_injury_minor()
    elif roll <= 90:
        return roll_injury_medium()
    else:
        return roll_fracture()

def roll_fall_injuries_tier3():
    """Падение с 3-го яруса: всегда перелом или вывернутая конечность."""
    injuries = []
    if random.random() < 0.95:
        injuries.append(roll_fracture())  #95% перелом
    else:
        injuries.append(_roll_dislocation())  #5% вывернутая конечность
    injuries.append(roll_multiple_abrasions())
    if random.random() < 0.35:
        injuries.append(_roll_tail_fracture())
    injuries.append(roll_injury_minor())
    return injuries, False

def roll_fall_injuries_tier2():
    """Падение со 2-го яруса: в основном мелкие и переломы, вывернутая лапа — очень редко. 60% преземление на лапы - остальное перелом/вывих"""
    land_on_paws = random.random() < 0.70
    injuries = []
    if land_on_paws:
        for _ in range(5):
            injuries.append(roll_injury_minor())
        return injuries, True
    else:
        r = random.random()
        if r < 0.55:
            injuries.append(roll_fracture())          # 55% перелом
        elif r < 0.60:
            injuries.append(_roll_dislocation())      # 5% вывернутая конечность
        else:
            injuries.append(roll_injury_medium())     # остальное — средние травмы

        injuries.append(roll_multiple_abrasions())
        for _ in range(3):
            injuries.append(roll_injury_minor())
        if random.random() < 0.25:
            injuries.append(_roll_tail_fracture())
        return injuries, False

def roll_fall_injuries_tier1():
    """Падение с 1-го яруса: в основном мелкие, минимальный шанс вывиха."""
    injuries = []
    if random.random() < 0.08:
        injuries.append(roll_injury_medium())
    injuries.append(roll_multiple_abrasions())
    for _ in range(4):
        injuries.append(roll_injury_minor())
    return injuries, True

def check_ongoing_injuries(climber):
    lines = []
    total_dmg = 0
    for inj in climber.injuries:
        if inj["ongoing"] > 0 and random.random() < inj["ongoing"]:
            extra = random.randint(*inj["ongoing_dmg"])
            total_dmg += extra
            msg = random.choice([
                " Боль даёт о себе знать.",
                " Травма напоминает о себе.",
                " Неприятные ощущения возвращаются.",
                " Боль снова беспокоит.",
                " Травма ноет сильнее, чем хотелось бы.",
                " На пару ударов сердца становится особенно больно."
            ])
            lines.append(f"{msg} -{extra} ЕЗ")
    return lines, total_dmg

# ==============================================================
# ААААААААААААААА МЕДИТАЦИЯ ЕБАЛА Я В РОТ Я УБЬЮ СЕБЯ УБЬЮ СЕБЯ
# ==============================================================

MEDITATION_MIN = 3 * 60
MEDITATION_MAX = 5 * 60
MEDITATION_HEAL = (5, 15)
MEDITATION_LUCK_BONUS = -5

MEDITATION_START_TEXTS = [
    "{name} закрывает глаза на верхушке. Ветер треплет шерсть.",
    "{name} устраивается на верхней ветке и замирает. Тишина.",
    "{name} прижимается к стволу и закрывает глаза. Мир внизу далеко.",
]
MEDITATION_COMPLETE_TEXTS = [
    "{name} открывает глаза. Мысли ясные, тело отдохнуло.",
    "{name} глубоко вдыхает и поднимается. Стало легче.",
    "{name} чувствует себя собраннее. Пора вниз.",
]

MEDITATION_SHINY_ITEMS = [
    "малый драгоценный камень",
    "крупный драгоценный камень",
    "мелкий мусор",
    "стекляшка",
]

# ==============================================================
# АААААААААААААААА ИНВЕНТАРЬ (ресурсы) ААААААААААААААААААААААААА
# ==============================================================

MAX_RESOURCE_SLOTS = 5
BAG_RESOURCE_SLOTS = 15

DROP_BREAKAGE = {
    "гибкая палка":  {"chance": 0.40, "result": [("прутик", 2, 3)]},
    "прочная палка":  {"chance": 0.25, "result": [("прутик", 2, 3)]},
    "малая ракушка":  {"chance": 0.35, "result": [("осколки ракушки", 1, 1)]},
}

def drop_item_from_tree(item_name):
    if item_name.startswith("яйцо"):
        return [], f"{item_name} разбивается при падении."
    rule = DROP_BREAKAGE.get(item_name)
    if rule and random.random() < rule["chance"]:
        results = []
        desc_parts = []
        for res_name, cmin, cmax in rule["result"]:
            count = random.randint(cmin, cmax)
            for _ in range(count):
                results.append(res_name)
            desc_parts.append(f"{count}x {res_name}")
        return results, f"{item_name} падает и ломается: {', '.join(desc_parts)}."
    return [item_name], f"{item_name} падает на землю."

# ==============================================================
# ААААААААААААААААА РЕСУРСЫ НА ВЕТКАХ АААААААААААААААААААААААААА
# ==============================================================

ITEMS_ON_BRANCHES = ["прутик", "гибкая палка", "прочная палка", "капля смолы"]
ITEMS_IN_BARK = ["камешек", "малый драгоценный камень", "глина",
                 "малая ракушка", "мелкий мусор", "стекляшка"]

# ==============================================================
# ААААААААААААААААААААА ДУПЛА АААААААААААААААААААААААААААААААААА
# ==============================================================

EGG_CLUTCHES = {
    "лесной голубь":             {"min": 1, "max": 2, "usual_min": 2, "usual_max": 2},
    "большой пёстрый дятел":    {"min": 4, "max": 8, "usual_min": 5, "usual_max": 7},
    "поползень":                   {"min": 4, "max": 12, "usual_min": 6, "usual_max": 9},
    "синица":                     {"min": 8, "max": 16, "usual_min": 9, "usual_max": 13},
}

def roll_clutch(bird_key):
    info = EGG_CLUTCHES[bird_key]
    if random.random() < 0.80:
        return random.randint(info["usual_min"], info["usual_max"])
    return random.randint(info["min"], info["max"])

def _eggs_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return "яйцо"
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "яйца"
    return "яиц"

def generate_hollow():
    roll = random.random()
    if roll < 0.25:
        return "Дупло. Пусто, пахнет прелыми листьями.", [], 0.0, 0
    elif roll < 0.45:
        possible = ["пух", "перья неизвестной птицы", "коготь"]
        loot = [item for item in possible if random.random() < 0.60]
        if not loot:
            loot = [random.choice(possible)]
        return (f"Дупло со старым гнездом. Внутри: {', '.join(loot)}.",
                [("items", loot)], 0.0, 0)
    elif roll < 0.60:
        return ("Из дупла высовывается птица. Клюёт в морду, орёт и улетает. "
                "Лапы чуть не соскальзывают.",
                [], 0.15, 1)
    elif roll < 0.85:
        bird = random.choice(list(EGG_CLUTCHES.keys()))
        count = roll_clutch(bird)
        w = _eggs_word(count)
        # пример: "В дупле гнездо лесного голубя. 3 яйца. Можно забрать."
        return (f"В дупле гнездо ({bird}). {count} {w}. Можно забрать.",
                [("eggs", bird, count)], 0.0, 0)
    else:
        bird = random.choice(list(EGG_CLUTCHES.keys()))
        count = roll_clutch(bird)
        w = _eggs_word(count)
        # пример: "В дупле сидит лесной голубь на 1 яйце и шипит на каждого, кто лезет ближе."
        return (f"В дупле сидит {bird} "
                "и явно не хочет, чтобы кто-то лез ближе.",
                [("brooding", bird, count)], 0.0, 0)


# ==============================================================
# ААААААААААА ЯРУСЫ (d100) — ПЕРЕСЧИТАННЫЕ ПОРОГИ + ШАНСЫ РЕСУРСОВ
# ==============================================================
# Нижний: мин. шансы, НЕТ дупел
# Средний: дупло ~33%, ресурсы средние
# Верхний: как было (высокие шансы)

TIERS = [
    {
        "name": "Нижний ярус", "base_fall_chance": 25,
        "bark_chance": 0.15, "find_chance": 0.20, "hollow_chance": 0.0,
        "climb_descriptions": [
            "Когти впиваются в кору. Нижние ветви рядом.",
            "Нижние ветки толстые, держат хорошо.",
            "Первая развилка. Ствол покрыт мхом, лапы не скользят.",
        ],
        "descend_descriptions": [
            "Спуск на землю. Последний прыжок — лапы на твёрдой почве.",
            "Соскальзывает по стволу вниз. Земля.",
            "Перебирается на нижнюю ветку и спрыгивает.",
        ],
    },
    {
        "name": "Средний ярус", "base_fall_chance": 40,
        "bark_chance": 0.30, "find_chance": 0.40, "hollow_chance": 0.33,
        "climb_descriptions": [
            "Ветви тоньше, ветер покачивает крону. Земля далеко внизу.",
            "Кора более гладкая, приходится цепляться сильнее.",
            "С ветки на ветку. Дерево поскрипывает под весом.",
        ],
        "descend_descriptions": [
            "Осторожно перебирается ниже. Ветки здесь надёжнее.",
            "Спускается, цепляясь за каждую развилку.",
            "Сползает по стволу на нижний ярус.",
        ],
    },
    {
        "name": "Верхний ярус", "base_fall_chance": 55,
        "bark_chance": 0.15, "find_chance": 0.40, "hollow_chance": 0.10,
        "climb_descriptions": [
            "Тонкие ветки прогибаются. Видно далеко вокруг.",
            "Почти верхушка. Ветки потрескивают.",
            "Крона раскачивается на ветру. Высоко.",
        ],
        "descend_descriptions": [
            "Начинает спуск с верхушки. Ветки тонкие, каждый шаг осторожный.",
            "Медленно перебирается вниз. Крона качается.",
            "Цепляется за ствол и сползает ниже.",
        ],
    },
]

FRAGILITY_MULTIPLIER = {1: 1.0, 2: 1.10, 3: 1.25, 4: 1.50}
FRAGILITY_FLAVOR = {
    2: ["Ветка прогибается под двойным весом.", "Вдвоём тесновато."],
    3: ["Ветка трещит — троим ей тяжело.", "Дерево покачивается от возни."],
    4: ["Ветка опасно прогибается. Четверо — слишком.", "Дерево стонет под весом четырёх."],
}

SAFETY_DAMAGE_REDUCTION = 0.5

CATCH_FLAVOR_SAME = [
    "{fallen} срывается, но {catcher} успевает поймать за шкирку.",
    "{fallen} летит вниз, но {catcher} вцепляется в холку и удерживает.",
    "{fallen} теряет опору, {catcher} перехватывает и не даёт упасть.",
    "{fallen} соскальзывает, но {catcher} успевает ухватить и притянуть обратно.",
    "{fallen} едва не падает, {catcher} вовремя подхватывает.",
    "{fallen} срывается с ветки, {catcher} цепляет за хвост и удерживает."
]

CATCH_FLAVOR_BELOW = [
    "{fallen} срывается с ветки, {catcher} ловит снизу и принимает на себя часть удара.",
    "{fallen} падает ниже, {catcher} успевает подставиться и смягчает падение.",
    "{fallen} летит вниз, {catcher} подхватывает на нижней ветке.",
    "{fallen} теряет опору, {catcher} перехватывает на ярусе ниже.",
    "{fallen} срывается, но {catcher} останавливает падение.",
    "{fallen} падает, {catcher} ловит на ветке ниже."
]

CATCH_FAIL_FLAVOR = [
    "Никто не успевает поймать {fallen}.",
    "{fallen} проносится мимо — слишком быстро.",
    "Лапы соскальзывают — {fallen} не удержать.",
]

EXPLORE_LIMIT_PER_TIER = 3

# Шанс мелкой травмы при подъёме для НЕ-древолазов
# На 2-й ярус: 50% если ловкость < 36
# На 3-й ярус: 85% если ловкость < 36
CLIMB_MINOR_INJURY_CHANCE_TIER2 = 0.50
CLIMB_MINOR_INJURY_CHANCE_TIER3 = 0.85

# Шанс падения при осмотре (НЕ-древолазы)
EXPLORE_FALL_BASE = {
    1: [20, 34, 47],  # средний ярус: 1,2,3 осмотр
    2: [30, 48, 65],  # верхний ярус
}

# ==============================================================
# АААААААААААААААААААААА КЛАСС ПЕРСОНАЖА ААААААААААААААААААААААА
# ==============================================================

class Climber:
    def __init__(self, user_id, char_name, skill=0,
                 hunger="сыт", size="стандартный",
                 is_treeclimber=False, agility=0,
                 custom_hp=None, has_bag=False):
        self.user_id = user_id
        self.name = char_name
        self.skill = skill
        self.is_treeclimber = is_treeclimber
        self.agility = max(-1, min(49, agility))
        self.has_bag = has_bag

        self.max_hp = calculate_max_hp(size)
        if custom_hp is not None:
            self.hp = max(1, min(self.max_hp, custom_hp))
        else:
            self.hp = calculate_current_hp(hunger, size)
        self.hunger_label = HUNGER_LEVELS[hunger]["label"]
        self.size_label = SIZE_LEVELS[size]["label"]

        self.current_tier = -1
        self.resources = []
        self.ground_stash = []
        self.is_active = True
        self.is_out = False
        self.extra_fall_chance = 0
        self.luck_bonus = 0
        self.injuries = []

        self.meditating = False
        self.meditation_start = 0
        self.meditation_duration = 0
        self.meditated = False
        self.meditation_shiny = None

        self.direction = "up"
        self.reached_top = False
        self.finished = False

        self.pending_brooding = None
        self.pending_eggs = None
        self.pending_found = None

        self.moving = False
        self.move_target = -1
        self.move_steps_left = 0

        self.explore_counts = {}

    @property
    def alive(self):
        return self.hp > 0

    @property
    def tier_name(self):
        if self.current_tier < 0:
            return "земля"
        return TIERS[self.current_tier]["name"]

    @property
    def max_slots(self):
        return BAG_RESOURCE_SLOTS if self.has_bag else MAX_RESOURCE_SLOTS

    @property
    def res_free(self):
        return self.max_slots - len(self.resources)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def apply_agility_penalty(self, penalty):
        self.agility = max(-1, self.agility - penalty)

    def injuries_summary(self):
        if not self.injuries:
            return ""
        return ", ".join(inj["name"] for inj in self.injuries)

    def check_out(self):
        if self.hp <= 0:
            self.hp = 0
            self.is_out = True
            self.is_active = False
            return True
        return False

    def res_contents(self):
        if not self.resources:
            return "пусто"
        return ", ".join(self.resources)

    def fall_chance_modifier(self):
        mod = 0
        mod -= int(self.agility * 0.6)
        if self.is_treeclimber:
            mod -= 25
        return mod

    def get_explore_count(self, tier_idx):
        return self.explore_counts.get(tier_idx, 0)

    def add_explore(self, tier_idx):
        self.explore_counts[tier_idx] = self.explore_counts.get(tier_idx, 0) + 1

    def status_line(self):
        flags = ""
        if self.is_out:
            flags += " [на земле]"
        if self.finished:
            flags += " [на земле]"
        if self.meditating:
            flags += " [медитация]"
        if self.moving:
            flags += f" [на дереве: {self.move_steps_left} х.]"
        if self.extra_fall_chance > 0:
            flags += " [!]"
        d = ""
        if (self.is_active and not self.meditating
                and self.current_tier >= 0 and self.direction == "down"):
            d = " [вниз]"
        tc = " древолаз" if self.is_treeclimber else ""
        inj = ""
        if self.injuries:
            inj = f" | травмы: {self.injuries_summary()}"
        ground = ""
        if self.ground_stash:
            ground = f" | на земле: {len(self.ground_stash)}"
        return (f"  {self.name}{flags}{tc} — {self.tier_name}{d} | "
                f"ЕЗ {self.hp}/{self.max_hp} | ловк. {self.agility}{inj} | "
                f"ресурсы: {len(self.resources)}/{self.max_slots}{ground}")

# ==============================================================
# ААААААААААААААААААА НАСТРОЙКА ПЕРСОНАЖА АААААААААААААААААААААА
# ==============================================================

class PendingSetup:
    def __init__(self, user_id):
        self.user_id = user_id
        self.char_name = None
        self.hunger = None
        self.size = None
        self.is_treeclimber = None
        self.agility = None
        self.custom_hp = None
        self.has_bag = None
        self.step = "name"

# ==============================================================
# АААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
# ==============================================================

class CoopTreeClimb:
    def __init__(self, host_id):
        self.host_id = host_id
        self.climbers = {}
        self.turn_order = []
        self.current_turn_idx = 0
        self.phase = "lobby"
        self.setup_queue = []
        self.setup_index = 0

    # -- Лобби --

    def add_player(self, user_id):
        if self.phase != "lobby":
            return "Уже нельзя!"
        if len(self.setup_queue) >= 4:
            return "Максимум 4."
        for ps in self.setup_queue:
            if ps.user_id == user_id:
                return "Уже в группе."
        self.setup_queue.append(PendingSetup(user_id))
        self.turn_order.append(user_id)
        n = len(self.setup_queue)
        return f"Персонаж присоединяется. ({n}/4)"

    # -- Характеристики --

    def begin_setup(self, user_id):
        if user_id != self.host_id:
            return None, None
        if not self.setup_queue:
            return "Нужен хотя бы один персонаж.", None
        self.phase = "setup"
        self.setup_index = 0
        return self._prompt_setup()

    def _prompt_setup(self):
        if self.setup_index >= len(self.setup_queue):
            return self._finish_setup()
        ps = self.setup_queue[self.setup_index]

        if ps.step == "name":
            return (f"Персонаж {self.setup_index + 1}.\n"
                    f"Имя: напишите имя персонажа в чат."), None

        elif ps.step == "agility":
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"Напишите число ловкости вашего персонажа:"), None

        elif ps.step == "treeclimber":
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"  Ловкость: {ps.agility}\n"
                    f"Персонаж — древолаз?"), self._treeclimber_kb()

        elif ps.step == "bag":
            tc = "да" if ps.is_treeclimber else "нет"
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"  Ловкость: {ps.agility} | Древолаз: {tc}\n"
                    f"У персонажа есть сумочка для ресурсов?"), self._bag_kb()

        elif ps.step == "hunger":
            tc = "да" if ps.is_treeclimber else "нет"
            slots = BAG_RESOURCE_SLOTS if ps.has_bag else MAX_RESOURCE_SLOTS
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"  Ловкость: {ps.agility} | Древолаз: {tc}\n"
                    f"  Слоты ресурсов: {slots}\n"
                    f"Уровень сытости:"), self._hunger_kb()

        elif ps.step == "size":
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"Рост:"), self._size_kb()

        elif ps.step == "hp_lowered":
            max_hp = calculate_max_hp(ps.size)
            cur_hp = calculate_current_hp(ps.hunger, ps.size)
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"  ЕЗ: {cur_hp}/{max_hp}\n"
                    f"Понижены ли у персонажа ЕЗ?"), self._hp_lowered_kb()

        elif ps.step == "hp_custom":
            max_hp = calculate_max_hp(ps.size)
            return (f"Имя: {ps.char_name}\n"
                    f"Характеристики:\n"
                    f"Напишите текущее количество ЕЗ (макс. {max_hp}):"), None

        else:
            self.setup_index += 1
            return self._prompt_setup()

    def handle_text_input(self, peer_id, user_id, text):
        if self.phase != "setup":
            return None, None
        if self.setup_index >= len(self.setup_queue):
            return None, None
        ps = self.setup_queue[self.setup_index]
        if ps.user_id != user_id:
            return None, None

        if ps.step == "name":
            ps.char_name = text.strip()[:30]
            ps.step = "agility"
            return self._prompt_setup()

        elif ps.step == "agility":
            try:
                val = int(text.strip())
            except ValueError:
                return "Введите число от -1 до 49.", None
            val = max(-1, min(49, val))
            ps.agility = val
            ps.step = "treeclimber"
            return self._prompt_setup()

        elif ps.step == "hp_custom":
            try:
                val = int(text.strip())
            except ValueError:
                return "Введите число.", None
            max_hp = calculate_max_hp(ps.size)
            val = max(1, min(max_hp, val))
            ps.custom_hp = val
            return self._finalize_player(ps)

        return None, None

    def handle_setup(self, user_id, action):
        if self.phase != "setup":
            return "Не в фазе характеристик.", None
        ps = self.setup_queue[self.setup_index]
        if ps.user_id != user_id:
            return "Сейчас характеристики другого персонажа.", None

        if ps.step == "treeclimber" and action.startswith("tc_"):
            ps.is_treeclimber = (action == "tc_yes")
            ps.step = "bag"
            return self._prompt_setup()

        if ps.step == "bag" and action.startswith("bag_"):
            ps.has_bag = (action == "bag_yes")
            ps.step = "hunger"
            return self._prompt_setup()

        if ps.step == "hunger" and action.startswith("hunger_"):
            key = action[len("hunger_"):]
            if key in HUNGER_LEVELS:
                ps.hunger = key
                ps.step = "size"
                return self._prompt_setup()

        elif ps.step == "size" and action.startswith("size_"):
            key = action[len("size_"):]
            if key in SIZE_LEVELS:
                ps.size = key
                ps.step = "hp_lowered"
                return self._prompt_setup()

        elif ps.step == "hp_lowered" and action.startswith("hplow_"):
            if action == "hplow_yes":
                ps.step = "hp_custom"
                return self._prompt_setup()
            else:
                ps.custom_hp = None
                return self._finalize_player(ps)

        return "Неверный выбор.", None

    def _finalize_player(self, ps):
        c = Climber(ps.user_id, ps.char_name, 0,
                    ps.hunger, ps.size,
                    ps.is_treeclimber, ps.agility,
                    ps.custom_hp, ps.has_bag or False)
        self.climbers[ps.user_id] = c
        tc = "да" if ps.is_treeclimber else "нет"
        confirm = (f"{ps.char_name}:\n"
                   f"  Рост: {c.size_label}\n"
                   f"  Ловкость: {c.agility}\n"
                   f"  Древолаз: {tc}\n"
                   f"  ЕЗ: {c.hp}/{c.max_hp}\n"
                   f"  Ресурсы: 0/{c.max_slots}")
        ps.step = "done"
        self.setup_index += 1
        if self.setup_index < len(self.setup_queue):
            msg2, kb2 = self._prompt_setup()
        else:
            msg2, kb2 = self._finish_setup()
        return confirm + "\n\n" + msg2, kb2

    def _finish_setup(self):
        self.phase = "playing"
        self.current_turn_idx = 0
        n = len(self.climbers)
        note = ""
        if n >= 2:
            note = "\nМожно страховать друг друга."
        roster = []
        for uid in self.turn_order:
            c = self.climbers[uid]
            tc = " (древолаз)" if c.is_treeclimber else ""
            roster.append(f"  - {c.name}{tc}: {c.size_label}, "
                          f"ЕЗ {c.hp}/{c.max_hp}, "
                          f"ловк. {c.agility}")
        cur = self.climbers[self.turn_order[0]]
        msg = (f"Лазание по дереву ({n} перс.):{note}\n\n"
               + "\n".join(roster)
               + "\n\nВысокое дерево. Кора шершавая, ветви крепкие."
               + f"\n\nХод: {cur.name}\n\n"
               + self._all_status())
        return msg, self._action_kb(cur)

    # -- Ход --

    @property
    def current_climber(self):
        if not self.turn_order:
            return None
        uid = self.turn_order[self.current_turn_idx % len(self.turn_order)]
        return self.climbers.get(uid)

    def handle_action(self, user_id, action):
        if self.phase != "playing":
            return "Никто не на дереве.", None
        cur = self.current_climber
        if not cur or cur.user_id != user_id:
            return "Сейчас не ваш ход.", None

        if cur.moving:
            if action == "continue_move":
                return self._continue_move(cur)
            return "Вы в пути. Продолжайте движение.", self._moving_kb()

        if cur.meditating:
            if action == "meditate_check":
                return self._check_meditation(cur)
            elapsed = time.time() - cur.meditation_start
            duration = cur.meditation_duration or MEDITATION_MIN
            remaining = max(0, duration - elapsed)
            return (f"{cur.name} медитирует. "
                    f"Осталось примерно {int(remaining // 60)} мин."), self._meditation_kb()

        if cur.pending_eggs and action.startswith("eggs_take_"):
            return self._post_action(cur, self._resolve_eggs(cur, action))
        if cur.pending_brooding and action in ("brood_scare", "brood_leave"):
            return self._post_action(cur, self._resolve_brooding(cur, action))
        if cur.pending_found and action.startswith("pick_"):
            return self._post_action(cur, self._resolve_pick(cur, action))
        if action.startswith("drop_") and action not in ("drop_menu", "drop_cancel"):
            return self._post_action(cur, self._do_drop(cur, action))

        if action == "climb":
            lines = self._do_climb(cur)
        elif action == "descend":
            lines = self._do_descend(cur)
        elif action == "explore":
            lines = self._do_explore(cur)
        elif action == "wait":
            lines = [gm_says(GM_WAIT_FLAVOR), f"{cur.name} пережидает на месте."]
        elif action == "meditate_start":
            lines = self._start_meditation(cur)
        elif action == "drop_menu":
            return self._show_drop_menu(cur)
        elif action == "drop_cancel":
            return self._post_action(cur, [])
        else:
            return "Неизвестное действие.", None

        return self._post_action(cur, lines)

    def _post_action(self, cur, lines):
        if cur.pending_eggs and cur.is_active:
            eggs = cur.pending_eggs
            lines.append(f"\nСколько забрать? "
                         f"(свободно: {cur.res_free}/{cur.max_slots})")
            return "\n".join(lines), self._eggs_kb(cur)

        if cur.pending_brooding and cur.is_active:
            lines.append("\nНаседка ждёт. Что делать?")
            return "\n".join(lines), self._brooding_kb()

        if cur.pending_found and cur.is_active:
            lines.append(f"\nРесурсы заполнены. Найдено: {', '.join(cur.pending_found)}. "
                         f"Выберите, что взять.")
            return "\n".join(lines), self._pick_kb(cur)

        if cur.meditating:
            return "\n".join(lines), self._meditation_kb()

        if cur.moving:
            return "\n".join(lines), self._moving_kb()

        active = [c for c in self.climbers.values() if c.is_active and not c.is_out]
        if not active:
            self.phase = "finished"
            lines.append("")
            lines.append(self._final_summary())
            return "\n".join(lines), self._end_kb()

        self._advance_turn()
        nxt = self.current_climber
        lines.append("")
        lines.append(self._all_status())
        lines.append(f"\nХод: {nxt.name}")
        return "\n".join(lines), self._action_kb(nxt)

    # -- Движение --

    def _start_move(self, climber, target_tier, direction):
        climber.moving = True
        climber.move_target = target_tier
        climber.move_steps_left = 2
        dir_word = "вверх" if direction == "up" else "вниз"
        target_name = TIERS[target_tier]["name"] if target_tier >= 0 else "земля"
        return [f"{climber.name} начинает движение {dir_word} ({target_name}). "
                f"Ещё {climber.move_steps_left} перехода."]

    def _continue_move(self, climber):
        climber.move_steps_left -= 1
        lines = []
        if climber.move_steps_left > 0:
            flavor_list = GM_CLIMB_FLAVOR if climber.direction == "up" else GM_DESCEND_FLAVOR
            lines.append(gm_says(flavor_list))
            lines.append(f"{climber.name} продолжает путь. "
                         f"Осталось: {climber.move_steps_left} переход(а).")
            return self._post_action(climber, lines)

        climber.moving = False
        target = climber.move_target
        climber.move_target = -1

        if target < 0:
            climber.current_tier = -1
            self._land(climber, lines)
            return self._post_action(climber, lines)

        climber.current_tier = target
        tier = TIERS[target]
        descs = tier["climb_descriptions"] if climber.direction == "up" else tier["descend_descriptions"]
        lines.append(random.choice(descs))
        lines.append(f"{climber.name} добирается до: {tier['name']}.")
        if target == len(TIERS) - 1 and climber.direction == "up":
            climber.reached_top = True
        return self._post_action(climber, lines)

    # -- Подъём --

    def _do_climb(self, climber):
        if climber.direction == "down":
            return [f"{climber.name} уже спускается. Нельзя лезть вверх."]
        lines = []
        next_tier = climber.current_tier + 1
        if next_tier >= len(TIERS):
            return [f"{climber.name} уже на верхушке."]

        if climber.injuries:
            inj_lines, inj_dmg = check_ongoing_injuries(climber)
            if inj_lines:
                lines.extend(inj_lines)
                climber.take_damage(inj_dmg)
                if climber.check_out():
                    lines.append(f"{climber.name} не может продолжать из-за травм.")
                    return lines

        tier = TIERS[next_tier]
        cats_on = self._count_on_tier(next_tier) + 1
        frag = FRAGILITY_MULTIPLIER.get(min(cats_on, 4), 1.50)
        threshold = (int(tier["base_fall_chance"] * frag)
                     + climber.extra_fall_chance + climber.fall_chance_modifier())
        threshold = max(2, min(90, threshold))
        climber.extra_fall_chance = 0

        roll = random.randint(1, 100)

        if cats_on >= 2 and cats_on in FRAGILITY_FLAVOR:
            lines.append(random.choice(FRAGILITY_FLAVOR[cats_on]))

        lines.append(gm_says(GM_CLIMB_FLAVOR))
        lines.append(f"{climber.name} лезет на {tier['name']}. "
                     f"Бросок: {roll}/100 (нужно > {threshold})")

        if roll <= threshold:
            lines.extend(self._handle_slip(climber, next_tier))
        else:
            # Мелкие травмы при подъёме для НЕ-древолазов
            if not climber.is_treeclimber and climber.agility < 36:
                chance = (CLIMB_MINOR_INJURY_CHANCE_TIER3 if next_tier == 2
                          else CLIMB_MINOR_INJURY_CHANCE_TIER2 if next_tier == 1
                          else 0.25)
                if random.random() < chance:
                    inj = roll_injury_minor()
                    climber.injuries.append(inj)
                    climber.take_damage(inj["dmg"])
                    lines.append(gm_says(GM_CLIMB_MINOR_INJURY_FLAVOR))
                    lines.append(f"  {inj['name']}, -{inj['dmg']} ЕЗ "
                                 f"({climber.hp}/{climber.max_hp})")
                    if climber.check_out():
                        lines.append(f"{climber.name} не может продолжать.")
                        return lines
            lines.extend(self._start_move(climber, next_tier, "up"))
        return lines

    # -- Спуск --

    def _do_descend(self, climber):
        if climber.current_tier < 0:
            return [f"{climber.name} уже на земле."]
        if climber.direction == "up":
            climber.direction = "down"
        lines = []
        current = climber.current_tier

        if climber.injuries:
            inj_lines, inj_dmg = check_ongoing_injuries(climber)
            if inj_lines:
                lines.extend(inj_lines)
                climber.take_damage(inj_dmg)
                if climber.check_out():
                    lines.append(f"{climber.name} не может продолжать из-за травм.")
                    return lines

        tier = TIERS[current]
        base = int(tier["base_fall_chance"] * 0.65)
        target = current - 1
        cats_on = self._count_on_tier(target) + 1 if target >= 0 else 1
        frag = FRAGILITY_MULTIPLIER.get(min(cats_on, 4), 1.50)
        threshold = (int(base * frag) + climber.extra_fall_chance
                     + climber.luck_bonus + climber.fall_chance_modifier())
        threshold = max(1, min(90, threshold))
        climber.extra_fall_chance = 0

        roll = random.randint(1, 100)
        lines.append(gm_says(GM_DESCEND_FLAVOR))
        lines.append(f"{climber.name} спускается с {tier['name']}. "
                     f"Бросок: {roll}/100 (нужно > {threshold})")

        if roll <= threshold:
            lines.extend(self._handle_slip(climber, current))
        else:
            target_tier = current - 1
            lines.extend(self._start_move(climber, target_tier, "down"))
        return lines

    def _land(self, climber, lines):
        climber.finished = True
        climber.is_active = False
        picked_up = []
        while climber.ground_stash and climber.res_free > 0:
            picked_up.append(climber.ground_stash.pop(0))
            climber.resources.append(picked_up[-1])
        leftover = list(climber.ground_stash)
        inj = ""
        if climber.injuries:
            inj = f"\n  Травмы: {climber.injuries_summary()}"
        lines.append(f"{climber.name} на земле.\n"
                     f"  Ресурсы: {climber.res_contents()}\n"
                     f"  ЕЗ {climber.hp}/{climber.max_hp}{inj}")
        if picked_up:
            lines.append(f"  Подобрано с земли: {', '.join(picked_up)}.")
        if leftover:
            lines.append(f"  Осталось на земле: {', '.join(leftover)}.")

    # -- Срыв / Падение --

    def _handle_slip(self, climber, from_tier):
        lines = []

        # Древолаз: удерживается или соскальзывает на ярус ниже
        if climber.is_treeclimber:
            # 50% вообще без травмы, 50% — только мелкая
            if random.random() < 0.5:
                lines.append(f"Срыв! Но {climber.name} — древолаз. "
                            f"Удерживается на дереве без серьёзных последствий.")
            else:
                injury = roll_injury_minor()  # только мелкая травма
                climber.take_damage(injury["dmg"])
                climber.injuries.append(injury)
                lines.append(
                    f"Срыв! Но {climber.name} — древолаз. "
                    f"Удерживается на дереве.\n"
                    f"Травма: {injury['name']}, -{injury['dmg']} ЕЗ "
                    f"({climber.hp}/{climber.max_hp})"
                )
            if climber.check_out():
                lines.append(f"{climber.name} не может продолжать. Нужна помощь целителя!")
            return lines

        catcher, fallen, caught_from_below = self._try_catch(climber, from_tier)
        if catcher:
            injury = roll_climb_injury()
            reduced = max(1, int(injury["dmg"] * SAFETY_DAMAGE_REDUCTION))
            climber.take_damage(reduced)
            inj_rec = dict(injury)
            inj_rec["dmg"] = reduced
            climber.injuries.append(inj_rec)

            if caught_from_below:
                flavor = random.choice(CATCH_FLAVOR_BELOW)
            else:
                flavor = random.choice(CATCH_FLAVOR_SAME)

            # после страховки падающий оказывается на уровне ловящего
            climber.current_tier = catcher.current_tier

            text = flavor.format(catcher=catcher.name, fallen=climber.name)
            lines.append(
                f"Срыв! {text}\n"
                f"Травма: {injury['name']} (смягчена), "
                f"-{reduced} ЕЗ ({climber.hp}/{climber.max_hp})"
            )
            if climber.check_out():
                lines.append(f"{climber.name} не может продолжать. Нужна помощь целителя!")
            return lines

        # Падение: зависит от яруса
        if from_tier == 2:
            injuries_list, landed_on_paws = roll_fall_injuries_tier3()
        elif from_tier == 1:
            injuries_list, landed_on_paws = roll_fall_injuries_tier2()
        else:
            injuries_list, landed_on_paws = roll_fall_injuries_tier1()

        total_dmg = 0
        injury_names = []
        for inj in injuries_list:
            climber.injuries.append(inj)
            climber.take_damage(inj["dmg"])
            total_dmg += inj["dmg"]
            injury_names.append(f"{inj['name']} (-{inj['dmg']})")
            if "agility_penalty" in inj:
                climber.apply_agility_penalty(inj["agility_penalty"])

        climber.current_tier = -1

        if self._has_allies_nearby(climber, from_tier):
            lines.append("ПАДЕНИЕ! " + random.choice(CATCH_FAIL_FLAVOR).format(
                fallen=climber.name))
        else:
            lines.append("ПАДЕНИЕ!")

        height = ["с нижних веток", "со среднего яруса", "с верхушки"][min(from_tier, 2)]

        if landed_on_paws:
            lines.append(f"{climber.name} срывается {height}, "
                         f"бьётся о ветки, но приземляется на лапы.\n"
                         f"Травмы: {', '.join(injury_names)}\n"
                         f"Итого: -{total_dmg} ЕЗ ({climber.hp}/{climber.max_hp})")
        else:
            lines.append(f"{climber.name} срывается {height} и падает на землю.\n"
                         f"Травмы: {', '.join(injury_names)}\n"
                         f"Итого: -{total_dmg} ЕЗ ({climber.hp}/{climber.max_hp})")

        if not climber.check_out():
            self._land(climber, lines)
        else:
            lines.append(f"{climber.name} не может продолжать. Нужна помощь целителя!")
        return lines

    # -- Осмотр (лимит 3 на ярус + шанс падения для НЕ-древолазов) --

    def _do_explore(self, climber):
        lines = []
        if climber.current_tier < 0:
            return [f"{climber.name} на земле. Сначала нужно залезть."]
        tier_idx = climber.current_tier
        tier = TIERS[tier_idx]

        if climber.get_explore_count(tier_idx) >= EXPLORE_LIMIT_PER_TIER:
            return [gm_says(GM_EXPLORE_FLAVOR),
                    f"{climber.name} осматривается ({tier['name']}).",
                    "  Ничего нового на этом ярусе."]

        # Шанс падения при осмотре для НЕ-древолазов (2-й и 3-й ярусы)
        if not climber.is_treeclimber and tier_idx in EXPLORE_FALL_BASE:
            explore_n = climber.get_explore_count(tier_idx)
            base_chances = EXPLORE_FALL_BASE[tier_idx]
            idx = min(explore_n, len(base_chances) - 1)
            base_fall = base_chances[idx]
            agility_reduction = max(0, climber.agility * 0.5)
            fall_chance = max(3, base_fall - int(agility_reduction))
            roll = random.randint(1, 100)
            if roll <= fall_chance:
                lines.append(gm_says(GM_EXPLORE_FALL_RISK))
                lines.append(f"{climber.name} теряет равновесие при осмотре!")
                climber.add_explore(tier_idx)
                lines.extend(self._handle_slip(climber, tier_idx))
                return lines

        climber.add_explore(tier_idx)

        lines.append(gm_says(GM_EXPLORE_FLAVOR))
        lines.append(f"{climber.name} осматривается ({tier['name']}).")
        found_items = []
        found = False

        if random.random() < tier["find_chance"]:
            name = random.choice(ITEMS_ON_BRANCHES)
            found_items.append(name)
            lines.append(f"  На ветке: {name}.")
            found = True

        if random.random() < tier["bark_chance"]:
            name = random.choice(ITEMS_IN_BARK)
            found_items.append(name)
            lines.append(f"  В расщелине коры: {name}.")
            found = True

        if tier["hollow_chance"] > 0 and random.random() < tier["hollow_chance"]:
            text, loot, extra_fall, dmg = generate_hollow()
            lines.append(f"  {text}")
            found = True
            if dmg > 0:
                climber.take_damage(dmg)
                lines.append(f"  Урон: -{dmg} ЕЗ ({climber.hp}/{climber.max_hp})")
            if extra_fall > 0:
                climber.extra_fall_chance += int(extra_fall * 100)
                lines.append("  Шанс падения временно повышен.")
            if loot:
                marker = loot[0]
                if marker[0] == "brooding":
                    climber.pending_brooding = {"bird": marker[1], "count": marker[2]}
                elif marker[0] == "eggs":
                    climber.pending_eggs = {"bird": marker[1], "count": marker[2]}
                elif marker[0] == "items":
                    found_items.extend(marker[1])
            if climber.check_out():
                lines.append(f"  {climber.name} больше не может продолжать.")
                return lines

        if not found:
            lines.append("  " + random.choice([
                "Ничего не нашлось.", "Только ветер в листве.",
                "Пусто.", "Ни добычи, ни находок."]))

        if found_items and not climber.pending_eggs and not climber.pending_brooding:
            taken, overflow = [], []
            for item in found_items:
                if climber.res_free > 0:
                    climber.resources.append(item)
                    taken.append(item)
                else:
                    overflow.append(item)
            if taken:
                lines.append(f"  Взято: {', '.join(taken)}. "
                             f"(ресурсы: {len(climber.resources)}/{climber.max_slots})")
            if overflow:
                climber.pending_found = overflow
        return lines

    # -- Яйца --

    def _resolve_eggs(self, climber, action):
        data = climber.pending_eggs
        bird, total = data["bird"], data["count"]
        climber.pending_eggs = None
        try:
            n = int(action.split("_")[-1])
        except ValueError:
            n = 0
        n = max(0, min(n, total, climber.res_free))
        if n == 0:
            return [f"{climber.name} оставляет яйца на месте."]
        w = _eggs_word(n)
        for _ in range(n):
            climber.resources.append(f"яйцо ({bird})")
        left = total - n
        lines = [f"{climber.name} берёт {n} {w} ({bird}). "
                 f"(ресурсы: {len(climber.resources)}/{climber.max_slots})"]
        if left > 0:
            lines.append(f"  Оставлено в гнезде: {left}.")
        return lines

    # -- Наседка --

    def _resolve_brooding(self, climber, action):
        data = climber.pending_brooding
        bird, count = data["bird"], data["count"]
        climber.pending_brooding = None
        if action == "brood_scare":
            if random.randint(1, 100) >= 35:
                climber.pending_eggs = {"bird": bird, "count": count}
                w = _eggs_word(count)
                return [f"{climber.name} прогоняет птицу. "
                        f"Наседка ({bird}) улетает.\n"
                        f"  В гнезде {count} {w}."]
            else:
                dmg = random.randint(2, 5)
                climber.take_damage(dmg)
                climber.extra_fall_chance += 10
                lines = [f"{climber.name} пытается прогнать птицу. "
                         f"Та клюёт и бьёт крыльями.\n"
                         f"  Урон: -{dmg} ЕЗ ({climber.hp}/{climber.max_hp}). "
                         "Шанс падения повышен."]
                if climber.check_out():
                    lines.append(f"  {climber.name} выбывает.")
                return lines
        return [f"{climber.name} оставляет наседку в покое."]

    # -- Выбор предмета --

    def _resolve_pick(self, climber, action):
        if action == "pick_skip":
            items = climber.pending_found
            climber.pending_found = None
            return [f"Оставлено: {', '.join(items)}."]
        try:
            idx = int(action.split("_")[-1])
        except ValueError:
            climber.pending_found = None
            return ["Ошибка выбора."]
        pending = climber.pending_found
        if idx < 0 or idx >= len(pending):
            climber.pending_found = None
            return ["Ошибка выбора."]
        new_item = pending[idx]
        if climber.res_free > 0:
            climber.resources.append(new_item)
            pending.pop(idx)
            lines = [f"Взято: {new_item}. "
                     f"(ресурсы: {len(climber.resources)}/{climber.max_slots})"]
        else:
            lines = ["Ресурсы заполнены."]
        if not pending:
            climber.pending_found = None
        return lines

    # -- Сброс --

    def _show_drop_menu(self, cur):
        if not cur.resources:
            return "Ресурсов нет.", self._action_kb(cur)
        return (f"Сбросить ресурс с дерева:\n"
                f"  Сейчас: {cur.res_contents()}"), self._drop_kb(cur)

    def _do_drop(self, cur, action):
        try:
            idx = int(action.split("_")[-1])
        except ValueError:
            return ["Ошибка."]
        if idx < 0 or idx >= len(cur.resources):
            return ["Нет такого ресурса."]
        item = cur.resources.pop(idx)
        ground_items, desc = drop_item_from_tree(item)
        cur.ground_stash.extend(ground_items)
        return [f"{desc} (ресурсы: {len(cur.resources)}/{cur.max_slots})"]

    # -- Медитация --

    def _start_meditation(self, climber):
        if climber.current_tier != len(TIERS) - 1:
            return ["Медитировать можно только на верхушке."]
        if climber.meditated:
            return [f"{climber.name} уже медитировал."]
        climber.meditating = True
        climber.meditation_start = time.time()
        climber.meditation_duration = random.randint(MEDITATION_MIN, MEDITATION_MAX)
        text = random.choice(MEDITATION_START_TEXTS).format(name=climber.name)
        approx_min = int(climber.meditation_duration // 60)
        return [text,
                f"Медитация займёт около {approx_min} минут.",
                "Ход переходит к следующему."]

    def _check_meditation(self, climber):
        elapsed = time.time() - climber.meditation_start
        duration = climber.meditation_duration or MEDITATION_MIN
        if elapsed < duration:
            r = duration - elapsed
            return (f"{climber.name} ещё медитирует. "
                    f"Осталось: {int(r // 60)} мин {int(r % 60)} сек."), self._meditation_kb()

        climber.meditating = False
        climber.meditated = True
        heal = random.randint(*MEDITATION_HEAL)
        climber.hp = min(climber.max_hp, climber.hp + heal)
        climber.luck_bonus += MEDITATION_LUCK_BONUS
        text = random.choice(MEDITATION_COMPLETE_TEXTS).format(name=climber.name)
        lines = [text,
                 f"  Восстановлено {heal} ЕЗ ({climber.hp}/{climber.max_hp}).",
                 "  Удача на спуске повышена."]

        shiny_roll = random.randint(1, 100)
        if shiny_roll > 50:
            item = random.choice(MEDITATION_SHINY_ITEMS)
            climber.meditation_shiny = item
            climber.ground_stash.append(item)
            lines.append("")
            lines.append("На земле что-то блеснуло. Показалось ли?")
            lines.append(f"x1 {item}")

        lines.append("")
        lines.append(self._all_status())
        lines.append(f"\nХод: {climber.name}")
        return "\n".join(lines), self._action_kb(climber)

    # -- Страховка (ловкость ловящего) --

    def _try_catch(self, fallen, from_tier):
        # Пытаемся найти союзников рядом с траекторией падения
        fallen_tier = fallen.current_tier
        nearby = []

        for c in self.climbers.values():
            if c.user_id == fallen.user_id:
                continue
            if not c.alive or c.is_out or c.finished:
                continue
            if c.current_tier < 0:
                continue
            # Союзник рядом, если на том же ярусе, что и падающий,
            # или на ярусе ниже (поймает снизу), или рядом с from_tier
            if abs(c.current_tier - fallen_tier) <= 1 or abs(c.current_tier - from_tier) <= 1:
                nearby.append(c)

        if not nearby:
            return None, None, False

        # Сортируем: древолазы первые, затем по ловкости
        nearby.sort(key=lambda c: (c.is_treeclimber, c.agility), reverse=True)

        for ally in nearby:
            # Древолаз всегда ловит
            if ally.is_treeclimber:
                caught_from_below = (ally.current_tier == fallen_tier - 1)
                return ally, fallen, caught_from_below

            # Ловкость 37+ = 100% шанс поймать
            if ally.agility >= 37:
                caught_from_below = (ally.current_tier == fallen_tier - 1)
                return ally, fallen, caught_from_below

            # От 19 до 36: линейный шанс (19 ≈ 5%, 36 ≈ 95%)
            if ally.agility >= 19:
                catch_chance = (ally.agility - 18) / (37 - 18)
                if random.random() < catch_chance:
                    caught_from_below = (ally.current_tier == fallen_tier - 1)
                    return ally, fallen, caught_from_below

        return None, None, False

    def _has_allies_nearby(self, climber, tier):
        fallen_tier = climber.current_tier
        for c in self.climbers.values():
            if c.user_id == climber.user_id:
                continue
            if not c.alive or c.is_out or c.finished or c.current_tier < 0:
                continue
            if abs(c.current_tier - tier) <= 1 or abs(c.current_tier - fallen_tier) <= 1:
                return True
        return False

    def _count_on_tier(self, tier_idx):
        return sum(1 for c in self.climbers.values()
                   if c.current_tier == tier_idx and c.alive and not c.is_out)

    # -- Смена хода --

    def _advance_turn(self):
        # активные – живы, не выбыл, не медитирует
        active_ids = [
            uid for uid in self.turn_order
            if self.climbers[uid].is_active
            and not self.climbers[uid].is_out
            and not self.climbers[uid].meditating
        ]

        # если активных нет, но кто-то медитирует – просто держим ход на первом медитирующем
        if not active_ids:
            med = [uid for uid in self.turn_order if self.climbers[uid].meditating]
            if med:
                for i, uid in enumerate(self.turn_order):
                    if uid == med[0]:
                        self.current_turn_idx = i
                        return
            return

        # крутим очередь, пока не найдём активного И не медитирующего
        for _ in range(len(self.turn_order)):
            self.current_turn_idx = (self.current_turn_idx + 1) % len(self.turn_order)
            uid = self.turn_order[self.current_turn_idx]
            c = self.climbers[uid]
            if c.is_active and not c.is_out and not c.meditating:
                return

    # -- Статус и итоги --

    def _all_status(self):
        lines = ["Статус:"]
        first = True
        for c in self.climbers.values():
            if not first:
                lines.append("")  # пустая строка‑разделитель
            first = False
            lines.append(c.status_line())
        return "\n".join(lines)

    def _final_summary(self):
        lines = ["Итоги:"]
        for uid in self.turn_order:
            c = self.climbers[uid]
            st = "[на земле]" if c.is_out else "[на земле]" if c.finished else ""
            inj = f"\n  Травмы: {c.injuries_summary()}" if c.injuries else ""
            tc = " (древолаз)" if c.is_treeclimber else ""
            items_str = ", ".join(c.resources) if c.resources else "-"
            lines.append(f"\n{c.name}{tc} {st}\n"
                         f"  Рост: {c.size_label}, ловк. {c.agility}\n"
                         f"  ЕЗ {c.hp}/{c.max_hp}{inj}\n"
                         f"  Ресурсы: {items_str}")
            if c.ground_stash:
                lines.append(f"  Осталось на земле: {', '.join(c.ground_stash)}")
        return "\n".join(lines)

    def _end_game(self):
        self.phase = "finished"
        return self._final_summary(), self._end_kb()

    # -- Клавиатуры --

    def _treeclimber_kb(self):
        return self._kb([
            [("Да", "positive", "tc_yes"),
             ("Нет", "secondary", "tc_no")],
        ])

    def _bag_kb(self):
        return self._kb([
            [("Да", "positive", "bag_yes"),
             ("Нет", "secondary", "bag_no")],
        ])

    def _hp_lowered_kb(self):
        return self._kb([
            [("Да", "negative", "hplow_yes"),
             ("Нет", "positive", "hplow_no")],
        ])

    def _hunger_kb(self):
        return self._kb([
            [("Сыт", "positive", "hunger_сыт"),
             ("Голоден", "primary", "hunger_голоден")],
            [("Сильно голоден", "secondary", "hunger_сильно_голоден"),
             ("Смерт. голоден", "negative", "hunger_смертельно_голоден")],
        ])

    def _size_kb(self):
        return self._kb([
            [("Малорослый", "secondary", "size_малорослый"),
             ("Стандартный", "primary", "size_стандартный")],
            [("Высокий", "primary", "size_высокий"),
             ("Здоровяк", "positive", "size_здоровяк")],
        ])

    def _action_kb(self, c):
        rows = []
        if c.current_tier < 0:
            if c.direction == "up" and not c.finished:
                rows.append([("Залезть", "positive", "climb")])
            rows.append([("Ждать", "secondary", "wait")])
        elif c.direction == "up":
            r1 = []
            if c.current_tier < len(TIERS) - 1:
                r1.append(("Выше", "positive", "climb"))
            r1.append(("Осмотреться", "primary", "explore"))
            rows.append(r1)
            r2 = [("Спуститься", "secondary", "descend")]
            if c.current_tier == len(TIERS) - 1 and not c.meditated:
                r2.append(("Медитация", "primary", "meditate_start"))
            rows.append(r2)
            r3 = [("Ждать", "secondary", "wait")]
            if c.resources:
                r3.append(("Сбросить", "negative", "drop_menu"))
            rows.append(r3)
        else:
            rows.append([("Осмотреться", "primary", "explore")])
            rows.append([("Спуститься", "secondary", "descend"),
                         ("Ждать", "secondary", "wait")])
            if c.resources:
                rows.append([("Сбросить", "negative", "drop_menu")])
        return self._kb(rows)

    def _moving_kb(self):
        return self._kb([[("Продолжить путь", "primary", "continue_move")]])

    def _eggs_kb(self, c):
        total = c.pending_eggs["count"]
        max_take = min(total, c.res_free)
        rows = [[("0 (не брать)", "secondary", "eggs_take_0")]]
        btn_row = []
        for i in range(1, max_take + 1):
            btn_row.append((str(i), "primary", f"eggs_take_{i}"))
            if len(btn_row) >= 5:
                rows.append(btn_row)
                btn_row = []
        if btn_row:
            rows.append(btn_row)
        return self._kb(rows)

    def _brooding_kb(self):
        return self._kb([[("Прогнать", "negative", "brood_scare"),
                          ("Оставить", "secondary", "brood_leave")]])

    def _pick_kb(self, c):
        rows = [[(f"{item}", "primary", f"pick_{i}")]
                for i, item in enumerate(c.pending_found)]
        rows.append([("Пропустить", "secondary", "pick_skip")])
        return self._kb(rows)

    def _drop_kb(self, c):
        rows = [[(f"{item}", "negative", f"drop_{i}")]
                for i, item in enumerate(c.resources)]
        rows.append([("Отмена", "secondary", "drop_cancel")])
        return self._kb(rows)

    def _meditation_kb(self):
        return self._kb([[("Проверить", "primary", "meditate_check")]])

    def _end_kb(self):
        return self._kb([
            [("Ещё раз", "positive", "restart")],
        ])

    def lobby_keyboard(self):
        return self._kb([
            [("Присоединиться", "primary", "join")],
            [("Начать", "positive", "go")],
        ])

    def _kb(self, rows):
        buttons = []
        for row in rows:
            buttons.append([{
                "action": {"type": "callback", "label": lbl,
                           "payload": json.dumps(
                               {"game": "tree", "action": act},
                               ensure_ascii=False)},
                "color": clr,
            } for lbl, clr, act in row])
        return json.dumps({"inline": True, "buttons": buttons},
                          ensure_ascii=False)

# ==============================================================
# АААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
# ==============================================================

active_games = {}

def cmd_tree(peer_id, user_id, args=None):
    game = active_games.get(peer_id)
    if game and game.phase == "lobby":
        return game.add_player(user_id), game.lobby_keyboard()
    elif game and game.phase in ("setup", "playing"):
        return "На дерево уже лезут.", None
    game = CoopTreeClimb(host_id=user_id)
    active_games[peer_id] = game
    msg = game.add_player(user_id)
    return (f"Лазание по дереву:\n\n{msg}\n\n"
            f"Другие могут присоединиться (макс. 4).\n"
            f"Ответственный начинает, когда все готовы."), game.lobby_keyboard()

def handle_tree_callback(peer_id, user_id, payload):
    if payload.get("game") != "tree":
        return None, None
    action = payload.get("action")
    game = active_games.get(peer_id)
    if not game:
        return "Никто еще не лезет на дерево. Напишите !дерево", None
    if action == "join":
        if game.phase != "lobby":
            return "На дерево уже лезут.", None
        return game.add_player(user_id), game.lobby_keyboard()
    elif action == "go":
        msg, kb = game.begin_setup(user_id)
        return (msg or "Только ответственный может начать."), kb
    elif action == "restart":
        del active_games[peer_id]
        return cmd_tree(peer_id, user_id)
    elif action.startswith("tc_"):
        return game.handle_setup(user_id, action)
    elif action.startswith("bag_"):
        return game.handle_setup(user_id, action)
    elif action.startswith("hunger_") or action.startswith("size_"):
        return game.handle_setup(user_id, action)
    elif action.startswith("hplow_"):
        return game.handle_setup(user_id, action)
    else:
        return game.handle_action(user_id, action)

def handle_text_in_game(peer_id, user_id, text):
    game = active_games.get(peer_id)
    if not game or game.phase != "setup":
        return None, None
    return game.handle_text_input(peer_id, user_id, text)

# ==============================================================
# АААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
# ==============================================================

if __name__ == "__main__":
    print("Бот запущен. Ожидание событий...")

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            text = msg["text"].strip()
            user_id = msg["from_id"]
            peer_id = msg["peer_id"]

            if text.lower().startswith("!дерево"):
                args = (text.split(maxsplit=1)[1]
                        if " " in text else None)
                response, keyboard = cmd_tree(peer_id, user_id, args)
                send(peer_id, response, keyboard)
            else:
                response, keyboard = handle_text_in_game(
                    peer_id, user_id, text)
                if response:
                    send(peer_id, response, keyboard)

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            user_id = event.object["user_id"]
            peer_id = event.object["peer_id"]
            payload = event.object.get("payload", {})

            if isinstance(payload, str):
                payload = json.loads(payload)

            response, keyboard = handle_tree_callback(
                peer_id, user_id, payload)

            if response:
                send(peer_id, response, keyboard)