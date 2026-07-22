import asyncio
import logging
from uuid import uuid4
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message,
)
from aiogram.filters import CommandStart, Command

from config import BOT_TOKEN, ADMIN_IDS
from actions_store import (
    load_actions, add_action, get_action, delete_action,
    is_public_adding_enabled, set_public_adding,
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# token -> {"sender_id", "sender_name", "action_key"}
pending_actions: dict[str, dict] = {}


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


class AddActionStates(StatesGroup):
    waiting_for_emoji_and_key = State()
    waiting_for_initial = State()
    waiting_for_accept = State()
    waiting_for_decline = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Напиши в любом чате @имя_бота и начни вводить действие "
        "(например: обнять, поцеловать) — появится список, выбери нужное.\n\n"
        "Команды:\n"
        "/listactions — список действий\n"
        "/addaction — запустить меню добавления своего действия\n"
        "/delaction ключ — удалить действие (своё — любой, чужое — только админ)\n"
        + ("/lockadd, /unlockadd — вкл/выкл добавление действий другими людьми (только админ)"
           if is_admin(message.from_user.id) else "")
    )


@dp.message(Command("listactions"))
async def list_actions_cmd(message: Message):
    actions = load_actions()
    lines = [f"{a['emoji']} {a['key']}" for a in actions]
    status = "🔓 открыто всем" if is_public_adding_enabled() else "🔒 закрыто (только админ)"
    await message.answer(
        "Доступные действия:\n" + "\n".join(lines) + f"\n\nДобавление действий: {status}"
    )


# --- FSM ДЛЯ ДОБАВЛЕНИЯ ДЕЙСТВИЯ ---

@dp.message(Command("addaction"))
async def start_adding_action(message: Message, state: FSMContext):
    if not is_public_adding_enabled() and not is_admin(message.from_user.id):
        await message.answer("🔒 Добавление новых действий сейчас закрыто администратором.")
        return

    await message.answer(
        "Отправь эмодзи и название действия через пробел.\n"
        "Пример: 💃 потанцевать"
    )
    await state.set_state(AddActionStates.waiting_for_emoji_and_key)


@dp.message(AddActionStates.waiting_for_emoji_and_key)
async def process_emoji_and_key(message: Message, state: FSMContext):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Пожалуйста, отправь эмодзи и название через пробел (например: 💃 потанцевать).")
        return
    
    emoji, key = parts[0], parts[1].lower()
    await state.update_data(emoji=emoji, key=key)
    
    await message.answer(
        "Отлично! Теперь напиши сообщение для **предложения** (что делает отправитель).\n"
        "❗️ Бот **сам** подставит твое имя в начало.\n"
        "*(Если хочешь смайлик в тексте — напиши его здесь, например: `хочет обнять вас 🤗`)*\n\n"
        "👉 *Пример:* `хочет обнять вас`"
    )
    await state.set_state(AddActionStates.waiting_for_initial)


@dp.message(AddActionStates.waiting_for_initial)
async def process_initial(message: Message, state: FSMContext):
    initial_text = f"{{sender}} {message.text}"
    await state.update_data(initial=initial_text)
    
    await message.answer(
        "Принято! Теперь напиши действие при **согласии**.\n"
        "❗️ Бот **сам** поставит твое имя в начало, а имя друга в конец.\n\n"
        "👉 *Пример:* `жестко отжарил кисик`"
    )
    await state.set_state(AddActionStates.waiting_for_accept)


@dp.message(AddActionStates.waiting_for_accept)
async def process_accept(message: Message, state: FSMContext):
    accept_text = f"{{sender}} {message.text} {{clicker}}"
    await state.update_data(accept=accept_text)
    
    await message.answer(
        "Супер. И последнее — действие при **отказе**.\n"
        "❗️ Тут бот поставит имя друга в начало, а твое в конец.\n\n"
        "👉 *Пример:* `не дался(лась)`"
    )
    await state.set_state(AddActionStates.waiting_for_decline)


