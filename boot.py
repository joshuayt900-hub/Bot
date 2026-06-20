import os
import discord
from discord.ext import commands
import functions

# --------------------
# INTENTS
# --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# --------------------
# BOT
# --------------------
bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# READY
# --------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🤖 Bot online als {bot.user}")

# --------------------
# LOAD FUNCTIONS
# --------------------
functions.register(bot)

# --------------------
# START BOT
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("TOKEN fehlt")
    exit(1)

bot.run(TOKEN)