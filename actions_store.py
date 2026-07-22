import json
import os

STORE_PATH = os.path.join(os.path.dirname(__file__), "actions_data.json")
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULT_SETTINGS = {"public_adding": True}

DEFAULT_ACTIONS = [
    {
        "key": "обнять", "emoji": "🤗",
        "initial": "{sender} хочет вас обнять",
        "accept": "{sender} и {clicker} обнялись",
        "decline": "{clicker} не хочет обниматься с {sender}",
    },
    {
        "key": "поцеловать", "emoji": "😘",
        "initial": "{sender} хочет вас поцеловать",
        "accept": "{sender} поцеловал(а) {clicker}",
        "decline": "{clicker} не хочет целоваться с {sender}",
    },
    {
        "key": "ударить", "emoji": "👊",
        "initial": "{sender} хочет вас ударить",
        "accept": "{clicker} позволил(а) себя ударить, {sender} врезал(а)",
        "decline": "{clicker} увернулся(лась) от удара {sender}",
    },
    {
        "key": "пнуть", "emoji": "🦵",
        "initial": "{sender} хочет вас пнуть",
        "accept": "{sender} пнул(а) {clicker}",
        "decline": "{clicker} увернулся(лась) от пинка {sender}",
    },
    {
        "key": "погладить", "emoji": "🤚",
        "initial": "{sender} хочет вас погладить",
        "accept": "{sender} погладил(а) {clicker}",
        "decline": "{clicker} не дался(лась) погладить {sender}",
    },
    {
        "key": "укусить", "emoji": "😬",
        "initial": "{sender} хочет вас укусить",
        "accept": "{sender} укусил(а) {clicker}",
        "decline": "{clicker} не дался(лась) укусить {sender}",
    },
    {
        "key": "толкнуть", "emoji": "🫸",
        "initial": "{sender} хочет вас толкнуть",
        "accept": "{sender} толкнул(а) {clicker}",
        "decline": "{clicker} устоял(а) на ногах, не поддавшись {sender}",
    },
    {
        "key": "щипнуть", "emoji": "🤏",
        "initial": "{sender} хочет вас ущипнуть",
        "accept": "{sender} ущипнул(а) {clicker}",
        "decline": "{clicker} не дался(лась) ущипнуть {sender}",
    },
    {
        "key": "напугать", "emoji": "👻",
        "initial": "{sender} хочет вас напугать",
        "accept": "{sender} напугал(а) {clicker}",
        "decline": "{clicker} не испугался(лась) {sender}",
    },
    {
        "key": "поприветствовать", "emoji": "👋",
        "initial": "{sender} машет вам рукой",
        "accept": "{sender} и {clicker} поприветствовали друг друга",
        "decline": "{clicker} проигнорировал(а) приветствие {sender}",
    },
    {
        "key": "подарок", "emoji": "🎁",
        "initial": "{sender} дарит вам подарок",
        "accept": "{clicker} принял(а) подарок от {sender}",
        "decline": "{clicker} отказался(лась) от подарка {sender}",
    },
    {
        "key": "танец", "emoji": "💃",
        "initial": "{sender} приглашает вас на танец",
        "accept": "{sender} и {clicker} танцуют",
        "decline": "{clicker} отказался(лась) танцевать с {sender}",
    },
    {
        "key": "трахнуть", "emoji": "🔞",
        "initial": "{sender} хочет вас трахнуть",
        "accept": "{sender} жестко трахнул(а) {clicker}",
        "decline": "{clicker} отказал(а) {sender} в сексе",
    },
    {
        "key": "засосать", "emoji": "👅",
        "initial": "{sender} хочет вас засосать",
        "accept": "{sender} страстно засосал(а) {clicker}",
        "decline": "{clicker} оттолкнул(а) {sender}, не дав себя засосать",
    },
    {
        "key": "подрочить", "emoji": "💦",
        "initial": "{sender} хочет подрочить вам",
        "accept": "{sender} подрочил(а) {clicker}",
        "decline": "{clicker} не позволил(а) {sender} подрочить",
    },
    {
        "key": "кончить", "emoji": "💦",
        "initial": "{sender} хочет спустить на вас сперму",
        "accept": "{sender} кончил(а) на {clicker}",
        "decline": "{clicker} увернулся(лась) от {sender}",
    },
    {
        "key": "отлизать", "emoji": "👅",
        "initial": "{sender} хочет отлизать вам",
        "accept": "{sender} нежно отлизал(а) у {clicker}",
        "decline": "{clicker} не дал(а) {sender} отлизать",
    },
    {
        "key": "отсосать", "emoji": "🍆",
        "initial": "{sender} хочет отсосать вам",
        "accept": "{sender} отсосал(а) у {clicker}",
        "decline": "{clicker} не позволил(а) {sender} отсосать",
    },
    {
        "key": "дать в рот", "emoji": "👄",
        "initial": "{sender} хочет дать вам в рот",
        "accept": "{clicker} взял(а) в рот у {sender}",
        "decline": "{clicker} отказался(лась) брать в рот у {sender}",
    },
    {
        "key": "приласкать", "emoji": "🥰",
        "initial": "{sender} хочет приласкать вас в объятиях",
        "accept": "{sender} нежно приласкал(а) {clicker}",
        "decline": "{clicker} отстранился(лась) от ласк {sender}",
    },
    {
        "key": "раздеть", "emoji": "👙",
        "initial": "{sender} хочет стянуть с вас трусики",
        "accept": "{sender} стянул(а) трусики с {clicker}",
        "decline": "{clicker} не позволил(а) {sender} себя раздеть",
    },
    {
        "key": "куст", "emoji": "😼",
        "initial": "{sender} хочет сделать вам кусь",
        "accept": "{sender} сделал(а) кусь {clicker}",
        "decline": "{clicker} не дался(лась) сделать кусь {sender}",
    },
    {
        "key": "заткнуть", "emoji": "🤐",
        "initial": "{sender} хочет заткнуть вам рот кляпом",
        "accept": "{sender} заткнул(а) рот {clicker} кляпом",
        "decline": "{clicker} не дал(а) {sender} заткнуть себе рот",
    },
    {
        "key": "порвать", "emoji": "💥",
        "initial": "{sender} хочет порвать вашу киску",
        "accept": "{sender} жестко порвал(а) киску {clicker}",
        "decline": "{clicker} не дал(а) {sender} сделать это",
    },
    {
        "key": "изнасиловать", "emoji": "⛓️",
        "initial": "{sender} хочет изнасиловать вас",
        "accept": "{sender} изнасиловал(а) {clicker}",
        "decline": "{clicker} смог(ла) отбиться от {sender}",
    },
    {
        "key": "раздеться", "emoji": "👕",
        "initial": "{sender} хочет снять с себя одежду перед вами",
        "accept": "{sender} снял(а) с себя одежду перед {clicker}",
        "decline": "{clicker} отвернулся(лась), пока {sender} раздевался(лась)",
    }
]

