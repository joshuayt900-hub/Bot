import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

# --------------------
# BASIC SETUP
# --------------------
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
    await bot.tree.sync()

    uptime = round(time.time() - START_TIME, 2)

    logging.info("===================================")
    logging.info("🤖 BOT ONLINE")
    logging.info(f"👤 {bot.user}")
    logging.info(f"⏱ Uptime: {uptime}s")
    logging.info("🚀 READY")
    logging.info("===================================")

# --------------------
# ERROR HANDLING
# --------------------
@bot.tree.error
async def on_app_command_error(interaction, error):
    log_error("slash", error)

    try:
        if interaction.response.is_done():
            await interaction.followup.send("❌ Fehler.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Fehler.", ephemeral=True)
    except:
        pass

# --------------------
# COMMAND HUB
# --------------------
@bot.tree.command(name="cmd", description="Command Hub")
async def cmd(interaction: discord.Interaction, action: str, user: discord.Member = None, reason: str = "Kein Grund"):
    """
    action:
    - help
    - ping
    - info
    - kick
    - ban
    """

    try:
        if action == "help":
            await interaction.response.send_message(
                "📜 Commands:\n"
                "ping | info | kick | ban"
            )

        elif action == "ping":
            await interaction.response.send_message("🏓 Pong")

        elif action == "info":
            await interaction.response.send_message(f"🤖 {bot.user}")

        elif action == "kick":
            if user:
                await user.kick(reason=reason)
                await interaction.response.send_message(f"👢 {user} gekickt")

        elif action == "ban":
            if user:
                await user.ban(reason=reason)
                await interaction.response.send_message(f"🔨 {user} gebannt")

        else:
            await interaction.response.send_message("❌ Ungültige Action")

    except Exception as e:
        log_error("cmd", e)

# --------------------
# START BOT
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt")
    exit(1)

bot.run(TOKEN)