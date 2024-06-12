import discord
import os
from discord import Intents, Client, Interaction
from discord.app_commands import CommandTree
from keep_alive import keep_alive

class MyClient(Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)
        
    async def setup_hook(self) -> None:
        await self.tree.sync()

intents = Intents.all()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.tree.command()
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$reaction'):
        emoji ="👍"
        await message.add_reaction(emoji)
        

@client.tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: Interaction):
    await interaction.response.send_message("てすと！")


class SampleView(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="観戦モード ON", style=discord.ButtonStyle.success)
    async def observe_on(self, button: discord.ui.Button, interaction: discord.Interaction):
        """if ' //' in interaction.user.nickname:
            reply = await interaction.response.send_message(f"{interaction.user.mention} すでに観戦中です！")
            await reply.delete(5000)
        else:"""
            reply = await interaction.response.send_message(f"{interaction.user.mention} 観戦モードにしました！")
            await interaction.user.setNickname(interaction.user.nickname + " //観戦中")
            await reply.delete(5000)

    @discord.ui.button(label="観戦モード OFF", style=discord.ButtonStyle.danger)
    async def observe_off(self, button: discord.ui.Button, interaction: discord.Interaction):
        if ' //' in interaction.user.nickname:
            reply = await interaction.response.send_message(f"{interaction.user.mention} 観戦モードを解除しました！")
            await interaction.user.setNickname(interaction.user.nickname.split(" //")[0])
            await reply.delete(5000)
        else:
            reply = await interaction.response.send_message(f"{interaction.user.mention} すでに観戦モードです！")
            await reply.delete(5000)

@client.tree.command(name="observer_button", description="観戦モード ON/OFFを追加します")
async def observer_button(interaction: Interaction):
    view = SampleView(timeout=None)
    await interaction.response.send_message(view=view)

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)

