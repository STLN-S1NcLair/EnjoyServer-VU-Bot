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

import discord
import asyncio
import random
from keep_alive import keep_alive
from discord.ext import tasks
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import os

# ↓元のコードは client = discord.client()
bot = discord.Client(intents_discord.Intents.all())

slash_client = SlashCommand(bot, sync_commands=True)

## 初期設定 ##
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# ↓元のコードは @bot.command()
@slash_client.slash(name="luck", description="君の今日の運勢は一体何かな～？")
# ↓元のコードは async def luck(ctx):
async def luck(ctx: SlashContext):
    fortune_list = ['大吉', '中吉', '吉', '小吉',
                    '末吉', '凶', '大凶', '判断が遅い', 'SSR', 'UR']
    fortune_length = len(fortune_list)

    await ctx.send(content=
        "今日の運勢は【" + fortune_list[random.randint(0, fortune_length - 1)] + "】だよ！")

keep_alive()
bot.run(os.getenv("TOKEN"))
