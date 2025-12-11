import os
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText
from keep_alive import keep_alive

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 0))  # ช่องที่จะแสดงข้อมูล

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")


# ================================
# Modal (Dialog) สำหรับกรอกข้อมูล
# ================================
class IntroModal(Modal):
    def __init__(self):
        super().__init__(title="แบบฟอร์มแนะนำตัว")

        self.add_item(InputText(label="ชื่อเล่น", placeholder="เช่น เอิร์ธ, โจ"))
        self.add_item(InputText(label="วันเกิด", placeholder="เช่น 12/05/2008"))
        self.add_item(InputText(label="คำอธิบายเพิ่มเติม", placeholder="เช่น นิสัย, สิ่งที่ชอบ"))


    async def callback(self, interaction: discord.Interaction):
        nickname = self.children[0].value
        birthday = self.children[1].value
        desc = self.children[2].value

        # ส่งไปยังห้องเป้าหมาย
        channel = bot.get_channel(TARGET_CHANNEL_ID)

        if channel is None:
            await interaction.response.send_message("ไม่พบห้องปลายทาง! ตรวจสอบ TARGET_CHANNEL_ID", ephemeral=True)
            return

        embed = discord.Embed(
            title="📌 ข้อมูลแนะนำตัวใหม่!",
            color=discord.Color.green()
        )
        embed.add_field(name="ชื่อเล่น", value=nickname, inline=False)
        embed.add_field(name="วันเกิด", value=birthday, inline=False)
        embed.add_field(name="รายละเอียดเพิ่มเติม", value=desc, inline=False)
        embed.set_footer(text=f"โดย {interaction.user}")

        await channel.send(embed=embed)
        await interaction.response.send_message("บันทึกข้อมูลเรียบร้อย ✔", ephemeral=True)


# ================================
# ปุ่มสำหรับเปิดฟอร์ม
# ================================
class IntroButton(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            Button(
                label="แนะนำตัว",
                style=discord.ButtonStyle.primary,
                custom_id="intro_button"
            )
        )

    @discord.ui.button(
        label="แนะนำตัว",
        style=discord.ButtonStyle.primary,
        custom_id="intro_button"
    )
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(IntroModal())


# ================================
# คำสั่ง !setupintro → ส่งปุ่มในห้อง
# ================================
@bot.command()
async def setupintro(ctx):
    await ctx.send("กดปุ่มเพื่อกรอกข้อมูลแนะนำตัว 👇", view=IntroButton())


bot.run(TOKEN)
