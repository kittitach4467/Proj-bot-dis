import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command()
async def intro(ctx):
    await ctx.send(f"สวัสดีครับ {ctx.author.mention}! ผมคือบอทแนะนำตัว 🤖")

bot.run(TOKEN)
