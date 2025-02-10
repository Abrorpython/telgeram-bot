from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = '7721986885:AAEh6OZmfKgO2qei9LNYDdEdKmjVg8QY1gc'
OPEN_CHANNEL = 'karyeralar'  # Kanal username

kino_files = {
    "203": "https://t.me/uzb_kinolar777/7",
    "KINO2": "HaqiqiyFileID2",
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    try:
        # Kanalga obuna bo'lganligini tekshirish
        status = await bot.get_chat_member(chat_id=f"@{OPEN_CHANNEL}", user_id=user_id)
        if status.status in ['member', 'administrator', 'creator']:
            # Agar foydalanuvchi obuna bo'lgan bo'lsa
            await message.reply(
                "Siz allaqachon kanalga obuna bo‘lgansiz! Endi kino kodini yuboring. Masalan: `203`",
                parse_mode="Markdown"
            )
        else:
            # Agar foydalanuvchi obuna bo'lmagan bo'lsa
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("📢 Kanalga Obuna Bo‘lish", url=f"https://t.me/{OPEN_CHANNEL}"))
            keyboard.add(InlineKeyboardButton("✅ Obunani Tekshirish", callback_data='check_subscription'))
            await message.reply(
                "Assalomu alaykum!\n\nKinoni olish uchun ochiq kanalga obuna bo‘ling va obunani tasdiqlang.",
                reply_markup=keyboard
            )
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")


@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        status = await bot.get_chat_member(chat_id=f"@{OPEN_CHANNEL}", user_id=user_id)
        if status.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(callback_query.id, "Obuna tasdiqlandi!")
            await callback_query.message.answer(
                "Tabriklaymiz! Endi kino kodini yuboring. Masalan: `203`",
                parse_mode="Markdown"
            )
        else:
            await bot.answer_callback_query(callback_query.id, "Siz hali kanalga obuna bo‘lmadingiz!", show_alert=True)
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, f"Xatolik yuz berdi: {e}", show_alert=True)


@dp.message_handler()
async def handle_kino_request(message: types.Message):
    kino_code = message.text.strip().upper()
    if kino_code in kino_files:
        try:
            await message.reply("Siz so‘ragan kino:")
            await bot.send_document(chat_id=message.chat.id, document=kino_files[kino_code])
        except Exception as e:
            await message.reply(f"❌ Faylni yuborishda xatolik yuz berdi: {e}")
    else:
        await message.reply(
            "❌ Bunday kod mavjud emas.\n"
            "Iltimos, to‘g‘ri kod kiriting yoki /start buyrug‘ini qayta kiriting."
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
