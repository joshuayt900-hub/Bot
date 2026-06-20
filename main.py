import os
import logging
import discord
from discord.ext import commands

# --------------------
# LOGGING
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------
# INTENTS
# --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# --------------------
# BOT
# --------------------
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# --------------------
# EVENTS
# --------------------
@bot.event
async def on_ready():
    logging.info(f"Bot online: {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Command Fehler: {error}")
    await ctx.send("❌ Beim Ausführen des Befehls ist ein Fehler aufgetreten.")

# --------------------
# COMMANDS
# --------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong")

@bot.command()
async def info(ctx):
    await ctx.send(
        f"🤖 Bot: {bot.user.name}\n"
        f"🆔 ID: {bot.user.id}"
    )

# --------------------
# MESSAGE LOGGING
# --------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    logging.info(
        f"[{message.guild}] "
        f"{message.author}: {message.content}"
    )

    await bot.process_commands(message)

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN nicht gefunden!")
else:
    bot.run(TOKEN)
