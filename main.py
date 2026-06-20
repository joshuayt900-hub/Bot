import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import time
from collections import defaultdict, deque

# ----------------------------
# Render Keep-Alive Webserver
# ----------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# ----------------------------
# DISCORD BOT SETUP
# ----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# ANTI-SPAM SIMPLE
# ----------------------------
user_msgs = defaultdict(lambda: deque(maxlen=5))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ----------------------------
# MESSAGE HANDLING (ANTI-SPAM)
# ----------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    now = time.time()
    uid = message.author.id

    user_msgs[uid].append(now)

    # simple spam protection
    if len(user_msgs[uid]) == 5:
        if now - user_msgs[uid][0] < 10:
            try:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} bitte kein Spam."
                )
            except:
                pass
            return

    await bot.process_commands(message)

# ----------------------------
# COMMANDS
# ----------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.command()
async def info(ctx):
    await ctx.send("Bot läuft stabil mit Anti-Spam & Render Setup")

# ----------------------------
# START BOT
# ----------------------------
bot.run(os.getenv("TOKEN"))