@dp.message(AddActionStates.waiting_for_decline)
async def process_decline(message: Message, state: FSMContext):
    decline_text = f"{{clicker}} {message.text} {{sender}}"
    data = await state.get_data()
    
    action = add_action(
        key=data["key"], 
        emoji=data["emoji"], 
        initial=data["initial"], 
        accept=data["accept"], 
        decline=decline_text, 
        added_by=message.from_user.id
    )
    
    await message.answer(
        f"✅ Действие «{action['emoji']} {action['key']}» успешно добавлено!\n\n"
        f"**Как это будет выглядеть:**\n"
        f"🔘 **Предложение:** {action['initial'].format(sender='Гошан', clicker='')}\n"
        f"✅ **Согласие:** {action['accept'].format(sender='Гошан', clicker='Аня')}\n"
        f"❌ **Отказ:** {action['decline'].format(sender='Гошан', clicker='Аня')}"
    )
    await state.clear()


# --- ОСТАЛЬНЫЕ КОМАНДЫ ---

@dp.message(Command("delaction"))
async def del_action_cmd(message: Message):
    key = message.text.partition(" ")[2].strip()
    if not key:
        await message.answer("Укажи ключ действия: /delaction обнять")
        return

    action = get_action(key)
    if not action:
        await message.answer(f"Действие «{key}» не найдено.")
        return

    is_owner = action.get("added_by") == message.from_user.id
    if not (is_owner or is_admin(message.from_user.id)):
        await message.answer("Удалить это действие может только тот, кто его добавил, или админ.")
        return

    delete_action(key)
    await message.answer(f"Действие «{key}» удалено.")


@dp.message(Command("lockadd"))
async def lockadd_cmd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда только для админа.")
        return
    set_public_adding(False)
    await message.answer("🔒 Добавление действий другими людьми закрыто. Только ты можешь добавлять.")


@dp.message(Command("unlockadd"))
async def unlockadd_cmd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда только для админа.")
        return
    set_public_adding(True)
    await message.answer("🔓 Добавление действий снова открыто для всех.")


@dp.inline_query()
async def handle_inline(inline_query: InlineQuery):
    query_text = inline_query.query.strip().lower()
    sender_name = inline_query.from_user.full_name
    sender_id = inline_query.from_user.id

    actions = load_actions()
    matched = [a for a in actions if query_text in a["key"]] if query_text else actions

    results = []
    for action in matched[:20]:
        token = uuid4().hex[:12]
        pending_actions[token] = {
            "sender_id": sender_id,
            "sender_name": sender_name,
            "action_key": action["key"],
        }

        initial_text = action["initial"].format(sender=sender_name, clicker="")

        # Клавиатура при отправке запроса (Принять / Отказаться + Кнопка ответа)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"act:{token}:accept"),
                InlineKeyboardButton(text="❌ Отказаться", callback_data=f"act:{token}:decline"),
            ],
            [
                InlineKeyboardButton(text="🔄 Ответить действием", switch_inline_query="")
            ]
        ])

        results.append(
            InlineQueryResultArticle(
                id=token,
                title=f"{action['emoji']} {action['key'].capitalize()}",
                description=initial_text,
                input_message_content=InputTextMessageContent(message_text=initial_text),
                reply_markup=keyboard,
            )
        )

    await inline_query.answer(results, cache_time=1, is_personal=True)


@dp.callback_query(F.data.startswith("act:"))
async def handle_action_callback(callback: CallbackQuery):
    try:
        _, token, decision = callback.data.split(":")
    except ValueError:
        await callback.answer("Некорректные данные кнопки.", show_alert=True)
        return

    data = pending_actions.get(token)
    if not data:
        await callback.answer("Это действие уже неактуально.", show_alert=True)
        return

    if callback.from_user.id == data["sender_id"]:
        await callback.answer("Нельзя ответить самому себе 🙂", show_alert=True)
        return

    action = get_action(data["action_key"])
    if not action:
        await callback.answer("Это действие больше не существует.", show_alert=True)
        return

    clicker_name = callback.from_user.full_name
    sender_name = data["sender_name"]

    template = action["accept"] if decision == "accept" else action["decline"]
    final_text = template.format(sender=sender_name, clicker=clicker_name)

    # Оставляем кнопку "Ответить действием" и после нажатия на Принять/Отказаться
    finish_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Ответить действием", switch_inline_query="")
        ]
    ])

    await bot.edit_message_text(
        text=final_text, 
        inline_message_id=callback.inline_message_id, 
        reply_markup=finish_keyboard
    )
    await callback.answer()
    pending_actions.pop(token, None)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())