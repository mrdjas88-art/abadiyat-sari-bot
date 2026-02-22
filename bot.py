from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, VIDEO_1, VIDEO_2, VIDEO_3, VIDEO_4

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchi qadami xotirasi
user_step = {}

# Progress-barni yaratish funksiyasi
def get_progress_bar(step):
    progress = ["○"] * 4
    for i in range(step):
        progress[i] = "●"
    return " ".join(progress)


# 1. AVTOMATIK TABRIKLASH
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def welcome_new_user(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_step:
        user_step[user_id] = 0
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text="🕋 TAFAKKUR YO'LIGA KIRISH",
                callback_data="step_1"
            )
        )
        
        await message.answer(
            "Assalomu alaykum. 🌙\n\n"
            "«ABADIYAT SARI» botiga xush kelibsiz.\n\n"
            "Bu 4 bosqichli yo'l sizni eng muhim narsalar —\n"
            "hayot, o'lim va abadiyat haqida o'ylashga chorlaydi.\n\n"
            "Birinchi qadamga tayyormisiz?\n"
            "Tayyor bo'lsangiz, pastdagi tugmani bosing...",
            reply_markup=keyboard
        )

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_step[message.from_user.id] = 0

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="▶️ Tafakkur yo'liga kirish",
            callback_data="step_1"
        )
    )

    await message.answer(
        "Assalomu alaykum.\n\n"
        "Agar hozir shu yerdasiz — bu tasodif emas.\n"
        "Ba'zida birgina eslatmaning o'zi kifoyadir,\n"
        "ichingizdagi bir narsa o'z o'rniga tushishi uchun.\n\n"
        "Eng muhim narsaga vaqt ajratishga tayyormisiz?\n"
        "4 bosqichdan iborat yo'lni bosib o'ting —\n"
        "o'limdan to abadiyatgacha.",
        reply_markup=keyboard
    )

@dp.callback_query_handler(text="step_1")
async def step_1(call: types.CallbackQuery):
    user_step[call.from_user.id] = 1

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕯️ Videoni oxirigacha ko'rdim",
            callback_data="step_2"
        )
    )

    await call.message.answer(
        f"{get_progress_bar(1)}\n"
        "🕯️ *O'limdan keyingi dastlabki soatlarda ruhni nima kutadi?*\n\n"
        "• O'lim farishtasi kelgan payt\n"
        "• Shaytonning so'nggi pichirlashi\n"
        "• Qabrdagi savollar: «Kim sening Parvardigoring?»\n\n"
        "⚠️ _Oxirigacha tomosha qiling — eng muhimi so'ngi qismlarda._",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_1
    )

    await call.message.answer(
        "Ko'rib bo'lganingizdan so'ng pastdagi tugmani bosing.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_2")
async def step_2(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 1:
        await call.answer("Avval oldingi videoni ko'ring.", show_alert=True)
        return

    user_step[call.from_user.id] = 2

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🌍 Keyingi qismni ko'rishga tayyorman",
            callback_data="step_3"
        )
    )

    await call.message.answer(
        f"{get_progress_bar(2)}\n"
        "🌍 *Dunyoning oxiri: qanday bo'ladi?*\n\n"
        "• Olamlarni yemiruvchi sur sadosi\n"
        "• Amalga oshayotgan 10 alomat\n"
        "• Buyuk belgilar: Dajjol, Mahdiy, Iso (alayhissalom)\n\n"
        "Bu fantastika emas. Bu — va'da qilingan haqiqat.",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_2
    )

    await call.message.answer(
        "Ko'rib bo'lganingizdan so'ng pastdagi tugmani bosing.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_3")
async def step_3(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 2:
        await call.answer("Avval oldingi bosqichni o'ting.", show_alert=True)
        return

    user_step[call.from_user.id] = 3

    await call.message.answer(
        f"{get_progress_bar(3)}\n"
        "⚖️ *Hamma narsa oshkor bo'ladigan kun*\n\n"
        "• Amallar daftari o'ng yoki chap qo'lda\n"
        "• Qildan nozik, qilichdan o'tkir Sirot ko'prigi\n"
        "• Har bir o'y-fikr taroziga tortiladigan kun",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_3
    )

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="⚖️ Hisob-kitob muhimligini angladim",
            callback_data="step_3_watched"
        )
    )

    await call.message.answer(
        "Videoni ko'rib bo'lganingizdan so'ng pastdagi tugmani bosing.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_3_watched")
