import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

START_TIME = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_error(where, error):
    logging.error(f"[{where}] {type(error).__name__}: {error}")

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

        logging.info("===================================")
        logging.info("🤖 BOT STARTED / RESTARTED")
        logging.info(f"👤 Logged in as: {bot.user}")
        logging.info(f"⏱ Uptime: {uptime}s")
        logging.info("🚀 STATUS: ONLINE")
        logging.info("===================================")

    except Exception as e:
        log_error("on_ready", e)

# --------------------
# SLASH ERROR HANDLER
# --------------------
@bot.tree.error
async def on_app_command_error(interaction, error):
    log_error("slash", error)

    try:
        if interaction.response.is_done():
            await interaction.followup.send("❌ Fehler im Command.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Fehler im Command.", ephemeral=True)
    except:
        pass

# --------------------
# TEXT ERROR HANDLER
# --------------------
@bot.event
async def on_command_error(ctx, error):
    log_error("text", error)
    await ctx.send("❌ Fehler beim Command.")

# --------------------
# COMMANDS
# --------------------
@bot.tree.command(name="ping")
async def ping(interaction):
    await interaction.response.send_message("🏓 Pong")

@bot.tree.command(name="info")
async def info(interaction):
    await interaction.response.send_message(f"🤖 {bot.user}")

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message("👢 gekickt")
    except Exception as e:
        log_error("kick", e)

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message("🔨 gebannt")
    except Exception as e:
        log_error("ban", e)

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt → Bot stoppt")
    exit(1)

bot.run(TOKEN)