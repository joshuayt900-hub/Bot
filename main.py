import os
import discord
from discord.ext import commands
import time
from collections import defaultdict, deque

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# ANTI-SPAM
# ----------------------------
user_messages = defaultdict(lambda: deque(maxlen=5))

SPAM_LIMIT = 5  # 5 messages
SPAM_WINDOW = 10  # 10 seconds

# ----------------------------
# ANTI-RAID
# ----------------------------
join_times = deque(maxlen=20)
JOIN_LIMIT = 10  # 10 joins
JOIN_WINDOW = 15  # 15 seconds

# ----------------------------
# BOT START
# ----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ----------------------------
# ANTI-SPAM CHECK
# ----------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    now = time.time()
    uid = message.author.id

    user_messages[uid].append(now)

    # Spam check
    if len(user_messages[uid]) == SPAM_LIMIT:
        if now - user_messages[uid][0] < SPAM_WINDOW:
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
# ANTI-RAID CHECK
# ----------------------------
@bot.event
async def on_member_join(member):
    now = time.time()
    join_times.append(now)

    if len(join_times) == JOIN_LIMIT:
        if now - join_times[0] < JOIN_WINDOW:
            # simple protection: warn in system channel
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    await channel.send("⚠️ Möglicher Raid erkannt!")
                    break

# ----------------------------
# COMMANDS
# ----------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.command()
async def info(ctx):
    await ctx.send("Bot läuft mit Moderation & Anti-Raid System.")

# ----------------------------
# START
# ----------------------------
bot.run(os.getenv("TOKEN"))