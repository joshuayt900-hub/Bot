import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Bot Info",
        description="Ein einfacher Discord Bot",
        color=0x00ffcc
    )
    embed.add_field(name="Befehl", value="!ping → Pong Antwort", inline=False)
    embed.add_field(name="Status", value="läuft auf Render", inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))