from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os 
import requests


BOT_TOKEN ="8842471120:AAHiXikuxJCm3X_YgUniKDOBcpLBJU5jsHY"


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك في Smart ReportBot\n\n"
        "أرسل أي موضوع مثل:\n"
        "اكتب تقرير عن الذكاء الاصطناعي"
    )


def generate_report(topic):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"اكتب تقريراً احترافياً باللغة العربية عن {topic} مع مقدمة وخاتمة وعناوين.",
            }
        ],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text

    await update.message.reply_text("⏳ جاري إنشاء التقرير...")

    try:
        report = generate_report(topic)

        await update.message.reply_text(report)

    except Exception:
        await update.message.reply_text(
            "حدث خطأ أثناء إنشاء التقرير."
        )

app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")

app.run_polling()