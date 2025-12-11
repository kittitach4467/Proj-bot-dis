import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle
from keep_alive import keep_alive
from datetime import datetime

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)


# ---------- ฟังก์ชันคำนวณอายุ ----------
def calculate_age(day, month, year):
    birth_date = datetime(year, month, day)
    today = datetime.today()

    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


# ---------- Modal ----------
class InfoModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("กรอกข้อมูลแนะนำตัว")

        self.nickname = nextcord.ui.TextInput(
            label="ชื่อเล่น",
            placeholder="เช่น Beam",
            required=True
        )
        self.add_item(self.nickname)

        self.birthday = nextcord.ui.TextInput(
            label="วันเกิด (รูปแบบ DD/MM/YYYY)",
            placeholder="เช่น 16/07/2004",
            required=True
        )
        self.add_item(self.birthday)

        self.description = nextcord.ui.TextInput(
            label="คำอธิบายอื่นๆ",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="เขียนเพิ่มเติม...",
            required=False
        )
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):

        # ---- ตรวจสอบรูปแบบ DD/MM/YYYY ----
        try:
            parts = self.birthday.value.split("/")
            if len(parts) != 3:
                raise ValueError()

            day, month, year = map(int, parts)

            # ตรวจสอบความถูกต้องของวันที่
            birth_date = datetime(year, month, day)
            age = calculate_age(day, month, year)

        except:
            return await interaction.response.send_message(
                "❌ วันเกิดต้องเป็นรูปแบบ **DD/MM/YYYY** เช่น **16/07/2004** และต้องเป็นวันที่จริง",
                ephemeral=True
            )

        # ---- ส่งข้อมูลไปที่ช่องเป้าหมาย ----
        channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        await channel.send(
            f"**ข้อมูลใหม่จาก {interaction.user.mention}**\n"
            f"**ชื่อเล่น:** {self.nickname.value}\n"
            f"**วันเกิด:** {self.birthday.value}\n"
            f"**อายุ:** {age} ปี\n"
            f"**อื่นๆ:** {self.description.value}"
        )

        await interaction.response.send_message("✅ บันทึกข้อมูลเรียบร้อย!", ephemeral=True)


# ---------- Button ----------
class InfoButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="กดเพื่อกรอกข้อมูล", style=ButtonStyle.primary)
    async def open_modal(self, button, interaction: Interaction):
        await interaction.response.send_modal(InfoModal())


# ---------- Slash Command ----------
@bot.slash_command(name="info", description="แสดงปุ่มสำหรับกรอกข้อมูล")
async def info_cmd(interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    await interaction.followup.send("กดปุ่มเพื่อกรอกข้อมูล:", view=InfoButton())


# ---------- Bot Ready ----------
@bot.event
async def on_ready():
    await bot.sync_application_commands()
    print(f"Bot logged in as {bot.user}")


bot.run(TOKEN)
