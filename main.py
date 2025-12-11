import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ButtonStyle
from keep_alive import keep_alive
keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)


# ---------- Modal ----------
class InfoModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("กรอกข้อมูลแนะนำตัว")

        self.nickname = nextcord.ui.TextInput(
            label="Your pronoun?",
            placeholder="Name",
            required=True
        )
        self.add_item(self.nickname)

        self.age = nextcord.ui.TextInput(
            label="Age",
            placeholder="Age",
            required=True
        )
        self.add_item(self.age)

        self.description = nextcord.ui.TextInput(
            label="description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="description...",
            required=False
        )
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        if not self.age.value.isdigit():
            return await interaction.response.send_message(
                "วันเกิดต้องเป็นตัวเลขเท่านั้น",
                ephemeral=True
            )
        channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        await channel.send(
            f"**ข้อมูลใหม่จาก {interaction.user.mention}**\n"
            f"**ชื่อเล่น:** {self.nickname.value}\n"
            f"**อายุ:** {self.age.value}\n"
            f"**อื่นๆ:** {self.description.value}"
        )
        await interaction.response.send_message("บันทึกข้อมูลเรียบร้อย!", ephemeral=True)


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
    await interaction.response.send_message("กดปุ่มเพื่อกรอกข้อมูล:", view=InfoButton())


# ---------- Bot Ready ----------
@bot.event
async def on_ready():
    await bot.sync_application_commands()   # สำคัญมาก!
    print(f"Bot logged in as {bot.user}")


bot.run(TOKEN)
