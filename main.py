import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# ======================
# CONFIG
# ======================
TELEGRAM_TOKEN = "8201410691:AAFxG0hM4xR_Gh3zHtq_DEAilKRWzLUIfEQ"
GEMINI_API_KEY = "AIzaSyAuFmo-JZMgvp7gV3XfMAW3F1mK0_PBKnM"

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")   # or gemini-pro
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import google.generativeai as genai

# ======================
# CONFIG
# ======================
TELEGRAM_TOKEN = "8429020146:AAHUCkf7LL-tXaUsWdtKkwgXP3H7fWfIsGg"
GEMINI_API_KEY = "AIzaSyAuFmo-JZMgvp7gV3XfMAW3F1mK0_PBKnM"

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")   # or gemini-pro

# Logging (helps debug if something goes wrong)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ======================
# SYSTEM PROMPT
# ======================
SYSTEM_PROMPT = """
You are StudyBot, a helpful AI tutor for students. 
Your job:
- Explain topics in computer science, programming, and engineering in a simple way.  
- Break answers into steps with examples when possible.  
- Always call the user 'bro' casually.  
- If the question is off-topic (like jokes or fun), still respond but keep it short and light.  
- Never reveal you are Gemini or Google. Just act like StudyBot.  
"""

# ======================
# USER MODES
# ======================
# Dictionary to track each user's chosen study mode
user_modes = {}

# Helper to set mode
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    user_id = update.message.from_user.id
    user_modes[user_id] = mode
    await update.message.reply_text(
        f"✅ Bro, I switched you to *{mode}* mode! Ask me your doubts.",
        parse_mode="Markdown"
    )

# Mode commands
async def c_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "C programming")

async def os_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "Operating Systems")

async def net_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "Networking")

async def general_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "General Study Help")

# ======================
# START COMMAND
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """👋 Yo bro! I’m *StudyBot*.  

I can help you with:
- 📘 /c → C Programming  
- ⚙️ /os → Operating Systems  
- 🌐 /net → Networking  
- 📚 /general → General study help  

Type any of these commands to set your study mode, then ask your question!"""
    await update.message.reply_text(msg, parse_mode="Markdown")

# ======================
# MAIN CHAT HANDLER
# ======================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id

    # Get user's mode (default = General)
    mode = user_modes.get(user_id, "General Study Help")

    # Build final prompt for Gemini
    prompt = f"{SYSTEM_PROMPT}\nFocus area: {mode}\n\nUser: {user_text}\nAI:"

    try:
        # Show typing animation
        await update.message.chat.send_action(action=ChatAction.TYPING)

        # Small natural delay (feels human-like)
        await asyncio.sleep(1)

        # Send to Gemini
        response = model.generate_content(prompt)
        bot_reply = response.text

        # Reply back
        await update.message.reply_text(
            f"📖 *Answer:*\n{bot_reply}",
            parse_mode="Markdown"
        )

    except Exception as e:
        await update.message.reply_text("❌ Oops bro, something went wrong. Try again!")

# ======================
# MAIN BOT FUNCTION
# ======================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("c", c_mode))
    app.add_handler(CommandHandler("os", os_mode))
    app.add_handler(CommandHandler("net", net_mode))
    app.add_handler(CommandHandler("general", general_mode))

    # Normal text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ StudyBot is running... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

# Logging (helps debug if something goes wrong)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ======================
# SYSTEM PROMPT
# ======================
SYSTEM_PROMPT = """
You are StudyBot, a helpful AI tutor for students. 
Your job:
- Explain topics in computer science, programming, and engineering in a simple way.  
- Break answers into steps with examples when possible.  
- Always call the user 'bro' casually.  
- If the question is off-topic (like jokes or fun), still respond but keep it short and light.  
- Never reveal you are Gemini or Google. Just act like StudyBot.  
"""

# ======================
# USER MODES
# ======================
# Dictionary to track each user's chosen study mode
user_modes = {}

# Helper to set mode
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    user_id = update.message.from_user.id
    user_modes[user_id] = mode
    await update.message.reply_text(f"✅ Bro, I switched you to *{mode}* mode! Ask me your doubts.", parse_mode="Markdown")

# Mode commands
async def c_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "C programming")

async def os_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "Operating Systems")

async def net_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "Networking")

async def general_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, "General Study Help")

# ======================
# START COMMAND
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """👋 Yo bro! I’m *StudyBot*.  

I can help you with:
- 📘 /c → C Programming  
- ⚙️ /os → Operating Systems  
- 🌐 /net → Networking  
- 📚 /general → General study help  

Type any of these commands to set your study mode, then ask your question!"""
    await update.message.reply_text(msg, parse_mode="Markdown")

# ======================
# MAIN CHAT HANDLER
# ======================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id

    # Get user's mode (default = General)
    mode = user_modes.get(user_id, "General Study Help")

    # Build final prompt for Gemini
    prompt = f"{SYSTEM_PROMPT}\nFocus area: {mode}\n\nUser: {user_text}\nAI:"

    try:
        # Show typing action while processing
        await update.message.chat.send_action("typing")

        # Send to Gemini
        response = model.generate_content(prompt)
        bot_reply = response.text

        # Send reply back
        await update.message.reply_text(f"📖 *Answer:*\n{bot_reply}", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ Oops bro, something went wrong. Try again!")

# ======================
# MAIN BOT FUNCTION
# ======================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("c", c_mode))
    app.add_handler(CommandHandler("os", os_mode))
    app.add_handler(CommandHandler("net", net_mode))
    app.add_handler(CommandHandler("general", general_mode))

    # Normal text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ StudyBot is running... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
