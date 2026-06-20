import os, time, logging
import discord
from discord import app_commands
from discord.ext import commands

start = time.time()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    logging.info("online")

@bot.tree.error
async def err(interaction: discord.Interaction, error: app_commands.AppCommandError):
    logging.error(error)
    try:
        await interaction.response.send_message("error", ephemeral=True)
    except:
        pass

@bot.tree.command(name="ping")
async def ping(i: discord.Interaction):
    await i.response.send_message("pong")

@bot.tree.command(name="info")
async def info(i: discord.Interaction):
    await i.response.send_message(f"{bot.user} | {int(time.time()-start)}s")

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(i: discord.Interaction, m: discord.Member, r=""):
    await m.kick(reason=r)
    await i.response.send_message("ok")

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(i: discord.Interaction, m: discord.Member, r=""):
    await m.ban(reason=r)
    await i.response.send_message("ok")

token = os.getenv("TOKEN")
if not token:
    raise SystemExit("no token")

bot.run(token)