import os
import logging
import discord
from discord import app_commands
from discord.ext import commands

# --------------------
# LOGGING (VERBESSERT)
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
# READY
# --------------------
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        logging.info(f"Bot online: {bot.user}")
    except Exception as e:
        log_error("on_ready sync", e)

# --------------------
# GLOBAL SLASH ERROR HANDLER
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
# TEXT COMMAND ERROR HANDLER
# --------------------
@bot.event
async def on_command_error(ctx, error):
    log_error("text_command", error)
    await ctx.send("❌ Fehler beim Ausführen des Commands.")

# --------------------
# SLASH COMMANDS
# --------------------

@bot.tree.command(name="ping", description="Test Command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong")

@bot.tree.command(name="info", description="Bot Info")
async def info(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(
            f"🤖 {bot.user}\n🆔 {bot.user.id}"
        )
    except Exception as e:
        log_error("info", e)

@bot.tree.command(name="kick", description="User kicken")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member} gekickt")
    except Exception as e:
        log_error("kick", e)
        await interaction.response.send_message("❌ Kick fehlgeschlagen", ephemeral=True)

@bot.tree.command(name="ban", description="User bannen")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member} gebannt")
    except Exception as e:
        log_error("ban", e)
        await interaction.response.send_message("❌ Ban fehlgeschlagen", ephemeral=True)

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt!")
else:
    try:
        bot.run(TOKEN)
    except Exception as e:
        log_error("bot_run", e)