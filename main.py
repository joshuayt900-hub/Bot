import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

# --------------------
# STARTUP
# --------------------
START_TIME = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# READY
# --------------------
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()

        uptime = round(time.time() - START_TIME, 2)

        logging.info("🤖 BOT ONLINE")
        logging.info(f"User: {bot.user}")
        logging.info(f"Uptime: {uptime}s")

    except Exception as e:
        logging.error(f"[on_ready] {type(e).__name__}: {e}")

# --------------------
# GLOBAL ERROR HANDLER
# --------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    try:
        logging.error(f"[slash_error] {type(error).__name__}: {error}")

        msg = "❌ Fehler im Command"

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

    except:
        pass

# --------------------
# COMMANDS
# --------------------
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong")

@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):
    uptime = round(time.time() - START_TIME, 2)
    await interaction.response.send_message(
        f"🤖 {bot.user}\n⏱ {uptime}s"
    )

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message("👢 gekickt")
    except Exception as e:
        logging.error(f"[kick] {type(e).__name__}: {e}")

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message("🔨 gebannt")
    except Exception as e:
        logging.error(f"[ban] {type(e).__name__}: {e}")

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt → Stop")
    exit(1)

bot.run(TOKEN)