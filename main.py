import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from keep_alive import keep_alive

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")


# ============================
# คำสั่ง !intro พร้อมปุ่ม
# ============================
@bot.command()
async def intro(ctx):
    # ปุ่ม
    button = Button(label="แนะนำตัวฉัน!", style=discord.ButtonStyle.primary)

    async def button_callback(interaction):
        await interaction.response.send_message(
            f"สวัสดีครับ {interaction.user.mention}! ผมคือบอทแนะนำตัว 🤖",
            ephemeral=True  # ให้ข้อความเห็นเฉพาะคนกด
        )

    button.callback = button_callback

    view = View()
    view.add_item(button)

    await ctx.send("กดปุ่มเพื่อให้ฉันแนะนำตัวให้คุณ 👇", view=view)


bot.run(TOKEN)
