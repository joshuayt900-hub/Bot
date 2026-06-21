import os
import time
import logging
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

START = time.time()

# --------------------
# LOGGING (CLEAN MODE)
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Discord intern ruhig stellen
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("discord.client").setLevel(logging.ERROR)
logging.getLogger("discord.gateway").setLevel(logging.ERROR)
logging.getLogger("discord.voice_client").setLevel(logging.CRITICAL)

# --------------------
# OWNER ROLE
# --------------------
OWNER_ROLE_ID = 1449769777470898226

# --------------------
# DATABASE
# --------------------
db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bans (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    reason TEXT,
    timestamp INTEGER
)
""")
db.commit()

def add_ban(user_id, username, reason):
    cursor.execute(
        "INSERT OR REPLACE INTO bans VALUES (?, ?, ?, ?)",
        (str(user_id), username, reason, int(time.time()))
    )
    db.commit()

def remove_ban(user_id):
    cursor.execute("DELETE FROM bans WHERE user_id = ?", (str(user_id),))
    db.commit()

def get_bans(limit=20):
    cursor.execute("SELECT user_id, username, reason FROM bans LIMIT ?", (limit,))
    return cursor.fetchall()

# --------------------
# BOT SETUP
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
        logging.error(f"on_ready error: {e}")

# --------------------
# ERROR HANDLER
# --------------------
@bot.tree.error
async def on_error(interaction, error):
    logging.error(f"{type(error).__name__}: {error}")
    try:
        if interaction.response.is_done():
            await interaction.followup.send("❌ Fehler", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Fehler", ephemeral=True)
    except:
        pass

# --------------------
# BASIC COMMANDS
# --------------------
@bot.tree.command(name="ping")
async def ping(interaction):
    await interaction.response.send_message(f"🏓 {round(bot.latency * 1000)}ms")

@bot.tree.command(name="info")
async def info(interaction):
    uptime = int(time.time() - START)
    await interaction.response.send_message(f"🤖 {bot.user} | {uptime}s")

# --------------------
# BAN SYSTEM
# --------------------
@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        add_ban(member.id, str(member), reason)
        await interaction.response.send_message("🔨 gebannt")
    except Exception as e:
        logging.error(f"ban error: {e}")
        await interaction.response.send_message("❌ Ban fehlgeschlagen", ephemeral=True)

@bot.tree.command(name="unban")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)

        remove_ban(user_id)

        await interaction.response.send_message("♻️ unban erfolgreich")

    except Exception as e:
        logging.error(f"unban error: {e}")
        try:
            if interaction.response.is_done():
                await interaction.followup.send("❌ Unban fehlgeschlagen", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Unban fehlgeschlagen", ephemeral=True)
        except:
            pass

@bot.tree.command(name="bans")
@app_commands.checks.has_permissions(ban_members=True)
async def bans(interaction):
    try:
        rows = get_bans()

        if not rows:
            return await interaction.response.send_message("Keine Bans")

        text = "\n".join([f"{u} | {n} | {r}" for u, n, r in rows])
        await interaction.response.send_message(text[:1900])

    except Exception as e:
        logging.error(f"bans error: {e}")
        await interaction.response.send_message("❌ Fehler", ephemeral=True)

# --------------------
# CLEAR
# --------------------
@bot.tree.command(name="clear")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction, amount: int):
    try:
        if amount < 1:
            return await interaction.response.send_message("❌ min 1")
        if amount > 100:
            return await interaction.response.send_message("❌ max 100")

        await interaction.response.defer()

        deleted = await interaction.channel.purge(limit=amount + 1)

        await interaction.followup.send(
            f"🧹 {len(deleted)-1} gelöscht",
            ephemeral=True
        )

    except Exception as e:
        logging.error(f"clear error: {e}")
        try:
            await interaction.followup.send("❌ Clear fehlgeschlagen", ephemeral=True)
        except:
            pass

# --------------------
# EMERGENCY STOP
# --------------------
@bot.tree.command(name="emergency_stop")
async def emergency_stop(interaction):
    member = interaction.user

    if not any(role.id == OWNER_ROLE_ID for role in member.roles):
        return await interaction.response.send_message("❌ keine Rechte", ephemeral=True)

    await interaction.response.send_message("🛑 Bot stoppt")
    logging.warning(f"EMERGENCY STOP by {member}")
    await bot.close()

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN fehlt")

bot.run(TOKEN)