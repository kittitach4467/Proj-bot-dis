import os
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from keep_alive import keep_alive

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 0))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")


# ============= Modal ฟอร์มแนะนำตัว =============
class IntroModal(Modal, title="แบบฟอร์มแนะนำตัว"):

    nickname = TextInput(label="ชื่อเล่น", placeholder="เช่น เอิร์ธ, มายด์")
    birthday = TextInput(label="วันเกิด", placeholder="เช่น 05/12/2008")
    desc = TextInput(label="คำอธิบายเพิ่มเติม", placeholder="เช่น งานอดิเรก นิสัย", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        channel = bot.get_channel(TARGET_CHANNEL_ID)

        if channel is None:
            await interaction.response.send_message("❌ ไม่พบห้องปลายทาง (TARGET_CHANNEL_ID)", ephemeral=True)
            return

        embed = discord.Embed(title="📌 ข้อมูลแนะนำตัวใหม่", color=discord.Color.green())
        embed.add_field(name="ชื่อเล่น", value=self.nickname.value, inline=False)
        embed.add_field(name="วันเกิด", value=self.birthday.value, inline=False)
        embed.add_field(name="รายละเอียดเพิ่มเติม", value=self.desc.value, inline=False)
        embed.set_footer(text=f"โดย {interaction.user}")

        await channel.send(embed=embed)
        await interaction.response.send_message("✔ บันทึกข้อมูลเรียบร้อย", ephemeral=True)


# ============= ปุ่มสำหรับเปิด Modal ============
class IntroButton(View):
    @discord.ui.button(label="แนะนำตัว", style=discord.ButtonStyle.primary)
    async def intro_button(self, interaction, button):
        await interaction.response.send_modal(IntroModal())


# ============= คำสั่ง !setupintro ============
@bot.command()
async def setupintro(ctx):
    await ctx.send("กดปุ่มเพื่อแนะนำตัว 👇", view=IntroButton())


bot.run(TOKEN)
