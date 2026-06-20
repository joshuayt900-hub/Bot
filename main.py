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
        logging.info("Bot online & ready")
    except Exception as e:
        logging.error(f"on_ready error: {e}")

# --------------------
# ERROR HANDLER
# --------------------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    logging.error(f"{type(error).__name__}: {error}")

    try:
        msg = "❌ Fehler im Command"
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except:
        pass

# --------------------
# INFO COMMANDS
# --------------------
@bot.tree.command(name="ping", description="Test Command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong")

@bot.tree.command(name="info", description="Bot Info")
async def info(interaction: discord.Interaction):
    uptime = round(time.time() - START_TIME, 1)
    await interaction.response.send_message(f"🤖 {bot.user} | {uptime}s uptime")

@bot.tree.command(name="serverinfo", description="Server Infos")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(
        f"📡 {guild.name}\n👥 Members: {guild.member_count}"
    )

@bot.tree.command(name="userinfo", description="User Infos")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    await interaction.response.send_message(
        f"👤 {user}\n🆔 {user.id}\n📅 Joined: {user.joined_at}"
    )

# --------------------
# MODERATION (ADMIN ONLY)
# --------------------
@bot.tree.command(name="kick", description="User kicken")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 {member} gekickt")

@bot.tree.command(name="ban", description="User bannen")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {member} gebannt")

# --------------------
# LINK FILTER (BASIC AUTOMOD)
# --------------------
INVITE_BLOCK = ["discord.gg/", "discord.com/invite/"]

WHITELIST = ["youtube.com", "youtu.be", "github.com"]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # Invite Block
    if any(x in content for x in INVITE_BLOCK):
        if not message.author.guild_permissions.administrator:
            await message.delete()
            await message.channel.send("🚫 Invite-Links sind nicht erlaubt", delete_after=5)
            return

    # Link Whitelist
    if "http" in content:
        if not any(x in content for x in WHITELIST):
            if not message.author.guild_permissions.administrator:
                await message.delete()
                await message.channel.send("🚫 Link nicht erlaubt", delete_after=5)
                return

    await bot.process_commands(message)

# --------------------
# START BOT
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN fehlt")
    raise SystemExit(1)

bot.run(TOKEN)