import os
import time
import logging
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

# --------------------
# CORE
# --------------------
START = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

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
        logging.info(f"Bot online als {bot.user}")
    except Exception as e:
        logging.error(f"on_ready error: {e}")

# --------------------
# GLOBAL ERROR HANDLER
# --------------------
@bot.tree.error
async def on_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
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
# PING
# --------------------
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(
            f"🏓 Pong | {round(bot.latency * 1000)}ms"
        )
    except Exception as e:
        logging.error(f"ping error: {e}")

# --------------------
# INFO
# --------------------
@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):
    try:
        uptime = int(time.time() - START)
        await interaction.response.send_message(
            f"🤖 {bot.user}\n⏱ {uptime}s uptime"
        )
    except Exception as e:
        logging.error(f"info error: {e}")

# --------------------
# BAN SYSTEM
# --------------------
@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund"):
    try:
        await member.ban(reason=reason)
        add_ban(member.id, str(member), reason)
        await interaction.response.send_message(f"🔨 {member} gebannt")
    except Exception as e:
        logging.error(f"ban error: {e}")
        await interaction.response.send_message("❌ Ban fehlgeschlagen", ephemeral=True)

@bot.tree.command(name="unban")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)

        remove_ban(user_id)

        await interaction.response.send_message("♻️ entbannt + DB aktualisiert")

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
async def bans(interaction: discord.Interaction):
    try:
        rows = get_bans()

        if not rows:
            return await interaction.response.send_message("Keine Bans gespeichert.")

        text = "\n".join([f"{u} | {name} | {reason}" for u, name, reason in rows])
        await interaction.response.send_message(text[:1900])

    except Exception as e:
        logging.error(f"bans error: {e}")
        await interaction.response.send_message("❌ Fehler beim Laden", ephemeral=True)

# --------------------
# CLEAR (SAFE)
# --------------------
@bot.tree.command(name="clear")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    try:
        if amount < 1:
            return await interaction.response.send_message("❌ min 1")

        if amount > 100:
            return await interaction.response.send_message("❌ max 100")

        await interaction.response.defer()

        deleted = await interaction.channel.purge(limit=amount + 1)

        await interaction.followup.send(
            f"🧹 {len(deleted)-1} Nachrichten gelöscht",
            ephemeral=True
        )

    except Exception as e:
        logging.error(f"clear error: {e}")
        try:
            await interaction.followup.send("❌ Clear fehlgeschlagen", ephemeral=True)
        except:
            pass

# --------------------
# START
# --------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("TOKEN fehlt")

bot.run(TOKEN)