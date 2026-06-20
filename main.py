import time
import logging
import discord
from discord import app_commands
from discord.ext import commands

START_TIME = time.time()

bot = None

# --------------------
# BOT SETUP FUNCTION
# --------------------
def start_bot(token: str):
    global bot

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    register_events()
    register_commands()

    bot.run(token)

# --------------------
# EVENTS
# --------------------
def register_events():

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
# COMMANDS
# --------------------
def register_commands():

    @bot.tree.command(name="ping")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong")

    @bot.tree.command(name="info")
    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(f"🤖 {bot.user}")

    @bot.tree.command(name="kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
        await member.kick(reason=reason)
        await interaction.response.send_message("👢 gekickt")

    @bot.tree.command(name="ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
        await member.ban(reason=reason)
        await interaction.response.send_message("🔨 gebannt")

# --------------------
# ERROR HANDLING
# --------------------
@bot.tree.error
async def on_app_command_error(interaction, error):
    try:
        msg = "❌ Fehler im Command"

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)

    except:
        pass