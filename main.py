  import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

# --------------------
# STARTUP STATE
# --------------------
START_TIME = time.time()

# --------------------
# LOGGING
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_error(where, error):
    logging.error(f"[{where}] {type(error).__name__}: {error}")

# --------------------
# INTENTS
# --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# READY EVENT
# --------------------
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()

        uptime = round(time.time() - START_TIME, 2)

        logging.info("===================================")
        logging.info("🤖 BOT STARTED / RESTARTED")
        logging.info(f"👤 Logged in as: {bot.user}")
        logging.info(f"⏱ Startup Uptime: {uptime}s")
        logging.info("🚀 STATUS: ONLINE")
        logging.info("===================================")

        # Discord Restart Nachricht
        channel_id = 1450245897819521166
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send("🔄 Bot wurde neu gestartet und ist wieder online.")

    except Exception as e:
        log_error("on_ready", e)

# --------------------
# ERROR HANDLER (SLASH)
# --------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    log_error("slash_command", error)

    try:
        msg = "❌ Fehler im Command."
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except Exception as e:
        log_error("error_handler", e)

# --------------------
# ERROR HANDLER (TEXT)
# --------------------
@bot.event
async def on_command_error(ctx, error):
    log_error("text_command", error)
    await ctx.send("❌ Fehler beim Command.")

# --------------------
# SLASH COMMANDS
# --------------------

@bot.tree.command(name="ping", description="Test Command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong")

@bot.tree.command(name="info", description="Bot Info")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🤖 Bot: {bot.user}\n🆔 ID: {bot.user.id}"
    )

@bot.tree.command(name="kick", description="User kicken")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member} wurde gekickt")
    except Exception as e:
        log_error("kick", e)
        await interaction.response.send_message("❌ Kick fehlgeschlagen", ephemeral=True)

@bot.tree.command(name="ban", description="User bannen")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member} wurde gebannt")
    except Exception as e:
        log_error("ban", e)
        await interaction.response.send_message("❌ Ban fehlgeschlagen", ephemeral=True)

# --------------------
# START BOT
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt!")
else:
    try:
        bot.run(TOKEN)
    except Exception as e:
        log_error("bot_run", e)