async def step_3_watched(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🤝 YAQINIMGA ULASHISH",
            switch_inline_query="Bu bot menga eng muhim narsalarni anglashga yordam berdi. Sizga ham ulashyapman. Vaqt ajratib o'rganing, tafakkur qiling — zero, bu bilimlar abadiy hayot uchun kerak. Alloh barchamizni to'g'ri yo'lga hidoyat qilsin 🤲 "
        ),
        types.InlineKeyboardButton(
            text="▶️ O'Z YO'LIMNI ABADIYAT SARI DAVOM ETTIRISH",
            callback_data="step_4"
        )
    )

    await call.message.answer(
        "🤔 *Ushbu videodan so'ng o'zingizdan so'rang:*\n"
        "«Mening yaqinlarimdan kimga hozir bu eslatma kerak?»\n\n"
        "👥 *Kimga bu eslatmani yuborishingiz mumkin?*\n\n"
        "Bunday mulohazalardan so'ng ko'pincha\n"
        "o'sha odamning siymosi ko'z oldingizga keladi —\n"
        "aynan hozir buni ko'rishi *juda muhim* bo'lgan inson.\n\n"
        "Pastdagi tugmani bosing va kontakt tanlang,\n"
        "u sizdan shaxsiy xabar oladi.\n\n"
        "Davom etishga tayyor bo'lsangiz — ikkinchi tugmani bosing.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await call.answer()

@dp.callback_query_handler(text="step_4")
async def step_4(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 3:
        await call.answer("Avval oldingi bosqichlarni o'ting.", show_alert=True)
        return

    user_step[call.from_user.id] = 4

    await call.message.answer(
        f"{get_progress_bar(4)}\n"
        "🏁 *Yakuniy tanlov: abadiy qaror*\n\n"
        "• Jannat: ko'z ko'rmagan, quloq eshitmagan ne'matlar\n"
        "• Do'zax: bir soatlik azob 50 000 yilga teng\n"
        "• Allohning jamolini ko'rish — eng ulug' mukofot\n\n"
        "Bu ertak emas. Bu — har birimizni kutayotgan haqiqat.",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_4
    )

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕋 Tafakkur yo'lini yakunladim",
            callback_data="step_4_watched"
        )
    )

    await call.message.answer(
        "Yakuniy videoni ko'rib bo'lganingizdan so'ng pastdagi tugmani bosing.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_4_watched")
async def step_4_watched(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕯️ «ABADIYAT SARI» kanalida yo'lni davom ettirish",
            url="https://t.me/TowardsEternity_UZ"
        ),
        types.InlineKeyboardButton(
            text="🤝 Bu botni boshqalarga ulashish",
            switch_inline_query="Bu bot menga eng muhim narsalarni anglashga yordam berdi. Sizga ham ulashyapman. Vaqt ajratib o'rganing, tafakkur qiling — zero, bu bilimlar abadiy hayot uchun kerak. Alloh barchamizni to'g'ri yo'lga hidoyat qilsin 🤲 "
        )
    )

    await call.message.answer(
        "🕋 *Siz tafakkur yo'lini yakunladingiz*\n\n"
        "Endi siz bilasiz:\n"
        "✅ O'limdan keyin bizni nima kutishini\n"
        "✅ Qiyomat qanday bo'lishini\n"
        "✅ Qilgan amallarimiz qanday tarozida tortilishini\n"
        "✅ Abadiy tanlovimiz esa: Jannat yoki Do'zax\n\n"
        "*Bu bilim — qo'rquv uchun emas, balki amal uchundir.*\n"
        "Bir namoz, bir yaxshilik, Alloh tomon bir qadam —\n"
        "butun abadiy taqdiringizni o'zgartirishi mumkin.\n\n"
        "Agar bu mavzularda chuqurroq bilim olishni istasangiz,\n"
        "bizning kanalimizda abadiyat haqida mulohazalar mavjud.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await call.answer()

@dp.channel_post_handler(content_types=types.ContentTypes.VIDEO)
async def get_channel_video_id(message: types.Message):
    print(message.video.file_id)

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)





