import os
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal, TextInput
from flask import Flask
import threading

# =======================
# Keep Alive (Koyeb)
# =======================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8000)

threading.Thread(target=run).start()

# =======================
# Discord Bot
# =======================
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", "0"))


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------- Modal ----------
class InfoModal(Modal):
    def __init__(self):
        super().__init__("กรอกข้อมูลส่วนตัว")

        self.nickname = TextInput(label="ชื่อเล่น", required=True)
        self.birthday = TextInput(label="วันเกิด (DD/MM)", required=True)
        self.description = TextInput(label="คำอธิบายอื่นๆ", required=False)

        self.add_item(self.nickname)
        self.add_item(self.birthday)
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction):

        # ใช้ตัวแปรแทน channel id ตรง ๆ
        channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)

        await channel.send(
            f"⭐ **ข้อมูลใหม่ถูกบันทึกแล้ว!**\n"
            f"- ชื่อเล่น: {self.nickname.value}\n"
            f"- วันเกิด: {self.birthday.value}\n"
            f"- อื่นๆ: {self.description.value}"
        )

        await interaction.response.send_message("บันทึกข้อมูลเรียบร้อยแล้ว!", ephemeral=True)

# ------------ Button ------------
class InfoButton(View):
    @nextcord.ui.button(label="กรอกข้อมูล", style=nextcord.ButtonStyle.green)
    async def button_callback(self, button, interaction: nextcord.Interaction):
        modal = InfoModal()
        await interaction.response.send_modal(modal)


# ------------ Command ------------
@bot.command()
async def register(ctx):
    await ctx.send("กดปุ่มเพื่อกรอกข้อมูล:", view=InfoButton())


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

bot.run(TOKEN)
