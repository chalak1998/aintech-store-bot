import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '9165569217:AAFraChMNcPflGo91Y7B1pw2Cy3_rTKeIQ8'
ADMIN_ID = 123456789  # لێرە ئایدی تیلیگرامی خۆت دابنە
ADMIN_USERNAME = "chalakramazan"  # یۆزەرنەمی تیلیگرامی خۆت بۆ پەیوەندی ڕاستەوخۆ

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# بەستنەوە بە داتابەیس
conn = sqlite3.connect('aintech_store.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT DEFAULT 'ku'
)
''')
conn.commit()

# فەرمانی سەرەتایی /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id, lang) VALUES (?, 'ku')", (user_id,))
    conn.commit()
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="کوردی 🇮🇶", callback_data="lang_ku"),
                InlineKeyboardButton(text="العربية 🇸🇦", callback_data="lang_ar")
            ]
        ]
    )
    
    await message.answer(
        "بەخێر هاتیت بۆ بۆتی ئاینتەک ستۆر! 🤖\nتکایە زمانەکەت هەڵبژێرە:\n\nمرحباً بك في بوت آينتك ستۆر!\nيرجى اختيار لغتك:",
        reply_markup=keyboard
    )

# گۆڕینی زمان و پیشاندانی ٣ مۆدێلە سەرەکییەکە
@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def set_language(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_lang = callback_query.data.split('_')[1]
    
    cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (selected_lang, user_id))
    conn.commit()
    
    if selected_lang == 'ku':
        text = (
            "🤖 **مۆدێلە زیرەکەکان (AI Subscriptions):**\n\n"
            "فەرموو یەکێک لەم مۆدێلانە هەڵبژێرە بۆ زانیاری و نرخ:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🟢 ChatGPT Pro", callback_data="chatgpt_pro")],
                [InlineKeyboardButton(text="🟣 Claude Pro", callback_data="claude_pro")],
                [InlineKeyboardButton(text="🔵 Gemini Pro", callback_data="gemini_pro")],
                [InlineKeyboardButton(text="💬 پەیوەندی بە بەڕێوەبەرەوە", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="⚙️ گۆڕینی زمان", callback_data="change_lang")]
            ]
        )
    else:
        text = (
            "🤖 **الاشتراكات الذكية (AI Subscriptions):**\n\n"
            "يرجى اختيار أحد هذه النماذج لمعرفة التفاصيل والسعر:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🟢 ChatGPT Pro", callback_data="chatgpt_pro")],
                [InlineKeyboardButton(text="🟣 Claude Pro", callback_data="claude_pro")],
                [InlineKeyboardButton(text="🔵 Gemini Pro", callback_data="gemini_pro")],
                [InlineKeyboardButton(text="💬 التواصل مع الإدارة", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="⚙️ تغيير اللغة", callback_data="change_lang")]
            ]
        )
        
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# زانیاری و نرخی ChatGPT Pro
@dp.callback_query(lambda c: c.data == 'chatgpt_pro')
async def model_chatgpt(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'ku'
    
    if lang == 'ku':
        text = (
            "🟢 **ChatGPT Pro**\n\n"
            "💰 **نرخ:** ١٠,٠٠٠ دینار (بۆ مانگێک)\n\n"
            "باشترین یاریدەدەری زیرەک بۆ نووسین، شیکاری و پرسیارە گشتییەکان."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 کڕینی ئیشتراک (پێدانی پارە)", callback_data="buy_chatgpt")],
                [InlineKeyboardButton(text="💬 پەیوەندی ڕاستەوخۆ", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 گەڕانەوە", callback_data="back_to_menu")]
            ]
        )
    else:
        text = (
            "🟢 **ChatGPT Pro**\n\n"
            "💰 **السعر:** ١٠,٠٠٠ دينار (لشهر واحد)\n\n"
            "الأفضل للمساعدة الذكية والكتابة والتحليل."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 شراء الاشتراك (الدفع)", callback_data="buy_chatgpt")],
                [InlineKeyboardButton(text="💬 تواصل مباشر", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_menu")]
            ]
        )
        
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# زانیاری و نرخی Claude Pro
@dp.callback_query(lambda c: c.data == 'claude_pro')
async def model_claude(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'ku'
    
    if lang == 'ku':
        text = (
            "🟣 **Claude Pro**\n\n"
            "💰 **نرخ:** ١٠,٠٠٠ دینار (بۆ مانگێک)\n\n"
            "تایبەت بە شیکاری قووڵی دەق، وەرگێڕان و یارمەتیدانی لێهاتوو لە کۆدکردندا."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 کڕینی ئیشتراک (پێدانی پارە)", callback_data="buy_claude")],
                [InlineKeyboardButton(text="💬 پەیوەندی ڕاستەوخۆ", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 گەڕانەوە", callback_data="back_to_menu")]
            ]
        )
    else:
        text = (
            "🟣 **Claude Pro**\n\n"
            "💰 **السعر:** ١٠,٠٠٠ دينار (لشهر واحد)\n\n"
            "مخصص للتحليل العميق والترجمة والمساعدة المتقدمة في البرمجة."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 شراء الاشتراك (الدفع)", callback_data="buy_claude")],
                [InlineKeyboardButton(text="💬 تواصل مباشر", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_menu")]
            ]
        )
        
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# زانیاری و نرخی Gemini Pro
@dp.callback_query(lambda c: c.data == 'gemini_pro')
async def model_gemini(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'ku'
    
    if lang == 'ku':
        text = (
            "🔵 **Gemini Pro**\n\n"
            "💰 **نرخ:** ١٠,٠٠٠ دینار (بۆ مانگێک)\n\n"
            "مۆدێلی پێشکەوتووی گووگڵ بۆ خێرایی، پرۆسێسکردنی زانیاری و وێنە."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 کڕینی ئیشتراک (پێدانی پارە)", callback_data="buy_gemini")],
                [InlineKeyboardButton(text="💬 پەیوەندی ڕاستەوخۆ", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 گەڕانەوە", callback_data="back_to_menu")]
            ]
        )
    else:
        text = (
            "🔵 **Gemini Pro**\n\n"
            "💰 **السعر:** ١٠,٠٠٠ دينار (لشهر واحد)\n\n"
            "نموذج جوجل المتقدم للسرعة ومعالجة البيانات والصور."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 شراء الاشتراك (الدفع)", callback_data="buy_gemini")],
                [InlineKeyboardButton(text="💬 تواصل مباشر", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_menu")]
            ]
        )
        
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# بەشی ڕێنمایی پارەدان بە ژمارە ڕاستەقینەکان
@dp.callback_query(lambda c: c.data.startswith('buy_'))
async def payment_methods(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'ku'
    
    if lang == 'ku':
        text = (
            "💳 **ڕێگاکانی پێدانی پارە (Payment Methods):**\n\n"
            "بۆ تەواوکردنی کڕینەکە، تکایە بڕی **١٠,٠٠٠ دینار** بنێرە بۆ یەکێک لەم هەژمارانەی خوارەوە:\n\n"
            "📱 **زین کاش (ZainCash):** `07831556444`\n"
            "💳 **ماستەرکارد (Mastercard):** `07517842044`\n"
            "🏦 **فێرست ئای بانک (FIB):** `07755184537`\n\n"
            "📷 دوای ناردنی پارەکە، وێنەی ڕەسیدەکە لێرە بنێرە یان دوگمەی خوارەوە بەکاربهێنە بۆ پەیوەندیکردن:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💬 ناردنی ڕەسید و پەیوەندی بە بەڕێوەبەر", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 گەڕانەوە بۆ مۆدێلەکان", callback_data="back_to_menu")]
            ]
        )
    else:
        text = (
            "💳 **طرق الدفع (Payment Methods):**\n\n"
            "لإتمام الشراء، يرجى إرسال مبلغ **١٠,٠٠٠ دينار** إلى أحد الحسابات التالية:\n\n"
            "📱 **زين كاش (ZainCash):** `07831556444`\n"
            "💳 **ماستركارد (Mastercard):** `07517842044`\n"
            "🏦 **فێرست ئای بانک (FIB):** `07755184537`\n\n"
            "📷 بعد إرسال المبلغ، أرسل صورة الإيصال أو استخدم الزر أدناه للتواصل:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💬 إرسال الإيصال والتواصل مع الإدارة", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="🔙 رجوع إلى النماذج", callback_data="back_to_menu")]
            ]
        )
        
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# گەڕانەوە بۆ مێنیووی سەرەکی مۆدێلەکان
@dp.callback_query(lambda c: c.data == 'back_to_menu')
async def back_to_menu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'ku'
    
    if lang == 'ku':
        text = (
            "🤖 **مۆدێلە زیرەکەکان (AI Subscriptions):**\n\n"
            "فەرموو یەکێک لەم مۆدێلانە هەڵبژێرە بۆ زانیاری و نرخ:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🟢 ChatGPT Pro", callback_data="chatgpt_pro")],
                [InlineKeyboardButton(text="🟣 Claude Pro", callback_data="claude_pro")],
                [InlineKeyboardButton(text="🔵 Gemini Pro", callback_data="gemini_pro")],
                [InlineKeyboardButton(text="💬 پەیوەندی بە بەڕێوەبەرەوە", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="⚙️ گۆڕینی زمان", callback_data="change_lang")]
            ]
        )
    else:
        text = (
            "🤖 **الاشتراكات الذكية (AI Subscriptions):**\n\n"
            "يرجى اختيار أحد هذه النماذج لمعرفة التفاصيل والسعر:"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🟢 ChatGPT Pro", callback_data="chatgpt_pro")],
                [InlineKeyboardButton(text="🟣 Claude Pro", callback_data="claude_pro")],
                [InlineKeyboardButton(text="🔵 Gemini Pro", callback_data="gemini_pro")],
                [InlineKeyboardButton(text="💬 التواصل مع الإدارة", url=f"https://t.me/{ADMIN_USERNAME}")],
                [InlineKeyboardButton(text="⚙️ تغيير اللغة", callback_data="change_lang")]
            ]
        )
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback_query.answer()

# گەڕانەوە بۆ گۆڕینی زمان
@dp.callback_query(lambda c: c.data == 'change_lang')
async def back_to_lang(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="کوردی 🇮🇶", callback_data="lang_ku"),
                InlineKeyboardButton(text="العربية 🇸🇦", callback_data="lang_ar")
            ]
        ]
    )
    await callback_query.message.edit_text(
        "تکایە زمانەکەت هەڵبژێرە:\n\nيرجى اختيار لغتك:",
        reply_markup=keyboard
    )
    await callback_query.answer()

async def main():
    print("بۆتەکە دەستی بە کارکرد کرد و چاوەڕێی پەیام دەکات...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())