def load_actions() -> list[dict]:
    if not os.path.exists(STORE_PATH):
        save_actions(DEFAULT_ACTIONS)
        return list(DEFAULT_ACTIONS)
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_actions(actions: list[dict]) -> None:
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(actions, f, ensure_ascii=False, indent=2)

def add_action(key: str, emoji: str, initial: str, accept: str, decline: str, added_by: int = 0) -> dict:
    """Сохраняет полностью кастомное действие от пользователя."""
    action = {
        "key": key.lower(),
        "emoji": emoji,
        "initial": initial,
        "accept": accept,
        "decline": decline,
        "added_by": added_by
    }
    
    actions = load_actions()
    actions = [a for a in actions if a["key"] != action["key"]]
    actions.append(action)
    save_actions(actions)
    
    return action

def get_action(key: str) -> dict | None:
    for a in load_actions():
        if a["key"] == key:
            return a
    return None

def delete_action(key: str) -> bool:
    actions = load_actions()
    new_actions = [a for a in actions if a["key"] != key]
    if len(new_actions) == len(actions):
        return False
    save_actions(new_actions)
    return True

# ---------- настройки (лок на добавление) ----------

def load_settings() -> dict:
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings: dict) -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def is_public_adding_enabled() -> bool:
    return load_settings().get("public_adding", True)

def set_public_adding(enabled: bool) -> None:
    settings = load_settings()
    settings["public_adding"] = enabled
    save_settings(settings)