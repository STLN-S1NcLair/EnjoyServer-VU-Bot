"""import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$reaction'):
        emoji ="👍"
        await message.add_reaction(emoji)
        

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)


class SampleView(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="観戦モード ON", style=discord.ButtonStyle.success)
    async def observe_on(self, button: discord.ui.Button, interaction: discord.Interaction):
        reply;
        if ' //' in interaction.user.nickname:
            reply = await interaction.response.send_message(f"{interaction.user.mention} すでに観戦中です！")
        else:
            reply = await interaction.response.send_message(f"{interaction.user.mention} 観戦モードにしました！")
            await interaction.user.setNickname(interaction.user.nickname + " //観戦中")
        await reply.delete(5000)

    @discord.ui.button(label="観戦モード OFF", style=discord.ButtonStyle.danger)
    async def observe_off(self, button: discord.ui.Button, interaction: discord.Interaction):
        reply;
        if ' //' in interaction.user.nickname:
            reply = await interaction.response.send_message(f"{interaction.user.mention} 観戦モードを解除しました！")
            await interaction.user.setNickname(interaction.user.nickname.split(" //")[0])
        else:
            reply = await interaction.response.send_message(f"{interaction.user.mention} すでに観戦モードです！")
        await reply.delete(5000)

@bot.hybrid_command(name="observer_button", description="観戦モード ON/OFFを追加します")
async def observer_button(ctx):
    view = SampleView(timeout=None)
    await ctx.send(view=view)

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)"""

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

    async def on_ready(self):
        print(f"login: {self.user.name} [{self.user.id}]")


intents = Intents.default()
client = MyClient(intents=intents)

@client.tree.command()
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

keep_alive()
client.run(os.getenv("TOKEN"))
