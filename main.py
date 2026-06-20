import os
import discord
from discord import app_commands
from discord.ext import commands
import logging

# ----------------------------
# LOGGING (stabil für Debug)
# ----------------------------
logging.basicConfig(level=logging.INFO)

# ----------------------------
# INTENTS
# ----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# READY EVENT
# ----------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# ----------------------------
# SLASH COMMAND: /ping
# ----------------------------
@bot.tree.command(name="ping", description="Bot antwortet mit Pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")

# ----------------------------
# SLASH COMMAND: /info
# ----------------------------
@bot.tree.command(name="info", description="Bot Info")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message("Bot läuft stabil mit Slash Commands 🚀")

# ----------------------------
# SLASH COMMAND: /kick
# ----------------------------
@bot.tree.command(name="kick", description="Mitglied kicken")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} wurde gekickt. Grund: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Fehler: {e}", ephemeral=True)

# ----------------------------
# SLASH COMMAND: /ban
# ----------------------------
@bot.tree.command(name="ban", description="Mitglied bannen")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} wurde gebannt. Grund: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Fehler: {e}", ephemeral=True)

# ----------------------------
# ERROR HANDLING (stabil)
# ----------------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f"Fehler: {error}", ephemeral=True)

# ----------------------------
# START BOT
# ----------------------------
bot.run(os.getenv("TOKEN"))