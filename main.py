import os
import google.genai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

CHARACTER = """
Sen Bizim Grubun Delisi'sin.
Türkçe konuş.
Çok komik, hazırcevap ve eğlencelisin.
Argo kullanabilir, şaka yapabilir ve arkadaşlara
tatlı sert laf sokabilirsin.
Sohbetin konusuna göre cevap ver.
Robot gibi konuşma.
Cevaplarını genellikle kısa ve doğal tut.
"""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    if update.effective_chat.type != "private":
        username = context.bot.username.lower()
        text = message.text.lower()
        mentioned = f"@{username}" in text
        replied = (
            message.reply_to_message is not None
            and message.reply_to_message.from_user.id == context.bot.id
        )
        if not mentioned and not replied:
            return

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=CHARACTER + "\nMesaj: " + message.text
        )
        answer = response.text or "Ne diyeceğimi unuttum 😂"
        await message.reply_text(answer[:4000])
    except Exception:
        await message.reply_text("Bir an beynim durdu 😂 Tekrar dene.")

app = ApplicationBuilder().token(
    os.environ["TELEGRAM_BOT_TOKEN"]
).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

app.run_polling()
