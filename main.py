import os
import logging
import discord
from discord import app_commands
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

bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# READY
# --------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    logging.info(f"Bot online als {bot.user}")

# --------------------
# GLOBAL ERROR HANDLER (WICHTIG)
# --------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    logging.error(f"Slash Error: {error}")

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                "❌ Fehler beim Command.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Fehler beim Command.",
                ephemeral=True
            )
    except:
        pass

# --------------------
# SLASH: /ping
# --------------------
@bot.tree.command(name="ping", description="Bot antwortet mit Pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong")

# --------------------
# SLASH: /info
# --------------------
@bot.tree.command(name="info", description="Bot Infos anzeigen")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🤖 Bot: {bot.user}\n🆔 ID: {bot.user.id}"
    )

# --------------------
# SLASH: /kick
# --------------------
@bot.tree.command(name="kick", description="User kicken")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(
            f"👢 {member} wurde gekickt. Grund: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Fehler: {e}",
            ephemeral=True
        )

# --------------------
# SLASH: /ban
# --------------------
@bot.tree.command(name="ban", description="User bannen")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"🔨 {member} wurde gebannt. Grund: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Fehler: {e}",
            ephemeral=True
        )

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt!")
else:
    bot.run(TOKEN)