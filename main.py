import os
import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

START = time.time()

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
        logging.info(f"Online als {bot.user}")
    except Exception as e:
        logging.error(f"on_ready: {e}")

# --------------------
# SOFT ERROR HANDLING
# --------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    logging.error(f"{type(error).__name__}: {error}")

    try:
        msg = "❌ Fehler beim Command (wird automatisch behandelt)"

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

    except Exception as e:
        logging.error(f"error_handler: {e}")

# --------------------
# PING (ECHTE LATENZ)
# --------------------
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    try:
        start = time.perf_counter()

        await interaction.response.send_message("🏓 Ping wird gemessen...")
        end = time.perf_counter()

        api_latency = round(bot.latency * 1000)
        response_latency = round((end - start) * 1000)

        await interaction.edit_original_response(
            content=f"🏓 Pong\n📡 API: {api_latency}ms\n⚡ Response: {response_latency}ms"
        )

    except Exception as e:
        logging.error(f"ping: {e}")

# --------------------
# INFO
# --------------------
@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):
    uptime = int(time.time() - START)
    await interaction.response.send_message(
        f"🤖 {bot.user}\n⏱ Uptime: {uptime}s"
    )

# --------------------
# MODERATION (STABIL)
# --------------------
@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member} gekickt")
    except Exception as e:
        logging.error(f"kick: {e}")
        await interaction.response.send_message("❌ Kick fehlgeschlagen", ephemeral=True)

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member} gebannt")
    except Exception as e:
        logging.error(f"ban: {e}")
        await interaction.response.send_message("❌ Ban fehlgeschlagen", ephemeral=True)

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt")
    raise SystemExit(1)

bot.run(TOKEN)