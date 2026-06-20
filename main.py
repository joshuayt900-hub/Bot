import os
import discord
from discord.ext import commands

# Intents (wichtig für Nachrichten + Mitglieder)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Start-Event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Commands
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.command()
async def info(ctx):
    await ctx.send("Bot läuft stabil auf Render 🚀")

# Start Bot (Token aus Environment Variable)
bot.run(os.getenv("TOKEN"))